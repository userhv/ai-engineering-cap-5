"""
Text-based user interface command definitions and utilities.
"""
from typing import Any, Callable, Optional, List
from abc import ABC, abstractmethod

from ...business.domain.employee import Employee
from ...business.domain.current_account import CurrentAccount


class Command(ABC):
    """Abstract base class for commands."""
    
    def __init__(self, label: str, action: Optional[Callable] = None):
        self.label = label
        self.action = action
    
    def get_label(self) -> str:
        return self.label
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass


class SimpleCommand(Command):
    """Simple command that executes an action."""
    
    def execute(self) -> None:
        if self.action:
            self.action()


class MenuCommand(Command):
    """Command that displays a submenu."""
    
    def __init__(self, label: str, menu: 'Menu'):
        super().__init__(label)
        self.menu = menu
    
    def execute(self) -> None:
        self.menu.show()


class Menu:
    """Menu for displaying options and handling user input."""
    
    def __init__(self, title: str, commands: List[Command] = None):
        self.title = title
        self.commands = commands or []
    
    def add_command(self, command: Command) -> None:
        """Add a command to the menu."""
        self.commands.append(command)
    
    def show(self) -> None:
        """Display the menu and handle user selection."""
        while True:
            print(f"\n{self.title}")
            print("=" * len(self.title))
            
            for i, command in enumerate(self.commands, 1):
                print(f"{i}. {command.get_label()}")
            
            print("0. Voltar/Sair")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                
                if choice == 0:
                    break
                elif 1 <= choice <= len(self.commands):
                    self.commands[choice - 1].execute()
                else:
                    print("Opção inválida!")
            except ValueError:
                print("Por favor, digite um número válido!")
            except KeyboardInterrupt:
                print("\nSaindo...")
                break


class InputReader:
    """Utility class for reading user input."""
    
    @staticmethod
    def read_string(prompt: str) -> str:
        """Read a string from user input."""
        return input(prompt).strip()
    
    @staticmethod
    def read_int(prompt: str) -> int:
        """Read an integer from user input."""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Por favor, digite um número válido!")
    
    @staticmethod
    def read_float(prompt: str) -> float:
        """Read a float from user input."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Por favor, digite um número válido!")
    
    @staticmethod
    def read_password(prompt: str = "Senha: ") -> str:
        """Read a password from user input."""
        import getpass
        return getpass.getpass(prompt)


class MessageDisplay:
    """Utility class for displaying messages."""
    
    @staticmethod
    def show_success(message: str) -> None:
        """Display a success message."""
        print(f"✓ {message}")
    
    @staticmethod
    def show_error(message: str) -> None:
        """Display an error message."""
        print(f"✗ Erro: {message}")
    
    @staticmethod
    def show_info(message: str) -> None:
        """Display an info message."""
        print(f"ℹ {message}")
    
    @staticmethod
    def show_warning(message: str) -> None:
        """Display a warning message."""
        print(f"⚠ Aviso: {message}")


class UserSession:
    """Manages user session data."""
    
    def __init__(self):
        self._employee: Optional[Employee] = None
        self._current_account: Optional[CurrentAccount] = None
    
    def set_employee(self, employee: Employee) -> None:
        """Set the logged-in employee."""
        self._employee = employee
    
    def get_employee(self) -> Optional[Employee]:
        """Get the logged-in employee."""
        return self._employee
    
    def set_current_account(self, account: CurrentAccount) -> None:
        """Set the current account."""
        self._current_account = account
    
    def get_current_account(self) -> Optional[CurrentAccount]:
        """Get the current account."""
        return self._current_account
    
    def clear_session(self) -> None:
        """Clear the session."""
        self._employee = None
        self._current_account = None
    
    def is_employee_logged_in(self) -> bool:
        """Check if an employee is logged in."""
        return self._employee is not None
    
    def is_client_logged_in(self) -> bool:
        """Check if a client is logged in."""
        return self._current_account is not None