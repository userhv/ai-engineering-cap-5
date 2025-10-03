"""
Utility class for generating random strings.
"""
import random
import string


class RandomString:
    """
    Utility class for generating random strings.
    """
    
    def __init__(self, length: int):
        self.length = length
    
    def next_string(self) -> str:
        """Generate a random string of specified length."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=self.length))