import io
import unittest
from unittest.mock import patch


class TestCalculate(unittest.TestCase):
    def setUp(self):
        # Import inside tests to ensure path is resolved at runtime
        from src.calculator import calculate  # type: ignore
        self.calculate = calculate

    def test_addition(self):
        self.assertEqual(self.calculate(2, '+', 3), 5)

    def test_subtraction(self):
        self.assertEqual(self.calculate(10, '-', 4), 6)

    def test_multiplication(self):
        self.assertEqual(self.calculate(7, '*', 6), 42)

    def test_division(self):
        self.assertEqual(self.calculate(7, '/', 2), 3.5)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculate(1, '/', 0)

    def test_unsupported_operation(self):
        with self.assertRaises(ValueError):
            self.calculate(1, '^', 2)

    def test_negative_numbers(self):
        self.assertEqual(self.calculate(-2, '*', 3), -6)
        self.assertEqual(self.calculate(-2, '-', -5), 3)

    def test_float_inputs(self):
        self.assertEqual(self.calculate(2.5, '+', 0.5), 3.0)


class TestReadNumber(unittest.TestCase):
    def setUp(self):
        from src.calculator import read_number  # type: ignore
        self.read_number = read_number

    def test_read_number_valid(self):
        with patch('builtins.input', return_value='  42  '):
            self.assertEqual(self.read_number('Enter number: '), 42.0)

    def test_read_number_invalid_then_valid(self):
        inputs = ['abc', '5']
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
                value = self.read_number('Enter number: ')
                output = fake_out.getvalue()
        self.assertEqual(value, 5.0)
        self.assertIn("That doesn't look like a number. Did your cat walk on the keyboard?", output)


class TestMainFlow(unittest.TestCase):
    def test_single_operation_then_quit(self):
        # Sequence: choose '+', enter 2, enter 3, then quit
        from src import calculator  # type: ignore
        user_inputs = ['+', '2', '3', 'q']
        with patch('builtins.input', side_effect=user_inputs):
            with patch('sys.stdout', new_callable=io.StringIO) as fake_out:
                calculator.main()
                out = fake_out.getvalue()
        self.assertIn('Result: 5.0', out)
        self.assertIn('Goodbye!', out)


if __name__ == '__main__':
    unittest.main(verbosity=2)

