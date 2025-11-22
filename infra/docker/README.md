# Docker Infrastructure

Configuração Docker para desenvolvimento local.

## Serviços Incluídos

- **PostgreSQL 16** - Banco de dados principal
- **Redis 7** - Cache e task queue
- **pgAdmin 4** - Interface web para PostgreSQL

## Iniciar Serviços

```powershell
cd infra\docker
docker-compose -f docker-compose.dev.yml up -d
```

## Parar Serviços

```powershell
docker-compose -f docker-compose.dev.yml down
```

## Parar e Remover Volumes (limpar dados)

```powershell
docker-compose -f docker-compose.dev.yml down -v
```

## Acessar Serviços

### PostgreSQL
- **Host:** localhost
- **Port:** 5432
- **User:** postgres
- **Password:** postgres
- **Database:** authbrasil_cnpj

### Redis
- **Host:** localhost
- **Port:** 6379

### pgAdmin
- **URL:** http://localhost:5050
- **Email:** admin@authbrasil.local
- **Password:** admin

## Conectar pgAdmin ao PostgreSQL

1. Acessar http://localhost:5050
2. Clicar em "Add New Server"
3. Configurar:
   - **Name:** AuthBrasil Local
   - **Host:** postgres (nome do container)
   - **Port:** 5432
   - **Username:** postgres
   - **Password:** postgres

## Status dos Containers

```powershell
docker-compose -f docker-compose.dev.yml ps
```

## Logs

Ver logs de todos os serviços:
```powershell
docker-compose -f docker-compose.dev.yml logs -f
```

Ver logs de um serviço específico:
```powershell
docker-compose -f docker-compose.dev.yml logs -f postgres
```
