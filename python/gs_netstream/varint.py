#!/usr/bin/env python
import numpy as np
from .constants import ENCODING_SIZES
"""Implementation for encoding unsigned varints."""


def encoding_size(value: int):
    """Computes the encoding size of a value."""
    dist = (ENCODING_SIZES - value) <= 0
    return 9 if not np.all(dist) else np.argmin(dist) + 1


def encode_unsigned(value):
    """Encodes a Python integer into its varint representation."""
    if not isinstance(value, int) or value < 0:
        raise TypeError("value argument is not an integer or is negative")
    size = encoding_size(value)
    buff = bytearray(size)
    for i in range(size):
        head = 128
        if i == size - 1:
            head = 0
        buff[i] = (((value >> (7 * i)) & 127) ^ head) & 255
    return buff
