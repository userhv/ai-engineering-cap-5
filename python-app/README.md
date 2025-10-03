# Sistema Bancário Didático - Python

Este é um sistema bancário didático desenvolvido em Python, baseado no projeto Java [didactic-bank-application](https://github.com/ingridnunes/didactic-bank-application). O sistema simula operações básicas de um banco com arquitetura em camadas.

## 🏗️ Arquitetura

O sistema segue uma arquitetura em 3 camadas:

### 1. Camada de Interface (UI)
- **Agência Bancária**: Interface para funcionários criarem contas
- **Caixa Eletrônico**: Interface para clientes realizarem operações

### 2. Camada de Negócio (Business)
- **Domain**: Objetos de domínio (User, Client, Employee, CurrentAccount, Transaction)
- **Services**: Serviços de negócio (AccountManagementService, AccountOperationService)
- **Implementations**: Implementações concretas dos serviços

### 3. Camada de Dados (Data)
- **Database**: Banco de dados em memória com dados de exemplo

## 🚀 Funcionalidades

### Para Funcionários (Agência)
- ✅ Login de funcionário
- ✅ Criação de contas correntes
- ✅ Consulta de informações de funcionário

### Para Clientes (Caixa Eletrônico)
- ✅ Login de cliente
- ✅ Consulta de saldo
- ✅ Depósitos
- ✅ Saques
- ✅ Transferências entre contas
- ✅ Extratos por período
- ✅ Extratos mensais
- ✅ Informações da conta

## 🛠️ Tecnologias

- **Python 3.11+**
- **pytest**: Framework de testes
- **Docker**: Containerização
- **Typing**: Tipagem estática

## 📦 Estrutura do Projeto

```
python-app/
├── bank/
│   ├── __init__.py
│   ├── main.py                    # Aplicação principal
│   ├── business/
│   │   ├── __init__.py
│   │   ├── business_exception.py  # Exceções de negócio
│   │   ├── services.py            # Interfaces dos serviços
│   │   ├── domain/                # Objetos de domínio
│   │   │   ├── user.py
│   │   │   ├── client.py
│   │   │   ├── employee.py
│   │   │   ├── current_account.py
│   │   │   ├── transaction.py
│   │   │   └── ...
│   │   └── impl/
│   │       └── service_impl.py    # Implementações dos serviços
│   ├── data/
│   │   ├── __init__.py
│   │   └── database.py            # Banco de dados em memória
│   ├── ui/
│   │   ├── __init__.py
│   │   └── text/                  # Interface de linha de comando
│   │       ├── ui_utils.py        # Utilitários de UI
│   │       ├── branch_interface.py
│   │       └── atm_interface.py
│   └── util/
│       ├── __init__.py
│       └── random_string.py       # Geração de senhas
├── tests/
│   ├── __init__.py
│   └── test_banking_system.py     # Testes abrangentes
├── requirements.txt
└── run_bank.py                    # Script de execução
```

## 🚀 Como Executar

### Usando Docker (Recomendado)

1. **Construir e executar o container:**
```bash
docker-compose up --build
```

2. **Executar o sistema bancário:**
```bash
# Dentro do container
python run_bank.py
```

### Executação Local

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Executar o sistema:**
```bash
python run_bank.py
```

## 🧪 Executar Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar com cobertura
pytest tests/ --cov=bank --cov-report=html
```

## 👥 Dados de Teste

O sistema é inicializado com dados de exemplo:

### Funcionários
- **Usuário:** `ingrid`
- **Senha:** `123`
- **Agência:** 1

### Clientes
- **Agência:** 1
- **Conta:** 1001, 1002, 1003...
- **Senhas:** Geradas automaticamente (exibidas na criação da conta)

## 🎯 Como Usar

### 1. Interface da Agência Bancária
```
1. Escolha "Agência Bancária" no menu principal
2. Faça login com: ingrid/123
3. Crie novas contas correntes
4. As senhas dos clientes são geradas automaticamente
```

### 2. Interface do Caixa Eletrônico
```
1. Escolha "Caixa Eletrônico" no menu principal
2. Digite: Agência, Número da Conta, Senha
3. Realize operações bancárias
```

## 🔧 Principais Classes

### Domain Objects
- **User**: Classe abstrata para usuários
- **Client**: Cliente do banco
- **Employee**: Funcionário do banco
- **CurrentAccount**: Conta corrente
- **Transaction**: Transações (Deposit, Withdrawal, Transfer)

### Business Services
- **AccountManagementService**: Gestão de contas e login de funcionários
- **AccountOperationService**: Operações bancárias dos clientes

### Data Layer
- **Database**: Banco de dados em memória com operações CRUD

## 🔒 Tratamento de Erros

O sistema implementa tratamento robusto de erros:
- Validação de saldo insuficiente
- Verificação de credenciais
- Validação de contas existentes
- Tratamento de exceções de negócio

## 📊 Padrões de Design

- **Repository Pattern**: Camada de dados
- **Service Layer**: Lógica de negócio
- **MVC**: Separação de responsabilidades
- **Factory Pattern**: Criação de objetos
- **Strategy Pattern**: Diferentes tipos de transação

## 🚦 Melhorias Futuras

- [ ] Persistência em banco de dados real
- [ ] Interface web (Flask/Django)
- [ ] API RESTful
- [ ] Autenticação JWT
- [ ] Logs de auditoria
- [ ] Validação de CPF
- [ ] Diferentes tipos de conta

## 📝 Licença

Este projeto é desenvolvido para fins educacionais baseado no projeto original Java.

---

**Desenvolvido como portabilidade do projeto Java para Python** 🐍