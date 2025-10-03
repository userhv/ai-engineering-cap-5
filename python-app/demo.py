#!/usr/bin/env python3
"""
Demo script to showcase the banking system functionality.
"""

import sys
import os

# Add the bank package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bank.data.database import Database
from bank.business.impl.service_impl import AccountManagementServiceImpl, AccountOperationServiceImpl
from bank.business.domain.current_account import CurrentAccount
from datetime import datetime

def demo_banking_system():
    """Demonstrate the banking system functionality."""
    print("=== DEMO DO SISTEMA BANCÁRIO ===\n")
    
    # Initialize database
    print("1. Inicializando banco de dados...")
    db = Database()
    print(f"   ✓ Database inicializado com {len(list(db.get_all_current_accounts()))} contas")
    print(f"   ✓ {len(list(db.get_all_employees()))} funcionários")
    print(f"   ✓ {len(list(db.get_all_operation_locations()))} locais de operação")
    
    # Initialize services
    account_mgmt = AccountManagementServiceImpl(db)
    account_ops = AccountOperationServiceImpl(db)
    
    print("\n2. Testando login de funcionário...")
    try:
        employee = account_mgmt.login("ingrid", "123")
        print(f"   ✓ Login realizado: {employee.get_first_name()} {employee.get_last_name()}")
    except Exception as e:
        print(f"   ✗ Erro no login: {e}")
        return
    
    print("\n3. Criando nova conta...")
    try:
        birthday = datetime(1990, 5, 15)
        new_account = account_mgmt.create_current_account(
            1, "João", "Silva", 12345678901, birthday, 1000.0
        )
        print(f"   ✓ Conta criada: Agência {new_account.get_id().get_branch().get_number()}, "
              f"Conta {new_account.get_id().get_number()}")
        print(f"   ✓ Cliente: {new_account.get_client().get_first_name()} {new_account.get_client().get_last_name()}")
        print(f"   ✓ Saldo inicial: R$ {new_account.get_balance():.2f}")
        print(f"   ✓ Senha: {new_account.get_client().get_password()}")
        
        # Test client login
        print("\n4. Testando login de cliente...")
        logged_account = account_ops.login(
            new_account.get_id().get_branch().get_number(),
            new_account.get_id().get_number(),
            new_account.get_client().get_password()
        )
        print(f"   ✓ Cliente logado com sucesso")
        
        # Test balance inquiry
        print("\n5. Consultando saldo...")
        balance = account_ops.get_balance(
            new_account.get_id().get_branch().get_number(),
            new_account.get_id().get_number()
        )
        print(f"   ✓ Saldo atual: R$ {balance:.2f}")
        
        # Test deposit
        print("\n6. Realizando depósito...")
        # Get first ATM
        from bank.business.domain.operation_location import ATM
        atm_locations = [loc for loc in db.get_all_operation_locations() if isinstance(loc, ATM)]
        if atm_locations:
            deposit = account_ops.deposit(
                atm_locations[0].get_number(),
                new_account.get_id().get_branch().get_number(),
                new_account.get_id().get_number(),
                123,
                500.0
            )
            print(f"   ✓ Depósito realizado: R$ {deposit.get_amount():.2f}")
            print(f"   ✓ Novo saldo: R$ {new_account.get_balance():.2f}")
        
        # Test withdrawal
        print("\n7. Realizando saque...")
        if atm_locations:
            withdrawal = account_ops.withdrawal(
                atm_locations[0].get_number(),
                new_account.get_id().get_branch().get_number(),
                new_account.get_id().get_number(),
                200.0
            )
            print(f"   ✓ Saque realizado: R$ {withdrawal.get_amount():.2f}")
            print(f"   ✓ Novo saldo: R$ {new_account.get_balance():.2f}")
        
        print("\n8. Consultando extrato...")
        transactions = account_ops.get_statement_by_month(
            new_account.get_id().get_branch().get_number(),
            new_account.get_id().get_number(),
            datetime.now().month,
            datetime.now().year
        )
        print(f"   ✓ {len(transactions)} transações encontradas")
        for i, transaction in enumerate(transactions[:3], 1):  # Show first 3
            print(f"   {i}. {transaction.__class__.__name__}: R$ {transaction.get_amount():.2f} "
                  f"em {transaction.get_date().strftime('%d/%m/%Y %H:%M')}")
        
    except Exception as e:
        print(f"   ✗ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== DEMO CONCLUÍDO COM SUCESSO! ===")
    print("\nO sistema bancário Python está funcionando corretamente!")
    print("Você pode executar 'python run_bank.py' para usar as interfaces interativas.")

if __name__ == "__main__":
    demo_banking_system()