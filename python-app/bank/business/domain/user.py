"""
Base User class for the banking system.
"""
from abc import ABC
from datetime import datetime
from typing import Optional


class User(ABC):
    """
    Abstract base class for users in the banking system.
    """
    
    def __init__(self, first_name: str, last_name: str, password: str, birthday: datetime):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.birthday = birthday
    
    def get_first_name(self) -> str:
        return self.first_name
    
    def set_first_name(self, first_name: str) -> None:
        self.first_name = first_name
    
    def get_last_name(self) -> str:
        return self.last_name
    
    def set_last_name(self, last_name: str) -> None:
        self.last_name = last_name
    
    def get_password(self) -> str:
        return self.password
    
    def set_password(self, password: str) -> None:
        self.password = password
    
    def get_birthday(self) -> datetime:
        return self.birthday
    
    def set_birthday(self, birthday: datetime) -> None:
        self.birthday = birthday
    
    def is_valid_password(self, password: str) -> bool:
        return self.password == password