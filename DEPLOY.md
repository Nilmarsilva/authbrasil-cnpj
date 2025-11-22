# Guia de Deploy - Produção

Deploy do AuthBrasil CNPJ na VPS com Traefik + Portainer.

## Pré-requisitos na VPS

- Docker instalado
- Docker Compose instalado
- Traefik configurado e rodando
- Portainer configurado (opcional)
- Rede `traefik_public` criada

### Verificar Rede Traefik

```bash
docker network ls | grep traefik
```

Se não existir, criar:
```bash
docker network create traefik_public
```

---

## Passo 1: Preparar VPS

### 1.1. Conectar na VPS

```bash
ssh usuario@89.116.186.161
```

### 1.2. Criar Estrutura de Diretórios

```bash
sudo mkdir -p /opt/authbrasil
cd /opt/authbrasil
```

### 1.3. Clonar Repositório

```bash
git clone https://github.com/Nilmarsilva/authbrasil-cnpj.git
cd authbrasil-cnpj
```

---

## Passo 2: Configurar Variáveis de Ambiente

### 2.1. Backend

```bash
cd /opt/authbrasil/authbrasil-cnpj/backend
cp .env.production.example .env.production

# Editar com variáveis reais
nano .env.production
```

**Configurações críticas:**
- `SECRET_KEY` - Gerar: `openssl rand -hex 32`
- `JWT_SECRET_KEY` - Gerar: `openssl rand -hex 32`
- `DATABASE_URL` - Usar nome do serviço docker `postgres`
- `STRIPE_SECRET_KEY` - Chaves de produção do Stripe
- `SENDGRID_API_KEY` - API key do SendGrid

### 2.2. Docker Compose

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/docker
cp .env.example .env

# Editar com senhas fortes
nano .env
```

**Gerar senhas fortes:**
```bash
# PostgreSQL password
openssl rand -base64 32

# Redis password
openssl rand -base64 32

# pgAdmin password
openssl rand -base64 24
```

---

## Passo 3: Build e Deploy

### 3.1. Build da Imagem

```bash
cd /opt/authbrasil/authbrasil-cnpj/backend
docker build -t authbrasil/api:latest .
```

### 3.2. Executar Migrations

```bash
# Criar container temporário para migrations
docker run --rm \
  --network authbrasil_network \
  --env-file .env.production \
  authbrasil/api:latest \
  alembic upgrade head
```

### 3.3. Iniciar Serviços

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/docker
docker-compose -f docker-compose.prod.yml up -d
```

### 3.4. Verificar Logs

```bash
docker-compose -f docker-compose.prod.yml logs -f api
```

---

## Passo 4: Configurar Cloudflare (Recomendado)

### 4.1. Adicionar Domínios

1. Acessar https://dash.cloudflare.com
2. Adicionar `authbrasil.app.br`
3. Copiar nameservers fornecidos

### 4.2. Atualizar Nameservers no Registro.br

1. Acessar https://registro.br
2. Login com certificado digital ou senha
3. Editar domínio `authbrasil.app.br`
4. Alterar nameservers para os da Cloudflare
5. Aguardar propagação (até 24h, geralmente < 1h)

### 4.3. Configurar DNS no Cloudflare

**Records:**
```
Tipo    Nome        Valor                   Proxy   TTL
A       server      89.116.186.161          Não     Auto
CNAME   api         server.authbrasil.app.br  Sim   Auto
CNAME   app         server.authbrasil.app.br  Sim   Auto
CNAME   pg          server.authbrasil.app.br  Não   Auto
CNAME   portainer   server.authbrasil.app.br  Não   Auto
```

**Configurações SSL/TLS:**
- Modo: Full (strict)
- Edge Certificates: Automatic HTTPS Rewrites ON
- Always Use HTTPS: ON
- Minimum TLS Version: 1.2

**Configurações Security:**
- Security Level: Medium
- Challenge Passage: 30 minutes
- Browser Integrity Check: ON

**Configurações Speed:**
- Auto Minify: JS, CSS, HTML
- Brotli: ON
- HTTP/3: ON
- Rocket Loader: ON (testar performance)

**Firewall Rules (opcional):**
```
Rule 1: Block bots
(cf.bot_management.score lt 30) then Block

Rule 2: Rate limit API
(http.host eq "api.authbrasil.app.br" and rate(5m) > 300) then Challenge
```

---

## Passo 5: Verificar Funcionamento

### 5.1. Testar Endpoints

```bash
# Health check
curl https://api.authbrasil.app.br/api/v1/health

# Documentação
curl https://api.authbrasil.app.br/api/v1/docs
```

### 5.2. Acessar Serviços

- **API:** https://api.authbrasil.app.br
- **API Docs:** https://api.authbrasil.app.br/api/v1/docs
- **pgAdmin:** https://pg.authbrasil.app.br
- **Portainer:** https://portainer.authbrasil.app.br

### 5.3. Verificar Logs

```bash
# API logs
docker logs -f authbrasil_api

# PostgreSQL logs
docker logs -f authbrasil_postgres

# Redis logs
docker logs -f authbrasil_redis
```

---

## Passo 6: Backup Automático

### 6.1. Criar Script de Backup

```bash
sudo nano /opt/authbrasil/backup.sh
```

```bash
#!/bin/bash
cd /opt/authbrasil/authbrasil-cnpj/infra/docker
docker-compose -f docker-compose.prod.yml --profile backup run --rm backup
```

```bash
sudo chmod +x /opt/authbrasil/backup.sh
```

### 6.2. Configurar Cron (backup diário às 3h)

```bash
sudo crontab -e
```

Adicionar:
```
0 3 * * * /opt/authbrasil/backup.sh >> /var/log/authbrasil-backup.log 2>&1
```

### 6.3. Testar Backup Manual

```bash
/opt/authbrasil/backup.sh
```

Verificar arquivo criado em `/opt/authbrasil/authbrasil-cnpj/infra/docker/backups/`

---

## Passo 7: Monitoramento

### 7.1. Health Check Script

```bash
sudo nano /opt/authbrasil/healthcheck.sh
```

```bash
#!/bin/bash
ENDPOINT="https://api.authbrasil.app.br/api/v1/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)

if [ $RESPONSE -eq 200 ]; then
    echo "[OK] API está saudável"
    exit 0
else
    echo "[ERRO] API retornou: $RESPONSE"
    # Opcional: enviar notificação
    exit 1
fi
```

```bash
sudo chmod +x /opt/authbrasil/healthcheck.sh
```

### 7.2. Monitoramento via Cron (a cada 5 min)

```bash
*/5 * * * * /opt/authbrasil/healthcheck.sh >> /var/log/authbrasil-health.log 2>&1
```

---

## Comandos Úteis

### Gerenciamento de Containers

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/docker

# Ver status
docker-compose -f docker-compose.prod.yml ps

# Parar serviços
docker-compose -f docker-compose.prod.yml down

# Reiniciar serviço específico
docker-compose -f docker-compose.prod.yml restart api

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f api

# Executar comando no container
docker exec -it authbrasil_api bash

# Ver uso de recursos
docker stats
```

### Atualização da Aplicação

```bash
cd /opt/authbrasil/authbrasil-cnpj

# Pull latest
git pull origin main

# Rebuild
cd backend
docker build -t authbrasil/api:latest .

# Migrations
docker exec authbrasil_api alembic upgrade head

# Restart
cd ../infra/docker
docker-compose -f docker-compose.prod.yml restart api
```

### Restore de Backup

```bash
# Listar backups
ls -lh /opt/authbrasil/authbrasil-cnpj/infra/docker/backups/

# Restore específico
docker exec -i authbrasil_postgres pg_restore \
  -U authbrasil_user \
  -d authbrasil_cnpj \
  -c \
  < /backups/backup_20241122_030000.dump
```

---

## Segurança - Checklist

- [ ] Variáveis de ambiente com senhas fortes
- [ ] Firewall UFW configurado
- [ ] SSH apenas com chave pública
- [ ] Fail2ban instalado e configurado
- [ ] Cloudflare WAF ativo
- [ ] pgAdmin com IP whitelist
- [ ] Backup automático funcionando
- [ ] Monitoramento de saúde ativo
- [ ] SSL/TLS configurado (via Traefik)
- [ ] Rate limiting configurado

---

## Troubleshooting

### API não inicia

```bash
# Ver logs detalhados
docker logs authbrasil_api --tail 100

# Verificar variáveis de ambiente
docker exec authbrasil_api env | grep -i database

# Testar conexão com banco
docker exec authbrasil_api pg_isready -h postgres -U authbrasil_user
```

### Erro de conexão com PostgreSQL

```bash
# Verificar se PostgreSQL está rodando
docker ps | grep postgres

# Verificar logs do PostgreSQL
docker logs authbrasil_postgres --tail 50

# Testar conexão
docker exec authbrasil_postgres psql -U authbrasil_user -d authbrasil_cnpj -c "SELECT 1;"
```

### Traefik não roteia

```bash
# Verificar labels do container
docker inspect authbrasil_api | grep -A 20 Labels

# Verificar rede
docker network inspect traefik_public

# Ver logs do Traefik
docker logs traefik --tail 100
```

### SSL não funciona

```bash
# Verificar certificados no Traefik
docker exec traefik cat /acme.json

# Forçar renovação (se necessário)
docker restart traefik
```

---

## Rollback

Se algo der errado:

```bash
# Parar containers
docker-compose -f docker-compose.prod.yml down

# Restore backup
docker exec -i authbrasil_postgres pg_restore ...

# Voltar versão do código
git checkout COMMIT_ANTERIOR

# Rebuild
docker build -t authbrasil/api:latest backend/

# Restart
docker-compose -f docker-compose.prod.yml up -d
```

---

**Última atualização:** 22/11/2024  
**Ambiente:** Produção (89.116.186.161)
