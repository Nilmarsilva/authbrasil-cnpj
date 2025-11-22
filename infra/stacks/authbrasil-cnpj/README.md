# Stack AuthBrasil CNPJ

API FastAPI do projeto principal.

## Características

- **2 réplicas** para alta disponibilidade
- **Load balancing** automático via Traefik
- **Rolling updates** sem downtime
- **Health checks** configurados
- **SSL** via Traefik
- **Rate limiting** e **CORS**

## Pré-requisitos

1. Stacks deployadas: Traefik, Portainer, Databases
2. Imagem Docker buildada: `authbrasil/api:latest`
3. Migrations executadas no PostgreSQL
4. Arquivo `.env` configurado

## Build da Imagem

### Na VPS

```bash
cd /opt/authbrasil/authbrasil-cnpj/backend

# Build
docker build -t authbrasil/api:latest .

# Verificar
docker images | grep authbrasil
```

### Alternativa: Build Local + Push

```bash
# Local (Windows)
cd backend
docker build -t authbrasil/api:latest .

# Tag para registry (se usar Docker Hub ou outro)
docker tag authbrasil/api:latest SEU_USUARIO/authbrasil-api:latest

# Push
docker push SEU_USUARIO/authbrasil-api:latest

# Na VPS, atualizar docker-compose.yml com a imagem do registry
```

## Executar Migrations

Antes do primeiro deploy, rodar migrations:

```bash
# Criar container temporário conectado ao postgres
docker run --rm \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:SENHA@postgres:5432/authbrasil_cnpj \
  authbrasil/api:latest \
  alembic upgrade head
```

## Configurar .env

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/authbrasil-cnpj

# Copiar exemplo
cp .env.example .env

# Editar
nano .env
```

**Gerar secrets fortes:**
```bash
# SECRET_KEY
openssl rand -hex 32

# JWT_SECRET_KEY
openssl rand -hex 32
```

**Importante:** Use as mesmas senhas configuradas nas outras stacks:
- `DB_PASSWORD` - Mesma senha do secret `db_password`
- `REDIS_PASSWORD` - Mesma senha da stack databases

## Deploy

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/authbrasil-cnpj

# Deploy da stack
docker stack deploy -c docker-compose.yml authbrasil

# Verificar
docker stack ps authbrasil
docker service logs authbrasil_api -f
```

## Acessar API

**URL:** https://api.authbrasil.app.br

**Documentação:** https://api.authbrasil.app.br/api/v1/docs

**Health Check:** https://api.authbrasil.app.br/api/v1/health

## Testar Endpoints

```bash
# Health check
curl https://api.authbrasil.app.br/api/v1/health

# Consultar CNPJ (após importar dados)
curl https://api.authbrasil.app.br/api/v1/cnpj/00000000000191

# Ver documentação
curl https://api.authbrasil.app.br/api/v1/docs
```

## Escalar

```bash
# Aumentar para 4 réplicas
docker service scale authbrasil_api=4

# Diminuir para 1 réplica
docker service scale authbrasil_api=1

# Ver status
docker service ps authbrasil_api
```

## Atualizar Código

### 1. Build Nova Imagem

```bash
cd /opt/authbrasil/authbrasil-cnpj/backend

# Pull código atualizado
git pull origin main

# Rebuild
docker build -t authbrasil/api:latest .
```

### 2. Executar Migrations (se necessário)

```bash
docker run --rm \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:SENHA@postgres:5432/authbrasil_cnpj \
  authbrasil/api:latest \
  alembic upgrade head
```

### 3. Update Service (Rolling Update)

```bash
# Update automático com zero downtime
docker service update --image authbrasil/api:latest authbrasil_api

# Acompanhar update
docker service ps authbrasil_api -f "desired-state=running"
```

O Swarm irá:
1. Iniciar nova réplica com código atualizado
2. Aguardar health check passar
3. Parar réplica antiga
4. Repetir para próxima réplica

## Logs

```bash
# Logs de todas as réplicas
docker service logs authbrasil_api -f

# Logs com timestamp
docker service logs authbrasil_api -f --timestamps

# Últimas 100 linhas
docker service logs authbrasil_api --tail 100

# Filtrar por erro
docker service logs authbrasil_api | grep ERROR
```

## Troubleshooting

### API não inicia

```bash
# Ver logs detalhados
docker service logs authbrasil_api --tail 200

# Ver status das tasks
docker service ps authbrasil_api --no-trunc

# Verificar variáveis de ambiente
docker service inspect authbrasil_api --format='{{json .Spec.TaskTemplate.ContainerSpec.Env}}' | jq

# Testar imagem localmente
docker run --rm -it authbrasil/api:latest python -c "from app.main import app; print('OK')"
```

### Erro de conexão com banco

```bash
# Verificar se postgres está rodando
docker service ls | grep postgres

# Testar conexão do container da API
docker exec $(docker ps -q -f name=authbrasil_api) \
  python -c "import psycopg2; psycopg2.connect('postgresql://authbrasil_user:SENHA@postgres:5432/authbrasil_cnpj')"

# Ver logs do postgres
docker service logs databases_postgres --tail 50
```

### SSL não funciona

```bash
# Verificar labels do Traefik
docker service inspect authbrasil_api --format='{{json .Spec.Labels}}' | jq

# Ver logs do Traefik
docker service logs traefik_traefik | grep authbrasil

# Verificar DNS
dig api.authbrasil.app.br
```

### High CPU/Memory

```bash
# Ver uso de recursos
docker stats

# Ver réplicas e distribuição
docker service ps authbrasil_api

# Verificar logs para erros
docker service logs authbrasil_api | grep -i "error\|exception"
```

## Rollback

Se algo der errado após update:

```bash
# Rollback automático para versão anterior
docker service rollback authbrasil_api

# Ver histórico de updates
docker service inspect authbrasil_api --format='{{json .PreviousSpec}}' | jq
```

## Monitoramento

### Health Checks

```bash
# Ver status de health
docker service ps authbrasil_api

# Testar health endpoint
while true; do curl -s https://api.authbrasil.app.br/api/v1/health | jq; sleep 5; done
```

### Métricas

```bash
# Requisições por segundo (via logs Traefik)
docker service logs traefik_traefik --since 5m | grep "authbrasil-api" | wc -l

# Response times (se configurado)
docker service logs authbrasil_api | grep "response_time"
```

## Segurança

### Secrets (Recomendado)

Migrar variáveis sensíveis para Docker Secrets:

```bash
# Criar secrets
echo "sua_secret_key" | docker secret create app_secret_key -
echo "seu_jwt_secret" | docker secret create app_jwt_secret -
echo "stripe_key" | docker secret create stripe_secret_key -

# Atualizar docker-compose.yml para usar secrets
# Depois: docker stack deploy -c docker-compose.yml authbrasil
```

### Rate Limiting

Configurado no Traefik:
- Average: 100 req/min
- Burst: 50 req

Ajustar no `docker-compose.yml` se necessário.

## Remover

```bash
# Remover stack
docker stack rm authbrasil

# Verificar
docker service ls
```

---

**Importante:** Sempre teste updates em ambiente de staging antes de produção!
