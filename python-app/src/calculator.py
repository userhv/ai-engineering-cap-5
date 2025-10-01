"""
Calculator class with various mathematical operations and utilities.
"""
import math
from typing import List, Union, Dict, Any


class Calculator:
    """
    A comprehensive calculator class with basic and advanced operations.
    """
    
    def __init__(self):
        self.history: List[str] = []
        self.memory: float = 0.0
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Calculate base raised to the power of exponent."""
        result = base ** exponent
        self.history.append(f"{base} ^ {exponent} = {result}")
        return result
    
    def square_root(self, number: float) -> float:
        """Calculate square root of a number."""
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(number)
        self.history.append(f"√{number} = {result}")
        return result
    
    def factorial(self, n: int) -> int:
        """Calculate factorial of n."""
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if not isinstance(n, int):
            raise TypeError("Factorial requires an integer")
        
        result = math.factorial(n)
        self.history.append(f"{n}! = {result}")
        return result
    
    def percentage(self, value: float, percent: float) -> float:
        """Calculate percentage of a value."""
        result = (value * percent) / 100
        self.history.append(f"{percent}% of {value} = {result}")
        return result
    
    def is_prime(self, n: int) -> bool:
        """Check if a number is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def fibonacci(self, n: int) -> List[int]:
        """Generate Fibonacci sequence up to n terms."""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        fib_sequence = [0, 1]
        for i in range(2, n):
            fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
        
        return fib_sequence
    
    def statistics(self, numbers: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate statistics for empty list")
        
        sorted_numbers = sorted(numbers)
        n = len(numbers)
        
        stats = {
            'count': n,
            'sum': sum(numbers),
            'mean': sum(numbers) / n,
            'min': min(numbers),
            'max': max(numbers),
            'range': max(numbers) - min(numbers)
        }
        
        # Median
        if n % 2 == 0:
            stats['median'] = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            stats['median'] = sorted_numbers[n//2]
        
        # Standard deviation
        mean = stats['mean']
        variance = sum((x - mean) ** 2 for x in numbers) / n
        stats['std_dev'] = math.sqrt(variance)
        
        return stats
    
    def clear_history(self) -> None:
        """Clear calculation history."""
        self.history.clear()
    
    def get_history(self) -> List[str]:
        """Get calculation history."""
        return self.history.copy()
    
    def memory_store(self, value: float) -> None:
        """Store value in memory."""
        self.memory = value
    
    def memory_recall(self) -> float:
        """Recall value from memory."""
        return self.memory
    
    def memory_clear(self) -> None:
        """Clear memory."""
        self.memory = 0.0
    
    def memory_add(self, value: float) -> None:
        """Add value to memory."""
        self.memory += value
    
    def quadratic_formula(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """
        Solve quadratic equation ax² + bx + c = 0 using quadratic formula.
        Returns dictionary with solutions and discriminant.
        """
        if a == 0:
            raise ValueError("Coefficient 'a' cannot be zero in quadratic equation")
        
        discriminant = b**2 - 4*a*c
        
        result = {
            'discriminant': discriminant,
            'a': a, 'b': b, 'c': c
        }
        
        if discriminant > 0:
            # Two real solutions
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            result['solutions'] = [x1, x2]
            result['solution_type'] = 'two_real'
        elif discriminant == 0:
            # One real solution
            x = -b / (2*a)
            result['solutions'] = [x]
            result['solution_type'] = 'one_real'
        else:
            # Complex solutions
            real_part = -b / (2*a)
            imaginary_part = math.sqrt(-discriminant) / (2*a)
            result['solutions'] = [
                f"{real_part} + {imaginary_part}i",
                f"{real_part} - {imaginary_part}i"
            ]
            result['solution_type'] = 'complex'
        
        return result