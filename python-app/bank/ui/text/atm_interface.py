"""
ATM interface - allows clients to perform banking operations.
"""
from datetime import datetime
from typing import List

from .ui_utils import Menu, Command, SimpleCommand, InputReader, MessageDisplay, UserSession
from ...business.impl.service_impl import AccountOperationServiceImpl
from ...business.business_exception import BusinessException
from ...business.domain.transaction import Transaction, Deposit, Withdrawal, Transfer
from ...data.database import Database


class ATMInterface:
    """ATM interface for client operations."""
    
    def __init__(self, database: Database):
        self.database = database
        self.operation_service = AccountOperationServiceImpl(database)
        self.session = UserSession()
        self.setup_menus()
    
    def setup_menus(self) -> None:
        """Setup the menu structure."""
        # Main menu
        self.main_menu = Menu("Sistema Bancário - Caixa Eletrônico")
        self.main_menu.add_command(SimpleCommand("Acessar Conta", self.client_login))
        
        # Client menu
        self.client_menu = Menu("Menu do Cliente")
        self.client_menu.add_command(SimpleCommand("Consultar Saldo", self.check_balance))
        self.client_menu.add_command(SimpleCommand("Depositar", self.deposit))
        self.client_menu.add_command(SimpleCommand("Sacar", self.withdraw))
        self.client_menu.add_command(SimpleCommand("Transferir", self.transfer))
        self.client_menu.add_command(SimpleCommand("Extrato por Período", self.statement_by_date))
        self.client_menu.add_command(SimpleCommand("Extrato Mensal", self.statement_by_month))
        self.client_menu.add_command(SimpleCommand("Informações da Conta", self.show_account_info))
        self.client_menu.add_command(SimpleCommand("Sair", self.logout))
    
    def start(self) -> None:
        """Start the ATM interface."""
        print("Bem-vindo ao Caixa Eletrônico!")
        self.main_menu.show()
    
    def client_login(self) -> None:
        """Handle client login."""
        try:
            branch = InputReader.read_int("Número da agência: ")
            account_number = InputReader.read_int("Número da conta: ")
            password = InputReader.read_password()
            
            account = self.operation_service.login(branch, account_number, password)
            self.session.set_current_account(account)
            
            client = account.get_client()
            MessageDisplay.show_success(f"Acesso autorizado! Bem-vindo, {client.get_name()}!")
            self.client_menu.show()
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def check_balance(self) -> None:
        """Check account balance."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        try:
            account = self.session.get_current_account()
            account_id = account.get_current_account_id()
            
            balance = self.operation_service.get_balance(
                account_id.get_branch().get_number(),
                account_id.get_account_number()
            )
            
            print(f"\nSaldo atual: R$ {balance:.2f}")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def deposit(self) -> None:
        """Perform a deposit."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        try:
            account = self.session.get_current_account()
            account_id = account.get_current_account_id()
            
            # Get ATM location (first ATM in database)
            atm_locations = [loc for loc in self.database.get_operation_locations() 
                           if hasattr(loc, 'get_number') and loc.get_number() >= 1000]
            if not atm_locations:
                MessageDisplay.show_error("Nenhum caixa eletrônico disponível")
                return
            
            atm_location = atm_locations[0].get_number()
            
            envelope = InputReader.read_int("Número do envelope: ")
            amount = InputReader.read_float("Valor do depósito: R$ ")
            
            if amount <= 0:
                MessageDisplay.show_error("Valor deve ser positivo")
                return
            
            deposit = self.operation_service.deposit(
                atm_location,
                account_id.get_branch().get_number(),
                account_id.get_account_number(),
                envelope,
                amount
            )
            
            print(f"\nDepósito realizado com sucesso!")
            print(f"Data: {deposit.get_date().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"Valor: R$ {deposit.get_amount():.2f}")
            print(f"Envelope: {deposit.get_envelope()}")
            print(f"Novo saldo: R$ {account.get_balance():.2f}")
            
            MessageDisplay.show_success("Depósito realizado com sucesso!")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def withdraw(self) -> None:
        """Perform a withdrawal."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        try:
            account = self.session.get_current_account()
            account_id = account.get_current_account_id()
            
            # Get ATM location (first ATM in database)
            atm_locations = [loc for loc in self.database.get_operation_locations() 
                           if hasattr(loc, 'get_number') and loc.get_number() >= 1000]
            if not atm_locations:
                MessageDisplay.show_error("Nenhum caixa eletrônico disponível")
                return
            
            atm_location = atm_locations[0].get_number()
            
            amount = InputReader.read_float("Valor do saque: R$ ")
            
            if amount <= 0:
                MessageDisplay.show_error("Valor deve ser positivo")
                return
            
            withdrawal = self.operation_service.withdrawal(
                atm_location,
                account_id.get_branch().get_number(),
                account_id.get_account_number(),
                amount
            )
            
            print(f"\nSaque realizado com sucesso!")
            print(f"Data: {withdrawal.get_date().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"Valor: R$ {withdrawal.get_amount():.2f}")
            print(f"Novo saldo: R$ {account.get_balance():.2f}")
            
            MessageDisplay.show_success("Saque realizado com sucesso!")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def transfer(self) -> None:
        """Perform a transfer."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        try:
            account = self.session.get_current_account()
            account_id = account.get_current_account_id()
            
            # Get ATM location (first ATM in database)  
            atm_locations = [loc for loc in self.database.get_operation_locations() 
                           if hasattr(loc, 'get_number') and loc.get_number() >= 1000]
            if not atm_locations:
                MessageDisplay.show_error("Nenhum caixa eletrônico disponível")
                return
            
            atm_location = atm_locations[0].get_number()
            
            dst_branch = InputReader.read_int("Agência destino: ")
            dst_account = InputReader.read_int("Conta destino: ")
            amount = InputReader.read_float("Valor da transferência: R$ ")
            
            if amount <= 0:
                MessageDisplay.show_error("Valor deve ser positivo")
                return
            
            transfer = self.operation_service.transfer(
                atm_location,
                account_id.get_branch().get_number(),
                account_id.get_account_number(),
                dst_branch,
                dst_account,
                amount
            )
            
            print(f"\nTransferência realizada com sucesso!")
            print(f"Data: {transfer.get_date().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"Valor: R$ {transfer.get_amount():.2f}")
            print(f"Conta destino: {dst_branch}-{dst_account}")
            print(f"Novo saldo: R$ {account.get_balance():.2f}")
            
            MessageDisplay.show_success("Transferência realizada com sucesso!")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def statement_by_date(self) -> None:
        """Get statement by date range."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        try:
            account = self.session.get_current_account()
            account_id = account.get_current_account_id()
            
            print("\n--- Período do Extrato ---")
            print("Data inicial:")
            start_day = InputReader.read_int("Dia: ")
            start_month = InputReader.read_int("Mês: ")
            start_year = InputReader.read_int("Ano: ")
            
            print("Data final:")
            end_day = InputReader.read_int("Dia: ")
            end_month = InputReader.read_int("Mês: ")
            end_year = InputReader.read_int("Ano: ")
            
            try:
                start_date = datetime(start_year, start_month, start_day)
                end_date = datetime(end_year, end_month, end_day, 23, 59, 59)
            except ValueError:
                MessageDisplay.show_error("Data inválida")
                return
            
            if start_date > end_date:
                MessageDisplay.show_error("Data inicial deve ser anterior à data final")
                return
            
            transactions = self.operation_service.get_statement_by_date(
                account_id.get_branch().get_number(),
                account_id.get_account_number(),
                start_date,
                end_date
            )
            
            self._display_statement(transactions, f"Extrato de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def statement_by_month(self) -> None:
        """Get statement by month."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        try:
            account = self.session.get_current_account()
            account_id = account.get_current_account_id()
            
            month = InputReader.read_int("Mês (1-12): ")
            year = InputReader.read_int("Ano: ")
            
            if not (1 <= month <= 12):
                MessageDisplay.show_error("Mês deve estar entre 1 e 12")
                return
            
            transactions = self.operation_service.get_statement_by_month(
                account_id.get_branch().get_number(),
                account_id.get_account_number(),
                month,
                year
            )
            
            months = [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]
            
            self._display_statement(transactions, f"Extrato de {months[month-1]} de {year}")
            
        except BusinessException as e:
            MessageDisplay.show_error(self._get_error_message(str(e)))
        except Exception as e:
            MessageDisplay.show_error("Erro interno do sistema")
    
    def show_account_info(self) -> None:
        """Show account information."""
        if not self.session.is_client_logged_in():
            MessageDisplay.show_error("Você precisa estar logado")
            return
        
        account = self.session.get_current_account()
        client = account.get_client()
        account_id = account.get_current_account_id()
        
        print("\n--- Informações da Conta ---")
        print(f"Agência: {account_id.get_branch().get_number()}")
        print(f"Conta: {account_id.get_account_number()}")
        print(f"Cliente: {client.get_name()} {client.get_last_name()}")
        print(f"CPF: {client.get_cpf()}")
        print(f"Data de Nascimento: {client.get_birthday().strftime('%d/%m/%Y')}")
        print(f"Saldo: R$ {account.get_balance():.2f}")
    
    def logout(self) -> None:
        """Logout current client."""
        if self.session.is_client_logged_in():
            client_name = self.session.get_current_account().get_client().get_name()
            self.session.clear_session()
            MessageDisplay.show_success(f"Logout realizado com sucesso! Até logo, {client_name}!")
        else:
            MessageDisplay.show_info("Nenhum usuário logado")
    
    def _display_statement(self, transactions: List[Transaction], title: str) -> None:
        """Display transaction statement."""
        print(f"\n--- {title} ---")
        
        if not transactions:
            print("Nenhuma transação encontrada no período.")
            return
        
        print(f"{'Data/Hora':<20} {'Tipo':<12} {'Valor':<15} {'Detalhes'}")
        print("-" * 70)
        
        for transaction in transactions:
            date_str = transaction.get_date().strftime('%d/%m/%Y %H:%M:%S')
            amount_str = f"R$ {transaction.get_amount():.2f}"
            
            if isinstance(transaction, Deposit):
                transaction_type = "Depósito"
                details = f"Envelope: {transaction.get_envelope()}"
            elif isinstance(transaction, Withdrawal):
                transaction_type = "Saque"
                details = ""
            elif isinstance(transaction, Transfer):
                transaction_type = "Transferência"
                dst_account = transaction.get_destination_account()
                dst_id = dst_account.get_current_account_id()
                details = f"Para: {dst_id.get_branch().get_number()}-{dst_id.get_account_number()}"
            else:
                transaction_type = "Desconhecido"
                details = ""
            
            print(f"{date_str:<20} {transaction_type:<12} {amount_str:<15} {details}")
        
        print(f"\nTotal de transações: {len(transactions)}")
    
    def _get_error_message(self, exception_key: str) -> str:
        """Get error message from exception key."""
        error_messages = {
            "exception.invalid.branch": "Agência inválida",
            "exception.inexistent.employee": "Funcionário não encontrado",
            "exception.invalid.password": "Senha inválida",
            "exception.inexistent.account": "Conta não encontrada",
            "exception.invalid.operation.location": "Local de operação inválido",
            "exception.insufficient.funds": "Saldo insuficiente",
        }
        return error_messages.get(exception_key, "Erro desconhecido")


def main():
    """Main function to start ATM interface."""
    database = Database()
    atm_interface = ATMInterface(database)
    atm_interface.start()


if __name__ == "__main__":
    main()