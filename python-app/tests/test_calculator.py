"""
Comprehensive tests for the Calculator class.
"""
import pytest
import math
from src.calculator import Calculator


class TestCalculator:
    """Test cases for Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calc = Calculator()
    
    def test_addition(self):
        """Test basic addition."""
        assert self.calc.add(2, 3) == 5
        assert self.calc.add(-1, 1) == 0
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)
    
    def test_subtraction(self):
        """Test basic subtraction."""
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(-1, -1) == 0
        assert self.calc.subtract(0.5, 0.2) == pytest.approx(0.3)
    
    def test_multiplication(self):
        """Test basic multiplication."""
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(-2, 3) == -6
        assert self.calc.multiply(0, 100) == 0
    
    def test_division(self):
        """Test basic division."""
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(-6, 3) == -2
        assert self.calc.divide(1, 3) == pytest.approx(0.33333, rel=1e-3)
    
    def test_division_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)
    
    def test_power(self):
        """Test power operation."""
        assert self.calc.power(2, 3) == 8
        assert self.calc.power(5, 0) == 1
        assert self.calc.power(4, 0.5) == 2
    
    def test_square_root(self):
        """Test square root operation."""
        assert self.calc.square_root(4) == 2
        assert self.calc.square_root(9) == 3
        assert self.calc.square_root(0) == 0
    
    def test_square_root_negative(self):
        """Test square root of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.square_root(-4)
    
    def test_factorial(self):
        """Test factorial operation."""
        assert self.calc.factorial(0) == 1
        assert self.calc.factorial(1) == 1
        assert self.calc.factorial(5) == 120
        assert self.calc.factorial(3) == 6
    
    def test_factorial_negative(self):
        """Test factorial of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
            self.calc.factorial(-1)
    
    def test_factorial_non_integer(self):
        """Test factorial of non-integer raises TypeError."""
        with pytest.raises(TypeError, match="Factorial requires an integer"):
            self.calc.factorial(3.5)
    
    def test_percentage(self):
        """Test percentage calculation."""
        assert self.calc.percentage(100, 50) == 50
        assert self.calc.percentage(200, 25) == 50
        assert self.calc.percentage(80, 12.5) == 10
    
    def test_is_prime(self):
        """Test prime number checking."""
        # Prime numbers
        assert self.calc.is_prime(2) is True
        assert self.calc.is_prime(3) is True
        assert self.calc.is_prime(5) is True
        assert self.calc.is_prime(17) is True
        assert self.calc.is_prime(97) is True
        
        # Non-prime numbers
        assert self.calc.is_prime(1) is False
        assert self.calc.is_prime(4) is False
        assert self.calc.is_prime(9) is False
        assert self.calc.is_prime(15) is False
        assert self.calc.is_prime(100) is False
        
        # Edge cases
        assert self.calc.is_prime(0) is False
        assert self.calc.is_prime(-5) is False
    
    def test_fibonacci(self):
        """Test Fibonacci sequence generation."""
        assert self.calc.fibonacci(0) == []
        assert self.calc.fibonacci(1) == [0]
        assert self.calc.fibonacci(2) == [0, 1]
        assert self.calc.fibonacci(5) == [0, 1, 1, 2, 3]
        assert self.calc.fibonacci(8) == [0, 1, 1, 2, 3, 5, 8, 13]
    
    def test_statistics(self):
        """Test statistics calculation."""
        numbers = [1, 2, 3, 4, 5]
        stats = self.calc.statistics(numbers)
        
        assert stats['count'] == 5
        assert stats['sum'] == 15
        assert stats['mean'] == 3
        assert stats['min'] == 1
        assert stats['max'] == 5
        assert stats['range'] == 4
        assert stats['median'] == 3
        assert stats['std_dev'] == pytest.approx(1.414, rel=1e-2)
    
    def test_statistics_even_count(self):
        """Test statistics with even number of elements."""
        numbers = [1, 2, 3, 4]
        stats = self.calc.statistics(numbers)
        assert stats['median'] == 2.5
    
    def test_statistics_empty_list(self):
        """Test statistics with empty list raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate statistics for empty list"):
            self.calc.statistics([])
    
    def test_history(self):
        """Test calculation history functionality."""
        assert self.calc.get_history() == []
        
        self.calc.add(2, 3)
        self.calc.multiply(4, 5)
        
        history = self.calc.get_history()
        assert len(history) == 2
        assert "2 + 3 = 5" in history
        assert "4 * 5 = 20" in history
        
        self.calc.clear_history()
        assert self.calc.get_history() == []
    
    def test_memory_operations(self):
        """Test memory store, recall, clear, and add operations."""
        # Initial memory should be 0
        assert self.calc.memory_recall() == 0
        
        # Store value
        self.calc.memory_store(42)
        assert self.calc.memory_recall() == 42
        
        # Add to memory
        self.calc.memory_add(8)
        assert self.calc.memory_recall() == 50
        
        # Clear memory
        self.calc.memory_clear()
        assert self.calc.memory_recall() == 0
    
    def test_quadratic_formula_two_real_solutions(self):
        """Test quadratic formula with two real solutions."""
        # x² - 5x + 6 = 0 (solutions: x = 2, x = 3)
        result = self.calc.quadratic_formula(1, -5, 6)
        
        assert result['solution_type'] == 'two_real'
        assert result['discriminant'] == 1
        assert 2 in result['solutions']
        assert 3 in result['solutions']
    
    def test_quadratic_formula_one_real_solution(self):
        """Test quadratic formula with one real solution."""
        # x² - 4x + 4 = 0 (solution: x = 2)
        result = self.calc.quadratic_formula(1, -4, 4)
        
        assert result['solution_type'] == 'one_real'
        assert result['discriminant'] == 0
        assert result['solutions'] == [2]
    
    def test_quadratic_formula_complex_solutions(self):
        """Test quadratic formula with complex solutions."""
        # x² + x + 1 = 0 (complex solutions)
        result = self.calc.quadratic_formula(1, 1, 1)
        
        assert result['solution_type'] == 'complex'
        assert result['discriminant'] == -3
        assert len(result['solutions']) == 2
        assert 'i' in result['solutions'][0]
        assert 'i' in result['solutions'][1]
    
    def test_quadratic_formula_zero_coefficient(self):
        """Test quadratic formula with zero 'a' coefficient raises ValueError."""
        with pytest.raises(ValueError, match="Coefficient 'a' cannot be zero"):
            self.calc.quadratic_formula(0, 1, 1)


class TestCalculatorIntegration:
    """Integration tests for Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_complex_calculation_workflow(self):
        """Test a complex workflow using multiple operations."""
        # Calculate (2 + 3) * 4 / 2 = 10
        step1 = self.calc.add(2, 3)  # 5
        step2 = self.calc.multiply(step1, 4)  # 20
        step3 = self.calc.divide(step2, 2)  # 10
        
        assert step3 == 10
        
        # Check history has all operations
        history = self.calc.get_history()
        assert len(history) == 3
        
        # Store result in memory
        self.calc.memory_store(step3)
        assert self.calc.memory_recall() == 10
    
    def test_statistics_with_fibonacci(self):
        """Test statistics calculation on Fibonacci sequence."""
        fib_sequence = self.calc.fibonacci(10)
        fib_floats = [float(x) for x in fib_sequence]
        stats = self.calc.statistics(fib_floats)
        
        assert stats['count'] == 10
        assert stats['min'] == 0
        assert stats['max'] == 34
        assert stats['sum'] == 88


# Performance tests
class TestCalculatorPerformance:
    """Performance tests for Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calc = Calculator()
    
    def test_large_fibonacci_sequence(self):
        """Test generating large Fibonacci sequence."""
        # This should complete reasonably quickly
        fib = self.calc.fibonacci(100)
        assert len(fib) == 100
        assert fib[0] == 0
        assert fib[1] == 1
        assert fib[-1] > 0  # Last element should be positive and large
    
    def test_prime_checking_performance(self):
        """Test prime checking for moderately large numbers."""
        # Test some known primes and composites
        assert self.calc.is_prime(97) is True
        assert self.calc.is_prime(101) is True
        assert self.calc.is_prime(100) is False
        assert self.calc.is_prime(121) is False


if __name__ == "__main__":
    pytest.main([__file__])