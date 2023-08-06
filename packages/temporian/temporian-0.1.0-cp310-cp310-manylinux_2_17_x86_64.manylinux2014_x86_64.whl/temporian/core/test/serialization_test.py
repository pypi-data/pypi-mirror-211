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

from absl import logging
from absl.testing import absltest
import pandas as pd

import temporian as tp
from temporian.core import serialization
from temporian.core import graph
from temporian.core.test import utils
from temporian.implementation.numpy.data.event_set import EventSet


class SerializeTest(absltest.TestCase):
    def test_serialize(self):
        i1 = utils.create_input_node()
        o2 = utils.OpI1O1(i1)
        i3 = utils.create_input_node()
        o4 = utils.OpI2O1(o2.outputs["output"], i3)
        o5 = utils.OpI1O2(o4.outputs["output"])

        original, _ = graph.infer_graph(
            {
                "io_input_1": i1,
                "io_input_2": i3,
            },
            {
                "io_output_1": o5.outputs["output_1"],
                "io_output_2": o4.outputs["output"],
            },
        )
        logging.info("original:\n%s", original)

        proto = serialization.serialize(original)
        logging.info("proto:\n%s", proto)

        restored = serialization.unserialize(proto)
        logging.info("restored:\n%s", restored)

        self.assertEqual(len(original.samplings), len(restored.samplings))
        self.assertEqual(len(original.features), len(restored.features))
        self.assertEqual(len(original.operators), len(restored.operators))
        self.assertEqual(len(original.nodes), len(restored.nodes))
        self.assertEqual(original.inputs.keys(), restored.inputs.keys())
        self.assertEqual(original.outputs.keys(), restored.outputs.keys())
        # TODO: Deep equality tests.

        # Ensures that "original" and "restored" don't link to the same objects.
        self.assertFalse(
            serialization.all_identifiers(original.samplings)
            & serialization.all_identifiers(restored.samplings)
        )
        self.assertFalse(
            serialization.all_identifiers(original.features)
            & serialization.all_identifiers(restored.features)
        )
        self.assertFalse(
            serialization.all_identifiers(original.operators)
            & serialization.all_identifiers(restored.operators)
        )
        self.assertFalse(
            serialization.all_identifiers(original.nodes)
            & serialization.all_identifiers(restored.nodes)
        )
        self.assertFalse(
            serialization.all_identifiers(original.inputs.values())
            & serialization.all_identifiers(restored.inputs.values())
        )
        self.assertFalse(
            serialization.all_identifiers(original.outputs.values())
            & serialization.all_identifiers(restored.outputs.values())
        )

    def test_serialize_autonode(self):
        input_data = EventSet.from_dataframe(
            pd.DataFrame(
                {
                    "timestamp": [0.0, 2.0, 4.0, 6.0],
                    "f1": [1.0, 2.0, 3.0, 4.0],
                    "x": [1, 1, 2, 2],
                },
            ),
            index_names=["x"],
        )

        input_node = input_data.node()
        output_node = tp.simple_moving_average(input_node, 2.0)

        original, _ = graph.infer_graph(
            {"i": input_node},
            {"o": output_node},
        )
        logging.info("original:\n%s", original)

        proto = serialization.serialize(original)
        logging.info("proto:\n%s", proto)

        restored = serialization.unserialize(proto)
        logging.info("restored:\n%s", restored)

    def test_serialize_attributes(self):
        """
        Test serialization with different types of operator attributes
        """
        attributes = {
            "attr_int": 1,
            "attr_str": "hello",
            "attr_list": ["temporian", "rocks"],
            "attr_float": 5.0,
            "attr_bool": True,
            "attr_map": {"good": "bye", "nice": "to", "meet": "you"},
        }
        i_event = utils.create_input_node()
        operator = utils.OpWithAttributes(i_event, **attributes)

        original, _ = graph.infer_graph(
            inputs={"i_event": i_event},
            outputs={"output": operator.outputs["output"]},
        )
        logging.info("original:\n%s", original)

        proto = serialization.serialize(original)
        logging.info("proto:\n%s", proto)

        restored = serialization.unserialize(proto)
        logging.info("restored:\n%s", restored)

        self.assertEqual(len(original.operators), len(restored.operators))
        self.assertEqual(original.inputs.keys(), restored.inputs.keys())
        self.assertEqual(original.outputs.keys(), restored.outputs.keys())

        # Check all restored attributes for the only operator
        restored_attributes = list(restored.operators)[0].attributes
        for attr_name, attr_value in attributes.items():
            self.assertEqual(attr_value, restored_attributes[attr_name])

        self.assertFalse(
            serialization.all_identifiers(original.operators)
            & serialization.all_identifiers(restored.operators)
        )
        self.assertFalse(
            serialization.all_identifiers(original.inputs.values())
            & serialization.all_identifiers(restored.inputs.values())
        )
        self.assertFalse(
            serialization.all_identifiers(original.outputs.values())
            & serialization.all_identifiers(restored.outputs.values())
        )


if __name__ == "__main__":
    absltest.main()
