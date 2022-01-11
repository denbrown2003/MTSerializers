from typing import Type
from .base import BaseSerializer

__all__ = [
    'ListSerializer'
]


class ListSerializer:

    __slots__ = "model", "buffer", "model_size"

    def __init__(self, model: Type[BaseSerializer], buffer: memoryview):
        self.model = model
        self.buffer = buffer

        self.model_size = model.full_size

    def __iter__(self):
        for idx, i in enumerate(range(0, len(self.buffer), self.model_size)):
            model_buff = self.buffer[i:i + self.model_size]
            model = self.model(model_buff)
            yield model.get_data()

    def get_objects(self):
        return list(self.__iter__())

    def __len__(self):
        return len(self.buffer) // self.model_size
