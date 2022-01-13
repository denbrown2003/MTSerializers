import time
import unittest
from src.mt4_utils import serializer
import datetime


class SerializerTestCase(unittest.TestCase):

    def test_check_string_field(self):

        class TestModel(serializer.BaseSerializer):
            name = serializer.String(length=5)

        test_string = "hello"

        ob = TestModel()
        ob.name = test_string
        data = ob.get_data()

        self.assertEqual(ob.name, test_string)
        self.assertEqual(data.name.decode(), test_string)

    def test_check_empty_integers(self):

        class TestModel(serializer.BaseSerializer):
            number = serializer.Int32()

        tm = TestModel()

        self.assertIsInstance(tm.number, int)
        self.assertEqual(tm.number, 0)

    def test_check_empty_floats(self):
        class TestModel(serializer.BaseSerializer):
            number = serializer.Float32()

        tm = TestModel()

        self.assertIsInstance(tm.number, float)
        self.assertEqual(tm.number, 0)

    def test_check_bool(self):
        class TestModel(serializer.BaseSerializer):
            flag = serializer.Bool()

        tm = TestModel()

        self.assertIsInstance(tm.flag, bool)
        self.assertFalse(tm.flag)

    def test_datetime_field(self):

        class TestModel(serializer.BaseSerializer):
            dt = serializer.Datetime()

        expected = datetime.datetime.now()
        test_obj = TestModel()
        test_obj.dt = expected

        self.assertIsInstance(test_obj.dt, datetime.datetime)
        self.assertEqual(expected, test_obj.dt)

    def test_datetime_empty_buffer(self):

        class TestModel(serializer.BaseSerializer):
            dt = serializer.Datetime()

        expected = datetime.datetime(1970, 1, 1, 4, 0)
        ob = TestModel()

        self.assertIsInstance(ob.dt, datetime.datetime)
        self.assertEqual(ob.dt, expected)

    def test_different_formats_datetime(self):

        class Test(serializer.BaseSerializer):
            time1 = serializer.Datetime()
            time2 = serializer.Datetime(data_type=serializer.UInt32)

        n = datetime.datetime.fromtimestamp(int(time.time()))
        t = Test()
        t.time1 = n
        t.time2 = n

        self.assertEqual(t.time1, n)
        self.assertEqual(t.time2, n)




class ListSerializerTestCase(unittest.TestCase):

    def setUp(self) -> None:

        class TestObject(serializer.BaseSerializer):
            a = serializer.Int32()
            b = serializer.Int32()

        self.model_class = TestObject
        self.size = 2
        self.buffer = memoryview(bytearray((255, 0, 0, 0, 100, 0, 0, 0) * self.size))

    def test_correct_size(self):
        l = serializer.ListSerializer(self.model_class, self.buffer)
        self.assertEqual(len(l), self.size)

    def test_check_objects(self):
        l = serializer.ListSerializer(self.model_class, self.buffer)
        for i in l:
            self.assertEqual(i.a, 255)
            self.assertEqual(i.b, 100)

    def test_wrong_buffer(self):
        buff = memoryview(bytearray([]))
        l = serializer.ListSerializer(self.model_class, buff)
        self.assertEqual(len(l), 0)

