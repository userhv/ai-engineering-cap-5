"""
Client class for the banking system.
"""
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from .user import User

if TYPE_CHECKING:
    from .current_account import CurrentAccount


class Client(User):
    """
    Client class representing bank customers.
    """
    
    def __init__(self, first_name: str, last_name: str, cpf: int, password: str, birthday: datetime):
        super().__init__(first_name, last_name, password, birthday)
        self.cpf = cpf
        self.account: Optional['CurrentAccount'] = None
    
    def get_cpf(self) -> int:
        return self.cpf
    
    def get_account(self) -> Optional['CurrentAccount']:
        return self.account
    
    def set_account(self, account: 'CurrentAccount') -> None:
        self.account = account