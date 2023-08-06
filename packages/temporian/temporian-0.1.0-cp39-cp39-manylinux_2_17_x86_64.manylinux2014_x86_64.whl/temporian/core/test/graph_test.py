# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from absl.testing import absltest

from temporian.core import graph
from temporian.core.test import utils


class GraphTest(absltest.TestCase):
    def test_infer_graph_basic(self):
        """Lists all the objects in a graph."""

        i1 = utils.create_input_node()
        o2 = utils.OpI1O1(i1)
        i3 = utils.create_input_node()
        o4 = utils.OpI2O1(o2.outputs["output"], i3)
        o5 = utils.OpI1O2(o4.outputs["output"])

        g, _ = graph.infer_graph(
            {
                "io_input_1": i1,
                "io_input_2": i3,
            },
            {
                "io_output_1": o5.outputs["output_1"],
                "io_output_2": o4.outputs["output"],
            },
        )
        self.assertLen(g.operators, 3)
        self.assertLen(g.samplings, 3)
        self.assertLen(g.nodes, 6)
        self.assertLen(g.features, 10)

    def test_infer_graph_passing_op(self):
        """With an opt that just passes features."""

        a = utils.create_input_node()
        b = utils.OpI1O1NotCreator(a)
        c = utils.OpI1O1(b.outputs["output"])

        g, _ = graph.infer_graph(
            {"my_input": a},
            {"my_output": c.outputs["output"]},
        )

        self.assertLen(g.operators, 2)
        self.assertLen(g.samplings, 2)
        self.assertLen(g.nodes, 3)
        self.assertLen(g.features, 4)

    def test_infer_graph_input_is_not_feature_creator(self):
        """When the user input is not the feature creator."""

        a = utils.create_input_node()
        b = utils.OpI1O1NotCreator(a)
        c = utils.OpI1O1(b.outputs["output"])

        g, _ = graph.infer_graph(
            {"my_input": b.outputs["output"]},
            {"my_output": c.outputs["output"]},
        )

        self.assertLen(g.operators, 1)
        self.assertLen(g.samplings, 2)
        self.assertLen(g.nodes, 2)
        self.assertLen(g.features, 4)

    def test_infer_graph_missing_input(self):
        """The input is missing."""

        i = utils.create_input_node()
        o2 = utils.OpI1O1(i)

        with self.assertRaisesRegex(
            ValueError,
            "but not provided as input",
        ):
            graph.infer_graph({}, {"io_output": o2.outputs["output"]})

    def test_infer_graph_automatic_input(self):
        """Infer automatically the input."""

        i1 = utils.create_input_node()
        i1.name = "io_input_1"
        o2 = utils.OpI1O1(i1)
        i3 = utils.create_input_node()
        i3.name = "io_input_2"
        o4 = utils.OpI2O1(o2.outputs["output"], i3)
        o5 = utils.OpI1O2(o4.outputs["output"])

        g, _ = graph.infer_graph(
            None,
            {
                "io_output_1": o5.outputs["output_1"],
                "io_output_2": o4.outputs["output"],
            },
        )

        self.assertLen(g.operators, 3)
        self.assertLen(g.samplings, 3)
        self.assertLen(g.nodes, 6)
        self.assertLen(g.features, 10)

    def test_automatic_input_missing_name(self):
        """Automated input is not allowed if the input node is not named."""

        i1 = utils.create_input_node()
        o2 = utils.OpI1O1(i1)

        with self.assertRaisesRegex(
            ValueError, "Cannot infer input on unnamed node"
        ):
            graph.infer_graph(None, {"io_output_1": o2.outputs["output"]})

    def test_automatic_input_equality_graph(self):
        """Automated inference when the input is the same as the output."""

        i1 = utils.create_input_node()
        i1.name = "io_1"

        g, _ = graph.infer_graph(None, {"io_2": i1})

        self.assertLen(g.operators, 0)
        self.assertLen(g.nodes, 1)
        self.assertLen(g.samplings, 1)
        self.assertLen(g.inputs, 1)
        self.assertLen(g.outputs, 1)
        self.assertEqual(g.inputs["io_1"], g.outputs["io_2"])


if __name__ == "__main__":
    absltest.main()
