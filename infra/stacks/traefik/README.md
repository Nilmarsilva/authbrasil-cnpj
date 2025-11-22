# Stack Traefik

Reverse proxy com SSL automático via Let's Encrypt.

## Características

- **SSL automático** via Let's Encrypt (HTTP Challenge)
- **Redirect HTTP → HTTPS** automático
- **Dashboard** opcional
- **Logs** estruturados
- **Docker Swarm** ready

## Pré-requisitos

1. Docker Swarm inicializado
2. Volume criado: `volume_swarm_certificates`
3. Rede criada: `network_public`
4. Portas 80 e 443 abertas no firewall

## Deploy

```bash
cd /opt/authbrasil/authbrasil-cnpj/infra/stacks/traefik

# Deploy da stack
docker stack deploy -c docker-compose.yml traefik

# Verificar
docker stack ps traefik
docker service logs traefik_traefik -f
```

## Verificar Funcionamento

```bash
# Ver se está rodando
docker service ls | grep traefik

# Ver logs
docker service logs traefik_traefik --tail 50

# Testar HTTP (deve redirecionar para HTTPS)
curl -I http://portainer.authbrasil.app.br

# Testar HTTPS
curl -I https://portainer.authbrasil.app.br
```

## Configuração

### Email Let's Encrypt

Configurado em `docker-compose.yml`:
```yaml
- "--certificatesresolvers.letsencryptresolver.acme.email=nilmarbiosilva@gmail.com"
```

### Network

Todos os serviços devem usar a rede `network_public`:
```yaml
networks:
  - network_public
```

### Labels para Expor Serviço

Exemplo de labels para um serviço ser roteado pelo Traefik:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.docker.network=network_public"
  - "traefik.http.routers.meuservico.rule=Host(`api.authbrasil.app.br`)"
  - "traefik.http.routers.meuservico.entrypoints=websecure"
  - "traefik.http.routers.meuservico.tls.certresolver=letsencryptresolver"
  - "traefik.http.services.meuservico.loadbalancer.server.port=8000"
```

## Dashboard (Opcional)

Por segurança, o dashboard está comentado. Para habilitar:

1. Editar `docker-compose.yml`
2. Descomentar as labels do dashboard
3. Atualizar serviço:

```bash
docker service update --force traefik_traefik
```

Acessar: https://traefik.authbrasil.app.br

**Importante:** Adicionar autenticação básica antes de habilitar em produção!

## Troubleshooting

### SSL não gera

```bash
# Ver logs do ACME
docker service logs traefik_traefik | grep acme

# Verificar se DNS está apontando corretamente
dig portainer.authbrasil.app.br

# Verificar arquivo de certificados
docker exec $(docker ps -q -f name=traefik) cat /etc/traefik/letsencrypt/acme.json
```

### Porta 80/443 em uso

```bash
# Ver o que está usando
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Parar processo conflitante (ex: nginx)
sudo systemctl stop nginx
sudo systemctl disable nginx
```

## Atualizar

```bash
# Atualizar para versão mais recente
docker service update --image traefik:latest traefik_traefik

# Ou especificar versão
docker service update --image traefik:v2.10 traefik_traefik
```

## Remover

```bash
# Remover stack
docker stack rm traefik

# Aguardar remoção completa
sleep 10

# Verificar
docker service ls
```

---

**Nota:** Traefik deve ser a primeira stack a ser deployada, pois gerencia todo o roteamento HTTPS.
