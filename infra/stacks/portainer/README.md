# Stack Portainer

Interface web para gerenciar Docker Swarm.

## Características

- **Interface visual** para containers, stacks, volumes, networks
- **Modo Swarm** com agent em todos os nodes
- **SSL automático** via Traefik
- **Acesso:** https://portainer.authbrasil.app.br

## Pré-requisitos

1. Stack Traefik deployada e funcionando
2. Volume criado: `portainer_data`
3. Rede: `network_public`

## Deploy

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/portainer

# Deploy da stack
docker stack deploy -c docker-compose.yml portainer

# Verificar
docker stack ps portainer
docker service logs portainer_portainer -f
```

## Primeiro Acesso

1. Acessar: https://portainer.authbrasil.app.br
2. **Atenção:** Você tem **5 minutos** para criar a senha de admin
3. Criar usuário `admin` com senha forte
4. Escolher ambiente: **Docker Swarm**

## Funcionalidades

### Dashboard
- Visão geral de containers, stacks, volumes, networks
- Status de recursos (CPU, memória)

### Stacks
- Deploy de stacks via interface
- Editar compose files
- Ver logs

### Services
- Ver todos os serviços do Swarm
- Escalar réplicas
- Ver logs em tempo real

### Volumes & Networks
- Gerenciar volumes
- Criar/remover networks

### Nodes
- Ver status dos nodes do Swarm
- Promover/drenar nodes

## Backup

Fazer backup do volume `portainer_data`:

```bash
docker run --rm \
  -v portainer_data:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/portainer_backup_$(date +%Y%m%d).tar.gz -C /source .
```

## Restore

```bash
# Parar Portainer
docker service scale portainer_portainer=0

# Restore
docker run --rm \
  -v portainer_data:/target \
  -v $(pwd):/backup \
  alpine sh -c "cd /target && tar xzf /backup/portainer_backup_YYYYMMDD.tar.gz"

# Reiniciar
docker service scale portainer_portainer=1
```

## Atualizar

```bash
# Atualizar para versão mais recente
docker service update --image portainer/portainer-ce:latest portainer_portainer
docker service update --image portainer/agent:latest portainer_agent
```

## Troubleshooting

### Não consegue acessar

```bash
# Ver logs
docker service logs portainer_portainer --tail 50

# Verificar se Traefik está roteando
docker service logs traefik_traefik | grep portainer

# Testar DNS
dig portainer.authbrasil.app.br
```

### Expirou os 5 minutos

```bash
# Remover volume e recriar
docker stack rm portainer
docker volume rm portainer_data
docker volume create portainer_data
docker stack deploy -c docker-compose.yml portainer
```

## Remover

```bash
# Remover stack
docker stack rm portainer

# Remover volume (CUIDADO: perde configurações)
docker volume rm portainer_data
```

---

**Importante:** Portainer facilita muito o gerenciamento, mas sempre tenha os comandos Docker à mão como backup.
