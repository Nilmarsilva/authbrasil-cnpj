# 🚀 Otimização do PostgreSQL para AuthBrasil CNPJ

## 📊 Visão Geral

Com **~135 milhões de registros**, precisamos de otimizações agressivas para manter performance.

---

## 🎯 Estratégias Implementadas

### 1. **Índices Otimizados**

#### Índices B-Tree (Padrão)
- `cnpj_basico` (todas as tabelas) - Chave de relacionamento
- `cnpj_completo` (estabelecimentos) - Busca por CNPJ
- `razao_social` (empresas) - Ordenação alfabética
- `uf`, `municipio` (estabelecimentos) - Filtros regionais

#### Índices GIN (Full-Text Search)
```sql
-- Busca por nome aproximado (trigram)
CREATE INDEX idx_empresas_razao_social_trgm 
ON empresas USING gin(razao_social gin_trgm_ops);

-- Busca por nome fantasia
CREATE INDEX idx_estabelecimentos_nome_fantasia_trgm 
ON estabelecimentos USING gin(nome_fantasia gin_trgm_ops);

-- Busca por nome de sócio
CREATE INDEX idx_socios_nome_socio_trgm 
ON socios USING gin(nome_socio gin_trgm_ops);
```

**Benefício:** Busca tipo "LIKE %termo%" rápida (~10-100x mais rápido)

#### Índices Compostos
```sql
-- Buscar por UF + Situação
CREATE INDEX idx_estabelecimentos_uf_situacao 
ON estabelecimentos(uf, situacao_cadastral);

-- Buscar por Município + CNAE
CREATE INDEX idx_estabelecimentos_municipio_cnae 
ON estabelecimentos(municipio, cnae_fiscal_principal);
```

**Benefício:** Queries com WHERE combinado são muito mais rápidas

#### Índices Parciais
```sql
-- Apenas estabelecimentos ativos (economiza espaço)
CREATE INDEX idx_estabelecimentos_ativos 
ON estabelecimentos(cnpj_completo) 
WHERE situacao_cadastral = '02';

-- Apenas matrizes
CREATE INDEX idx_estabelecimentos_matrizes 
ON estabelecimentos(cnpj_basico) 
WHERE identificador_matriz_filial = '1';
```

**Benefício:** Índices menores = queries mais rápidas + menos disco

---

### 2. **VACUUM e Autovacuum**

#### O que é VACUUM?
- Remove linhas "mortas" (deleted/updated)
- Libera espaço em disco
- Atualiza estatísticas do planner

#### Configuração Autovacuum
```sql
-- Para tabelas grandes (>10M linhas)
ALTER TABLE estabelecimentos SET (
    autovacuum_vacuum_scale_factor = 0.05,     -- 5% de linhas mortas
    autovacuum_vacuum_threshold = 10000,       -- Mínimo 10k linhas
    autovacuum_analyze_scale_factor = 0.02,    -- 2% para análise
    autovacuum_analyze_threshold = 5000        -- Mínimo 5k linhas
);
```

#### VACUUM Manual
```bash
# VACUUM normal (não bloqueia)
python backend/scripts/optimize_database.py

# VACUUM FULL (reescreve tabela, BLOQUEIA!)
# Apenas durante manutenção programada
psql -U postgres -d authbrasil_cnpj -c "VACUUM FULL VERBOSE estabelecimentos"
```

**Frequência Recomendada:**
- Autovacuum: Automático (configurado)
- VACUUM ANALYZE: Semanal (via cron)
- VACUUM FULL: Semestral (janela de manutenção)

---

### 3. **Configuração do PostgreSQL**

#### `postgresql.conf` Otimizado

```ini
# Memória
shared_buffers = 2GB              # 25% da RAM (8GB)
effective_cache_size = 6GB        # 75% da RAM
work_mem = 50MB                   # Para sorts/joins
maintenance_work_mem = 512MB      # Para VACUUM/CREATE INDEX

# Checkpoints
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100   # Estatísticas mais precisas

# Autovacuum
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = 10s          # Verifica a cada 10s

# Planner
random_page_cost = 1.1            # Para SSD (padrão=4.0)
effective_io_concurrency = 200    # Para SSD
```

#### Como Aplicar
```bash
# 1. Editar arquivo de configuração
sudo nano /etc/postgresql/16/main/postgresql.conf

# 2. Reiniciar PostgreSQL
sudo systemctl restart postgresql

# 3. Verificar
psql -U postgres -c "SHOW shared_buffers"
```

---

### 4. **Particionamento de Tabelas (Futuro)**

Para tabelas com **>50M registros**, considerar particionamento:

```sql
-- Particionar estabelecimentos por UF
CREATE TABLE estabelecimentos_sp PARTITION OF estabelecimentos
FOR VALUES IN ('SP');

CREATE TABLE estabelecimentos_rj PARTITION OF estabelecimentos
FOR VALUES IN ('RJ');

-- etc...
```

**Benefícios:**
- Queries em SP só leem partição SP
- VACUUM mais rápido (por partição)
- Manutenção independente

**Quando Implementar:**
- Quando queries por UF forem >70% do total
- Ou quando tabela passar de 100M linhas

---

### 5. **Monitoramento**

#### Queries Lentas
```sql
-- Habilitar log de queries lentas
ALTER DATABASE authbrasil_cnpj SET log_min_duration_statement = 1000;  -- >1s

-- Ver queries mais lentas
SELECT 
    query,
    calls,
    total_time / 1000 / 60 as total_minutes,
    mean_time / 1000 as mean_seconds
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat%'
ORDER BY total_time DESC
LIMIT 20;
```

#### Tamanho das Tabelas
```sql
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

#### Índices Não Utilizados
```sql
-- Índices que nunca são usados (candidatos para remoção)
SELECT 
    schemaname, tablename, indexname,
    idx_scan as scans,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

### 6. **Cache (Redis)**

Para queries frequentes, usar Redis:

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_empresa_cached(cnpj_basico: str):
    # Tentar cache primeiro
    cache_key = f"empresa:{cnpj_basico}"
    cached = redis_client.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    # Se não estiver em cache, buscar no DB
    empresa = await db.query(Empresa).filter(...).first()
    
    # Guardar em cache (24h)
    redis_client.setex(cache_key, 86400, json.dumps(empresa))
    
    return empresa
```

**Queries para Cachear:**
- Busca por CNPJ completo
- Empresas mais consultadas
- Tabelas auxiliares (CNAEs, Municípios, etc)

---

## 🔧 Scripts de Manutenção

### Otimização Completa
```bash
python backend/scripts/optimize_database.py
```

**O que faz:**
1. Configura autovacuum
2. Cria índices full-text
3. Cria índices compostos
4. Cria índices parciais
5. Executa VACUUM ANALYZE
6. Mostra estatísticas

### Cron Job (Manutenção Automática)
```bash
# Editar crontab
crontab -e

# Adicionar linha (todo domingo às 2h)
0 2 * * 0 cd /path/to/backend && python scripts/optimize_database.py >> /var/log/db_optimize.log 2>&1
```

---

## 📈 Benchmarks Esperados

| Operação | Sem Otimização | Com Otimização | Melhora |
|----------|----------------|----------------|---------|
| Busca por CNPJ | ~500ms | ~10ms | 50x |
| Busca por nome (LIKE) | ~30s | ~300ms | 100x |
| Busca por UF + CNAE | ~10s | ~100ms | 100x |
| Join Empresa + Estabelecimento | ~2s | ~50ms | 40x |
| Count total (estabelecimentos) | ~15s | ~50ms | 300x |

---

## ⚠️ Avisos Importantes

### VACUUM FULL
- **BLOQUEIA a tabela** durante execução
- Pode demorar horas em tabelas grandes
- Apenas em janela de manutenção programada
- **NÃO rodar em produção sem aviso!**

### Índices
- Cada índice **aumenta tempo de INSERT/UPDATE**
- Índices não usados **desperdiçam espaço**
- Monitorar uso com `pg_stat_user_indexes`

### Memória
- `shared_buffers` > 25% RAM pode piorar performance
- `work_mem` muito alto = risco de OOM (Out of Memory)
- Sempre testar antes de aplicar em produção

---

## 📚 Referências

- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [pg_trgm Extension](https://www.postgresql.org/docs/current/pgtrgm.html)
- [VACUUM Best Practices](https://www.postgresql.org/docs/current/sql-vacuum.html)
- [Effective use of PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)

---

**Última atualização:** 22/11/2024  
**Versão PostgreSQL:** 16+
