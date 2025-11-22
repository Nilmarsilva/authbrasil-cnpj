# 🚀 Deploy do Frontend - AuthBrasil CNPJ

## 📋 Instruções para Deploy na VPS

### 1. Preparar ambiente na VPS

```bash
# SSH na VPS
ssh root@SEU_IP

# Criar diretório do frontend
mkdir -p /root/frontend
```

### 2. Copiar código do frontend

```bash
# Ir para o diretório infra e puxar código
cd /root/infra
git pull origin main

# Copiar frontend
cp -r /root/infra/frontend/* /root/frontend/

# Verificar se copiou
ls -la /root/frontend/
```

### 3. Build da imagem Docker

```bash
cd /root/frontend

# Build da imagem
docker build -t authbrasil/frontend:latest .
```

### 4. Criar Docker Swarm Service

```bash
# Criar service do frontend
docker service create \
  --name authbrasil_frontend \
  --replicas 2 \
  --network authbrasil_network \
  --publish 3000:3000 \
  --env NEXT_PUBLIC_API_URL=https://api.authbrasil.app.br/api/v1 \
  authbrasil/frontend:latest

# Verificar se está rodando
docker service ps authbrasil_frontend
```

### 5. Atualizar Nginx (se necessário)

Se quiser expor em um domínio (ex: app.authbrasil.com.br):

```nginx
server {
    listen 80;
    server_name app.authbrasil.com.br;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔄 Atualizar Frontend (após mudanças)

```bash
cd /root/infra
git pull origin main

cp -r /root/infra/frontend/* /root/frontend/

cd /root/frontend
docker build -t authbrasil/frontend:latest .

docker service update --force --image authbrasil/frontend:latest authbrasil_frontend
```

---

## ✅ Verificar se está funcionando

```bash
# Ver logs
docker service logs authbrasil_frontend -f

# Testar localmente
curl http://localhost:3000

# Ver services rodando
docker service ls
```

---

## 🔧 Troubleshooting

### Build demorado?
O Next.js pode demorar 2-5 minutos para fazer build. É normal!

### Erro de memória?
Aumentar swap ou usar máquina com mais RAM

### Frontend não conecta no backend?
Verificar se `NEXT_PUBLIC_API_URL` está correto
