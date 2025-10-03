"""
Employee class for the banking system.
"""
from datetime import datetime
from typing import Optional

from .user import User
from .credentials import Credentials


class Employee(User, Credentials):
    """
    Employee class representing bank employees.
    """
    
    def __init__(self, first_name: str, last_name: str, username: str, password: str, birthday: datetime):
        super().__init__(first_name, last_name, password, birthday)
        self.username = username
    
    def get_username(self) -> str:
        return self.username
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Employee):
            return False
        return self.username == other.username
    
    def __hash__(self) -> int:
        return hash(self.username)