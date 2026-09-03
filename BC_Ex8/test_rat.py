import math
import unittest

from rat_num import RatNum
from rat_poly import RatPoly


class TestRatNum(unittest.TestCase):

    def test_create_integer(self):
        self.assertEqual(str(RatNum(4)), "4")

    def test_create_fraction(self):
        self.assertEqual(str(RatNum(2, 4)), "1/2")

    def test_negative_denominator(self):
        self.assertEqual(str(RatNum(1, -2)), "-1/2")

    def test_zero(self):
        self.assertEqual(str(RatNum(0, 15)), "0")

    def test_nan(self):
        self.assertTrue(RatNum(5, 0).is_nan())
        self.assertEqual(str(RatNum(5, 0)), "NaN")

    def test_constructor_type_error(self):
        with self.assertRaises(TypeError):
            RatNum(1.5, 2)

    def test_is_negative(self):
        self.assertTrue(RatNum(-1, 2).is_negative())
        self.assertFalse(RatNum(0).is_negative())
        self.assertFalse(RatNum(1, 0).is_negative())

    def test_is_positive(self):
        self.assertTrue(RatNum(1, 2).is_positive())
        self.assertFalse(RatNum(0).is_positive())
        self.assertFalse(RatNum(1, 0).is_positive())

    def test_compare(self):
        self.assertEqual(RatNum(1, 2).compare_to(RatNum(2, 3)), -1)
        self.assertEqual(RatNum(2, 3).compare_to(RatNum(1, 2)), 1)
        self.assertEqual(RatNum(2, 4).compare_to(RatNum(1, 2)), 0)

    def test_compare_nan(self):
        nan = RatNum(0, 0)
        self.assertEqual(nan.compare_to(RatNum(10)), 1)
        self.assertEqual(RatNum(10).compare_to(nan), -1)
        self.assertEqual(nan.compare_to(RatNum(1, 0)), 0)

    def test_float_value(self):
        self.assertAlmostEqual(RatNum(1, 4).float_value(), 0.25)
        self.assertTrue(math.isnan(RatNum(1, 0).float_value()))

    def test_int_value(self):
        self.assertEqual(RatNum(7, 3).int_value(), 2)
        self.assertEqual(RatNum(-7, 3).int_value(), -2)

    def test_int_value_nan(self):
        with self.assertRaises(ValueError):
            RatNum(1, 0).int_value()

    def test_negative(self):
        self.assertEqual(-RatNum(2, 3), RatNum(-2, 3))

    def test_add(self):
        self.assertEqual(RatNum(1, 2) + RatNum(1, 3), RatNum(5, 6))

    def test_sub(self):
        self.assertEqual(RatNum(1, 2) - RatNum(1, 3), RatNum(1, 6))

    def test_mul(self):
        self.assertEqual(RatNum(2, 3) * RatNum(3, 4), RatNum(1, 2))

    def test_div(self):
        self.assertEqual(RatNum(2, 3) / RatNum(4, 5), RatNum(5, 6))

    def test_div_by_zero(self):
        self.assertTrue((RatNum(1) / RatNum(0)).is_nan())

    def test_nan_operations(self):
        nan = RatNum(0, 0)
        number = RatNum(2)
        self.assertTrue((nan + number).is_nan())
        self.assertTrue((nan - number).is_nan())
        self.assertTrue((nan * number).is_nan())
        self.assertTrue((number / nan).is_nan())

    def test_gcd(self):
        self.assertEqual(RatNum.gcd(12, 8), 4)
        self.assertEqual(RatNum.gcd(-12, 8), 4)
        self.assertEqual(RatNum.gcd(0, 5), 5)

    def test_equality(self):
        self.assertEqual(RatNum(2, 4), RatNum(1, 2))
        self.assertNotEqual(RatNum(1, 2), RatNum(2, 3))
        self.assertEqual(RatNum(1, 0), RatNum(100, 0))

    def test_hash(self):
        self.assertEqual(hash(RatNum(2, 4)), hash(RatNum(1, 2)))

    def test_immutable(self):
        number = RatNum(1, 2)
        with self.assertRaises(AttributeError):
            number._num = 100


class TestRatPoly(unittest.TestCase):

    def make_poly(self, *numbers):
        coeffs = []
        for number in numbers:
            coeffs.append(RatNum(number))
        return RatPoly(coeffs)

    def test_zero_poly(self):
        self.assertEqual(str(RatPoly()), "0")
        self.assertEqual(RatPoly().degree(), 0)

    def test_remove_high_zeros(self):
        poly = RatPoly([RatNum(1), RatNum(2), RatNum(0)])
        self.assertEqual(poly.degree(), 1)

    def test_nan_poly(self):
        poly = RatPoly([RatNum(1), RatNum(0, 0)])
        self.assertTrue(poly.is_nan())
        self.assertEqual(str(poly), "NaN")

    def test_degree(self):
        self.assertEqual(self.make_poly(1, 2, 3).degree(), 2)

    def test_degree_nan(self):
        with self.assertRaises(ValueError):
            RatPoly([RatNum(0, 0)]).degree()

    def test_get_coeff(self):
        poly = self.make_poly(1, 2, 3)
        self.assertEqual(poly.get_coeff(1), RatNum(2))
        self.assertEqual(poly.get_coeff(10), RatNum(0))

    def test_get_coeff_error(self):
        with self.assertRaises(ValueError):
            self.make_poly(1).get_coeff(-1)

    def test_scale_coeff(self):
        poly = self.make_poly(1, 2)
        result = poly.scale_coeff(RatNum(2))
        self.assertEqual(result, self.make_poly(2, 4))

    def test_negative(self):
        poly = self.make_poly(1, -2, 3)
        self.assertEqual(-poly, self.make_poly(-1, 2, -3))

    def test_add(self):
        first = self.make_poly(1, 2)
        second = self.make_poly(3, 4, 5)
        self.assertEqual(first + second, self.make_poly(4, 6, 5))

    def test_sub(self):
        first = self.make_poly(5, 4, 3)
        second = self.make_poly(2, 4)
        self.assertEqual(first - second, self.make_poly(3, 0, 3))

    def test_mul(self):
        first = self.make_poly(1, 1)
        second = self.make_poly(-1, 1)
        self.assertEqual(first * second, self.make_poly(-1, 0, 1))

    def test_div_exact(self):
        dividend = RatPoly.value_of("x^2-1")
        divisor = RatPoly.value_of("x-1")
        self.assertEqual(dividend / divisor, RatPoly.value_of("x+1"))

    def test_div_with_remainder(self):
        dividend = RatPoly.value_of("x^2+1")
        divisor = RatPoly.value_of("x+1")
        self.assertEqual(dividend / divisor, RatPoly.value_of("x-1"))

    def test_div_by_zero(self):
        result = self.make_poly(1, 2) / self.make_poly(0)
        self.assertTrue(result.is_nan())

    def test_eval_ratnum(self):
        poly = RatPoly.value_of("x^2+2*x+1")
        self.assertEqual(poly.eval(RatNum(2)), RatNum(9))

    def test_eval_float(self):
        poly = RatPoly.value_of("x^2+2*x+1")
        self.assertAlmostEqual(poly.eval(0.5), 2.25)

    def test_differentiate(self):
        poly = RatPoly.value_of("3*x^2+2*x+1")
        self.assertEqual(poly.differentiate(), RatPoly.value_of("6*x+2"))

    def test_differentiate_constant(self):
        self.assertEqual(self.make_poly(5).differentiate(), self.make_poly(0))

    def test_anti_differentiate(self):
        poly = RatPoly.value_of("4*x+3")
        result = poly.anti_differentiate(RatNum(7))
        self.assertEqual(result, RatPoly.value_of("2*x^2+3*x+7"))

    def test_integrate(self):
        poly = RatPoly.value_of("2*x")
        self.assertEqual(poly.integrate(RatNum(0), RatNum(3)), RatNum(9))

    def test_integrate_float(self):
        poly = RatPoly.value_of("x^2")
        self.assertAlmostEqual(poly.integrate(0.0, 2.0), 8 / 3)

    def test_value_of_zero(self):
        self.assertEqual(RatPoly.value_of("0"), self.make_poly(0))

    def test_value_of_nan(self):
        self.assertTrue(RatPoly.value_of("NaN").is_nan())

    def test_value_of_x(self):
        self.assertEqual(RatPoly.value_of("x"), self.make_poly(0, 1))
        self.assertEqual(RatPoly.value_of("-x"), self.make_poly(0, -1))

    def test_value_of_complex(self):
        poly = RatPoly.value_of("3/2*x^3-x+4")
        expected = RatPoly([
            RatNum(4),
            RatNum(-1),
            RatNum(0),
            RatNum(3, 2)
        ])
        self.assertEqual(poly, expected)

    def test_value_of_invalid(self):
        bad_values = ["", " x", "x ", "x^^2", "x+x", "2/0*x"]

        for value in bad_values:
            with self.assertRaises(ValueError):
                RatPoly.value_of(value)

    def test_string(self):
        poly = RatPoly([
            RatNum(1, 2),
            RatNum(-1),
            RatNum(3, 2)
        ])
        self.assertEqual(str(poly), "3/2*x^2-x+1/2")

    def test_equality_and_hash(self):
        first = self.make_poly(1, 2, 3)
        second = self.make_poly(1, 2, 3)
        self.assertEqual(first, second)
        self.assertEqual(hash(first), hash(second))


if __name__ == "__main__":
    unittest.main()
