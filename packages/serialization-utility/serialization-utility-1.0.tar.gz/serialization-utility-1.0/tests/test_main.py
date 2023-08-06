import inspect
import math

from lib.parsers.json_parser import JsonSerializer
from tests import test_data

serializer = JsonSerializer()


def serialize_pattern(value: any):
    serialized = serializer.dumps(value)

    return serializer.loads(serialized)


def get_pub_attributes(class_type: type):
    attributes = inspect.getmembers(class_type, lambda attr: not (inspect.isroutine(attr)))

    return [attr for attr in attributes if not (attr[0].startswith('__') and attr[0].endswith('__'))]


def test_primitives():
    result = serialize_pattern(test_data.primitive_int)
    assert result == test_data.primitive_int

    result = serialize_pattern(test_data.primitive_str)
    assert result == test_data.primitive_str

    result = serialize_pattern(test_data.primitive_float)
    assert result == test_data.primitive_float

    result = serialize_pattern(test_data.primitive_bool)
    assert result == test_data.primitive_bool

    result = serialize_pattern(test_data.primitive_none)
    assert result == test_data.primitive_none


def test_bytes():
    result = serialize_pattern(test_data.example_bytes)
    assert result.hex() == test_data.example_bytes_hex


def test_list_dict_tuple():
    result = serialize_pattern(test_data.example_dict)
    assert result == test_data.example_dict

    result = serialize_pattern(test_data.example_list)
    assert result == test_data.example_list

    result = serialize_pattern(test_data.example_tuple)
    assert result == test_data.example_tuple


def test_functions():
    result = serialize_pattern(test_data.example_function)
    assert math.isclose(result(0), test_data.example_function(0)) == True

    result = serialize_pattern(test_data.example_function)
    assert math.isclose(result(1), test_data.example_function(1)) == True

    result = serialize_pattern(test_data.example_function)
    assert math.isclose(result(2), test_data.example_function(-2)) == False


def test_classes():
    result = serialize_pattern(test_data.TestSimpleClass)
    assert get_pub_attributes(result) == get_pub_attributes(test_data.TestSimpleClass)

    result = serialize_pattern(test_data.TestClass)
    assert result(5).inner_func(7) == test_data.TestClass(5).inner_func(7)
