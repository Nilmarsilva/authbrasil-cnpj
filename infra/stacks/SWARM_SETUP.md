# Setup Docker Swarm - AuthBrasil

Comandos para inicializar e configurar Docker Swarm do zero.

## Inicializar Swarm

### 1. Inicializar no Manager Node

```bash
# Conectar na VPS
ssh usuario@89.116.186.161

# Inicializar Swarm
docker swarm init --advertise-addr 89.116.186.161

# Verificar status
docker info | grep Swarm
# Deve mostrar: Swarm: active
```

### 2. Verificar Node

```bash
docker node ls

# Output esperado:
# ID         HOSTNAME    STATUS    AVAILABILITY   MANAGER STATUS
# xxx123*    servidor    Ready     Active         Leader
```

---

## Criar Volumes e Redes

### Volumes

```bash
# Volume para certificados SSL
docker volume create volume_swarm_certificates

# Volume para Portainer
docker volume create portainer_data

# Verificar
docker volume ls
```

### Rede

```bash
# Criar rede overlay (necessária para Swarm)
docker network create --driver overlay --attachable network_public

# Verificar
docker network ls | grep network_public
```

---

## Deploy das Stacks

### 1. Deploy Traefik (primeiro)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/traefik

# Deploy
docker stack deploy -c docker-compose.yml traefik

# Verificar
docker stack ps traefik
docker service logs traefik_traefik -f
```

**Aguardar:** Traefik iniciar e gerar certificado SSL (1-2 min)

### 2. Deploy Portainer (segundo)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/portainer

# Deploy
docker stack deploy -c docker-compose.yml portainer

# Verificar
docker stack ps portainer
docker service logs portainer_portainer -f
```

**Acessar:** https://portainer.authbrasil.app.br

**Primeira vez:** Criar senha de admin (tem 5 minutos)

### 3. Deploy Databases (terceiro)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/databases

# Deploy
docker stack deploy -c docker-compose.yml databases

# Verificar
docker stack ps databases
```

### 4. Deploy AuthBrasil CNPJ (quarto)

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/authbrasil-cnpj

# Deploy
docker stack deploy -c docker-compose.yml authbrasil

# Verificar
docker stack ps authbrasil
```

---

## Comandos Úteis - Swarm

### Stacks

```bash
# Listar stacks
docker stack ls

# Ver serviços de uma stack
docker stack services traefik

# Ver tarefas de uma stack
docker stack ps traefik

# Remover stack
docker stack rm traefik
```

### Services

```bash
# Listar todos os serviços
docker service ls

# Ver logs de um serviço
docker service logs traefik_traefik -f

# Escalar serviço
docker service scale portainer_portainer=2

# Atualizar serviço
docker service update --image traefik:latest traefik_traefik

# Inspecionar serviço
docker service inspect traefik_traefik
```

### Nodes

```bash
# Listar nodes
docker node ls

# Inspecionar node
docker node inspect self

# Promover node para manager (se tiver mais nodes)
docker node promote NODE_ID

# Drenar node (manutenção)
docker node update --availability drain NODE_ID

# Reativar node
docker node update --availability active NODE_ID
```

### Networks

```bash
# Listar redes
docker network ls

# Inspecionar rede
docker network inspect network_public

# Ver containers conectados
docker network inspect network_public | grep Name
```

### Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect volume_swarm_certificates

# Ver onde está montado
docker volume inspect portainer_data | grep Mountpoint
```

---

## Troubleshooting

### Traefik não inicia

```bash
# Ver logs
docker service logs traefik_traefik --tail 100

# Verificar se portas estão livres
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Verificar volume de certificados
docker volume inspect volume_swarm_certificates

# Recriar serviço
docker service update --force traefik_traefik
```

### Portainer não acessa

```bash
# Ver logs
docker service logs portainer_portainer --tail 50

# Verificar se Traefik está roteando
docker service logs traefik_traefik | grep portainer

# Verificar labels
docker service inspect portainer_portainer --format '{{json .Spec.Labels}}' | jq
```

### SSL não funciona

```bash
# Ver logs do ACME (Let's Encrypt)
docker service logs traefik_traefik | grep acme

# Verificar arquivo acme.json
docker exec $(docker ps -q -f name=traefik) ls -la /etc/traefik/letsencrypt/

# Forçar renovação (remover certificado)
docker exec $(docker ps -q -f name=traefik) rm /etc/traefik/letsencrypt/acme.json
docker service update --force traefik_traefik
```

### DNS não resolve

```bash
# Testar DNS
dig portainer.authbrasil.app.br
dig api.authbrasil.app.br

# Verificar propagação
nslookup portainer.authbrasil.app.br

# Flush DNS local (se necessário)
sudo systemd-resolve --flush-caches
```

### Serviço não atualiza

```bash
# Forçar update
docker service update --force NOME_DO_SERVICO

# Exemplo
docker service update --force traefik_traefik
```

---

## Backup e Restore

### Backup de Volumes

```bash
# Backup volume de certificados
docker run --rm \
  -v volume_swarm_certificates:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/certificates_backup.tar.gz -C /source .

# Backup Portainer
docker run --rm \
  -v portainer_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/portainer_backup.tar.gz -C /source .
```

### Restore de Volumes

```bash
# Restore certificados
docker run --rm \
  -v volume_swarm_certificates:/target \
  -v $(pwd):/backup \
  alpine sh -c "cd /target && tar xzf /backup/certificates_backup.tar.gz"

# Restore Portainer
docker run --rm \
  -v portainer_data:/target \
  -v $(pwd):/backup \
  alpine sh -c "cd /target && tar xzf /backup/portainer_backup.tar.gz"
```

---

## Manutenção

### Limpar Recursos Não Usados

```bash
# Limpar containers parados
docker container prune -f

# Limpar imagens não usadas
docker image prune -a -f

# Limpar volumes não usados (CUIDADO!)
docker volume prune -f

# Limpar tudo
docker system prune -a --volumes -f
```

### Atualizar Imagens

```bash
# Atualizar Traefik
docker service update --image traefik:latest traefik_traefik

# Atualizar Portainer
docker service update --image portainer/portainer-ce:latest portainer_portainer
docker service update --image portainer/agent:latest portainer_agent
```

### Ver Uso de Recursos

```bash
# CPU e memória por serviço
docker stats

# Espaço em disco
df -h

# Tamanho dos volumes
docker system df -v
```

---

## Comandos de Emergência

### Resetar Swarm (CUIDADO!)

```bash
# Remover todas as stacks
docker stack rm $(docker stack ls --format '{{.Name}}')

# Aguardar remoção completa
sleep 30

# Deixar o swarm
docker swarm leave --force

# Reinicializar
docker swarm init --advertise-addr 89.116.186.161
```

### Reiniciar Docker Daemon

```bash
sudo systemctl restart docker

# Verificar status
sudo systemctl status docker
```

---

## Checklist de Deploy

- [ ] Swarm inicializado
- [ ] Volume `volume_swarm_certificates` criado
- [ ] Volume `portainer_data` criado
- [ ] Rede `network_public` criada
- [ ] Stack Traefik deployada
- [ ] Traefik gerando SSL com sucesso
- [ ] Stack Portainer deployada
- [ ] Portainer acessível via browser
- [ ] DNS configurado no Cloudflare
- [ ] Subdomínios resolvendo corretamente

---

**Importante:** Docker Swarm mantém os serviços sempre rodando. Se um container falhar, ele é automaticamente recriado.
