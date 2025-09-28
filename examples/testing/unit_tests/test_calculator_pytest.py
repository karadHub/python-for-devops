# Unit Tests for Calculator using pytest

import pytest
import sys
import os

# Add the parent directory to the Python path to import the calculator module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculator import Calculator

class TestCalculatorPytest:
    """Test cases for Calculator class using pytest framework."""

    def setup_method(self):
        """Setup before each test method."""
        self.calc = Calculator()

    def test_addition(self):
        """Test addition functionality."""
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0, 0) == 0
        assert self.calc.add(-5, -3) == -8

    def test_subtraction(self):
        """Test subtraction functionality."""
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(0, 5) == -5
        assert self.calc.subtract(-3, -5) == 2

    def test_multiplication(self):
        """Test multiplication functionality."""
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(-2, 3) == -6
        assert self.calc.multiply(0, 100) == 0
        assert self.calc.multiply(-4, -5) == 20

    def test_division(self):
        """Test division functionality."""
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 2) == 3.5
        assert self.calc.divide(-10, 2) == -5
        assert self.calc.divide(-10, -2) == 5

    def test_division_by_zero(self):
        """Test division by zero raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)

        with pytest.raises(ZeroDivisionError):
            self.calc.divide(-5, 0)

    def test_power(self):
        """Test power functionality."""
        assert self.calc.power(2, 3) == 8
        assert self.calc.power(5, 0) == 1
        assert self.calc.power(3, 2) == 9
        assert self.calc.power(-2, 3) == -8

    def test_square_root(self):
        """Test square root functionality."""
        assert self.calc.square_root(9) == 3
        assert self.calc.square_root(16) == 4
        assert self.calc.square_root(0) == 0
        assert abs(self.calc.square_root(2) - 1.414) < 0.001

    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root"):
            self.calc.square_root(-1)

        with pytest.raises(ValueError):
            self.calc.square_root(-10)

    def test_factorial(self):
        """Test factorial functionality."""
        assert self.calc.factorial(0) == 1
        assert self.calc.factorial(1) == 1
        assert self.calc.factorial(5) == 120
        assert self.calc.factorial(3) == 6

    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Factorial is not defined"):
            self.calc.factorial(-1)

        with pytest.raises(ValueError):
            self.calc.factorial(-5)

# Parametrized tests
class TestCalculatorParametrized:
    """Parametrized tests for Calculator class."""

    @pytest.fixture
    def calc(self):
        """Calculator fixture."""
        return Calculator()

    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (-5, -3, -8),
        (100, 200, 300)
    ])
    def test_add_parametrized(self, calc, a, b, expected):
        """Parametrized test for addition."""
        assert calc.add(a, b) == expected

    @pytest.mark.parametrize("a,b,expected", [
        (5, 3, 2),
        (0, 5, -5),
        (-3, -5, 2),
        (10, 10, 0)
    ])
    def test_subtract_parametrized(self, calc, a, b, expected):
        """Parametrized test for subtraction."""
        assert calc.subtract(a, b) == expected

    @pytest.mark.parametrize("base,exp,expected", [
        (2, 3, 8),
        (5, 0, 1),
        (3, 2, 9),
        (-2, 3, -8),
        (10, 1, 10)
    ])
    def test_power_parametrized(self, calc, base, exp, expected):
        """Parametrized test for power calculation."""
        assert calc.power(base, exp) == expected

    @pytest.mark.parametrize("number,expected", [
        (0, 1),
        (1, 1),
        (3, 6),
        (5, 120),
        (4, 24)
    ])
    def test_factorial_parametrized(self, calc, number, expected):
        """Parametrized test for factorial calculation."""
        assert calc.factorial(number) == expected

# Test markers examples
class TestCalculatorMarkers:
    """Tests demonstrating pytest markers."""

    @pytest.fixture
    def calc(self):
        return Calculator()

    @pytest.mark.unit
    def test_basic_operations(self, calc):
        """Test marked as unit test."""
        assert calc.add(1, 1) == 2
        assert calc.multiply(2, 3) == 6

    @pytest.mark.slow
    def test_large_factorial(self, calc):
        """Test marked as slow (hypothetically)."""
        result = calc.factorial(10)
        assert result == 3628800

    @pytest.mark.edge_case
    def test_edge_cases(self, calc):
        """Test marked for edge cases."""
        assert calc.add(float('inf'), 1) == float('inf')
        assert calc.multiply(0, float('inf')) != calc.multiply(0, float('inf'))  # NaN

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
