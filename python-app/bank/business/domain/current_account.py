"""
Current Account class for the banking system.
"""
from typing import List, TYPE_CHECKING
from ..business_exception import BusinessException
from .credentials import Credentials
from .current_account_id import CurrentAccountId

if TYPE_CHECKING:
    from .client import Client
    from .operation_location import Branch, OperationLocation
    from .transaction import Transaction, Deposit, Withdrawal, Transfer


class CurrentAccount(Credentials):
    """
    Current account class representing bank accounts.
    """
    
    def __init__(self, branch: 'Branch', number: int, client: 'Client', initial_balance: float = 0.0):
        self.id = CurrentAccountId(branch, number)
        branch.add_account(self)
        self.client = client
        client.set_account(self)
        self.balance = initial_balance
        self.deposits: List['Deposit'] = []
        self.transfers: List['Transfer'] = []
        self.withdrawals: List['Withdrawal'] = []
    
    def get_id(self) -> CurrentAccountId:
        return self.id
    
    def get_client(self) -> 'Client':
        return self.client
    
    def get_balance(self) -> float:
        return self.balance
    
    def get_deposits(self) -> List['Deposit']:
        return self.deposits.copy()
    
    def get_transfers(self) -> List['Transfer']:
        return self.transfers.copy()
    
    def get_withdrawals(self) -> List['Withdrawal']:
        return self.withdrawals.copy()
    
    def get_transactions(self) -> List['Transaction']:
        """Get all transactions for this account."""
        transactions = []
        transactions.extend(self.deposits)
        transactions.extend(self.withdrawals)
        transactions.extend(self.transfers)
        return transactions
    
    def deposit(self, location: 'OperationLocation', envelope: int, amount: float) -> 'Deposit':
        """Perform a deposit operation."""
        self._deposit_amount(amount)
        
        from .transaction import Deposit
        deposit = Deposit(location, self, envelope, amount)
        self.deposits.append(deposit)
        
        return deposit
    
    def withdrawal(self, location: 'OperationLocation', amount: float) -> 'Withdrawal':
        """Perform a withdrawal operation."""
        self._withdrawal_amount(amount)
        
        from .transaction import Withdrawal
        withdrawal = Withdrawal(location, self, amount)
        self.withdrawals.append(withdrawal)
        
        return withdrawal
    
    def transfer(self, location: 'OperationLocation', destination_account: 'CurrentAccount', 
                amount: float) -> 'Transfer':
        """Perform a transfer operation."""
        self._withdrawal_amount(amount)
        destination_account._deposit_amount(amount)
        
        from .transaction import Transfer
        transfer = Transfer(location, self, destination_account, amount)
        self.transfers.append(transfer)
        destination_account.transfers.append(transfer)
        
        return transfer
    
    def _deposit_amount(self, amount: float) -> None:
        """Internal method to deposit amount."""
        if not self._is_valid_amount(amount):
            raise BusinessException("exception.invalid.amount")
        
        self.balance += amount
    
    def _withdrawal_amount(self, amount: float) -> None:
        """Internal method to withdraw amount."""
        if not self._is_valid_amount(amount):
            raise BusinessException("exception.invalid.amount")
        
        if not self._has_enough_balance(amount):
            raise BusinessException("exception.insufficient.balance")
        
        self.balance -= amount
    
    def _is_valid_amount(self, amount: float) -> bool:
        """Check if amount is valid (greater than 0)."""
        return amount > 0
    
    def _has_enough_balance(self, amount: float) -> bool:
        """Check if account has enough balance for the operation."""
        return amount <= self.balance