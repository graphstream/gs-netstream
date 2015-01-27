#!/usr/bin/env python

"""Implementation for encoding unsigned varints."""

def encoding_size(value):
    """Computes the encoding size of a value."""
    if value < (1L << 7):
        return 1
    if value < (1L << 14):
        return 2
    if value < (1L << 21):
        return 3
    if value < (1L << 28):
        return 4
    if value < (1L << 35):
        return 5
    if value < (1L << 42):
        return 6
    if value < (1L << 49):
        return 7
    if value < (1L << 56):
        return 8
    return 9

def encode_unsigned(value):
    """Encodes a Python integer into its varint representation."""
    if not isinstance(value, int) or value < 0:
        raise TypeError("value argument is not an integer or is negative")
    size = encoding_size(value)
    buff = bytearray(size)
    for i in xrange(size):
        head = 128
        if i == size - 1:
            head = 0
        buff[i] = (((value >> (7 * i)) & 127) ^ head) & 255
    return buff
