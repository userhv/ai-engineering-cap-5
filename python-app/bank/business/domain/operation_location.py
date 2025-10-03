"""
Operation Location classes for the banking system.
"""
from abc import ABC
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .current_account import CurrentAccount


class OperationLocation(ABC):
    """
    Abstract base class for operation locations (ATM, Branch).
    """
    
    def __init__(self, number: int):
        self.number = number
    
    def get_number(self) -> int:
        return self.number
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, OperationLocation):
            return False
        return self.number == other.number
    
    def __hash__(self) -> int:
        return hash(self.number)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.number}"


class Branch(OperationLocation):
    """
    Branch class representing bank branches.
    """
    
    def __init__(self, number: int, name: str = None):
        super().__init__(number)
        self.name = name
        self.accounts: List['CurrentAccount'] = []
    
    def get_name(self) -> str:
        return self.name
    
    def add_account(self, current_account: 'CurrentAccount') -> None:
        self.accounts.append(current_account)
    
    def get_accounts(self) -> List['CurrentAccount']:
        return self.accounts.copy()
    
    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.number})"
        return f"Branch {self.number}"


class ATM(OperationLocation):
    """
    ATM class representing automated teller machines.
    """
    
    def __init__(self, number: int):
        super().__init__(number)