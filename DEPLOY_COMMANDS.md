# 🚀 Comandos de Deploy - AuthBrasil CNPJ

## 📋 SETUP INICIAL (Executar apenas 1 vez)

### 1. Configurar Git na VPS

```bash
# Configurar Git
cd /root
git config --global user.name "Deploy Bot"
git config --global user.email "deploy@authbrasil.app.br"

# Clonar repositório com token
cd /root
mkdir -p infra
cd infra
git init
git remote add origin https://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@github.com/Nilmarsilva/authbrasil-cnpj.git
git fetch origin main
git checkout -b main origin/main

# Reorganizar pastas
cd /root
cp -r infra/backend /root/
cp -r infra/infra /root/
cp -r infra/frontend /root/
```

### 2. Criar Docker Secrets (apenas 1 vez)

```bash
# Senhas do banco
echo "xWxt64YrzAFWc3ylNHrAbMoF0Z8h_b6kCQT4aX8sdgM" | docker secret create db_password -

# Senha do pgAdmin
echo "admin123secure" | docker secret create pgadmin_password -

# Senha do Redis
echo "vezEgze0KAtTuvn20ITwme_Ud8--aXdB" | docker secret create redis_password -
```

### 3. Copiar script de deploy

```bash
# Copiar script de deploy
cp /root/infra_old/deploy-backend.sh /root/
chmod +x /root/deploy-backend.sh
```

---

## 🔄 DEPLOY COMPLETO (Executar após cada push)

### Opção 1: Deploy Automatizado Completo

```bash
# Script único para deploy de tudo
cd /root && bash deploy-all.sh
```

### Opção 2: Deploy Manual Passo a Passo

```bash
# 1. Puxar código atualizado
cd /root/infra
git pull origin main

# 2. Atualizar backend
cd /root
cp -r /root/infra/backend/* /root/backend/

# 3. Build da imagem
cd /root/backend
docker build -t authbrasil/api:latest .

# 4. Migrations
docker run --rm --user root \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:xWxt64YrzAFWc3ylNHrAbMoF0Z8h_b6kCQT4aX8sdgM@postgres:5432/authbrasil_cnpj \
  -e SECRET_KEY=2dedddaff60c04b3fa767ebc720a2dec4c94969be65cb9e4ff8f76e8a9b7e142 \
  -e JWT_SECRET_KEY=65248bd67bca837ae6e003075ce97a9bed277a8324eb1eb86e5b9160ad2d6c5e \
  -e REDIS_URL=redis://:vezEgze0KAtTuvn20ITwme_Ud8--aXdB@redis:6379/0 \
  -e STRIPE_SECRET_KEY=sk_test_temp \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_temp \
  -e STRIPE_WEBHOOK_SECRET=whsec_temp \
  -e SENDGRID_API_KEY=SG_temp \
  authbrasil/api:latest python -m alembic upgrade head

# 5. Update do serviço
docker service update --force authbrasil_api

# 6. Aguardar
sleep 10

# 7. Verificar status
docker service ls

# 8. Ver logs
docker service logs authbrasil_api --tail 30
```

---

## 📦 DEPLOY APENAS BACKEND

```bash
cd /root/infra && git pull origin main && \
cp -r /root/infra/backend/* /root/backend/ && \
cd /root/backend && \
docker build -t authbrasil/api:latest . && \
docker run --rm --user root --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:xWxt64YrzAFWc3ylNHrAbMoF0Z8h_b6kCQT4aX8sdgM@postgres:5432/authbrasil_cnpj \
  -e SECRET_KEY=2dedddaff60c04b3fa767ebc720a2dec4c94969be65cb9e4ff8f76e8a9b7e142 \
  -e JWT_SECRET_KEY=65248bd67bca837ae6e003075ce97a9bed277a8324eb1eb86e5b9160ad2d6c5e \
  -e REDIS_URL=redis://:vezEgze0KAtTuvn20ITwme_Ud8--aXdB@redis:6379/0 \
  -e STRIPE_SECRET_KEY=sk_test_temp \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_temp \
  -e STRIPE_WEBHOOK_SECRET=whsec_temp \
  -e SENDGRID_API_KEY=SG_temp \
  authbrasil/api:latest python -m alembic upgrade head && \
docker service update --force authbrasil_api && \
sleep 10 && \
docker service ls
```

---

## 🌐 DEPLOY APENAS FRONTEND (quando pronto)

```bash
cd /root/infra && git pull origin main && \
cp -r /root/infra/frontend/* /root/frontend/ && \
cd /root/frontend && \
docker build -t authbrasil/frontend:latest . && \
docker service update --force frontend_web && \
docker service ls
```

---

## 🗄️ DEPLOY DATABASES

```bash
cd /root/infra && git pull origin main && \
cp -r /root/infra/infra/stacks/databases/* /root/infra/stacks/databases/ && \
cd /root/infra/stacks/databases && \
docker stack deploy -c docker-compose.yml databases && \
sleep 10 && \
docker service ls
```

---

## 🔍 COMANDOS DE VERIFICAÇÃO

### Ver status de todos os serviços

```bash
docker service ls
```

### Ver logs do backend

```bash
docker service logs authbrasil_api --tail 50 -f
```

### Ver logs do Redis

```bash
docker service logs databases_redis --tail 30
```

### Ver logs do PostgreSQL

```bash
docker service logs databases_postgres --tail 30
```

### Testar API

```bash
curl https://api.authbrasil.app.br/api/v1/health
```

### Ver uso de recursos

```bash
docker stats --no-stream
```

---

## 🧹 COMANDOS DE LIMPEZA

### Limpar containers parados

```bash
docker container prune -f
```

### Limpar imagens não utilizadas

```bash
docker image prune -f
```

### Limpar volumes órfãos

```bash
docker volume prune -f
```

### Limpeza completa

```bash
docker system prune -af --volumes
```

---

## 🚨 TROUBLESHOOTING

### Service não sobe (0/1 replicas)

```bash
# Ver o que está acontecendo
docker service ps authbrasil_api --no-trunc

# Ver logs com mais detalhes
docker service logs authbrasil_api --tail 100
```

### Reiniciar um serviço

```bash
docker service update --force SERVICE_NAME
```

### Remover e recriar uma stack

```bash
docker stack rm authbrasil
sleep 10
docker stack deploy -c /root/docker-compose.backend.yml authbrasil
```

### Verificar secrets

```bash
docker secret ls
```

### Recriar um secret (se necessário)

```bash
# Remover
docker secret rm redis_password

# Recriar
echo "vezEgze0KAtTuvn20ITwme_Ud8--aXdB" | docker secret create redis_password -
```

---

## 📝 WORKFLOW RECOMENDADO

### No PC (desenvolvimento):

```bash
# 1. Fazer alterações
# 2. Testar localmente
git add .
git commit -m "feat: sua alteração"
git push origin main
```

### Na VPS (deploy):

```bash
# Comando único para deploy completo
cd /root/infra && git pull origin main && \
cp -r /root/infra/backend/* /root/backend/ && \
cd /root/backend && \
docker build -t authbrasil/api:latest . && \
docker run --rm --user root --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:xWxt64YrzAFWc3ylNHrAbMoF0Z8h_b6kCQT4aX8sdgM@postgres:5432/authbrasil_cnpj \
  -e SECRET_KEY=2dedddaff60c04b3fa767ebc720a2dec4c94969be65cb9e4ff8f76e8a9b7e142 \
  -e JWT_SECRET_KEY=65248bd67bca837ae6e003075ce97a9bed277a8324eb1eb86e5b9160ad2d6c5e \
  -e REDIS_URL=redis://:vezEgze0KAtTuvn20ITwme_Ud8--aXdB@redis:6379/0 \
  -e STRIPE_SECRET_KEY=sk_test_temp \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_temp \
  -e STRIPE_WEBHOOK_SECRET=whsec_temp \
  -e SENDGRID_API_KEY=SG_temp \
  authbrasil/api:latest python -m alembic upgrade head && \
docker service update --force authbrasil_api && \
docker service logs authbrasil_api --tail 30 -f
```

---

## ✅ CHECKLIST PÓS-DEPLOY

- [ ] `docker service ls` - Todos os serviços 1/1 ou 2/2?
- [ ] `curl https://api.authbrasil.app.br/api/v1/health` - API responde 200?
- [ ] `curl https://api.authbrasil.app.br/api/v1/docs` - Swagger abre?
- [ ] Portainer mostra tudo verde?
- [ ] Logs sem erros?

---

**🎯 DICA:** Salve este arquivo e sempre consulte quando for fazer deploy!
