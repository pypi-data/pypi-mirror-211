import unittest

from lab3.custom_serializer.encoder import Encoder, Decoder


class ClassWithValue:
    a = 1


class ClassWithDecorators:
    a = 1

    @staticmethod
    def test_static():
        return 1

    @classmethod
    def test_class(cls):
        return cls.a


class TestSimpleClass(unittest.TestCase):
    def test_class_with_value(self):
        encoded = Encoder.encode(ClassWithValue)
        decoded = Decoder.decode(encoded)

        result = ClassWithValue.a
        test_result = decoded.a

        self.assertEqual(result, test_result)

    def test_class_with_decorator(self):
        encoded = Encoder.encode(ClassWithDecorators)
        decoded = Decoder.decode(encoded)

        result = ClassWithDecorators.test_static()
        test_result = decoded.test_static()

        self.assertEqual(result, test_result)

        result = ClassWithDecorators.test_class()
        test_result = decoded.test_class()

        self.assertEqual(result, test_result)


class ClassA:
    def __init__(self):
        super().__init__()
        self.a = 1

    def method_a(self):
        return self.a


class ClassB:
    def __init__(self):
        super().__init__()
        self.b = 2

    def method_b(self):
        return self.b


class ClassC(ClassB, ClassA):
    def __init__(self):
        super().__init__()


class TestInherited(unittest.TestCase):
    def test_inheritance(self):
        encoded = Encoder.encode(ClassC)
        decoded = Decoder.decode(encoded)

        result = ClassC().method_a()
        result_to_test = decoded().method_a()

        self.assertEqual(result, result_to_test)

        result = ClassC().method_b()
        result_to_test = decoded().method_b()

        self.assertEqual(result, result_to_test)


class TestObjects(unittest.TestCase):
    def test_object(self):
        encoded = Encoder.encode(ClassC())
        decoded = Decoder.decode(encoded)

        result = ClassC().method_a()
        result_to_test = decoded.method_a()

        self.assertEqual(result, result_to_test)

        result = ClassC().method_b()
        result_to_test = decoded.method_b()

        self.assertEqual(result, result_to_test)


if __name__ == '__main__':
    unittest.main()
