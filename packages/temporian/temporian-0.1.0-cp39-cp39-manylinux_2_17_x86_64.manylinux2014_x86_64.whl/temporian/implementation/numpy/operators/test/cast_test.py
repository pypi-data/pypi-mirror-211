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

import numpy as np
import pandas as pd
from absl.testing import absltest

from temporian.core.data.node import Node, Feature
from temporian.core.data.sampling import Sampling
from temporian.implementation.numpy.data.event_set import EventSet
from temporian.implementation.numpy.operators.cast import (
    CastNumpyImplementation,
    CastOperator,
)
from temporian.core.data.dtype import DType


class CastNumpyImplementationTest(absltest.TestCase):
    """Test numpy implementation of all arithmetic operators,
    but using a two-level index and disordered rows."""

    def setUp(self):
        # store ids
        TRYO_SHOP = 42
        GOOGLE_SHOP = 101
        # product ids
        MATE_ID = 1
        BOOK_ID = 2
        PIXEL_ID = 3

        # Some numbers above int32 and below int64
        abv_i32 = np.iinfo(np.int32).max + 1
        blw_i64 = np.finfo(np.float64).min  # below float32 too

        # 2 index columns, 3 features: float64, int64, str, boolean
        self.input_evset = EventSet.from_dataframe(
            pd.DataFrame(
                data=[
                    [TRYO_SHOP, MATE_ID, 0.0, -14.0, abv_i32, "1.2", True],
                    [TRYO_SHOP, MATE_ID, 1.0, 15.0, 0, "2.0", True],
                    [TRYO_SHOP, MATE_ID, 2.0, 16, 3, "000000", True],
                    [TRYO_SHOP, BOOK_ID, 1.0, 10, 4, "100", False],
                    [GOOGLE_SHOP, BOOK_ID, 1.0, 0, 5, "3.2", False],
                    [GOOGLE_SHOP, BOOK_ID, 2.0, 0, 6, "001", True],
                    [GOOGLE_SHOP, PIXEL_ID, 0.0, -1, -8, "-3.5", False],
                    [GOOGLE_SHOP, PIXEL_ID, 1.0, blw_i64, 8, "-2", False],
                ],
                columns=[
                    "store_id",
                    "product_id",
                    "timestamp",
                    # The following are just tricky column names :)
                    "float_64",
                    "int_64",
                    "str",
                    "boolean",
                ],
            ),
            index_names=["store_id", "product_id"],
        )

        # Expected event set when applying some downcast operations
        self.expected_evset_1 = EventSet.from_dataframe(
            pd.DataFrame(
                data=[
                    # Note: astype() below will truncate above/below numbers
                    [TRYO_SHOP, MATE_ID, 0.0, -14.0, abv_i32, 1.2, 1],
                    [TRYO_SHOP, MATE_ID, 1.0, 15.0, 0, 2, 1],
                    [TRYO_SHOP, MATE_ID, 2.0, 16, 3, 0, 1],
                    [TRYO_SHOP, BOOK_ID, 1.0, 10, 4, 100, 0],
                    [GOOGLE_SHOP, BOOK_ID, 1.0, 0, 5, 3.2, 0],
                    [GOOGLE_SHOP, BOOK_ID, 2.0, 0, 6, 1, 1],
                    [GOOGLE_SHOP, PIXEL_ID, 0.0, -1, -8, -3.5, 0],
                    [GOOGLE_SHOP, PIXEL_ID, 1.0, blw_i64, 8, -2, 0],
                ],
                columns=[
                    "store_id",
                    "product_id",
                    "timestamp",
                    "float_64",
                    "int_64",
                    "str",
                    "boolean",
                ],
                # Even more tricky: these columns won't match their type
            ).astype({"float_64": np.float32, "int_64": np.int32}),
            index_names=["store_id", "product_id"],
        )

        # Expected when converting everything to float32
        self.expected_evset_2 = EventSet.from_dataframe(
            pd.DataFrame(
                data=[
                    # Note: astype() below will truncate above/below numbers
                    [TRYO_SHOP, MATE_ID, 0.0, -14.0, abv_i32, 1.2, 1],
                    [TRYO_SHOP, MATE_ID, 1.0, 15.0, 0, 2, 1],
                    [TRYO_SHOP, MATE_ID, 2.0, 16, 3, 0, 1],
                    [TRYO_SHOP, BOOK_ID, 1.0, 10, 4, 100, 0],
                    [GOOGLE_SHOP, BOOK_ID, 1.0, 0, 5, 3.2, 0],
                    [GOOGLE_SHOP, BOOK_ID, 2.0, 0, 6, 1, 1],
                    [GOOGLE_SHOP, PIXEL_ID, 0.0, -1, -8, -3.5, 0],
                    [GOOGLE_SHOP, PIXEL_ID, 1.0, blw_i64, 8, -2, 0],
                ],
                columns=[
                    "store_id",
                    "product_id",
                    "timestamp",
                    "float_64",
                    "int_64",
                    "str",
                    "boolean",
                ],
            ).astype(
                {
                    "float_64": np.float32,
                    "int_64": np.float32,
                    "str": np.float32,
                    "boolean": np.float32,
                }
            ),
            index_names=["store_id", "product_id"],
        )

        self.sampling = Sampling(
            [("store_id", int), ("product_id", int)],
            is_unix_timestamp=False,
        )
        self.input_node = Node(
            [
                ("float_64", float),  # tp.float64
                ("int_64", int),  # tp.int64
                ("str", str),
                ("boolean", bool),
            ],
            sampling=self.sampling,
            creator=None,
        )

    def test_cast_op_by_feature(self) -> None:
        """Test correct casting by feat. names, without overflow check."""

        operator = CastOperator(
            input=self.input_node,
            from_features={
                "float_64": DType.FLOAT32,
                "int_64": DType.INT32,
                "str": DType.FLOAT64,
                "boolean": DType.INT64,
            },
            check_overflow=False,
        )

        cast_implementation = CastNumpyImplementation(operator)

        operator_output = cast_implementation.call(input=self.input_evset)

        self.assertTrue(self.expected_evset_1 == operator_output["output"])

    def test_cast_op_by_dtype(self) -> None:
        """Test correct casting by origin DType, without overflow check."""

        operator = CastOperator(
            input=self.input_node,
            from_dtypes={
                DType.FLOAT64: DType.FLOAT32,
                DType.INT64: DType.INT32,
                DType.STRING: DType.FLOAT64,
                DType.BOOLEAN: DType.INT64,
                DType.INT32: DType.INT64,  # This one should have no effect
            },
            check_overflow=False,
        )

        cast_implementation = CastNumpyImplementation(operator)

        operator_output = cast_implementation.call(input=self.input_evset)

        self.assertTrue(self.expected_evset_1 == operator_output["output"])

    def test_cast_to_dtype(self) -> None:
        """Test correct casting everything to float32, no overflow check."""

        operator = CastOperator(
            input=self.input_node,
            to_dtype=DType.FLOAT32,
            check_overflow=False,
        )

        cast_implementation = CastNumpyImplementation(operator)

        operator_output = cast_implementation.call(input=self.input_evset)

        self.assertTrue(self.expected_evset_2 == operator_output["output"])

    def test_cast_no_effect(self) -> None:
        """Test the case in which there's nothing to do actually."""

        operator = CastOperator(
            input=self.input_node,
            from_dtypes={
                DType.FLOAT64: DType.FLOAT64,
                DType.INT64: DType.INT64,
                DType.STRING: DType.STRING,
                DType.BOOLEAN: DType.BOOLEAN,
            },
            check_overflow=True,
        )

        cast_implementation = CastNumpyImplementation(operator)

        operator_output = cast_implementation.call(input=self.input_evset)

        # Check against input event set
        self.assertTrue(self.input_evset == operator_output["output"])

    def test_overflow_int64_int32(self) -> None:
        """Test overflow check for int32, coming from int64."""

        operator = CastOperator(
            input=self.input_node,
            from_features={
                "int_64": DType.INT32,
            },
            check_overflow=True,
        )

        cast_implementation = CastNumpyImplementation(operator)

        with self.assertRaisesRegex(ValueError, "Overflow"):
            _ = cast_implementation.call(input=self.input_evset)

    def test_overflow_float64_float32(self) -> None:
        """Test overflow check for float32, coming from float64."""

        operator = CastOperator(
            input=self.input_node,
            from_dtypes={
                DType.FLOAT64: DType.FLOAT32,
            },
            check_overflow=True,
        )

        cast_implementation = CastNumpyImplementation(operator)

        with self.assertRaisesRegex(ValueError, "Overflow"):
            _ = cast_implementation.call(input=self.input_evset)

    def test_overflow_float64_int64(self) -> None:
        """Test overflow check for int64, coming from max float64"""

        operator = CastOperator(
            input=self.input_node,
            from_features={
                "float_64": DType.INT64,
            },
            check_overflow=True,
        )

        cast_implementation = CastNumpyImplementation(operator)

        with self.assertRaisesRegex(ValueError, "Overflow"):
            _ = cast_implementation.call(input=self.input_evset)

    def test_no_overflow_boolean(self) -> None:
        """Test that no overflow error is raised when
        converting to boolean type"""

        operator = CastOperator(
            input=self.input_node,
            from_features={
                "int_64": DType.BOOLEAN,
                "float_64": DType.BOOLEAN,
            },
            check_overflow=True,
        )

        cast_implementation = CastNumpyImplementation(operator)

        # This shouldn't raise error
        _ = cast_implementation.call(input=self.input_evset)

    def test_cast_by_feature_python_types(self) -> None:
        """Test correct casting by feat. names and using some python types"""

        operator = CastOperator(
            input=self.input_node,
            from_features={
                "float_64": DType.FLOAT32,
                "int_64": DType.INT32,
                "str": float,
                "boolean": int,
            },
            check_overflow=False,
        )

        cast_implementation = CastNumpyImplementation(operator)

        operator_output = cast_implementation.call(input=self.input_evset)

        self.assertTrue(self.expected_evset_1 == operator_output["output"])

    def test_cast_by_dtype_python_types(self) -> None:
        """Test correct casting by origin DType, without overflow check."""

        operator = CastOperator(
            input=self.input_node,
            from_dtypes={
                float: DType.FLOAT32,
                int: DType.INT32,
                str: DType.FLOAT64,
                bool: DType.INT64,
            },
            check_overflow=False,
        )

        cast_implementation = CastNumpyImplementation(operator)

        operator_output = cast_implementation.call(input=self.input_evset)

        self.assertTrue(self.expected_evset_1 == operator_output["output"])


if __name__ == "__main__":
    absltest.main()
