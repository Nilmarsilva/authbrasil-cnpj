# Stack Databases

PostgreSQL, Redis e pgAdmin para o AuthBrasil CNPJ.

## Serviços

- **PostgreSQL 16** - Banco de dados principal
- **Redis 7** - Cache e filas
- **pgAdmin 4** - Interface web para PostgreSQL

## Pré-requisitos

1. Stack Traefik deployada
2. Rede `network_public` criada
3. Secrets criados (ver abaixo)

## Criar Secrets

Docker Secrets são a forma segura de gerenciar senhas no Swarm.

### 1. Senha do PostgreSQL

```bash
# Gerar senha forte
openssl rand -base64 32

# Criar secret (substituir SUA_SENHA_AQUI)
echo "SUA_SENHA_AQUI" | docker secret create db_password -

# Verificar
docker secret ls
```

### 2. Senha do pgAdmin

```bash
# Gerar senha forte
openssl rand -base64 24

# Criar secret
echo "SUA_SENHA_AQUI" | docker secret create pgadmin_password -
```

### 3. Configurar .env

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/databases

# Copiar exemplo
cp .env.example .env

# Editar
nano .env
```

Configurar:
- `REDIS_PASSWORD` - Senha forte para Redis
- `PGADMIN_EMAIL` - Seu email de admin

## Deploy

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/databases

# Deploy da stack
docker stack deploy -c docker-compose.yml databases

# Verificar
docker stack ps databases
docker service logs databases_postgres -f
```

## Acessar Serviços

### pgAdmin

**URL:** https://pg.authbrasil.app.br

**Login:**
- Email: (configurado no .env)
- Senha: (a que você criou no secret pgadmin_password)

### Conectar pgAdmin ao PostgreSQL

1. Acessar pgAdmin
2. Add New Server
3. Configurar:
   - **Name:** AuthBrasil Production
   - **Host:** postgres (nome do serviço Swarm)
   - **Port:** 5432
   - **Database:** authbrasil_cnpj
   - **Username:** authbrasil_user
   - **Password:** (senha do secret db_password)

### Conectar API ao PostgreSQL

No serviço da API, usar:

```
DATABASE_URL=postgresql://authbrasil_user:SENHA_DO_SECRET@postgres:5432/authbrasil_cnpj
```

**Importante:** Substituir `SENHA_DO_SECRET` pela senha real ou usar Docker Secrets também na API.

### Conectar API ao Redis

```
REDIS_URL=redis://:SENHA_REDIS@redis:6379/0
```

## Backup

### Backup PostgreSQL

```bash
# Backup completo
docker exec $(docker ps -q -f name=databases_postgres) \
  pg_dump -U authbrasil_user -Fc authbrasil_cnpj > backup_$(date +%Y%m%d_%H%M%S).dump

# Backup com compressão
docker exec $(docker ps -q -f name=databases_postgres) \
  pg_dump -U authbrasil_user authbrasil_cnpj | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Restore PostgreSQL

```bash
# Restore de dump custom format
docker exec -i $(docker ps -q -f name=databases_postgres) \
  pg_restore -U authbrasil_user -d authbrasil_cnpj -c < backup_20241122_103000.dump

# Restore de SQL
gunzip < backup_20241122_103000.sql.gz | \
  docker exec -i $(docker ps -q -f name=databases_postgres) \
  psql -U authbrasil_user -d authbrasil_cnpj
```

### Backup Redis

```bash
# Trigger save manual
docker exec $(docker ps -q -f name=databases_redis) redis-cli -a SENHA_REDIS SAVE

# Copiar arquivo RDB
docker cp $(docker ps -q -f name=databases_redis):/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb
```

## Troubleshooting

### PostgreSQL não inicia

```bash
# Ver logs
docker service logs databases_postgres --tail 100

# Verificar secret
docker secret inspect db_password

# Verificar volume
docker volume inspect databases_postgres_data

# Forçar restart
docker service update --force databases_postgres
```

### Redis não aceita conexões

```bash
# Ver logs
docker service logs databases_redis --tail 50

# Testar conexão
docker exec $(docker ps -q -f name=databases_redis) redis-cli -a SENHA_REDIS ping
# Deve retornar: PONG

# Verificar configuração
docker exec $(docker ps -q -f name=databases_redis) redis-cli -a SENHA_REDIS CONFIG GET maxmemory
```

### pgAdmin não acessa PostgreSQL

```bash
# Verificar se estão na mesma rede
docker network inspect network_public

# Testar conexão do pgAdmin para o postgres
docker exec $(docker ps -q -f name=databases_pgadmin) ping -c 3 postgres

# Ver logs do pgAdmin
docker service logs databases_pgadmin --tail 50
```

## Manutenção

### Ver Estatísticas PostgreSQL

```bash
# Conectar ao PostgreSQL
docker exec -it $(docker ps -q -f name=databases_postgres) \
  psql -U authbrasil_user -d authbrasil_cnpj

# Dentro do psql:
\l                          -- Listar databases
\dt                         -- Listar tabelas
\d nome_tabela              -- Descrever tabela
SELECT version();           -- Versão do PostgreSQL
SELECT count(*) FROM users; -- Contar registros
\q                          -- Sair
```

### Ver Info Redis

```bash
# Conectar ao Redis
docker exec -it $(docker ps -q -f name=databases_redis) redis-cli -a SENHA_REDIS

# Dentro do redis-cli:
INFO                    -- Informações gerais
DBSIZE                  -- Número de keys
MEMORY STATS            -- Uso de memória
CONFIG GET maxmemory    -- Limite de memória
```

### Limpar Cache Redis

```bash
# Limpar todo o cache (CUIDADO!)
docker exec $(docker ps -q -f name=databases_redis) redis-cli -a SENHA_REDIS FLUSHALL

# Limpar database específica
docker exec $(docker ps -q -f name=databases_redis) redis-cli -a SENHA_REDIS -n 0 FLUSHDB
```

## Atualizar

```bash
# Atualizar PostgreSQL (com cuidado!)
docker service update --image postgres:16-alpine databases_postgres

# Atualizar Redis
docker service update --image redis:7-alpine databases_redis

# Atualizar pgAdmin
docker service update --image dpage/pgadmin4:latest databases_pgadmin
```

## Segurança

### IP Whitelist para pgAdmin

Descomentar labels no `docker-compose.yml`:

```yaml
- "traefik.http.middlewares.pgadmin-ipwhitelist.ipwhitelist.sourcerange=SEU_IP/32"
- "traefik.http.routers.pgadmin.middlewares=pgadmin-ipwhitelist"
```

Substituir `SEU_IP` pelo seu IP real:
```bash
curl -s https://api.ipify.org
```

### Rotacionar Senhas

```bash
# 1. Criar novo secret
echo "NOVA_SENHA" | docker secret create db_password_v2 -

# 2. Atualizar docker-compose.yml para usar db_password_v2

# 3. Atualizar serviço
docker stack deploy -c docker-compose.yml databases

# 4. Remover secret antigo (após confirmar funcionamento)
docker secret rm db_password
```

## Remover

```bash
# Remover stack (mantém volumes)
docker stack rm databases

# Remover volumes (CUIDADO: perde dados!)
docker volume rm databases_postgres_data
docker volume rm databases_redis_data
docker volume rm databases_pgadmin_data

# Remover secrets
docker secret rm db_password
docker secret rm pgadmin_password
```

---

**Importante:** Faça backups regulares do PostgreSQL. Os dados são críticos!
