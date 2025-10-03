"""
Service interfaces for the banking system.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from .business_exception import BusinessException
from .domain.employee import Employee
from .domain.current_account import CurrentAccount
from .domain.transaction import Transaction, Deposit, Withdrawal, Transfer


class AccountManagementService(ABC):
    """
    Interface for account management operations.
    """
    
    @abstractmethod
    def create_current_account(self, branch: int, name: str, last_name: str, 
                             cpf: int, birthday: datetime, balance: float) -> CurrentAccount:
        """Create a new current account."""
        pass
    
    @abstractmethod
    def login(self, username: str, password: str) -> Employee:
        """Employee login."""
        pass


class AccountOperationService(ABC):
    """
    Interface for account operations.
    """
    
    @abstractmethod
    def deposit(self, operation_location: int, branch: int, account_number: int, 
               envelope: int, amount: float) -> Deposit:
        """Perform a deposit operation."""
        pass
    
    @abstractmethod
    def get_balance(self, branch: int, account_number: int) -> float:
        """Get account balance."""
        pass
    
    @abstractmethod
    def get_statement_by_date(self, branch: int, account_number: int, 
                            begin: datetime, end: datetime) -> List[Transaction]:
        """Get statement by date range."""
        pass
    
    @abstractmethod
    def get_statement_by_month(self, branch: int, account_number: int, 
                             month: int, year: int) -> List[Transaction]:
        """Get statement by month."""
        pass
    
    @abstractmethod
    def login(self, branch: int, account_number: int, password: str) -> CurrentAccount:
        """Client login."""
        pass
    
    @abstractmethod
    def transfer(self, operation_location: int, src_branch: int, src_account_number: int,
                dst_branch: int, dst_account_number: int, amount: float) -> Transfer:
        """Perform a transfer operation."""
        pass
    
    @abstractmethod
    def withdrawal(self, operation_location: int, branch: int, account_number: int, 
                  amount: float) -> Withdrawal:
        """Perform a withdrawal operation."""
        pass