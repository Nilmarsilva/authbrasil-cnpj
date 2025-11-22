# Infraestrutura de Produção - AuthBrasil CNPJ

## Domínios Disponíveis

### authbrasil.com.br
**Uso:** Landing page e marketing
- Site institucional
- Páginas de vendas
- Blog (futuro)
- Pode ser hospedado em Vercel/Netlify (Next.js estático) ou na VPS

### authbrasil.app.br
**Uso:** Infraestrutura de aplicações
- Todos os serviços rodando na VPS
- Gestão centralizada via Traefik + Portainer

---

## Arquitetura Proposta para AuthBrasil CNPJ

### Subdomínios (authbrasil.app.br)

| Subdomínio | Serviço | Container | Porta Interna |
|------------|---------|-----------|---------------|
| `api.authbrasil.app.br` | Backend FastAPI | authbrasil-api | 8000 |
| `app.authbrasil.app.br` | Dashboard Next.js | authbrasil-app | 3000 |
| `pg.authbrasil.app.br` | pgAdmin | authbrasil-pgadmin | 80 |
| `portainer.authbrasil.app.br` | Portainer | portainer | 9000 |

### Infraestrutura Base (Docker)

```
VPS (89.116.186.161)
├── Traefik (reverse proxy + SSL)
├── Portainer (gestão)
├── PostgreSQL (dados)
├── Redis (cache)
├── authbrasil-api (FastAPI)
└── authbrasil-app (Next.js)
```

---

## Recomendação: Migrar DNS para Cloudflare

### Vantagens

**1. Segurança**
- WAF (Web Application Firewall)
- Proteção DDoS automática
- Rate limiting global
- SSL/TLS gerenciado

**2. Performance**
- CDN global gratuito
- Cache de assets estáticos
- Compressão automática (Brotli)
- HTTP/3 e QUIC

**3. Funcionalidades**
- Firewall rules customizáveis
- Page Rules para otimização
- Analytics avançado
- Workers (edge computing se necessário)

**4. Custo**
- Plano Free já resolve 90% das necessidades
- Upgrade para Pro (US$ 20/mês) se precisar mais

### Configuração Cloudflare

#### Passo 1: Adicionar Domínios
1. Criar conta: https://dash.cloudflare.com/sign-up
2. Adicionar `authbrasil.com.br`
3. Adicionar `authbrasil.app.br`

#### Passo 2: Atualizar Nameservers no Registro.br
Cloudflare fornecerá nameservers como:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

Atualizar em: https://registro.br/

#### Passo 3: Configurar DNS no Cloudflare

**authbrasil.app.br:**
```
Tipo    Nome        Valor                   Proxy   TTL
A       server      89.116.186.161          Sim     Auto
CNAME   api         server.authbrasil.app.br  Sim   Auto
CNAME   app         server.authbrasil.app.br  Sim   Auto
CNAME   pg          server.authbrasil.app.br  Não   Auto
CNAME   portainer   server.authbrasil.app.br  Não   Auto
```

**Importante:**
- **Proxy ON (laranja)** para `api` e `app` → CDN + proteção
- **Proxy OFF (cinza)** para `pg` e `portainer` → Acesso direto (evita problemas WebSocket)

#### Passo 4: SSL/TLS
- **Modo:** Full (strict)
- Origem: Traefik gerará certificados Let's Encrypt
- Cloudflare ↔ Traefik: HTTPS

---

## Docker Compose - Produção

### Estrutura de Deploy

```
/opt/authbrasil/
├── docker-compose.yml
├── traefik/
│   ├── traefik.yml
│   └── acme.json
├── postgres/
│   └── data/
├── redis/
│   └── data/
├── api/
│   ├── Dockerfile
│   └── .env
└── app/
    ├── Dockerfile
    └── .env.production
```

### docker-compose.yml (Produção)

```yaml
version: '3.8'

networks:
  authbrasil_network:
    external: true
  traefik_public:
    external: true

volumes:
  postgres_data:
  redis_data:

services:
  postgres:
    image: postgres:16-alpine
    container_name: authbrasil_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: authbrasil_cnpj
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - authbrasil_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 30s
      timeout: 5s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: authbrasil_redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - authbrasil_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 3s
      retries: 3

  api:
    build: ./api
    container_name: authbrasil_api
    restart: unless-stopped
    env_file:
      - ./api/.env
    depends_on:
      - postgres
      - redis
    networks:
      - authbrasil_network
      - traefik_public
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.authbrasil-api.rule=Host(`api.authbrasil.app.br`)"
      - "traefik.http.routers.authbrasil-api.entrypoints=websecure"
      - "traefik.http.routers.authbrasil-api.tls.certresolver=letsencrypt"
      - "traefik.http.services.authbrasil-api.loadbalancer.server.port=8000"
      # CORS headers
      - "traefik.http.middlewares.authbrasil-cors.headers.accesscontrolallowmethods=GET,POST,PUT,DELETE,OPTIONS"
      - "traefik.http.middlewares.authbrasil-cors.headers.accesscontrolalloworiginlist=https://app.authbrasil.app.br,https://authbrasil.com.br"
      - "traefik.http.middlewares.authbrasil-cors.headers.accesscontrolallowheaders=*"
      - "traefik.http.routers.authbrasil-api.middlewares=authbrasil-cors"

  app:
    build: ./app
    container_name: authbrasil_app
    restart: unless-stopped
    env_file:
      - ./app/.env.production
    networks:
      - traefik_public
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.authbrasil-app.rule=Host(`app.authbrasil.app.br`)"
      - "traefik.http.routers.authbrasil-app.entrypoints=websecure"
      - "traefik.http.routers.authbrasil-app.tls.certresolver=letsencrypt"
      - "traefik.http.services.authbrasil-app.loadbalancer.server.port=3000"

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: authbrasil_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD}
    networks:
      - authbrasil_network
      - traefik_public
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.authbrasil-pgadmin.rule=Host(`pg.authbrasil.app.br`)"
      - "traefik.http.routers.authbrasil-pgadmin.entrypoints=websecure"
      - "traefik.http.routers.authbrasil-pgadmin.tls.certresolver=letsencrypt"
      - "traefik.http.services.authbrasil-pgadmin.loadbalancer.server.port=80"
      # IP Whitelist (opcional - adicionar seus IPs)
      - "traefik.http.middlewares.pgadmin-ipwhitelist.ipwhitelist.sourcerange=0.0.0.0/0"
```

---

## Traefik Configuration

### traefik.yml (se ainda não tiver)

```yaml
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt

certificatesResolvers:
  letsencrypt:
    acme:
      email: seu-email@authbrasil.com.br
      storage: /acme.json
      httpChallenge:
        entryPoint: web

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
    network: traefik_public

log:
  level: INFO
  filePath: /var/log/traefik/traefik.log

accessLog:
  filePath: /var/log/traefik/access.log
```

---

## Decisão: Limpar VPS ou Manter Estrutura?

### Opção 1: Manter Traefik + Portainer (RECOMENDADO)
**Vantagens:**
- Traefik já gerencia SSL e roteamento
- Portainer facilita gestão
- Outros projetos podem coexistir
- Zero downtime para outros serviços

**Ação:**
- Manter containers existentes
- Adicionar AuthBrasil CNPJ à rede do Traefik
- Usar labels do Traefik para roteamento

### Opção 2: Limpar Tudo
**Vantagens:**
- Setup limpo e documentado desde zero
- Total controle sobre configuração

**Desvantagens:**
- Perder configurações existentes
- Reconfigurar tudo
- Potencial downtime

---

## Recomendação Final

### Infraestrutura
1. **Manter:** Traefik + Portainer
2. **Migrar DNS:** Para Cloudflare
3. **Adicionar:** Containers do AuthBrasil CNPJ

### Domínios
- **authbrasil.com.br** → Landing page (Vercel ou VPS)
- **api.authbrasil.app.br** → FastAPI
- **app.authbrasil.app.br** → Dashboard Next.js
- **pg.authbrasil.app.br** → pgAdmin (acesso restrito)
- **portainer.authbrasil.app.br** → Portainer (acesso restrito)

### Segurança
- Cloudflare WAF ativado
- Rate limiting configurado
- IP whitelist para pgAdmin e Portainer
- Secrets em variáveis de ambiente
- Backup automático PostgreSQL

### Próximos Passos
1. Decidir sobre Cloudflare
2. Criar Dockerfiles para produção
3. Configurar CI/CD (GitHub Actions → VPS)
4. Testar deploy completo

---

## Custos Estimados

| Item | Valor | Observação |
|------|-------|------------|
| VPS | Já possui | - |
| Domínios | Já possui | - |
| Cloudflare | R$ 0 (Free) | Upgrade Pro R$ 100/mês (opcional) |
| Backup Storage | ~R$ 20/mês | Wasabi ou similar (opcional) |
| **Total** | **~R$ 0-20/mês** | Além da VPS existente |

---

**Última atualização:** 22/11/2024
