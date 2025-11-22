# Guia de Setup - AuthBrasil CNPJ

Instruções para configurar o ambiente de desenvolvimento.

## Pré-requisitos

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/) (para frontend futuro)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download](https://git-scm.com/downloads)

## Setup Backend

### 1. Iniciar Banco de Dados com Docker

```powershell
cd infra\docker
docker-compose -f docker-compose.dev.yml up -d
```

Aguarde os containers iniciarem. Verifique com:
```powershell
docker-compose -f docker-compose.dev.yml ps
```

### 2. Configurar Python

Criar ambiente virtual:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instalar dependências:
```powershell
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

O arquivo `.env` já foi criado em `backend/.env` com configurações padrão.
Verifique se a `DATABASE_URL` está correta:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/authbrasil_cnpj
```

### 4. Executar Migrations

Criar migration inicial:
```powershell
alembic revision --autogenerate -m "initial tables"
```

Aplicar migration:
```powershell
alembic upgrade head
```

### 5. Iniciar API

```powershell
python run.py
```

A API estará disponível em:
- **API Base:** http://localhost:8000
- **Documentação:** http://localhost:8000/api/v1/docs

### 6. Testar Endpoints

Abra o navegador em http://localhost:8000/api/v1/docs

Teste o endpoint:
- `GET /api/v1/health` - Deve retornar status "healthy"

## Verificar Instalação

### PostgreSQL

Acessar pgAdmin: http://localhost:5050
- **Email:** admin@authbrasil.local
- **Password:** admin

### Verificar Tabelas

No pgAdmin, conecte ao servidor e verifique se as tabelas foram criadas:
- users
- plans
- subscriptions
- api_keys
- empresas
- estabelecimentos
- socios

## Próximos Passos

### Importar Dados da Receita (ETL)

Os dados ainda não estão no banco. Próximas tarefas:

1. Criar script ETL em `backend/scripts/etl_receita.py`
2. Baixar dados de https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/
3. Processar e importar para PostgreSQL
4. Testar endpoint `/cnpj/{cnpj}` com dados reais

### Desenvolvimento Frontend

1. Inicializar projeto Next.js em `frontend/`
2. Configurar TailwindCSS + shadcn/ui
3. Criar páginas de login e dashboard

## Troubleshooting

### Erro de conexão com PostgreSQL

Verifique se o container está rodando:
```powershell
docker ps
```

Se não estiver, inicie novamente:
```powershell
cd infra\docker
docker-compose -f docker-compose.dev.yml up -d postgres
```

### Erro no Alembic

Se houver problemas com migrations, limpe e recrie:
```powershell
# Remover migrations anteriores
Remove-Item backend\alembic\versions\*.py

# Criar nova migration
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
```

### Python venv não ativa

No PowerShell, pode ser necessário habilitar scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Comandos Úteis

### Docker

```powershell
# Parar containers
docker-compose -f docker-compose.dev.yml down

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Resetar dados (cuidado!)
docker-compose -f docker-compose.dev.yml down -v
```

### Alembic

```powershell
# Ver histórico de migrations
alembic history

# Ver migration atual
alembic current

# Reverter última migration
alembic downgrade -1
```

### Git

```powershell
# Ver status
git status

# Commit
git add .
git commit -m "feat: descrição da mudança"

# Push
git push
```

## Suporte

Consulte a documentação completa em:
- `Projeto.md` - Especificação técnica
- `backend/README.md` - Documentação do backend
- `PROXIMOS_PASSOS.md` - Roadmap de desenvolvimento
