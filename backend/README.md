# AuthBrasil CNPJ - Backend

API REST em FastAPI para consulta de dados corporativos brasileiros.

## Requisitos

- Python 3.11+
- PostgreSQL 16+
- Redis 7+ (opcional no MVP)

## Instalação

### 1. Criar ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as configurações:

```powershell
Copy-Item ..\.env.example .env
```

Edite o arquivo `.env` com suas configurações de banco de dados.

### 4. Criar banco de dados

No PostgreSQL:

```sql
CREATE DATABASE authbrasil_cnpj;
```

### 5. Executar migrations

```powershell
alembic upgrade head
```

## Executar em Desenvolvimento

### Opção 1: Usando run.py

```powershell
python run.py
```

### Opção 2: Usando uvicorn diretamente

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **API:** http://localhost:8000
- **Documentação (Swagger):** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc

## Endpoints Disponíveis

### Health Check
- `GET /api/v1/health` - Status básico
- `GET /api/v1/health/detailed` - Status detalhado

### CNPJ
- `GET /api/v1/cnpj/{cnpj}` - Consulta CNPJ completo
- `GET /api/v1/cnpj/search/razao-social?q=empresa` - Busca por razão social

## Estrutura

```
backend/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API endpoints
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/            # Core configurations
│   │   └── config.py
│   ├── db/              # Database setup
│   │   └── base.py
│   ├── models/          # SQLAlchemy models
│   └── main.py          # FastAPI application
├── requirements.txt     # Python dependencies
└── run.py              # Development server
```

## Migrations

### Criar nova migration

```powershell
alembic revision --autogenerate -m "description"
```

### Aplicar migrations

```powershell
alembic upgrade head
```

### Reverter migration

```powershell
alembic downgrade -1
```

## Testes

```powershell
pytest
```

## Próximos Passos

1. Importar dados da Receita Federal
2. Implementar autenticação JWT
3. Adicionar rate limiting
4. Implementar cache Redis
5. Adicionar testes unitários
