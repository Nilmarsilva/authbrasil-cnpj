# Reset Completo da VPS

Guia para limpar completamente a VPS e começar do zero.

## Informações da VPS

- **IP:** 89.116.186.161
- **Domínio:** authbrasil.app.br
- **Objetivo:** Setup limpo sem senhas antigas

---

## Passo 1: Backup (Opcional)

Se houver algo que deseja manter:

```bash
# Conectar na VPS
ssh usuario@89.116.186.161

# Backup de volumes Docker (se necessário)
docker run --rm -v nome_do_volume:/source -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /source .
```

---

## Passo 2: Limpar Docker Completo

### 2.1. Parar Todos os Containers

```bash
docker stop $(docker ps -aq)
```

### 2.2. Remover Todos os Containers

```bash
docker rm $(docker ps -aq)
```

### 2.3. Remover Todas as Imagens

```bash
docker rmi $(docker images -q)
```

### 2.4. Remover Todos os Volumes

```bash
docker volume rm $(docker volume ls -q)
```

### 2.5. Remover Todas as Redes

```bash
docker network rm $(docker network ls -q)
```

### 2.6. Prune Completo (limpeza profunda)

```bash
docker system prune -a --volumes -f
```

### 2.7. Verificar Limpeza

```bash
docker ps -a
docker images
docker volume ls
docker network ls
```

Tudo deve estar vazio.

---

## Passo 3: Limpar Diretórios Antigos

### 3.1. Remover Configurações Antigas

```bash
# Remover diretórios de projetos antigos
sudo rm -rf /opt/*

# Remover configurações antigas
sudo rm -rf /etc/traefik
sudo rm -rf /etc/portainer

# Limpar logs antigos
sudo rm -rf /var/log/traefik
sudo rm -rf /var/log/nginx
```

### 3.2. Criar Nova Estrutura

```bash
# Criar diretório base
sudo mkdir -p /opt/authbrasil
sudo chown -R $USER:$USER /opt/authbrasil
```

---

## Passo 4: Configurar Cloudflare

### 4.1. Criar Conta Cloudflare

1. Acessar: https://dash.cloudflare.com/sign-up
2. Confirmar email

### 4.2. Adicionar Domínio

1. Clicar em "Add a Site"
2. Digitar: `authbrasil.app.br`
3. Escolher plano: **Free**
4. Copiar os nameservers fornecidos

Exemplo:
```
alexa.ns.cloudflare.com
boyd.ns.cloudflare.com
```

### 4.3. Atualizar Nameservers no Registro.br

1. Acessar: https://registro.br/
2. Login com certificado digital ou senha
3. Selecionar domínio `authbrasil.app.br`
4. Editar nameservers
5. Trocar de:
   ```
   ns1.registro.br
   ns2.registro.br
   ```
   Para os nameservers da Cloudflare (os que foram fornecidos)

6. Salvar e aguardar propagação (15min - 24h)

### 4.4. Verificar Propagação DNS

```bash
# Verificar nameservers
nslookup -type=NS authbrasil.app.br

# Deve retornar os nameservers da Cloudflare
```

### 4.5. Configurar DNS no Cloudflare

Na dashboard da Cloudflare, adicionar records:

| Tipo | Nome | Conteúdo | Proxy | TTL |
|------|------|----------|-------|-----|
| A | server | 89.116.186.161 | DNS only (cinza) | Auto |
| CNAME | traefik | server.authbrasil.app.br | DNS only (cinza) | Auto |
| CNAME | portainer | server.authbrasil.app.br | DNS only (cinza) | Auto |
| CNAME | pg | server.authbrasil.app.br | DNS only (cinza) | Auto |
| CNAME | api | server.authbrasil.app.br | Proxied (laranja) | Auto |
| CNAME | app | server.authbrasil.app.br | Proxied (laranja) | Auto |

### 4.6. Configurar SSL/TLS

1. **SSL/TLS > Overview**
   - Modo: **Full (strict)**

2. **SSL/TLS > Edge Certificates**
   - Always Use HTTPS: **ON**
   - HTTP Strict Transport Security (HSTS): **Enable**
   - Minimum TLS Version: **TLS 1.2**
   - Automatic HTTPS Rewrites: **ON**

3. **SSL/TLS > Origin Server**
   - Criar certificado de origem (opcional, Traefik gerará Let's Encrypt)

### 4.7. Obter API Token

1. **My Profile > API Tokens**
2. Clicar em "Create Token"
3. Template: **Edit zone DNS**
4. Permissions:
   - Zone / DNS / Edit
   - Zone / Zone / Read
5. Zone Resources:
   - Include / Specific zone / authbrasil.app.br
6. Criar e **copiar o token** (salvar em local seguro)

---

## Passo 5: Verificar Sistema da VPS

### 5.1. Atualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 5.2. Verificar Docker

```bash
docker --version
docker-compose --version
```

Se não estiver instalado:

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout e login novamente
exit
```

### 5.3. Configurar Firewall

```bash
# Instalar UFW
sudo apt install ufw -y

# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

---

## Passo 6: Clonar Repositório

```bash
cd /opt/authbrasil
git clone https://github.com/Nilmarsilva/authbrasil-cnpj.git
cd authbrasil-cnpj
```

---

## Passo 7: Preparar Stacks

### 7.1. Criar Rede Docker

```bash
docker network create traefik_public
```

### 7.2. Verificar Estrutura

```bash
ls -la infra/stacks/

# Deve mostrar:
# - traefik/
# - portainer/
# - databases/
# - authbrasil-cnpj/
# - monitoring/
# - backups/
```

---

## Próximos Passos

Após reset completo:

1. [ ] Configurar arquivos da stack Traefik
2. [ ] Deploy do Traefik
3. [ ] Configurar e deploy Portainer
4. [ ] Configurar e deploy Databases
5. [ ] Configurar e deploy AuthBrasil CNPJ
6. [ ] Testar todos os endpoints
7. [ ] Configurar backups automáticos

---

## Comandos Úteis

### Verificar Logs do Sistema

```bash
# Logs gerais
sudo journalctl -xe

# Logs do Docker
sudo journalctl -u docker.service

# Espaço em disco
df -h

# Memória
free -h

# Processos Docker
docker stats
```

### Resolver Problemas DNS

```bash
# Testar DNS
dig authbrasil.app.br
dig api.authbrasil.app.br

# Flush DNS local (se necessário)
sudo systemd-resolve --flush-caches

# Ver resolvers
cat /etc/resolv.conf
```

---

## Checklist Final

Antes de começar o deploy:

- [ ] VPS limpa (Docker zerado)
- [ ] Diretórios antigos removidos
- [ ] Cloudflare configurado
- [ ] DNS propagado e funcionando
- [ ] API Token do Cloudflare obtido
- [ ] Firewall configurado
- [ ] Docker e Docker Compose instalados
- [ ] Rede `traefik_public` criada
- [ ] Repositório clonado em `/opt/authbrasil`

---

**Status:** VPS pronta para receber as stacks do zero  
**Próximo:** Configurar stack do Traefik
