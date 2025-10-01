# Python App

Este é um projeto Python simples com testes unitários.

## Estrutura
```
python-app/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
└── requirements.txt
```

## Como usar

### Executar testes localmente
```bash
cd python-app
pip install -r requirements.txt
pytest tests/ -v
```

### Executar com Docker
```bash
# Build e run
docker-compose build python
docker-compose run --rm python pytest tests/ -v

# Com coverage
docker-compose run --rm python pytest tests/ -v --cov=src
```