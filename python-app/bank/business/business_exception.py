"""
Business exceptions for the banking system.
"""


class BusinessException(Exception):
    """
    Business exception raised when an error occurs in the business layer.
    """
    
    def __init__(self, message: str, args: list = None):
        super().__init__(message)
        self.args_list = args or []
        
    def get_args(self) -> list:
        return self.args_list