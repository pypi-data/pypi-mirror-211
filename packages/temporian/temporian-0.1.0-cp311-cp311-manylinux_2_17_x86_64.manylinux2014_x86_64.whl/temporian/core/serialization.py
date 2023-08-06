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

"""Serialization/unserialization of a graph and its components."""

from typing import Set, Any, Dict, Tuple, Optional, Mapping

from google.protobuf import text_format

from temporian.core import operator_lib
from temporian.core import graph
from temporian.core.data.node import Node
from temporian.core.data.feature import Feature
from temporian.core.data.sampling import Sampling
from temporian.core.operators import base
from temporian.core.data.dtype import DType
from temporian.proto import core_pb2 as pb


def save(
    inputs: Optional[graph.MultipleNodeArg],
    outputs: graph.MultipleNodeArg,
    path: str,
) -> None:
    """Saves the graph between `inputs` and `outputs` to a file.

    Usage example:
        ```python
        a = t.input_node(...)
        b = t.sma(a, window_length=7.0)
        t.save(inputs={"io_a": a}, outputs={"io_b": b}, path="graph.tem")

        inputs, outputs = t.load(path="graph.tem")
        print(t.evaluate(
            query=outputs["io_b"],
            input_data{inputs["io_a"]: pandas.DataFrame(...)}
        ))
        ```

    Args:
        inputs: Input nodes. If None, the inputs is inferred. In this case,
            input nodes have to be named.
        outputs: Output nodes.
        path: File path to save to.
    """

    # TODO: Add support for compressed / binary serialization.

    if inputs is not None:
        inputs = graph.normalize_multiple_node_arg(inputs)

    outputs = graph.normalize_multiple_node_arg(outputs)

    g, _ = graph.infer_graph(inputs=inputs, outputs=outputs)
    proto = serialize(g)
    with open(path, "w") as f:
        f.write(text_format.MessageToString(proto))


def load(
    path: str, squeeze: bool = False
) -> Tuple[Dict[str, Node], Dict[str, Node]]:
    """Loads a graph from a file.

    Args:
        path: File path to load from.
        squeeze: If true, and if the input/output contains a single node,
            returns a node (instead of a dictionary of nodes).

    Returns:
        Input and output nodes.
    """

    with open(path, "r") as f:
        proto = text_format.Parse(f.read(), pb.Graph())
    g = unserialize(proto)

    inputs = g.inputs
    outputs = g.outputs

    if squeeze and len(inputs) == 1:
        inputs = list(inputs.values())[0]

    if squeeze and len(outputs) == 1:
        outputs = list(outputs.values())[0]

    return inputs, outputs


def serialize(src: graph.Graph) -> pb.Graph:
    """Serializes a graph into a protobuffer."""

    return pb.Graph(
        operators=[_serialize_operator(o) for o in src.operators],
        nodes=[_serialize_node(e) for e in src.nodes],
        features=[_serialize_feature(f) for f in src.features],
        samplings=[_serialize_sampling(s) for s in src.samplings],
        inputs=[_serialize_io_signature(k, e) for k, e in src.inputs.items()],
        outputs=[_serialize_io_signature(k, e) for k, e in src.outputs.items()],
    )


def unserialize(src: pb.Graph) -> graph.Graph:
    """Unserializes a protobuffer into a graph."""

    # Decode the components.
    # All the fields except for the "creator" ones are set.
    samplings = {s.id: _unserialize_sampling(s) for s in src.samplings}
    features = {f.id: _unserialize_feature(f, samplings) for f in src.features}
    nodes = {e.id: _unserialize_node(e, samplings, features) for e in src.nodes}
    operators = {o.id: _unserialize_operator(o, nodes) for o in src.operators}

    # Set the creator fields.
    def get_creator(op_id: str) -> base.Operator:
        if op_id not in operators:
            raise ValueError(f"Non existing creator operator {op_id}")
        return operators[op_id]

    for src_node in src.nodes:
        if src_node.creator_operator_id:
            nodes[src_node.id].creator = get_creator(
                src_node.creator_operator_id
            )
    for src_feature in src.features:
        if src_feature.creator_operator_id:
            features[src_feature.id].creator = get_creator(
                src_feature.creator_operator_id
            )
    for src_sampling in src.samplings:
        if src_sampling.creator_operator_id:
            samplings[src_sampling.id].creator = get_creator(
                src_sampling.creator_operator_id
            )

    # Copy extracted items.
    g = graph.Graph()
    for sampling in samplings.values():
        g.samplings.add(sampling)
    for node in nodes.values():
        g.nodes.add(node)
    for feature in features.values():
        g.features.add(feature)
    for operator in operators.values():
        g.operators.add(operator)

    # IO Signature
    def get_node(node_id: str) -> Node:
        if node_id not in nodes:
            raise ValueError(f"Non existing node {node_id}")
        return nodes[node_id]

    for item in src.inputs:
        g.inputs[item.key] = get_node(item.node_id)

    for item in src.outputs:
        g.outputs[item.key] = get_node(item.node_id)

    return g


def _identifier(item: Any) -> str:
    """Creates a unique identifier for an object within a graph."""
    if item is None:
        raise ValueError("Cannot get id of None")
    return str(id(item))


def all_identifiers(collection: Any) -> Set[str]:
    """Builds the set of identifiers of a collections of nodes/features/..."""
    return {_identifier(x) for x in collection}


def _serialize_operator(src: base.Operator) -> pb.Operator:
    return pb.Operator(
        id=_identifier(src),
        operator_def_key=src.definition().key,
        inputs=[
            pb.Operator.NodeArgument(key=k, node_id=_identifier(v))
            for k, v in src.inputs.items()
        ],
        outputs=[
            pb.Operator.NodeArgument(key=k, node_id=_identifier(v))
            for k, v in src.outputs.items()
        ],
        attributes=[
            _attribute_to_proto(k, v) for k, v in src.attributes.items()
        ],
    )


def _unserialize_operator(
    src: pb.Operator, nodes: Dict[str, Node]
) -> base.Operator:
    operator_class = operator_lib.get_operator_class(src.operator_def_key)

    def get_node(key):
        if key not in nodes:
            raise ValueError(f"Non existing node {key}")
        return nodes[key]

    input_args = {x.key: get_node(x.node_id) for x in src.inputs}
    output_args = {x.key: get_node(x.node_id) for x in src.outputs}
    attribute_args = {x.key: _attribute_from_proto(x) for x in src.attributes}

    # We construct the operator.
    op: base.Operator = operator_class(**input_args, **attribute_args)

    # Check that the operator signature matches the expected one.
    if op.inputs.keys() != input_args.keys():
        raise ValueError(
            f"Restoring the operator {src.operator_def_key} lead "
            "to an unexpected input signature. "
            f"Expected: {input_args.keys()} Effective: {op.inputs.keys()}"
        )

    if op.outputs.keys() != output_args.keys():
        raise ValueError(
            f"Restoring the operator {src.operator_def_key} lead "
            "to an unexpected output signature. "
            f"Expected: {output_args.keys()} Effective: {op.outputs.keys()}"
        )

    if op.attributes.keys() != attribute_args.keys():
        raise ValueError(
            f"Restoring the operator {src.operator_def_key} lead to an"
            " unexpected attributes signature. Expected:"
            f" {attribute_args.keys()} Effective: {op.attributes.keys()}"
        )
    # TODO: Deep check of equality of the inputs / outputs / attributes

    # Override the inputs / outputs / attributes
    op.inputs = input_args
    op.outputs = output_args
    op.attributes = attribute_args
    return op


def _serialize_node(src: Node) -> pb.Node:
    return pb.Node(
        id=_identifier(src),
        sampling_id=_identifier(src.sampling),
        feature_ids=[_identifier(f) for f in src.features],
        name=src.name,
        creator_operator_id=(
            _identifier(src.creator) if src.creator is not None else None
        ),
    )


def _unserialize_node(
    src: pb.Node, samplings: Dict[str, Sampling], features: Dict[str, Feature]
) -> Node:
    if src.sampling_id not in samplings:
        raise ValueError(f"Non existing sampling {src.sampling_id} in {src}")

    def get_feature(key):
        if key not in features:
            raise ValueError(f"Non existing feature {key}")
        return features[key]

    return Node(
        sampling=samplings[src.sampling_id],
        features=[get_feature(f) for f in src.feature_ids],
        name=src.name,
        creator=None,
    )


def _serialize_feature(src: Feature) -> pb.Feature:
    return pb.Feature(
        id=_identifier(src),
        name=src.name,
        dtype=_serialize_dtype(src.dtype),
        sampling_id=_identifier(src.sampling),
        creator_operator_id=(
            _identifier(src.creator) if src.creator is not None else None
        ),
    )


def _unserialize_feature(
    src: pb.Feature, samplings: Dict[str, Sampling]
) -> Feature:
    if src.sampling_id not in samplings:
        raise ValueError(f"Non existing sampling {src.sampling_id} in {src}")

    return Feature(
        name=src.name,
        dtype=_unserialize_dtype(src.dtype),
        sampling=samplings[src.sampling_id],
        creator=None,
    )


def _serialize_sampling(src: Sampling) -> pb.Sampling:
    return pb.Sampling(
        id=_identifier(src),
        index=pb.Index(
            levels=[
                pb.Index.IndexLevel(name=name, dtype=_serialize_dtype(dtype))
                for name, dtype in zip(src.index.names, src.index.dtypes)
            ]
        ),
        creator_operator_id=(
            _identifier(src.creator) if src.creator is not None else None
        ),
        is_unix_timestamp=src.is_unix_timestamp,
    )


def _unserialize_sampling(src: pb.Sampling) -> Sampling:
    return Sampling(
        index_levels=[
            (index_level.name, _unserialize_dtype(index_level.dtype))
            for index_level in src.index.levels
        ],
        creator=None,
        is_unix_timestamp=src.is_unix_timestamp,
    )


def _serialize_dtype(dtype) -> pb.DType:
    if dtype not in DTYPE_MAPPING:
        raise ValueError(f"Non supported type {dtype}")
    return DTYPE_MAPPING[dtype]


def _unserialize_dtype(dtype: pb.DType):
    if dtype not in INV_DTYPE_MAPPING:
        raise ValueError(f"Non supported type {dtype}")
    return INV_DTYPE_MAPPING[dtype]


DTYPE_MAPPING = {
    DType.FLOAT64: pb.DType.FLOAT64,
    DType.FLOAT32: pb.DType.FLOAT32,
    DType.INT64: pb.DType.INT64,
    DType.INT32: pb.DType.INT32,
    DType.BOOLEAN: pb.DType.BOOLEAN,
    DType.STRING: pb.DType.STRING,
}
INV_DTYPE_MAPPING = {v: k for k, v in DTYPE_MAPPING.items()}


def _attribute_to_proto(
    key: str, value: base.AttributeType
) -> pb.Operator.Attribute:
    if isinstance(value, str):
        return pb.Operator.Attribute(key=key, str=value)
    if isinstance(value, bool):
        # NOTE: Check this before int (isinstance(False, int) is also True)
        return pb.Operator.Attribute(key=key, boolean=value)
    if isinstance(value, int):
        return pb.Operator.Attribute(key=key, integer_64=value)
    if isinstance(value, float):
        return pb.Operator.Attribute(key=key, float_64=value)
    # list of strings
    if isinstance(value, list) and all(isinstance(val, str) for val in value):
        return pb.Operator.Attribute(
            key=key, list_str=pb.Operator.Attribute.ListString(value=value)
        )
    # map<str, str>
    if (
        isinstance(value, Mapping)
        and all(isinstance(key, str) for key in value.keys())
        and all(isinstance(val, str) for val in value.values())
    ):
        return pb.Operator.Attribute(
            key=key, map_str_str=pb.Operator.Attribute.MapStrStr(value=value)
        )
    raise ValueError(
        f"Non supported type {type(value)} for attribute {key}={value}"
    )


def _attribute_from_proto(src: pb.Operator.Attribute) -> base.AttributeType:
    if src.HasField("integer_64"):
        return src.integer_64
    if src.HasField("str"):
        return src.str
    if src.HasField("float_64"):
        return src.float_64
    if src.HasField("list_str"):
        return list(src.list_str.value)
    if src.HasField("boolean"):
        return bool(src.boolean)
    if src.HasField("map_str_str"):
        return dict(src.map_str_str.value)
    raise ValueError(f"Non supported proto attribute {src}")


def _serialize_io_signature(key: str, node: Node):
    return pb.IOSignature(
        key=key,
        node_id=_identifier(node),
    )
