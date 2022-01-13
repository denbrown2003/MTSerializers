import datetime
from typing import Union, Type
from .dersciptor import BaseDescriptor, SequentialDescriptor

__all__ = [
    'Int8',
    'Int16',
    'Int32',
    'Int64',
    'UInt8',
    'UInt16',
    'UInt32',
    'UInt64',
    'Float32',
    'Float64',
    'String',
    'Bool',
    'Datetime'
]


# Integers
class Int8(BaseDescriptor):
    format = "b"


class Int16(BaseDescriptor):
    format = "h"


class Int32(BaseDescriptor):
    format = "i"


class Int64(BaseDescriptor):
    format = "l"


class UInt8(BaseDescriptor):
    format = "B"


class UInt16(BaseDescriptor):
    format = "H"


class UInt32(BaseDescriptor):
    format = "I"


class UInt64(BaseDescriptor):
    format = "L"


# Number with float point
class Float32(BaseDescriptor):
    format = "f"


class Float64(BaseDescriptor):
    format = "d"


# Rest
class Bool(BaseDescriptor):
    format = "?"


class String(SequentialDescriptor):
    format = "s"

    def __get__(self, instance, owner):
        return super().__get__(instance, owner).replace(b"\x00", b"").decode()

    def __set__(self, instance, value):
        super().__set__(instance, value.encode())


TimestampType = Union[Type[UInt32], Type[UInt64]]


class Datetime(BaseDescriptor):

    def __init__(self, *, data_type: TimestampType = UInt64, offset: int = None):
        """
            Some doc
        :param offset:
        """
        super().__init__(offset=offset)
        self.format = data_type.format

    def __get__(self, instance, owner):
        timestamp = super().__get__(instance, owner)
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt

    def __set__(self, instance, value):
        if isinstance(value, datetime.datetime):
            super().__set__(instance, int(value.timestamp()))
        elif isinstance(value, int):
            super().__set__(instance, value)
        else:
            raise TypeError("Wrong Datetime type")
