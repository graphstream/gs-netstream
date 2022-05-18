"""Sender encoding utils"""
import struct
from itertools import chain
from typing import List, Callable

from .constants import *
import numpy as np


def encoding_size(value: int):
    """Computes the encoding size of a value."""
    dist = (ENCODING_SIZES - value) <= 0
    return 9 if not np.all(dist) else np.argmin(dist) + 1


def encode_unsigned(value):
    """Encodes a Python integer into its varint representation."""
    assert isinstance(value, int) and value >= 0, f"Value argument is not an integer or is negative = {value}"
    size = encoding_size(value)
    buff = bytearray(size)
    for i in range(size):
        head = 128
        if i == size - 1:
            head = 0
        buff[i] = (((value >> (7 * i)) & 127) ^ head) & 255
    return buff


TYPES_CONVERTER = {
    'bool': (TYPE_BOOLEAN, TYPE_BOOLEAN_ARRAY),
    'int': (TYPE_INT, TYPE_INT_ARRAY),
    'float': (TYPE_DOUBLE, TYPE_DOUBLE_ARRAY),
    'str': (TYPE_STRING, TYPE_STRING)
}


def get_type(value):
    """Get the data type for a given value."""
    is_array = isinstance(value, list)
    value_type_str = type(value[0] if is_array else value).__name__
    netstream_type = value_type_str.get(value_type_str, None)
    if netstream_type is None:
        raise NotImplementedError("dicts are not supported")

    type_pos = int(is_array)
    return netstream_type[type_pos]


def encode_array(values_array: List, single_value_type, encoding_method: Callable) -> bytearray:
    assert isinstance(values_array, list) and all([isinstance(v, single_value_type) for v in values_array]), \
        f"Values_array should be an array with values of type {single_value_type}, but values array = {values_array}"
    return bytearray(chain(encode_unsigned(len(values_array)), *[encoding_method(elem) for elem in values_array]))


def encode_boolean(value):
    """Encode a boolean type."""
    return bytearray([value & 1])


def encode_boolean_array(value: List[bool]):
    """Encode an array of boolean values."""
    return encode_array(value, bool, encode_boolean)


def encode_int_array(value):
    """Encode an array of integer values."""
    return encode_array(value, int, encode_unsigned)


def encode_double(value):
    """Encode a double type."""
    return bytearray(struct.pack("!d", value))


def encode_double_array(value):
    """Encode an array of double values."""
    return encode_array(value, float, encode_double)


def encode_string(string):
    """Encode a string type."""
    data = bytearray(string, "UTF-8")
    return bytearray(chain(encode_unsigned(len(data)), data))


def encode_byte(value):
    """Encode a byte type."""
    return bytearray([value])


TYPE_TO_ENCODER = {
    TYPE_BOOLEAN: encode_boolean,
    TYPE_BOOLEAN_ARRAY: encode_boolean_array,
    TYPE_INT: encode_unsigned,
    TYPE_INT_ARRAY: encode_int_array,
    TYPE_LONG: encode_unsigned,
    TYPE_LONG_ARRAY: encode_int_array,
    TYPE_DOUBLE: encode_double,
    TYPE_DOUBLE_ARRAY: encode_double_array,
    TYPE_STRING: encode_string
}


def encode_value(value, dtype):
    """Encode a value according to a given data type."""
    encoder = TYPE_TO_ENCODER[dtype]
    return encoder(value) if encoder is not None else None
