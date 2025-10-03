"""
In-memory database for the banking system.
"""
import random
from calendar import Calendar
from datetime import datetime, timedelta
from typing import Dict, Collection, Optional

from ..business.domain.operation_location import OperationLocation, Branch, ATM
from ..business.domain.employee import Employee
from ..business.domain.client import Client
from ..business.domain.current_account import CurrentAccount
from ..business.domain.current_account_id import CurrentAccountId
from ..business.domain.transaction import Transaction, Deposit, Withdrawal, Transfer


class Database:
    """
    In-memory database for the banking system.
    """
    
    def __init__(self, init_data: bool = True):
        self.current_accounts: Dict[CurrentAccountId, CurrentAccount] = {}
        self.employees: Dict[str, Employee] = {}
        self.operation_locations: Dict[int, OperationLocation] = {}
        self._next_account_number = 1
        
        if init_data:
            self._init_data()
    
    def get_all_current_accounts(self) -> Collection[CurrentAccount]:
        """Get all current accounts."""
        return self.current_accounts.values()
    
    def get_all_employees(self) -> Collection[Employee]:
        """Get all employees."""
        return self.employees.values()
    
    def get_all_operation_locations(self) -> Collection[OperationLocation]:
        """Get all operation locations."""
        return self.operation_locations.values()
    
    def get_current_account(self, current_account_id: CurrentAccountId) -> Optional[CurrentAccount]:
        """Get current account by ID."""
        return self.current_accounts.get(current_account_id)
    
    def get_employee(self, username: str) -> Optional[Employee]:
        """Get employee by username."""
        return self.employees.get(username)
    
    def get_operation_location(self, number: int) -> Optional[OperationLocation]:
        """Get operation location by number."""
        return self.operation_locations.get(number)
    
    def get_next_current_account_number(self) -> int:
        """Get next available account number."""
        number = self._next_account_number
        self._next_account_number += 1
        return number
    
    def save_current_account(self, current_account: CurrentAccount) -> None:
        """Save current account."""
        self.current_accounts[current_account.get_id()] = current_account
        
        # Update next account number if necessary
        account_number = current_account.get_id().get_number()
        if account_number >= self._next_account_number:
            self._next_account_number = account_number + 1
    
    def save_employee(self, employee: Employee) -> None:
        """Save employee."""
        self.employees[employee.get_username()] = employee
    
    def save_operation_location(self, operation_location: OperationLocation) -> None:
        """Save operation location."""
        self.operation_locations[operation_location.get_number()] = operation_location
    
    def _init_data(self) -> None:
        """Initialize database with sample data."""
        # Operation Locations
        ol_id = 0
        
        b1 = Branch(ol_id := ol_id + 1, "Campus Vale")
        self.save_operation_location(b1)
        
        b2 = Branch(ol_id := ol_id + 1, "Centro")
        self.save_operation_location(b2)
        
        atm1 = ATM(ol_id := ol_id + 1)
        self.save_operation_location(atm1)
        
        atm2 = ATM(ol_id := ol_id + 1)
        self.save_operation_location(atm2)
        
        atm3 = ATM(ol_id := ol_id + 1)
        self.save_operation_location(atm3)
        
        # Employee
        employee = Employee("Ingrid", "Nunes", "ingrid", "123", datetime.now())
        self.save_employee(employee)
        
        # Current Accounts
        client1 = Client("Ingrid", "Nunes", 1234567890, "123", datetime.now())
        ca1 = CurrentAccount(b1, 1, client1, 300)
        self.save_current_account(ca1)
        
        client2 = Client("Joao", "Silva", 1234567890, "123", datetime.now())
        ca2 = CurrentAccount(b2, 2, client2, 200)
        self.save_current_account(ca2)
        
        client3 = Client("Richer", "Rich", 1234567890, "123", datetime.now())
        ca3 = CurrentAccount(b2, 3, client3, 10000)
        self.save_current_account(ca3)
        
        # Sample Transactions
        self._create_sample_transactions([ca1, ca2, ca3], [atm1, atm2, b1, b2])
    
    def _create_sample_transactions(self, accounts: list, locations: list) -> None:
        """Create sample transactions for testing."""
        base_date = datetime.now() - timedelta(days=180)
        
        for i in range(8):
            # Vary the date
            date_offset = random.randint(1, 30) * i
            transaction_date = base_date + timedelta(days=date_offset)
            
            # Create random transactions
            account = random.choice(accounts)
            location = random.choice(locations)
            
            # Create different types of transactions
            transaction_type = random.randint(1, 3)
            
            if transaction_type == 1 and account.get_balance() > 50:
                # Withdrawal
                amount = random.uniform(10, min(100, account.get_balance() * 0.5))
                try:
                    withdrawal = account.withdrawal(location, amount)
                    withdrawal.set_date(transaction_date)
                except:
                    pass  # Skip if insufficient balance
                    
            elif transaction_type == 2:
                # Deposit
                amount = random.uniform(50, 500)
                envelope = random.randint(1000, 9999)
                deposit = account.deposit(location, envelope, amount)
                deposit.set_date(transaction_date)
                
            elif transaction_type == 3 and len(accounts) > 1 and account.get_balance() > 50:
                # Transfer
                dest_account = random.choice([a for a in accounts if a != account])
                amount = random.uniform(10, min(200, account.get_balance() * 0.3))
                try:
                    transfer = account.transfer(location, dest_account, amount)
                    transfer.set_date(transaction_date)
                except:
                    pass  # Skip if insufficient balance