"""
Branch employee interface - allows employees to create accounts and manage clients.
"""
from datetime import datetime
from typing import Optional

from .ui_utils import Menu, Command, SimpleCommand, InputReader, MessageDisplay, UserSession
from ...business.impl.service_impl import AccountManagementServiceImpl
from ...business.business_exception import BusinessException
from ...data.database import Database
from ...business.domain.employee import Employee


class BranchInterface:
    """Branch interface for employee operations."""
    
    def __init__(self, database: Database):
        self.database = database
        self.account_service = AccountManagementServiceImpl(database)
        self.session = UserSession()
        self.setup_menus()
    
    def setup_menus(self) -> None:
        """Setup the menu structure."""
        # Main menu
        self.main_menu = Menu("Sistema Bancário - Agência")
        self.main_menu.add_command(SimpleCommand("Login", self.employee_login))
        
        # Employee menu
        self.employee_menu = Menu("Menu do Funcionário")
        self.employee_menu.add_command(SimpleCommand("Criar Conta Corrente", self.create_account))
        self.employee_menu.add_command(SimpleCommand("Informações da Conta", self.show_employee_info))
        self.employee_menu.add_command(SimpleCommand("Logout", self.logout))
    
    def start(self) -> None:
        """Start the branch interface."""
        print("Bem-vindo ao Sistema Bancário!")
        self.main_menu.show()
    
    def employee_login(self) -> None:
        """Handle employee login."""
        try:
            username = InputReader.read_string("Nome de usuário: ")
            password = InputReader.read_password()
            
            employee = self.account_service.login(username, password)
            self.session.set_employee(employee)
            
            MessageDisplay.show_success(f"Login realizado com sucesso! Bem-vindo, {employee.get_name()}!")
            self.employee_menu.show()
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def create_account(self) -> None:
        """Create a new current account."""
        if not self.session.is_employee_logged_in():
            MessageDisplay.show_error("Você precisa estar logado para criar uma conta")
            return
        
        try:
            print("\n--- Criar Nova Conta Corrente ---")
            
            # Get branch number from logged employee
            employee = self.session.get_employee()
            branch_number = employee.get_operation_location().get_number()
            
            # Read client information
            name = InputReader.read_string("Nome: ")
            last_name = InputReader.read_string("Sobrenome: ")
            cpf = InputReader.read_int("CPF (apenas números): ")
            
            # Read birthday
            print("Data de nascimento:")
            day = InputReader.read_int("Dia: ")
            month = InputReader.read_int("Mês: ")
            year = InputReader.read_int("Ano: ")
            
            try:
                birthday = datetime(year, month, day)
            except ValueError:
                MessageDisplay.show_error("Data de nascimento inválida")
                return
            
            balance = InputReader.read_float("Saldo inicial: R$ ")
            
            if balance < 0:
                MessageDisplay.show_error("Saldo inicial não pode ser negativo")
                return
            
            # Create account
            account = self.account_service.create_current_account(
                branch_number, name, last_name, cpf, birthday, balance
            )
            
            print("\n--- Conta Criada com Sucesso ---")
            print(f"Agência: {account.get_current_account_id().get_branch().get_number()}")
            print(f"Conta: {account.get_current_account_id().get_account_number()}")
            print(f"Cliente: {account.get_client().get_name()} {account.get_client().get_last_name()}")
            print(f"CPF: {account.get_client().get_cpf()}")
            print(f"Senha: {account.get_client().get_password()}")
            print(f"Saldo: R$ {account.get_balance():.2f}")
            
            MessageDisplay.show_success("Conta criada com sucesso!")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def show_employee_info(self) -> None:
        """Show employee information."""
        if not self.session.is_employee_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        employee = self.session.get_employee()
        print("\n--- Informações do Funcionário ---")
        print(f"Nome: {employee.get_name()} {employee.get_last_name()}")
        print(f"CPF: {employee.get_cpf()}")
        print(f"Usuário: {employee.get_username()}")
        print(f"Agência: {employee.get_operation_location().get_number()}")
        print(f"Endereço: {employee.get_operation_location().get_address()}")
    
    def logout(self) -> None:
        """Logout current employee."""
        if self.session.is_employee_logged_in():
            employee_name = self.session.get_employee().get_name()
            self.session.clear_session()
            MessageDisplay.show_success(f"Logout realizado com sucesso! Até logo, {employee_name}!")
        else:
            MessageDisplay.show_info("Nenhum usuário logado")
    
    def _get_error_message(self, exception_key: str) -> str:
        """Get error message from exception key."""
        error_messages = {
            "exception.invalid.branch": "Agência inválida",
            "exception.inexistent.employee": "Funcionário não encontrado",
            "exception.invalid.password": "Senha inválida",
            "exception.inexistent.account": "Conta não encontrada",
            "exception.invalid.operation.location": "Local de operação inválido",
        }
        return error_messages.get(exception_key, "Erro desconhecido")


def main():
    """Main function to start branch interface."""
    database = Database()
    branch_interface = BranchInterface(database)
    branch_interface.start()


if __name__ == "__main__":
    main()