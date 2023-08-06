"""Test interplay of the various Avro helper classes"""
from datetime import datetime
from typing import List
from unittest import TestCase

from opaque_keys.edx.keys import CourseKey, UsageKey

from openedx_events.event_bus.avro.deserializer import AvroSignalDeserializer, deserialize_bytes_to_event_data
from openedx_events.event_bus.avro.serializer import AvroSignalSerializer, serialize_event_data_to_bytes
from openedx_events.event_bus.avro.tests.test_utilities import (
    EventData,
    NestedAttrsWithDefaults,
    SimpleAttrsWithDefaults,
    SubTestData0,
    SubTestData1,
    create_simple_signal,
)
from openedx_events.tests.utils import FreezeSignalCacheMixin
from openedx_events.tooling import OpenEdxPublicSignal, load_all_signals

# If a signal is explicitly not for use with the event bus, add it to this list
#  and document why in the event's annotations
KNOWN_UNSERIALIZABLE_SIGNALS = [
    "org.openedx.learning.discussions.configuration.changed.v1",
    "org.openedx.content_authoring.course.certificate_config.changed.v1",
    "org.openedx.content_authoring.course.certificate_config.deleted.v1",
]


def generate_test_event_data_for_data_type(data_type):
    """
    Generates test data for use in the event bus test cases.

    Builds data by filling in dummy data for basic data types (int/float/bool/str)
    and recursively breaks down the classes for nested classes into basic data types.

    Arguments:
        data_type: The type of the data which we are generating data for

    Returns:
        (dict): A data dictionary containing dummy data for all attributes of the class
    """
    data_dict = {}
    defaults_per_type = {
        int: 1,
        bool: True,
        str: "default",
        float: 1.0,
        CourseKey: CourseKey.from_string("course-v1:edX+DemoX.1+2014"),
        UsageKey: UsageKey.from_string(
            "block-v1:edx+DemoX+Demo_course+type@video+block@UaEBjyMjcLW65gaTXggB93WmvoxGAJa0JeHRrDThk",
        ),
        List[int]: [1, 2, 3],
        datetime: datetime.now(),
    }
    for attribute in data_type.__attrs_attrs__:
        result = defaults_per_type.get(attribute.type, None)
        if result is not None:
            data_dict.update({attribute.name: result})
        elif attribute.type in [dict, list]:
            # pylint: disable-next=broad-exception-raised
            raise Exception("Unable to generate Avro schema for dict or array fields")
        else:
            data_dict.update({attribute.name: attribute.type(**generate_test_event_data_for_data_type(attribute.type))})
    return data_dict


class TestAvro(FreezeSignalCacheMixin, TestCase):
    """Tests for end-to-end serialization and deserialization of events"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure we can usefully call all_events()
        load_all_signals()

    def test_all_events(self):
        for signal in OpenEdxPublicSignal.all_events():
            if signal.event_type in KNOWN_UNSERIALIZABLE_SIGNALS:
                continue
            test_data = {}
            serializer = AvroSignalSerializer(signal)
            for key, curr_class in signal.init_data.items():
                example_data = generate_test_event_data_for_data_type(curr_class)
                example_data_processed = curr_class(**example_data)
                test_data.update({key: example_data_processed})
            serialized = serializer.to_dict(test_data)
            deserializer = AvroSignalDeserializer(signal)
            deserialized = deserializer.from_dict(serialized)
            self.assertDictEqual(deserialized, test_data)

    def test_full_serialize_deserialize(self):
        SIGNAL = create_simple_signal({"test_data": EventData})
        event_data = {"test_data": EventData(
            "foo",
            "bar.course",
            SubTestData0("a.sub.name", "a.nother.course"),
            SubTestData1("b.uber.sub.name", "b.uber.another.course"),
        )}
        serialized = serialize_event_data_to_bytes(event_data, SIGNAL)
        deserialized = deserialize_bytes_to_event_data(serialized, SIGNAL)
        self.assertIsInstance(deserialized["test_data"], EventData)
        self.assertEqual(deserialized, event_data)
        # ensure signal can actually send deserialized event data
        SIGNAL.send_event(**deserialized)

    def test_full_serialize_deserialize_with_optional_fields(self):
        SIGNAL = create_simple_signal({"test_data": NestedAttrsWithDefaults})
        event_data = {"test_data": NestedAttrsWithDefaults(field_0=SimpleAttrsWithDefaults())}
        serialized = serialize_event_data_to_bytes(event_data, SIGNAL)
        deserialized = deserialize_bytes_to_event_data(serialized, SIGNAL)
        self.assertIsInstance(deserialized["test_data"], NestedAttrsWithDefaults)
        self.assertEqual(deserialized, event_data)
        # ensure signal can actually send deserialized event data
        SIGNAL.send_event(**deserialized)
