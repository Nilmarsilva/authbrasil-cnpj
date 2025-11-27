# 🚀 Deploy do Sistema ETL na VPS

## 📋 CHECKLIST PRÉ-DEPLOY

- [x] Backend commitado
- [x] Frontend commitado
- [x] Worker corrigido para detectar container dinamicamente
- [ ] Push para repositório
- [ ] Deploy na VPS

---

## 1️⃣ PUSH DO CÓDIGO (Local)

```bash
# Verificar status
git status

# Push para repositório
git push origin main
```

---

## 2️⃣ ATUALIZAR CÓDIGO NA VPS

```bash
# SSH na VPS
ssh root@srv773011

# Ir para o diretório
cd /root/authbrasil-cnpj

# Atualizar código
git pull origin main

# Verificar arquivos novos
ls -la backend/app/etl/worker_v2.py
ls -la backend/app/api/v1/endpoints/etl.py
ls -la backend/alembic/versions/20251127_0730_create_etl_status.py
```

---

## 3️⃣ APLICAR MIGRATION

```bash
# Verificar se tabela existe
docker exec databases_postgres.1.mrttx12uwquw44ho80kojdweo \
  psql -U authbrasil_user -d authbrasil_cnpj \
  -c "\dt etl_status"

# Se NÃO existir, aplicar migration
docker exec authbrasil_api.1.kwdd4khfwu6h43blsejaumh7f \
  alembic upgrade head

# Verificar novamente
docker exec databases_postgres.1.mrttx12uwquw44ho80kojdweo \
  psql -U authbrasil_user -d authbrasil_cnpj \
  -c "\dt etl_status"
```

---

## 4️⃣ CRIAR SUPERUSER

```bash
# Conectar no PostgreSQL
docker exec -it databases_postgres.1.mrttx12uwquw44ho80kojdweo \
  psql -U authbrasil_user -d authbrasil_cnpj
```

Dentro do PostgreSQL:

```sql
-- Ver usuários existentes
SELECT id, email, is_superuser FROM users;

-- Tornar seu usuário superuser (SUBSTITUA O EMAIL!)
UPDATE users SET is_superuser = true WHERE email = 'seu@email.com';

-- Verificar
SELECT id, email, is_superuser FROM users WHERE is_superuser = true;

-- Sair
\q
```

---

## 5️⃣ REBUILD DOS SERVIÇOS

### Backend (API):

```bash
# Ir para o diretório
cd /root/authbrasil-cnpj

# Rebuild da imagem
docker build -t authbrasil/api:latest ./backend

# Atualizar serviço
docker service update --image authbrasil/api:latest authbrasil_api

# Verificar logs
docker service logs -f authbrasil_api --tail 50
```

### Frontend:

```bash
# Rebuild da imagem
docker build -t authbrasil/frontend:latest ./frontend

# Atualizar serviço
docker service update --image authbrasil/frontend:latest authbrasil_frontend

# Verificar logs
docker service logs -f authbrasil_frontend --tail 50
```

---

## 6️⃣ VERIFICAR FUNCIONAMENTO

### Testar API:

```bash
# Verificar endpoint de validação
curl -H "Authorization: Bearer SEU_TOKEN" \
  https://api.authbrasil.app.br/api/v1/etl/validate
```

### Testar Frontend:

```bash
# Abrir no navegador
https://app.authbrasil.app.br/admin/etl

# Fazer login com usuário superuser
# Acessar painel ETL
```

---

## 7️⃣ COMANDOS ÚTEIS

### Ver containers rodando:

```bash
docker ps
```

### Ver serviços:

```bash
docker service ls
```

### Ver logs da API:

```bash
docker service logs -f authbrasil_api --tail 100
```

### Ver logs do ETL (quando rodar):

```bash
tail -f /var/log/etl.log
```

### Verificar espaço em disco:

```bash
df -h
```

### Ver status do PostgreSQL:

```bash
docker exec databases_postgres.1.mrttx12uwquw44ho80kojdweo \
  psql -U authbrasil_user -d authbrasil_cnpj \
  -c "SELECT COUNT(*) FROM estabelecimentos;"
```

---

## ⚠️ TROUBLESHOOTING

### Migration não aplica:

```bash
# Entrar no container da API
docker exec -it authbrasil_api.1.kwdd4khfwu6h43blsejaumh7f bash

# Dentro do container
cd /app
alembic current
alembic upgrade head

# Sair
exit
```

### API não reinicia:

```bash
# Ver logs
docker service logs authbrasil_api --tail 100

# Force update
docker service update --force authbrasil_api
```

### Frontend não atualiza:

```bash
# Limpar cache do navegador
# Ou forçar rebuild:
docker service update --force authbrasil_frontend
```

---

## 📊 ORDEM DE EXECUÇÃO

1. ✅ Push código (local)
2. ✅ Git pull (VPS)
3. ✅ Aplicar migration
4. ✅ Criar superuser
5. ✅ Rebuild backend
6. ✅ Rebuild frontend
7. ✅ Testar

---

## 🎯 RESULTADO ESPERADO

- ✅ Endpoint `/api/v1/etl/validate` funcionando
- ✅ Endpoint `/api/v1/etl/start` funcionando
- ✅ Endpoint `/api/v1/etl/status` funcionando
- ✅ Página `/admin/etl` acessível
- ✅ Painel mostrando status
- ✅ Botão "Iniciar Atualização" visível
