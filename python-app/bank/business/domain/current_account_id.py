"""
Current Account ID class for composite key.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .operation_location import Branch


class CurrentAccountId:
    """
    Composite identifier for current accounts.
    """
    
    def __init__(self, branch: 'Branch', number: int):
        self.branch = branch
        self.number = number
    
    def get_branch(self) -> 'Branch':
        return self.branch
    
    def get_number(self) -> int:
        return self.number
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CurrentAccountId):
            return False
        return self.branch == other.branch and self.number == other.number
    
    def __hash__(self) -> int:
        return hash((self.branch, self.number))