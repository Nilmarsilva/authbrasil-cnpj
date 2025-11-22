# 🚀 COMANDOS PARA RODAR NA VPS (COPIAR E COLAR)

## ⚡ EXECUÇÃO RÁPIDA (5 MINUTOS)

### 1️⃣ Conectar na VPS
```bash
ssh root@89.116.188.161
```

---

### 2️⃣ Atualizar código e instalar dependências
```bash
cd /root/backend
git pull origin main
cd ..
pip3 install httpx beautifulsoup4 lxml
```

---

### 3️⃣ Criar banco de dados
```bash
sudo -u postgres psql -c "CREATE DATABASE authbrasil_cnpj" || echo "Banco já existe"
```

---

### 4️⃣ Criar tabelas (migrations)
```bash
cd /root/backend
alembic upgrade head
```

---

### 5️⃣ Criar diretório para dados
```bash
mkdir -p /root/data/receita
cd /root
```

---

### 6️⃣ **RODAR ETL (deixar rodando a noite toda)**
```bash
nohup python3 backend/run_etl.py --truncate > etl.log 2>&1 &
```

**Anote o PID que aparecer!**

---

### 7️⃣ Monitorar execução
```bash
# Ver log em tempo real
tail -f etl.log

# Pressione CTRL+C para sair (não para o ETL)
```

---

## 📊 COMANDOS ÚTEIS

### Ver progresso no banco
```bash
sudo -u postgres psql -d authbrasil_cnpj -c "
SELECT 
    'empresas' as tabela, COUNT(*) as registros FROM empresas
UNION ALL
SELECT 'estabelecimentos', COUNT(*) FROM estabelecimentos
UNION ALL
SELECT 'socios', COUNT(*) FROM socios
UNION ALL
SELECT 'simples', COUNT(*) FROM simples;
"
```

### Ver tamanho do banco
```bash
sudo -u postgres psql -d authbrasil_cnpj -c "SELECT pg_size_pretty(pg_database_size('authbrasil_cnpj'));"
```

### Ver processo rodando
```bash
ps aux | grep run_etl.py
```

### Ver últimas 50 linhas do log
```bash
tail -n 50 etl.log
```

---

## 🛑 SE PRECISAR PARAR

```bash
# Encontrar PID
ps aux | grep run_etl.py

# Matar processo
kill <PID>
```

---

## ⏱️ TEMPO ESTIMADO

| Fase | Tempo |
|------|-------|
| Download (37 arquivos, ~15GB) | 30-60 min |
| Processar auxiliares | 5 min |
| Processar Empresas (24M) | 2-3h |
| Processar Estabelecimentos (25M) | 3-4h |
| Processar Sócios (8M) | 1-2h |
| Processar Simples (45M) | 2-3h |
| Criar índices | 30-60 min |
| **TOTAL** | **6-12 horas** |

---

## ✅ AMANHÃ DE MANHÃ

Quando terminar, rodar otimização:

```bash
cd /root/backend
python3 scripts/optimize_database.py
```

---

## 🔥 SE DER ERRO

### Erro: "ModuleNotFoundError"
```bash
pip3 install httpx beautifulsoup4 asyncpg psycopg2-binary
```

### Erro: "database does not exist"
```bash
sudo -u postgres psql -c "CREATE DATABASE authbrasil_cnpj"
```

### Erro: Alembic não encontrado
```bash
pip3 install alembic
```

### Erro: "No space left on device"
```bash
# Ver espaço em disco
df -h

# Limpar arquivos antigos se necessário
rm -rf /root/data/receita/*
```

---

**BOM TRABALHO! DEIXE RODANDO E VÁ DESCANSAR! 🚀**
