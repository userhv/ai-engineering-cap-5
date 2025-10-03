"""
Main application entry point for the banking system.
"""
from .ui.text.ui_utils import Menu, SimpleCommand, MessageDisplay
from .ui.text.branch_interface import BranchInterface
from .ui.text.atm_interface import ATMInterface
from .data.database import Database


class BankingApplication:
    """Main banking application."""
    
    def __init__(self):
        self.database = Database()
        self.setup_menu()
    
    def setup_menu(self) -> None:
        """Setup the main application menu."""
        self.main_menu = Menu("Sistema Bancário")
        self.main_menu.add_command(SimpleCommand("Agência Bancária", self.start_branch_interface))
        self.main_menu.add_command(SimpleCommand("Caixa Eletrônico", self.start_atm_interface))
        self.main_menu.add_command(SimpleCommand("Sobre o Sistema", self.show_about))
    
    def run(self) -> None:
        """Run the banking application."""
        print("=" * 50)
        print("    SISTEMA BANCÁRIO DIDÁTICO")
        print("    Versão 1.0 - Python Implementation")
        print("=" * 50)
        print()
        
        MessageDisplay.show_info("Banco de dados inicializado com dados de exemplo")
        MessageDisplay.show_info("Use as credenciais padrão para teste")
        print()
        
        self.main_menu.show()
        
        print("\nObrigado por usar o Sistema Bancário!")
    
    def start_branch_interface(self) -> None:
        """Start the branch interface."""
        branch_interface = BranchInterface(self.database)
        branch_interface.start()
    
    def start_atm_interface(self) -> None:
        """Start the ATM interface."""
        atm_interface = ATMInterface(self.database)
        atm_interface.start()
    
    def show_about(self) -> None:
        """Show information about the system."""
        print("\n" + "=" * 50)
        print("           SOBRE O SISTEMA BANCÁRIO")
        print("=" * 50)
        print()
        print("Este é um sistema bancário didático desenvolvido em Python.")
        print("Ele simula operações básicas de um banco, incluindo:")
        print()
        print("FUNCIONALIDADES:")
        print("• Criação de contas correntes")
        print("• Depósitos e saques")
        print("• Transferências entre contas")
        print("• Consulta de saldo e extratos")
        print("• Gestão de funcionários e clientes")
        print()
        print("INTERFACES:")
        print("• Agência Bancária - Para funcionários")
        print("• Caixa Eletrônico - Para clientes")
        print()
        print("DADOS DE TESTE:")
        print("Funcionário: admin / senha: admin")
        print("Cliente: Agência 1, Conta 1001 / senha: gerada automaticamente")
        print()
        print("ARQUITETURA:")
        print("• Camada de Interface (UI)")
        print("• Camada de Negócio (Business)")
        print("• Camada de Dados (Data)")
        print()
        print("Desenvolvido como projeto didático.")
        print("=" * 50)


def main():
    """Main entry point."""
    try:
        app = BankingApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n\nAplicação encerrada pelo usuário.")
    except Exception as e:
        print(f"\nErro crítico: {e}")
        print("A aplicação será encerrada.")


if __name__ == "__main__":
    main()