"""
Implementation of business services.
"""
from datetime import datetime
from typing import List
from calendar import monthrange

from ..business_exception import BusinessException
from ..services import AccountManagementService, AccountOperationService
from ..domain.employee import Employee
from ..domain.client import Client
from ..domain.current_account import CurrentAccount
from ..domain.current_account_id import CurrentAccountId
from ..domain.operation_location import Branch, OperationLocation
from ..domain.transaction import Transaction, Deposit, Withdrawal, Transfer
from ...data.database import Database
from ...util.random_string import RandomString


class AccountManagementServiceImpl(AccountManagementService):
    """
    Implementation of AccountManagementService.
    """
    
    def __init__(self, database: Database):
        self.database = database
        self.random = RandomString(8)
    
    def create_current_account(self, branch: int, name: str, last_name: str, 
                             cpf: int, birthday: datetime, balance: float) -> CurrentAccount:
        """Create a new current account."""
        operation_location = self.database.get_operation_location(branch)
        if operation_location is None or not isinstance(operation_location, Branch):
            raise BusinessException("exception.invalid.branch")
        
        client = Client(name, last_name, cpf, self.random.next_string(), birthday)
        current_account = CurrentAccount(
            operation_location, 
            self.database.get_next_current_account_number(), 
            client, 
            balance
        )
        
        self.database.save_current_account(current_account)
        return current_account
    
    def login(self, username: str, password: str) -> Employee:
        """Employee login."""
        employee = self.database.get_employee(username)
        
        if employee is None:
            raise BusinessException("exception.inexistent.employee")
        if not employee.get_password() == password:
            raise BusinessException("exception.invalid.password")
        
        return employee


class AccountOperationServiceImpl(AccountOperationService):
    """
    Implementation of AccountOperationService.
    """
    
    def __init__(self, database: Database):
        self.database = database
    
    def deposit(self, operation_location: int, branch: int, account_number: int, 
               envelope: int, amount: float) -> Deposit:
        """Perform a deposit operation."""
        current_account = self._read_current_account(branch, account_number)
        deposit = current_account.deposit(
            self._get_operation_location(operation_location), 
            envelope, 
            amount
        )
        return deposit
    
    def get_balance(self, branch: int, account_number: int) -> float:
        """Get account balance."""
        return self._read_current_account(branch, account_number).get_balance()
    
    def get_statement_by_date(self, branch: int, account_number: int, 
                            begin: datetime, end: datetime) -> List[Transaction]:
        """Get statement by date range."""
        current_account = self._read_current_account(branch, account_number)
        return self._get_statement_by_date(current_account, begin, end)
    
    def get_statement_by_month(self, branch: int, account_number: int, 
                             month: int, year: int) -> List[Transaction]:
        """Get statement by month."""
        current_account = self._read_current_account(branch, account_number)
        
        # Get first and last day of the month
        first_day = datetime(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = datetime(year, month, last_day_num, 23, 59, 59)
        
        return self._get_statement_by_date(current_account, first_day, last_day)
    
    def login(self, branch: int, account_number: int, password: str) -> CurrentAccount:
        """Client login."""
        current_account = self._read_current_account(branch, account_number)
        if not current_account.get_client().get_password() == password:
            raise BusinessException("exception.invalid.password")
        
        return current_account
    
    def transfer(self, operation_location: int, src_branch: int, src_account_number: int,
                dst_branch: int, dst_account_number: int, amount: float) -> Transfer:
        """Perform a transfer operation."""
        source = self._read_current_account(src_branch, src_account_number)
        destination = self._read_current_account(dst_branch, dst_account_number)
        
        transfer = source.transfer(
            self._get_operation_location(operation_location), 
            destination, 
            amount
        )
        return transfer
    
    def withdrawal(self, operation_location: int, branch: int, account_number: int, 
                  amount: float) -> Withdrawal:
        """Perform a withdrawal operation."""
        current_account = self._read_current_account(branch, account_number)
        withdrawal = current_account.withdrawal(
            self._get_operation_location(operation_location), 
            amount
        )
        return withdrawal
    
    def _read_current_account(self, branch: int, account_number: int) -> CurrentAccount:
        """Read current account by branch and account number."""
        account_id = CurrentAccountId(Branch(branch), account_number)
        current_account = self.database.get_current_account(account_id)
        
        if current_account is None:
            raise BusinessException("exception.inexistent.account")
        
        return current_account
    
    def _get_operation_location(self, operation_location_number: int) -> OperationLocation:
        """Get operation location by number."""
        operation_location = self.database.get_operation_location(operation_location_number)
        if operation_location is None:
            raise BusinessException("exception.invalid.operation.location")
        return operation_location
    
    def _get_statement_by_date(self, current_account: CurrentAccount, 
                             begin: datetime, end: datetime) -> List[Transaction]:
        """Get transactions by date range."""
        transactions = current_account.get_transactions()
        filtered_transactions = [
            t for t in transactions 
            if begin <= t.get_date() <= end
        ]
        # Sort by date descending
        filtered_transactions.sort(key=lambda t: t.get_date(), reverse=True)
        return filtered_transactions