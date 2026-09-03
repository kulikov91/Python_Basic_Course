import unittest

from task9 import Fibo, integers, primes


class TestFibo(unittest.TestCase):

    def test_first_numbers(self):
        fibo = Fibo()

        result = []

        for i in range(10):
            result.append(next(fibo))

        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

        self.assertEqual(result, expected)

    def test_iter_returns_self(self):
        fibo = Fibo()

        self.assertIs(iter(fibo), fibo)

    def test_two_iterators_are_independent(self):
        first = Fibo()
        second = Fibo()

        self.assertEqual(next(first), 0)
        self.assertEqual(next(first), 1)

        self.assertEqual(next(second), 0)
        self.assertEqual(next(second), 1)


class TestIntegers(unittest.TestCase):

    def test_first_numbers(self):
        generator = integers()

        result = []

        for i in range(10):
            result.append(next(generator))

        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertEqual(result, expected)

    def test_generator_continues(self):
        generator = integers()

        for i in range(100):
            number = next(generator)

        self.assertEqual(number, 99)


class TestPrimes(unittest.TestCase):

    def test_first_primes(self):
        generator = primes()

        result = []

        for i in range(10):
            result.append(next(generator))

        expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        self.assertEqual(result, expected)

    def test_more_primes(self):
        generator = primes()

        result = []

        for i in range(15):
            result.append(next(generator))

        self.assertEqual(
            result,
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        )


if __name__ == "__main__":
    unittest.main()
