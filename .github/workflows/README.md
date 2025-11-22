# GitHub Actions - AuthBrasil CNPJ

Automação completa de deploy via GitHub Actions.

## Workflows Disponíveis

### 1. Setup VPS (Primeira Vez)
**Arquivo:** `setup-vps.yml`

**O que faz:**
- Inicializa Docker Swarm
- Cria redes e volumes
- Cria secrets
- Clona repositório
- Deploya TODAS as stacks automaticamente
- Verifica se tudo está funcionando

**Quando usar:** Primeira vez ou após resetar VPS

**Como executar:**
1. GitHub → Actions → "Setup VPS (Primeira Vez)"
2. Run workflow → Run workflow
3. Aguardar ~5-10 minutos

### 2. Deploy Production
**Arquivo:** `deploy-production.yml`

**O que faz:**
- Atualiza código na VPS
- Deploy/update de stacks específicas
- Ver logs
- Ver status

**Opções:**
- **Stack:** all, traefik, portainer, databases, authbrasil
- **Ação:** deploy, update, logs, status

**Como executar:**
1. GitHub → Actions → "Deploy Production"
2. Run workflow
3. Escolher stack e ação
4. Run workflow

## Configurar Secrets no GitHub

**Obrigatório antes de usar!**

GitHub → Settings → Secrets and variables → Actions → New repository secret

### Secrets Necessários

| Nome | Valor | Exemplo |
|------|-------|---------|
| `VPS_HOST` | IP da VPS | `89.116.186.161` |
| `VPS_USER` | Usuário SSH | `root` ou `ubuntu` |
| `VPS_SSH_KEY` | Chave privada SSH | Conteúdo do arquivo `~/.ssh/id_rsa` |
| `DB_PASSWORD` | Senha PostgreSQL | Gerar com: `openssl rand -base64 32` |
| `PGADMIN_PASSWORD` | Senha pgAdmin | Gerar com: `openssl rand -base64 24` |
| `REDIS_PASSWORD` | Senha Redis | Gerar com: `openssl rand -base64 24` |
| `SECRET_KEY` | Secret Key API | Gerar com: `openssl rand -hex 32` |
| `JWT_SECRET_KEY` | JWT Secret | Gerar com: `openssl rand -hex 32` |
| `STRIPE_SECRET_KEY` | Stripe API Key | `sk_live_...` |
| `STRIPE_PUBLISHABLE_KEY` | Stripe Public Key | `pk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | Stripe Webhook | `whsec_...` |
| `SENDGRID_API_KEY` | SendGrid API | `SG.xxx...` |

## Como Obter a Chave SSH

### Windows (PowerShell)

```powershell
# Ver conteúdo da chave
Get-Content ~\.ssh\id_rsa

# Copiar para clipboard
Get-Content ~\.ssh\id_rsa | clip
```

### Linux/Mac

```bash
# Ver conteúdo
cat ~/.ssh/id_rsa

# Copiar para clipboard (Mac)
cat ~/.ssh/id_rsa | pbcopy

# Copiar para clipboard (Linux)
cat ~/.ssh/id_rsa | xclip -selection clipboard
```

**Importante:** Copiar TUDO, incluindo:
```
-----BEGIN OPENSSH PRIVATE KEY-----
...conteúdo...
-----END OPENSSH PRIVATE KEY-----
```

## Gerar Senhas Fortes

### Windows (PowerShell)

```powershell
# Senha de 32 caracteres (PostgreSQL, Redis)
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

# Ou usar Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Linux/Mac

```bash
# PostgreSQL
openssl rand -base64 32

# Redis
openssl rand -base64 24

# Secret Keys
openssl rand -hex 32
```

## Passo a Passo Completo

### 1. Gerar Senhas

```bash
# Gerar TODAS as senhas de uma vez
echo "DB_PASSWORD=$(openssl rand -base64 32)"
echo "PGADMIN_PASSWORD=$(openssl rand -base64 24)"
echo "REDIS_PASSWORD=$(openssl rand -base64 24)"
echo "SECRET_KEY=$(openssl rand -hex 32)"
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)"
```

Copiar os valores gerados.

### 2. Configurar Secrets GitHub

1. Acessar: https://github.com/Nilmarsilva/authbrasil-cnpj/settings/secrets/actions
2. Clicar "New repository secret"
3. Adicionar cada secret (nome e valor)
4. Repetir para todos os 12 secrets

### 3. Executar Setup

1. GitHub → Actions
2. "Setup VPS (Primeira Vez)"
3. Run workflow → main → Run workflow
4. Aguardar conclusão (~5-10 min)

### 4. Verificar

Acessar:
- https://api.authbrasil.app.br/api/v1/health
- https://portainer.authbrasil.app.br
- https://pg.authbrasil.app.br

## Uso Diário

### Atualizar API após mudanças no código

```
1. Fazer push para main
2. GitHub → Actions → "Deploy Production"
3. Stack: authbrasil
4. Action: update
5. Run workflow
```

### Ver logs da API

```
1. GitHub → Actions → "Deploy Production"
2. Stack: authbrasil
3. Action: logs
4. Run workflow
5. Ver output do workflow
```

### Ver status geral

```
1. GitHub → Actions → "Deploy Production"
2. Stack: all
3. Action: status
4. Run workflow
```

## Troubleshooting

### Erro: "Permission denied (publickey)"

- Verificar se `VPS_SSH_KEY` está correto
- Verificar se chave pública está em `~/.ssh/authorized_keys` na VPS

### Erro: "Could not resolve hostname"

- Verificar se `VPS_HOST` está correto (IP da VPS)

### Erro: "docker: command not found"

- Docker não instalado na VPS
- Instalar: `curl -fsSL https://get.docker.com | sh`

### Secret não encontrado

- Verificar nome do secret (case-sensitive)
- Verificar se foi criado no repositório correto

## Dicas

✅ **Sempre use "Setup VPS" na primeira vez**  
✅ **Guarde as senhas em local seguro (1Password, LastPass)**  
✅ **Use "Deploy Production" para updates do dia a dia**  
✅ **Monitore os logs dos workflows para detectar erros**  
✅ **Teste em ambiente local antes de fazer push**

---

**Importante:** Nunca commite secrets no código! Sempre use GitHub Secrets.
