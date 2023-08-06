import math
import unittest

from Lab3.custom_serializer.encoder import Encoder, Decoder


def return_5():
    return 5


def recursion(x):
    if x < 2:
        return 1

    return recursion(x - 1) * x


def square(value):
    return value * value


def sqrt(value):
    return math.sqrt(value)


def function_use_return_5():
    return return_5()


GLOBAL_VAR = 10


def function_use_global_value():
    return GLOBAL_VAR


def double_result(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        return value * 2

    return wrapper


@double_result
def doubled():
    return 5


def func_with_closure():
    a = 10

    def closure():
        nonlocal a
        a += 1
        return a

    return closure


class TestFunction(unittest.TestCase):
    def test_without_params(self):
        encoded = Encoder.encode(return_5)
        decoded = Decoder.decode(encoded)

        result = return_5()
        test_result = decoded()

        self.assertEqual(result, test_result)

    def test_with_params(self):
        encoded = Encoder.encode(square)
        decoded = Decoder.decode(encoded)

        x = 2
        result = square(x)
        test_result = decoded(x)

        self.assertEqual(result, test_result)

    def test_with_lib(self):
        encoded = Encoder.encode(sqrt)
        decoded = Decoder.decode(encoded)

        x = 2
        result = sqrt(x)
        test_result = decoded(x)

        self.assertEqual(result, test_result)

    def test_with_recursion(self):
        encoded = Encoder.encode(recursion)
        decoded = Decoder.decode(encoded)

        x = 2
        result = recursion(x)
        test_result = decoded(x)

        self.assertEqual(result, test_result)

    def test_with_lambda(self):
        func = lambda val: val * val
        encoded = Encoder.encode(func)
        decoded = Decoder.decode(encoded)

        x = 2
        result = func(x)
        test_result = decoded(x)

        self.assertEqual(result, test_result)

    def test_function_with_another_function(self):
        encoded = Encoder.encode(function_use_return_5)
        decoded = Decoder.decode(encoded)

        result = function_use_return_5()
        test_result = decoded()

        self.assertEqual(result, test_result)

    def test_function_use_global_value(self):
        encoded = Encoder.encode(function_use_global_value)
        decoded = Decoder.decode(encoded)

        result = function_use_global_value()
        test_result = decoded()

        self.assertEqual(result, test_result)

    def test_with_decorator(self):
        encoded = Encoder.encode(doubled)
        decoded = Decoder.decode(encoded)

        result = doubled()
        test_result = decoded()

        self.assertEqual(result, test_result)

    def test_with_closure(self):
        encoded = Encoder.encode(func_with_closure())
        decoded = Decoder.decode(encoded)

        result = func_with_closure()()
        test_result = decoded()

        self.assertEqual(result, test_result)


iterator = iter([1, 2, 3])


def gen():
    yield 1
    yield 2
    yield 3


class TestIterators(unittest.TestCase):
    def test_iter(self):
        encoded = Encoder.encode(iterator)
        decoded_iter = Decoder.decode(encoded)

        result = [1, 2, 3]
        result_to_test = list(decoded_iter)

        return self.assertSequenceEqual(result, result_to_test)

    def test_generator_function(self):
        encoded = Encoder.encode(gen)
        decoded_function = Decoder.decode(encoded)

        result = [1, 2, 3]
        result_to_test = list(decoded_function())

        return self.assertSequenceEqual(result, result_to_test)

    def test_generator_obj(self):
        encoded = Encoder.encode(gen())
        decoded_gen = Decoder.decode(encoded)

        result = [1, 2, 3]
        result_to_test = list(decoded_gen)

        return self.assertSequenceEqual(result, result_to_test)


if __name__ == '__main__':
    unittest.main()
