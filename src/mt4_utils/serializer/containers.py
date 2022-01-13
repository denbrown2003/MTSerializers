from functools import lru_cache
from typing import Type, TypeVar, Generic


__all__ = [
    'ListSerializer'
]

T = TypeVar('T')


class ListSerializer(Generic[T]):

    __slots__ = (
        "model",
        "buffer",
        "model_size",
        "model_full_length",
        "get_objects"
    )

    def __init__(self, model: T, buffer: memoryview):
        self.model = model
        self.buffer = buffer

        self.model_full_length = model.size if model.size else model.format_size
        self.model_size = model.format_size

        self.get_objects = lru_cache(maxsize=None)(self._get_objects)

    def __iter__(self):
        for idx, i in enumerate(range(0, len(self.buffer), self.model_full_length)):
            model_buff = self.buffer[i:i + self.model_size]
            model = self.model(model_buff)
            yield model.get_data()

    def _get_objects(self):
        return list(self.__iter__())

    def __len__(self):
        return len(self.buffer) // self.model_size
