import collections
from functools import lru_cache
import struct
from typing import Optional, Union

from .dersciptor import BaseDescriptor


__all__ = [
    'BaseSerializer'
]


class SerializerMeta(type):

    def __new__(mcs, name, bases, dct):
        """
            Calculate size of struct and creating a struct format for unpacking
        :param name:
        :param bases:
        :param dct:
        """
        x = super().__new__(mcs, name, bases, dct)
        format_size = 0
        format_ = "<"

        if bases:
            for k, i in  dct.items():
                if isinstance(i, BaseDescriptor):
                    offset = i.offset if i.offset is not None else format_size
                    size_ = struct.calcsize(i.format) + offset

                    if size_ < format_size:
                        raise SyntaxError("Wrong offset")

                    if format_size != offset:               # If schema has a paddings -> we make it
                        pad_size = i.offset - format_size
                        format_ += f"{pad_size}x{i.format}"
                    else:
                        format_ += i.format

                    format_size = size_
                    i.offset = offset

        x.format_size = format_size
        x.format = format_
        return x


class BaseSerializer(metaclass=SerializerMeta):

    size = None

    def __init__(self, byte_data: Optional[Union[bytearray, memoryview]] = None):

        if isinstance(byte_data, bytearray):
            byte_data = memoryview(byte_data)

        elif byte_data is None:
            byte_data = memoryview(bytearray(b"\x00" * self.format_size))

        self._byte_data: memoryview = byte_data

        self.get_data = lru_cache(maxsize=None)(self._get_data)     # fix for gc

    def _get_data(self) -> collections.namedtuple:
        """
            To access to cache use get_data method
        :return:
        """
        tup = collections.namedtuple(self.__class__.__name__, self.names)
        return tup._make(struct.unpack(getattr(self, "format"), self._byte_data))

    def get_bytes(self) -> memoryview:
        return memoryview(self._byte_data)
