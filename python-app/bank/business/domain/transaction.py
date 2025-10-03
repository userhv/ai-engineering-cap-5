"""
Transaction classes for the banking system.
"""
from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .current_account import CurrentAccount  
    from .operation_location import OperationLocation


class Transaction(ABC):
    """
    Abstract base class for all transactions.
    """
    
    def __init__(self, location: 'OperationLocation', account: 'CurrentAccount', amount: float):
        self.location = location
        self.account = account
        self.amount = amount
        self.date = datetime.now()
    
    def get_account(self) -> 'CurrentAccount':
        return self.account
    
    def get_amount(self) -> float:
        return self.amount
    
    def get_date(self) -> datetime:
        return self.date
    
    def get_location(self) -> 'OperationLocation':
        return self.location
    
    def set_date(self, date: datetime) -> None:
        """This method is here for initializing the database."""
        self.date = date


class Deposit(Transaction):
    """
    Deposit transaction.
    """
    
    def __init__(self, location: 'OperationLocation', account: 'CurrentAccount', envelope: int, amount: float):
        super().__init__(location, account, amount)
        self.envelope = envelope
    
    def get_envelope(self) -> int:
        return self.envelope


class Withdrawal(Transaction):
    """
    Withdrawal transaction.
    """
    
    def __init__(self, location: 'OperationLocation', account: 'CurrentAccount', amount: float):
        super().__init__(location, account, amount)


class Transfer(Transaction):
    """
    Transfer transaction.
    """
    
    def __init__(self, location: 'OperationLocation', account: 'CurrentAccount', 
                 destination_account: 'CurrentAccount', amount: float):
        super().__init__(location, account, amount)
        self.destination_account = destination_account
    
    def get_destination_account(self) -> 'CurrentAccount':
        return self.destination_account