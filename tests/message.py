from typing import Type
import unittest
import serilizer
import message


class MessageTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.dispatcher = message.Dispatcher()

    def test_dispatcher_callback_wrapper(self):

        class TestModel(serilizer.BaseSerializer):
            status = serilizer.Int32()

        @self.dispatcher.callback(message_code=99)
        def test_func(data: Type[TestModel]) -> TestModel:
            return data

        callback = self.dispatcher._Dispatcher__callbacks[99]
        self.assertIsNotNone(callback)

    def test_dispatcher_wrapper_callbacks_mapper(self):

        class TestModel(serilizer.BaseSerializer):
            status = serilizer.String(length=5)

        class TestModel2(serilizer.BaseSerializer):
            code = serilizer.Int32()

        @self.dispatcher.callback(message_code=1)
        def test_func(data: Type[TestModel]) -> TestModel:
            return data

        @self.dispatcher.callback(message_code=2)
        def test_func2(data: Type[TestModel2]) -> TestModel2:
            return data

        payload1 = b"Hello"
        payload2 = b"\xFF\x00\x00\x00"

        response1 = self.dispatcher.invoke(1, payload1)
        response2 = self.dispatcher.invoke(2, payload2)

        self.assertIsInstance(response1, TestModel)
        self.assertIsInstance(response2, TestModel2)

        self.assertEqual(response1.status, "Hello")
        self.assertEqual(response2.code, 255)
