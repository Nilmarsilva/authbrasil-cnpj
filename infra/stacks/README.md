# Stacks de Infraestrutura

Estrutura organizada por serviços separados para deploy na VPS.

## Estrutura de Pastas

```
stacks/
├── traefik/              # Reverse Proxy + SSL
│   ├── config/          # Configurações dinâmicas
│   └── logs/            # Logs do Traefik
├── portainer/           # Gerenciamento de containers
├── databases/           # PostgreSQL + Redis + pgAdmin
├── authbrasil-cnpj/     # API FastAPI do projeto
├── monitoring/          # Grafana + Prometheus (futuro)
└── backups/             # Scripts de backup
```

## Ordem de Deploy

### 1. Traefik (primeiro)
- Cria a rede `traefik_public`
- Gerencia SSL via Cloudflare
- Roteia todo tráfego HTTPS

**Arquivos necessários:**
- `docker-compose.yml`
- `traefik.yml` (configuração estática)
- `config/dynamic.yml` (middlewares, headers)
- `.env` (Cloudflare credentials)

### 2. Portainer (segundo)
- Interface web para gerenciar containers
- Acesso via `portainer.authbrasil.app.br`

**Arquivos necessários:**
- `docker-compose.yml`

### 3. Databases (terceiro)
- PostgreSQL 16
- Redis 7
- pgAdmin 4

**Arquivos necessários:**
- `docker-compose.yml`
- `.env` (senhas dos bancos)

### 4. AuthBrasil CNPJ (quarto)
- API FastAPI
- App Next.js (futuro)

**Arquivos necessários:**
- `docker-compose.yml`
- `.env.production` (variáveis da aplicação)

### 5. Monitoring (opcional)
- Grafana + Prometheus
- Métricas e dashboards

## Subdomínios Necessários (Cloudflare)

```
Tipo    Nome        Valor                    Proxy
A       server      89.116.186.161          Não
CNAME   traefik     server.authbrasil.app.br  Não
CNAME   portainer   server.authbrasil.app.br  Não
CNAME   pg          server.authbrasil.app.br  Não
CNAME   api         server.authbrasil.app.br  Sim (CDN)
CNAME   app         server.authbrasil.app.br  Sim (CDN)
```

## Rede Docker

Todas as stacks compartilham a rede `traefik_public`:

```bash
docker network create traefik_public
```

## Como Usar

Cada stack é independente e pode ser gerenciada separadamente:

```bash
# Iniciar uma stack
cd infra/stacks/traefik
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Restart
docker-compose restart
```

## Benefícios da Separação

1. **Isolamento** - Cada serviço tem seu docker-compose
2. **Manutenção** - Atualizar um não afeta outros
3. **Organização** - Fácil localizar configurações
4. **Backup** - Backup seletivo por stack
5. **Escalabilidade** - Adicionar novos serviços facilmente

## Próximos Passos

1. Criar configurações do Traefik
2. Configurar Cloudflare DNS
3. Deploy ordenado das stacks
4. Testar acessos aos subdomínios
5. Configurar backups automáticos

---

**Nota:** Esta estrutura foi criada para recomeçar a VPS do zero, sem senhas ou configurações antigas.
