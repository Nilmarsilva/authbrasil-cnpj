# Deploy Completo - Docker Swarm

Guia step-by-step para deploy completo do AuthBrasil CNPJ na VPS.

## Visão Geral

```
1. Reset VPS           → Limpar tudo
2. Configurar Cloudflare → DNS e SSL
3. Inicializar Swarm    → Setup Docker Swarm
4. Deploy Traefik       → Reverse Proxy (1º)
5. Deploy Portainer     → Gestão Visual (2º)
6. Deploy Databases     → PostgreSQL + Redis (3º)
7. Deploy AuthBrasil    → API FastAPI (4º)
```

---

## Fase 1: Preparação

### 1.1. Cloudflare (Fazer Primeiro!)

1. Criar conta: https://dash.cloudflare.com/sign-up
2. Add site: `authbrasil.app.br`
3. Plano: **Free**
4. Copiar nameservers fornecidos

**Exemplo:**
```
alexa.ns.cloudflare.com
boyd.ns.cloudflare.com
```

5. Atualizar no Registro.br:
   - Login em https://registro.br
   - Editar `authbrasil.app.br`
   - Trocar nameservers
   - Salvar e aguardar propagação (até 24h)

6. Configurar DNS no Cloudflare:

| Tipo | Nome | Valor | Proxy |
|------|------|-------|-------|
| A | server | 89.116.186.161 | DNS only |
| CNAME | traefik | server.authbrasil.app.br | DNS only |
| CNAME | portainer | server.authbrasil.app.br | DNS only |
| CNAME | pg | server.authbrasil.app.br | DNS only |
| CNAME | api | server.authbrasil.app.br | Proxied ☁️ |

7. SSL/TLS: **Full (strict)**
8. Always Use HTTPS: **ON**

### 1.2. Reset VPS

```bash
ssh usuario@89.116.186.161

# Parar tudo
docker stop $(docker ps -aq)

# Remover containers, imagens, volumes, redes
docker system prune -a --volumes -f

# Limpar diretórios
sudo rm -rf /opt/*

# Criar estrutura nova
sudo mkdir -p /opt/authbrasil
sudo chown -R $USER:$USER /opt/authbrasil
```

---

## Fase 2: Setup Swarm

### 2.1. Inicializar Swarm

```bash
docker swarm init --advertise-addr 89.116.186.161

# Verificar
docker node ls
```

### 2.2. Criar Rede

```bash
docker network create --driver overlay --attachable network_public
```

### 2.3. Criar Volumes

```bash
docker volume create volume_swarm_certificates
docker volume create portainer_data
```

### 2.4. Clonar Repositório

```bash
cd /opt/authbrasil
git clone https://github.com/Nilmarsilva/authbrasil-cnpj.git
cd authbrasil-cnpj
```

---

## Fase 3: Deploy das Stacks

### 3.1. Traefik (Primeiro)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/traefik

# Deploy
docker stack deploy -c docker-compose.yml traefik

# Verificar
docker service logs traefik_traefik -f
```

**Aguardar:** SSL ser gerado (1-2 min)

**Testar:**
```bash
curl -I https://portainer.authbrasil.app.br
# Deve redirecionar de HTTP para HTTPS
```

### 3.2. Portainer (Segundo)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/portainer

# Deploy
docker stack deploy -c docker-compose.yml portainer

# Verificar
docker service logs portainer_portainer -f
```

**Acessar:** https://portainer.authbrasil.app.br

**IMPORTANTE:** Criar senha de admin em 5 minutos!

### 3.3. Databases (Terceiro)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/databases

# Criar secrets
echo "$(openssl rand -base64 32)" | docker secret create db_password -
echo "$(openssl rand -base64 24)" | docker secret create pgadmin_password -

# Configurar .env
cp .env.example .env
nano .env
# Editar REDIS_PASSWORD e PGADMIN_EMAIL

# Deploy
docker stack deploy -c docker-compose.yml databases

# Verificar
docker service logs databases_postgres -f
```

**Testar:** https://pg.authbrasil.app.br

### 3.4. AuthBrasil CNPJ (Quarto)

#### Build da Imagem

```bash
cd /opt/authbrasil/authbrasil-cnpj/backend
docker build -t authbrasil/api:latest .
```

#### Executar Migrations

```bash
# Pegar senha do secret
DB_PASS=$(docker secret inspect db_password --format='{{.Spec.Data}}' | base64 -d)

# Rodar migrations
docker run --rm \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:$DB_PASS@postgres:5432/authbrasil_cnpj \
  authbrasil/api:latest \
  alembic upgrade head
```

#### Configurar e Deploy

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/authbrasil-cnpj

# Configurar .env
cp .env.example .env
nano .env
# Configurar todas as variáveis (secrets, Stripe, etc)

# Deploy
docker stack deploy -c docker-compose.yml authbrasil

# Verificar
docker service logs authbrasil_api -f
```

**Testar:** https://api.authbrasil.app.br/api/v1/health

---

## Fase 4: Verificação

### 4.1. Checar Todas as Stacks

```bash
docker stack ls

# Deve mostrar:
# NAME           SERVICES
# authbrasil     1
# databases      3
# portainer      2
# traefik        1
```

### 4.2. Testar Endpoints

```bash
# Health check
curl https://api.authbrasil.app.br/api/v1/health

# Documentação
curl https://api.authbrasil.app.br/api/v1/docs

# pgAdmin
curl -I https://pg.authbrasil.app.br

# Portainer
curl -I https://portainer.authbrasil.app.br
```

### 4.3. Ver Logs

```bash
# Traefik
docker service logs traefik_traefik --tail 50

# API
docker service logs authbrasil_api --tail 50

# PostgreSQL
docker service logs databases_postgres --tail 50
```

---

## Fase 5: Configuração Pós-Deploy

### 5.1. Conectar pgAdmin ao PostgreSQL

1. Acessar https://pg.authbrasil.app.br
2. Add New Server:
   - Name: AuthBrasil Production
   - Host: postgres
   - Port: 5432
   - Database: authbrasil_cnpj
   - Username: authbrasil_user
   - Password: (do secret db_password)

### 5.2. Importar Dados da Receita (ETL)

```bash
# Criar script ETL em backend/scripts/
# Executar import inicial
docker run --rm \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:SENHA@postgres:5432/authbrasil_cnpj \
  -v /opt/authbrasil/data:/data \
  authbrasil/api:latest \
  python scripts/etl_receita.py
```

### 5.3. Testar CNPJ Real

```bash
curl https://api.authbrasil.app.br/api/v1/cnpj/00000000000191
```

---

## Manutenção

### Atualizar Código

```bash
cd /opt/authbrasil/authbrasil-cnpj
git pull origin main

# Rebuild
cd backend
docker build -t authbrasil/api:latest .

# Migrations (se necessário)
docker run --rm \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:SENHA@postgres:5432/authbrasil_cnpj \
  authbrasil/api:latest \
  alembic upgrade head

# Update com zero downtime
docker service update --image authbrasil/api:latest authbrasil_api
```

### Backup Diário

```bash
# Criar script
nano /opt/authbrasil/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/opt/authbrasil/backups
mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec $(docker ps -q -f name=databases_postgres) \
  pg_dump -U authbrasil_user -Fc authbrasil_cnpj \
  > $BACKUP_DIR/backup_$DATE.dump

# Remover backups antigos (>30 dias)
find $BACKUP_DIR -name "*.dump" -mtime +30 -delete

echo "Backup concluído: $DATE"
```

```bash
chmod +x /opt/authbrasil/backup.sh

# Adicionar no cron (diário às 3h)
crontab -e
0 3 * * * /opt/authbrasil/backup.sh >> /var/log/authbrasil-backup.log 2>&1
```

### Escalar API

```bash
# Aumentar réplicas
docker service scale authbrasil_api=4

# Diminuir réplicas
docker service scale authbrasil_api=1
```

---

## Troubleshooting Rápido

### SSL não funciona
```bash
docker service logs traefik_traefik | grep acme
dig api.authbrasil.app.br
```

### API não conecta no banco
```bash
docker service logs authbrasil_api --tail 100
docker service logs databases_postgres --tail 50
```

### Portainer não acessa
```bash
docker service logs portainer_portainer --tail 50
docker network inspect network_public
```

---

## Checklist Final

- [ ] Cloudflare configurado
- [ ] DNS propagado
- [ ] Swarm inicializado
- [ ] Traefik deployado e SSL funcionando
- [ ] Portainer acessível
- [ ] Databases deployados
- [ ] pgAdmin conectado ao PostgreSQL
- [ ] API deployada
- [ ] Health check retorna 200
- [ ] Documentação acessível
- [ ] Backup configurado
- [ ] Dados da Receita importados

---

**Tempo Estimado:** 2-4 horas (incluindo propagação DNS)

**Status:** Infraestrutura pronta para produção!
