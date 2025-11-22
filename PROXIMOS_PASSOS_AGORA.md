# Próximos Passos - AGORA

Você já fez:
- ✅ Conta Cloudflare criada
- ✅ Nameservers alterados (propagando)
- ✅ Senhas geradas

---

## 1️⃣ Pegar Chave SSH (1 minuto)

Abra PowerShell e rode:

```powershell
Get-Content ~\.ssh\id_rsa
```

**Copie TODA a saída** (incluindo `-----BEGIN...` e `-----END...`)

Se der erro "arquivo não encontrado", você precisa criar uma chave SSH:

```powershell
ssh-keygen -t rsa -b 4096 -C "seu-email@example.com"
# Pressione Enter 3 vezes (sem senha)
Get-Content ~\.ssh\id_rsa
```

---

## 2️⃣ Adicionar Secrets no GitHub (5 minutos)

**Link direto:** https://github.com/Nilmarsilva/authbrasil-cnpj/settings/secrets/actions

Para cada secret abaixo:
1. Clicar em "New repository secret"
2. Copiar o nome exato
3. Copiar o valor
4. "Add secret"

### Secrets para adicionar:

| Nome do Secret | Valor |
|----------------|-------|
| `VPS_HOST` | `89.116.186.161` |
| `VPS_USER` | `root` (ou seu usuário SSH) |
| `VPS_SSH_KEY` | Colar TODO o conteúdo da chave SSH |
| `DB_PASSWORD` | `xWxt64YrzAFWc3ylNHrAbMoF0Z8h_b6kCQT4aX8sdgM` |
| `PGADMIN_PASSWORD` | `uar22mFMZwtjdKo047B_5V3osyK3f7CB` |
| `REDIS_PASSWORD` | `vezEgze0KAtTuvn20ITwme_Ud8--aXdB` |
| `SECRET_KEY` | `2dedddaff60c04b3fa767ebc720a2dec4c94969be65cb9e4ff8f76e8a9b7e142` |
| `JWT_SECRET_KEY` | `65248bd67bca837ae6e003075ce97a9bed277a8324eb1eb86e5b9160ad2d6c5e` |
| `STRIPE_SECRET_KEY` | `sk_test_xxx` (deixe vazio ou use chave de teste) |
| `STRIPE_PUBLISHABLE_KEY` | `pk_test_xxx` (deixe vazio ou use chave de teste) |
| `STRIPE_WEBHOOK_SECRET` | `whsec_xxx` (deixe vazio por enquanto) |
| `SENDGRID_API_KEY` | `SG.xxx` (deixe vazio por enquanto) |

**Dica:** Abra o arquivo `SENHAS_GERADAS.txt` e copie/cole de lá!

**Importante:** 
- Stripe e SendGrid podem ficar vazios por enquanto
- Você pode criar depois e adicionar os secrets

---

## 3️⃣ Adicionar Chave SSH Pública na VPS (2 minutos)

Para o GitHub Actions conseguir conectar na VPS, precisa adicionar a chave pública:

```powershell
# Ver sua chave pública
Get-Content ~\.ssh\id_rsa.pub

# Copiar a saída
```

Agora conecte na VPS:

```bash
ssh root@89.116.186.161

# Adicionar a chave
echo "COLAR_CHAVE_PUBLICA_AQUI" >> ~/.ssh/authorized_keys

# Verificar
cat ~/.ssh/authorized_keys

# Sair
exit
```

**Testar se funciona:**
```powershell
ssh root@89.116.186.161
# Deve conectar SEM pedir senha
```

---

## 4️⃣ Executar Deploy Automático (1 clique!)

**Importante:** Aguarde a propagação DNS do Cloudflare (você disse 2 horas)

Quando o DNS estiver propagado:

1. Acesse: https://github.com/Nilmarsilva/authbrasil-cnpj/actions
2. Clique em **"Setup VPS (Primeira Vez)"**
3. Clique em **"Run workflow"** (botão verde)
4. Selecione **"main"**
5. Clique em **"Run workflow"** novamente
6. Aguarde 5-10 minutos ☕

---

## 5️⃣ Verificar se Funcionou

Após o workflow terminar com sucesso:

```bash
# Verificar DNS propagado
nslookup api.authbrasil.app.br

# Testar endpoints (aguarde SSL ser gerado - 1-2 min após deploy)
curl https://api.authbrasil.app.br/api/v1/health
curl https://portainer.authbrasil.app.br
```

**URLs finais:**
- 🚀 API: https://api.authbrasil.app.br
- 📖 Docs: https://api.authbrasil.app.br/api/v1/docs
- 🐳 Portainer: https://portainer.authbrasil.app.br
- 🗄️ pgAdmin: https://pg.authbrasil.app.br

---

## 🆘 Se Algo Der Errado

### Erro de SSH no GitHub Actions

```powershell
# Testar conexão SSH localmente
ssh -vvv root@89.116.186.161
```

Se pedir senha = chave SSH não foi configurada corretamente

### DNS não resolvendo

```bash
# Verificar propagação
nslookup api.authbrasil.app.br
dig api.authbrasil.app.br
```

Aguardar mais tempo (pode levar até 24h)

### Ver logs do workflow

1. GitHub → Actions
2. Clicar no workflow em execução
3. Ver erros detalhados

---

## Checklist Final

Antes de rodar o workflow:

- [ ] 12 secrets configurados no GitHub
- [ ] Chave SSH pública na VPS
- [ ] Consegue conectar via SSH sem senha
- [ ] DNS propagado (aguardar 2 horas)
- [ ] VPS limpa (opcional)

**Tudo pronto?** Clique em "Run workflow"! 🚀

---

**Tempo total:** ~15 minutos (+ 2h aguardando DNS)

**Dúvidas?** Só chamar! 😊
