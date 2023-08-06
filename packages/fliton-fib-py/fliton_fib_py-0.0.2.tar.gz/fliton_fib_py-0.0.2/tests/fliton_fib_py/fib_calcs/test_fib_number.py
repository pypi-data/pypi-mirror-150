from unittest import main, TestCase
from fliton_fib_py.fib_calcs.fib_number import recur_fib_num


class RecurringFibNumbersTest(TestCase):
    def test_zero(self):
        self.assertEqual(0, recur_fib_num(number=0))

    def test_negative(self):
        with self.assertRaises(ValueError) as raised_error:
            recur_fib_num(-1)
        self.assertEqual("Fibonacci has to start from 1",
                         str(raised_error.exception))

    def test_one(self):
        self.assertEqual(1, recur_fib_num(1))

    def test_two(self):
        self.assertEqual(1, recur_fib_num(2))

    def test_twenty(self):
        self.assertEqual(6765, recur_fib_num(number=20))


if __name__ == "__main__":
    main()
