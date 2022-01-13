from abc import ABC
from functools import lru_cache
import struct


__all__ = [
    'BaseDescriptor',
    'SequentialDescriptor'
]


class BaseDescriptor(ABC):

    format = None

    def __set_name__(self, owner, name):
        """ Prepare name sequence for namedtuple """
        names = getattr(owner, "names", "")
        setattr(owner, "names", names + f"{name} ")

    def __init__(self, *, offset: int = None):
        """
            Some doc
        :param offset:
        """
        self.offset = offset

    @lru_cache(maxsize=10)
    def __get__(self, instance, owner):
        value, = struct.unpack_from(self.format, instance._byte_data, self.offset)
        return value

    def __set__(self, instance, value):
        struct.pack_into(self.format, instance._byte_data, self.offset, value)


class SequentialDescriptor(BaseDescriptor, ABC):
    """
        BaseDescription for strings
    """

    def __init__(self, *, length: int, offset: int = None):
        super().__init__(offset=offset)
        self.format = f"{length}{self.format}"
        self.length = length

    def __set__(self, instance, value):
        if len(value) > self.length:
            value = value[:self.length]
        super().__set__(instance, value)
