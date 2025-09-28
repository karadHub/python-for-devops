# Unit Tests for Calculator using unittest

import unittest
import sys
import os

# Add the parent directory to the Python path to import the calculator module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator import Calculator

class TestCalculator(unittest.TestCase):
    """Test cases for Calculator class using unittest framework."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()

    def tearDown(self):
        """Clean up after each test method."""
        pass

    def test_addition(self):
        """Test addition functionality."""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)
        self.assertEqual(self.calc.add(-5, -3), -8)

    def test_subtraction(self):
        """Test subtraction functionality."""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(0, 5), -5)
        self.assertEqual(self.calc.subtract(-3, -5), 2)

    def test_multiplication(self):
        """Test multiplication functionality."""
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
        self.assertEqual(self.calc.multiply(-4, -5), 20)

    def test_division(self):
        """Test division functionality."""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertEqual(self.calc.divide(-10, 2), -5)
        self.assertEqual(self.calc.divide(-10, -2), 5)

    def test_division_by_zero(self):
        """Test division by zero raises ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(-5, 0)

    def test_power(self):
        """Test power functionality."""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(3, 2), 9)
        self.assertEqual(self.calc.power(-2, 3), -8)

    def test_square_root(self):
        """Test square root functionality."""
        self.assertEqual(self.calc.square_root(9), 3)
        self.assertEqual(self.calc.square_root(16), 4)
        self.assertEqual(self.calc.square_root(0), 0)
        self.assertAlmostEqual(self.calc.square_root(2), 1.414, places=3)

    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.square_root(-1)

        with self.assertRaises(ValueError):
            self.calc.square_root(-10)

    def test_factorial(self):
        """Test factorial functionality."""
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(1), 1)
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(3), 6)

    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.factorial(-1)

        with self.assertRaises(ValueError):
            self.calc.factorial(-5)

if __name__ == '__main__':
    # Run the tests
    unittest.main()
