from abc import ABC, abstractmethod
import typing
from typing import Union, Dict, Any
from weakref import WeakValueDictionary
from ..serializer import BaseSerializer


class Base(ABC):

    _callbacks = WeakValueDictionary()

    def callback(self, message_code: int):
        """
            Callbacks register
            Example of callback

            @dispatcher.callback(message_code=3)
            async def account_handler(data: Account, account_id: Optional[int]) -> None:
                print(data.holder)

            data - User defined serializer class

        :param message_code: Code of message from message headers
        :return:
        """
        def wrapper(f):
            def inner_wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            self.__class__._callbacks[message_code] = f
            return inner_wrapper
        return wrapper

    def parse_binary_data(self, message_serializer, binary_data):

        if isinstance(message_serializer, typing._GenericAlias):
            model = message_serializer.__args__[0]
            data = message_serializer(model=model, buffer=binary_data)
        elif issubclass(message_serializer, BaseSerializer):
            data = message_serializer(byte_data=binary_data)
        else:
            raise TypeError()

        return data

    def parse_arguments(self, f, **kwargs) -> Dict[str, Any]:
        parameters = dict()

        message_serializer = f.__annotations__['data']
        parameters['data'] = self.parse_binary_data(message_serializer, kwargs['binary_data'])

        if 'account_id' in f.__annotations__:
            parameters['account_id'] = kwargs.get('account_id')

        return parameters

    @abstractmethod
    def invoke(
            self,
            message_code: int,
            payload: Union[memoryview, bytearray, bytes],
            *,
            account_id: int = None
    ):
        ...


class Dispatcher(Base):

    def invoke(
            self,
            message_code: int,
            payload: Union[memoryview, bytearray, bytes],
            *,
            account_id: int = None
    ):
        callback = self._callbacks.get(message_code)
        if callback:
            return callback(**self.parse_arguments(callback, binary_data=payload, account_id=account_id))


class AsyncDispatcher(Base):

    async def invoke(
            self,
            message_code: int,
            payload: Union[memoryview, bytearray, bytes],
            *,
            account_id: int = None
    ):
        callback = self._callbacks.get(message_code)
        if callback:
            return await callback(**self.parse_arguments(callback, binary_data=payload, account_id=account_id))
