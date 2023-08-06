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

import pandas as pd

from temporian.core import evaluation
from temporian.core.data.dtype import DType
from temporian.core.data.node import Node
from temporian.core.data.node import Feature
from temporian.core.data.sampling import Sampling
from temporian.core.operators.lag import lag
from temporian.core.operators.lag import leak
from temporian.core.operators.lag import LagOperator
from temporian.implementation.numpy.data.event_set import EventSet
from temporian.implementation.numpy.operators.lag import LagNumpyImplementation


class LagNumpyImplementationTest(absltest.TestCase):
    """Test numpy implementation of lag operator."""

    def test_correct_lag(self) -> None:
        """Test correct lag operator."""
        input_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 1, 10.0],
                    [0, 1.5, 11.0],
                    [0, 3, 12.0],
                    [0, 3.5, 13.0],
                    [0, 4, 14.0],
                    [0, 10, 15.0],
                    [0, 20, 16.0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        output_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 3, 10.0],
                    [0, 3.5, 11.0],
                    [0, 5, 12.0],
                    [0, 5.5, 13.0],
                    [0, 6, 14.0],
                    [0, 12, 15.0],
                    [0, 22, 16.0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        node = Node(
            [Feature("sales", DType.FLOAT64)],
            sampling=Sampling(
                [("store_id", DType.INT64)], is_unix_timestamp=False
            ),
            creator=None,
        )
        operator = LagOperator(
            duration=2.0,
            input=node,
        )
        lag_implementation = LagNumpyImplementation(operator)
        operator_output = lag_implementation.call(input=input_evset)

        self.assertTrue(output_evset == operator_output["output"])

    def test_correct_multiple_lags(self) -> None:
        """Test correct lag operator with duration list."""
        input_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 1.0, 10.0],
                    [0, 2.0, 11.0],
                    [0, 3.0, 12.0],
                    [0, 4.0, 13.0],
                    [0, 5.0, 14.0],
                    [0, 6.0, 15.0],
                    [0, 7.0, 16.0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        expected_lag_1_output_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 2.0, 10.0],
                    [0, 3.0, 11.0],
                    [0, 4.0, 12.0],
                    [0, 5.0, 13.0],
                    [0, 6.0, 14.0],
                    [0, 7.0, 15.0],
                    [0, 8.0, 16.0],
                ],
                columns=[
                    "store_id",
                    "timestamp",
                    "sales",
                ],
            ),
            index_names=["store_id"],
        )
        expected_lag_2_output_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 3.0, 10.0],
                    [0, 4.0, 11.0],
                    [0, 5.0, 12.0],
                    [0, 6.0, 13.0],
                    [0, 7.0, 14.0],
                    [0, 8.0, 15.0],
                    [0, 9.0, 16.0],
                ],
                columns=[
                    "store_id",
                    "timestamp",
                    "sales",
                ],
            ),
            index_names=["store_id"],
        )
        node = input_evset.node()

        # lag multiple durations
        lags = lag(input=node, duration=[1, 2])
        lag_1 = lags[0]

        # evaluate
        output_evset_lag_1 = evaluation.evaluate(
            lag_1,
            input={
                node: input_evset,
            },
        )
        # validate
        self.assertEqual(expected_lag_1_output_evset, output_evset_lag_1)
        lag_2 = lags[1]

        # evaluate
        output_evset_lag_2 = evaluation.evaluate(
            lag_2,
            input={
                node: input_evset,
            },
        )
        # validate
        self.assertEqual(expected_lag_2_output_evset, output_evset_lag_2)

    def test_correct_leak(self) -> None:
        """Test correct leak operator."""
        input_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 1, 10.0],
                    [0, 1.5, 11.0],
                    [0, 3, 12.0],
                    [0, 3.5, 13.0],
                    [0, 4, 14.0],
                    [0, 10, 15.0],
                    [0, 20, 16.0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        output_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, -1, 10.0],
                    [0, -0.5, 11.0],
                    [0, 1, 12.0],
                    [0, 1.5, 13.0],
                    [0, 2, 14.0],
                    [0, 8, 15.0],
                    [0, 18, 16.0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        node = Node(
            [Feature("sales", DType.FLOAT64)],
            sampling=Sampling(
                [("store_id", DType.INT64)], is_unix_timestamp=False
            ),
            creator=None,
        )
        operator = LagOperator(
            duration=-2.0,
            input=node,
        )
        lag_implementation = LagNumpyImplementation(operator)
        operator_output = lag_implementation.call(input=input_evset)

        self.assertTrue(output_evset == operator_output["output"])

    def test_correct_multiple_leaks(self) -> None:
        """Test correct leak operator with duration list."""
        input_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 1.0, 10.0],
                    [0, 2.0, 11.0],
                    [0, 3.0, 12.0],
                    [0, 4.0, 13.0],
                    [0, 5.0, 14.0],
                    [0, 6.0, 15.0],
                    [0, 7.0, 16.0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            index_names=["store_id"],
        )
        expected_leak_1_output_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, 0.0, 10.0],
                    [0, 1.0, 11.0],
                    [0, 2.0, 12.0],
                    [0, 3.0, 13.0],
                    [0, 4.0, 14.0],
                    [0, 5.0, 15.0],
                    [0, 6.0, 16.0],
                ],
                columns=[
                    "store_id",
                    "timestamp",
                    "sales",
                ],
            ),
            index_names=["store_id"],
        )
        expected_leak_2_output_evset = EventSet.from_dataframe(
            pd.DataFrame(
                [
                    [0, -1.0, 10.0],
                    [0, 0.0, 11.0],
                    [0, 1.0, 12.0],
                    [0, 2.0, 13.0],
                    [0, 3.0, 14.0],
                    [0, 4.0, 15.0],
                    [0, 5.0, 16.0],
                ],
                columns=[
                    "store_id",
                    "timestamp",
                    "sales",
                ],
            ),
            index_names=["store_id"],
        )
        node = input_evset.node()

        # leak multiple durations
        leaks = leak(input=node, duration=[1, 2])
        leak_1 = leaks[0]

        # evaluate
        output_evset_leak_1 = evaluation.evaluate(
            leak_1,
            input={
                node: input_evset,
            },
        )
        # validate
        self.assertEqual(expected_leak_1_output_evset, output_evset_leak_1)
        leak_2 = leaks[1]

        # evaluate
        output_evset_leak_2 = evaluation.evaluate(
            leak_2,
            input={
                node: input_evset,
            },
        )
        # validate
        self.assertEqual(expected_leak_2_output_evset, output_evset_leak_2)


if __name__ == "__main__":
    absltest.main()
