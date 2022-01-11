from typing import Union, Dict, Callable
from weakref import WeakValueDictionary


class Dispatcher:

    __callbacks = WeakValueDictionary()

    def invoke(self, message_code: int, payload: Union[memoryview, bytearray, bytes]):
        callback = self.__callbacks.get(message_code)
        if callback:
            return self._invoker(callback, payload)

    def _invoker(self, f, binary_data):
        message_serializer = f.__annotations__['data'].__args__[0]
        data = message_serializer(byte_data=binary_data)
        return f(data)

    async def async_invoke(self, message_code: int, payload: Union[memoryview, bytearray, bytes]):
        callback = self.__callbacks.get(message_code)
        if callback:
            return await self._async_invoker(callback, payload)

    async def _async_invoker(self, f, binary_data):
        message_serializer = f.__annotations__['data'].__args__[0]
        data = message_serializer(byte_data=binary_data)
        return await f(data)

    def callback(self, message_code: int):
        """
            Callbacks register
        :param message_code:
        :return:
        """
        def wrapper(f):
            def inner_wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            self.__class__.__callbacks[message_code] = f
            return inner_wrapper
        return wrapper
