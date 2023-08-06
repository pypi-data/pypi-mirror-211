"""Bokeh plotting backend."""

import datetime
from typing import Optional, List, Any, Set

import numpy as np

from temporian.core.data import duration
from temporian.implementation.numpy.data.event_set import EventSet
from temporian.implementation.numpy.data.plotter import (
    Options,
    Style,
    is_uniform,
    get_num_plots,
    auto_style,
)


def plot_bokeh(
    evsets: List[EventSet],
    indexes: List[tuple],
    features: Set[str],
    options: Options,
):
    from bokeh.plotting import figure
    from bokeh.io import output_notebook, show
    from bokeh.layouts import gridplot, column
    from bokeh.models import (
        ColumnDataSource,
        CategoricalColorMapper,
        HoverTool,
    )
    from bokeh.models import ColumnDataSource, CustomJS
    from bokeh.palettes import Dark2_5 as colors

    num_plots = get_num_plots(evsets, indexes, features, options)

    figs = []

    # Actual plotting
    plot_idx = 0
    for index in indexes:
        if plot_idx >= num_plots:
            # Too much plots are displayed already.
            break

        # Note: Don't display the tuple parenthesis is the index contain a
        # single dimension.
        title = str(index[0] if len(index) == 1 else index)

        # Index of the next color to use in the plot.
        color_idx = 0

        for evset in evsets:
            if plot_idx >= num_plots:
                break

            feature_names = [f for f in evset.feature_names if f in features]

            xs = evset.data[index].timestamps
            uniform = is_uniform(xs)

            plot_mask = np.full(len(xs), True)
            if options.min_time is not None:
                plot_mask = plot_mask & (xs >= options.min_time)
            if options.max_time is not None:
                plot_mask = plot_mask & (xs <= options.max_time)
            if options.max_points is not None and len(xs) > options.max_points:
                # Too many timestamps. Only keep the fist ones.
                plot_mask = plot_mask & (
                    np.cumsum(plot_mask) <= options.max_points
                )

            xs = xs[plot_mask]

            if evset.is_unix_timestamp:
                # Matplotlib understands datetimes.
                xs = [
                    datetime.datetime.fromtimestamp(x, tz=datetime.timezone.utc)
                    for x in xs
                ]

            if len(feature_names) == 0:
                # There is not features to plot. Instead, plot the timestamps.
                figs.append(
                    _bokeh_sub_plot(
                        xs=xs,
                        ys=np.zeros(len(xs)),
                        options=options,
                        color=colors[color_idx % len(colors)],
                        name="[sampling]",
                        is_unix_timestamp=evset.is_unix_timestamp,
                        title=title,
                        style=Style.vline,
                    )
                )
                # Only print the index / title once
                title = None

                color_idx += 1
                plot_idx += 1

            for feature_name in feature_names:
                feature_idx = evset.feature_names.index(feature_name)
                if plot_idx >= num_plots:
                    # Too much plots are displayed already.
                    break

                ys = evset.data[index].features[feature_idx][plot_mask]
                if options.style == Style.auto:
                    effective_stype = auto_style(uniform, xs, ys)
                else:
                    effective_stype = options.style

                figs.append(
                    _bokeh_sub_plot(
                        xs=xs,
                        ys=ys,
                        options=options,
                        color=colors[color_idx % len(colors)],
                        name=feature_name,
                        is_unix_timestamp=evset.is_unix_timestamp,
                        title=title,
                        style=effective_stype,
                    )
                )

                # Only print the index / title once
                title = None

                color_idx += 1
                plot_idx += 1

    if len(figs) > 1:
        # Sync x-axes
        js_vars = [f"p{fig_idx+1}_x_range" for fig_idx, fig in enumerate(figs)]
        js_inputs = {}
        core_code = ""
        for js_var, fig in zip(js_vars, figs):
            js_inputs[js_var] = fig.x_range

            sub_core_code = "\n".join(
                [
                    f"""
            {other_js_var}.start = start;
            {other_js_var}.end = end;
            """
                    for other_js_var in js_vars
                    if other_js_var != js_var
                ]
            )

            core_code += f"""
            if (cb_obj == {js_var}) {{
                const start =  {js_var}.start;
                const end =  {js_var}.end;
                {sub_core_code}
            }}
            """

        callback = CustomJS(args=js_inputs, code=core_code)

        for fig in figs:
            fig.x_range.js_on_change("start", callback)
            fig.x_range.js_on_change("end", callback)

        figure_set = gridplot(
            [[f] for f in figs],
            merge_tools=True,
            toolbar_location="right",
            toolbar_options=dict(logo=None),
        )
    else:
        figure_set = figs[0]
        figure_set.toolbar.logo = None

    output_notebook(hide_banner=True)
    show(figure_set)
    return figure_set


def _bokeh_sub_plot(
    xs,
    ys,
    options: Options,
    color,
    name: str,
    is_unix_timestamp: bool,
    title: Optional[str],
    style: Style,
) -> Any:
    """Plots "(xs, ys)" on the axis "ax"."""

    from bokeh.plotting import figure
    from bokeh.io import output_notebook, show
    from bokeh.layouts import gridplot, column
    from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool
    from bokeh.models import ColumnDataSource, CustomJS, Range1d
    from bokeh.palettes import Dark2_5 as colors

    tools = [
        "xpan",
        "pan",
        "xwheel_zoom",
        "ywheel_zoom",
        "box_zoom",
        "reset",
        "undo",
        "save",
        "hover",
    ]

    fig_args = {}
    if is_unix_timestamp:
        fig_args["x_axis_type"] = "datetime"
    if title:
        fig_args["title"] = title

    is_string = ys.dtype.type is np.str_ or ys.dtype.type is np.string_
    if is_string:
        unique_ys_values = list(set(ys))
        fig_args["y_range"] = unique_ys_values
    else:
        unique_ys_values = None

    fig = figure(
        width=options.width_px,
        height=options.height_per_plot_px,
        tools=tools,
        **fig_args,
    )

    if options.min_time is not None or options.max_time is not None:
        args = {}
        if options.min_time is not None:
            args["start"] = (
                duration.convert_date_to_duration(options.min_time)
                if not is_unix_timestamp
                else options.min_time
            )
        if options.max_time is not None:
            args["end"] = (
                duration.convert_date_to_duration(options.max_time)
                if not is_unix_timestamp
                else options.max_time
            )
        fig.x_range = Range1d(**args)

    data = {"x": xs, "y": ys, "color": color}

    if is_string:
        fig.circle(x=xs, y=ys)
    elif style == Style.line:
        fig.line(**data)
    elif style == Style.marker:
        fig.scatter(**data)
    elif style == Style.vline:
        fig.scatter(**data)
    else:
        raise ValueError("Non implemented style")

    fig.yaxis.axis_label = name

    return fig
