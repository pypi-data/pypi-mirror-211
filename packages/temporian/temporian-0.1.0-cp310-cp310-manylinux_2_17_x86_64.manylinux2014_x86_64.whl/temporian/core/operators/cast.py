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

"""Cast operator class and public API function definition."""

from typing import Union, Mapping, Optional
from temporian.core.data.feature import Feature

from temporian.core.data.dtype import DType, py_types_to_dtypes
from temporian.core import operator_lib
from temporian.core.data.node import Node
from temporian.core.operators.base import Operator
from temporian.proto import core_pb2 as pb


dtype = Union[DType, type]


class CastOperator(Operator):
    def __init__(
        self,
        input: Node,
        to_dtype: Optional[dtype] = None,
        from_dtypes: Optional[Mapping[dtype, dtype]] = None,
        from_features: Union[
            Mapping[str, dtype], Mapping[str, str], None
        ] = None,
        check_overflow: bool = True,
    ):
        super().__init__()

        # Convert to DTypes any python types found
        to_dtype = py_types_to_dtypes(to_dtype)
        from_dtypes = py_types_to_dtypes(from_dtypes)
        from_features = py_types_to_dtypes(from_features)

        # Check that provided arguments are coherent
        self._check_args(input, to_dtype, from_dtypes, from_features)

        # Convert anything to {feature_name: target_dtype}, include all features
        from_features_all = self._get_feature_dtype_map(
            input, to_dtype, from_dtypes, from_features
        )

        # Attributes
        self.add_attribute("check_overflow", check_overflow)
        # Convert dtype -> str for serialization
        self.add_attribute(
            "from_features",
            {feat: dtype.value for feat, dtype in from_features_all.items()},
        )

        # Inputs
        self.add_input("input", input)

        # Output node features
        output_features = []
        reuse_node = True
        for feature in input.features:
            if from_features_all[feature.name] is feature.dtype:
                # Reuse feature
                output_features.append(feature)
            else:
                # Create new feature
                reuse_node = False
                output_features.append(
                    # Note: we're not renaming output features here
                    Feature(
                        feature.name,
                        from_features_all[feature.name],
                        feature.sampling,
                        creator=self,
                    )
                )

        # Output node: don't create new if all features are reused
        self.add_output(
            "output",
            input
            if reuse_node
            else Node(
                features=output_features,
                sampling=input.sampling,
                creator=self,
            ),
        )

        # Used in implementation
        self.reuse_node = reuse_node

        self.check()

    @property
    def check_overflow(self) -> bool:
        return self.attributes["check_overflow"]

    @property
    def from_features(self) -> dict[str, DType]:
        return self.attributes["from_features"]

    def _check_args(
        self,
        input: Node,
        to_dtype: Optional[DType] = None,
        from_dtypes: Optional[Mapping[DType, DType]] = None,
        from_features: Optional[Mapping[str, DType]] = None,
    ) -> None:
        # Check that only one of these args was provided
        oneof_args = [to_dtype, from_dtypes, from_features]
        if sum(arg is not None for arg in oneof_args) != 1:
            raise ValueError(
                "One and only one of to_dtype, from_dtypes or from_features"
                " should be provided to CastOperator."
            )

        # Check: to_dtype is actually a dtype
        if to_dtype is not None and not isinstance(to_dtype, DType):
            raise ValueError(f"Cast: expected DType but got {type(to_dtype)=}")

        # Check: from_dtypes is a dict {dtype: dtype}
        if from_dtypes is not None and (
            not isinstance(from_dtypes, Mapping)
            or any(not isinstance(key, DType) for key in from_dtypes)
            or any(not isinstance(val, DType) for val in from_dtypes.values())
        ):
            raise ValueError(
                "Cast: target dict must have valid DTypes or feature names"
            )

        # Check: from_features is {feature_name: dtype}
        if from_features is not None and (
            not isinstance(from_features, Mapping)
            or any(key not in input.feature_names for key in from_features)
            or any(
                not isinstance(val, (DType, str))
                for val in from_features.values()
            )
        ):
            raise ValueError(
                "Cast: target dict must have valid DTypes or feature names"
            )

    def _get_feature_dtype_map(
        self,
        input: Node,
        to_dtype: Optional[DType] = None,
        from_dtypes: Optional[Mapping[DType, DType]] = None,
        from_features: Optional[Mapping[str, DType]] = None,
    ) -> dict[str, DType]:
        if to_dtype is not None:
            return {feature.name: to_dtype for feature in input.features}
        if from_features is not None:
            # NOTE: In this special case, it's allowed to provide target DType
            # as a string instead of DType (for serialization purposes, since
            # from_features is also an attribute)
            return {
                feature.name: DType(
                    from_features.get(feature.name, feature.dtype)
                )
                for feature in input.features
            }
        if from_dtypes is not None:
            return {
                feature.name: from_dtypes.get(feature.dtype, feature.dtype)
                for feature in input.features
            }

    @classmethod
    def build_op_definition(cls) -> pb.OperatorDef:
        return pb.OperatorDef(
            key="CAST",
            attributes=[
                pb.OperatorDef.Attribute(
                    key="from_features",
                    type=pb.OperatorDef.Attribute.Type.MAP_STR_STR,
                    is_optional=False,
                ),
                pb.OperatorDef.Attribute(
                    key="check_overflow",
                    type=pb.OperatorDef.Attribute.Type.BOOL,
                    is_optional=False,
                ),
            ],
            inputs=[
                pb.OperatorDef.Input(key="input"),
            ],
            outputs=[pb.OperatorDef.Output(key="output")],
        )


operator_lib.register_operator(CastOperator)


def cast(
    input: Node,
    target: Union[dtype, Union[Mapping[str, dtype], Mapping[dtype, dtype]]],
    check_overflow: bool = True,
) -> Node:
    """Casts the dtype of features to the dtype(s) specified in `target`.

    Python types are also accepted, with numeric types mapped to 64-bit DTypes.

    Feature names are preserved, and reused (not copied) if not changed.

    Examples:
        Given an input `Node` with features 'A' (`int64`), 'B'
        (`int64`), 'C' (`float64`) and 'D' (`str_`):

        1. `cast(input, target=tp.int32)`
           Try to convert all features to `int32`, or raise `ValueError` if some
           string value in 'D' is invalid, or any column value is out of range
           for `int32`.

        2. `cast(input, target={int: tp.int32, tp.str_: tp.float32})`
            Convert features 'A' and 'B' to `int32` (note that `int=tp.int64`),
            'D' to `float32`, leave 'C' unchanged.

        3. `cast(input, target={'A': tp.float32, 'B': tp.int32})`
            Convert 'A' to `float32` and 'B' to `int32`.

        4. `cast(input, target={'A': tp.float32, tp.float64: tp.int32})`
            Raises ValueError: don't mix dtype and feature name keys

    Args:
        input: Input `Node` object to cast the columns from.
        target: Single dtype or a map. Providing a single dtype will cast all
            columns to it. The mapping keys can be either feature names or the
            original dtypes (and not both types mixed), and the values are the
            target dtypes for them.
        check_overflow: Flag to check overflow when casting to a dtype with a
            shorter range (e.g: `int64`->`int32`). Note that this check adds
            some computation overhead. Defaults to `True`.

    Returns:
        New `Node` (or the same if no features actually changed dtype), with
        the same feature names as the input one, but with the new dtypes as
        specified in `target`.

    Raises:
        ValueError: If `check_overflow=True` and some value is out of the range
            of the `target` dtype.
        ValueError: If trying to cast a non-numeric string to numeric dtype.
        ValueError: If `target` is not a dtype nor a mapping.
        ValueError: If `target` is a mapping, but some of the keys are not a
            dtype nor a feature in `input.feature_names`, or if those types are
            mixed.
    """
    # Convert 'target' to one of these:
    to_dtype = None
    from_features = None
    from_dtypes = None

    # Further type verifications are done in the operator
    if isinstance(target, Mapping):
        if all(key in input.feature_names for key in target):
            from_features = target
        elif all(isinstance(key, (DType, type)) for key in target):
            from_dtypes = target
        else:
            raise ValueError(
                "Cast: mapping keys should be all DType or feature names.\n"
                f"Keys: {target.keys()}\n"
                f"Feature names: {input.feature_names}"
            )
    else:
        to_dtype = target

    return CastOperator(
        input,
        to_dtype=to_dtype,
        from_features=from_features,
        from_dtypes=from_dtypes,
        check_overflow=check_overflow,
    ).outputs["output"]
