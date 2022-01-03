from typing import Optional, Union
import struct
import collections
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
        full_size = 0
        format_ = "<"

        if bases:
            for k, i in  dct.items():
                if isinstance(i, BaseDescriptor):
                    offset = i.offset if i.offset is not None else full_size
                    size_ = struct.calcsize(i.format) + offset

                    if size_ < full_size:
                        raise SyntaxError("Wrong offset")

                    if full_size != offset:               # If schema has a paddings -> we make it
                        pad_size = i.offset - full_size
                        format_ += f"{pad_size}x{i.format}"
                    else:
                        format_ += i.format

                    full_size = size_
                    i.offset = offset

        x.full_size = full_size
        x.format = format_
        return x


class BaseSerializer(metaclass=SerializerMeta):

    def __init__(self, byte_data: Optional[Union[bytearray, memoryview]] = None):

        if isinstance(byte_data, bytearray):
            byte_data = memoryview(byte_data)

        elif byte_data is None:
            byte_data = memoryview(bytearray(b"\x00" * self.full_size))

        self._byte_data: memoryview = byte_data

    def get_data(self):
        tup = collections.namedtuple(self.__class__.__name__, self.names)
        return tup._make(struct.unpack(getattr(self, "format"), self._byte_data))

    def get_bytes(self) -> memoryview:
        return memoryview(self._byte_data)
