from typing import Type, TypeVar, Generic, List, Iterator
from .base import BaseSerializer

__all__ = [
    'ListSerializer'
]

T = TypeVar('T')


class ListSerializer(Generic[T]):

    __slots__ = "model", "buffer", "model_size", "model_full_length"

    def __init__(self, model: T, buffer: memoryview):
        self.model = model
        self.buffer = buffer

        self.model_full_length = model.size if model.size else model.format_size
        self.model_size = model.format_size

    def __iter__(self) -> Iterator[T]:
        for idx, i in enumerate(range(0, len(self.buffer), self.model_full_length)):
            model_buff = self.buffer[i:i + self.model_size]
            model = self.model(model_buff)
            yield model

    def get_objects(self) -> List[T]:
        return list(self.__iter__())

    def __len__(self):
        return len(self.buffer) // self.model_size
