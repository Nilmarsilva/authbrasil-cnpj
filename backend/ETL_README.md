# ETL - Receita Federal CNPJ

Sistema completo de ETL para importação dos dados abertos da Receita Federal.

## 📋 Visão Geral

O ETL processa **37 arquivos ZIP** (~15-20GB) da Receita Federal e carrega no PostgreSQL.

**Fonte dos dados:**
```
https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-11/
```

## 🎯 Estratégia de Processamento

### FASE 1: Download Completo
- Baixa TODOS os 37 arquivos (~15-20GB)
- Tempo estimado: 30-60 minutos
- Arquivos salvos em: `./data/receita/`

### FASE 2: Processamento Ordenado

**1. Tabelas Auxiliares (lookup)**
- CNAEs (~1.5K registros)
- Municípios (~5.5K registros)
- Naturezas Jurídicas (~100 registros)
- Países (~250 registros)
- Qualificações (~100 registros)
- Motivos (~100 registros)

**2. Dados Principais**
- Empresas - 10 arquivos (~453MB cada) = ~50M registros
- Estabelecimentos - 10 arquivos (~320MB cada) = ~60M registros
- Sócios - 10 arquivos (~47MB cada) = ~25M registros
- Simples Nacional - 1 arquivo

**Total: ~135 milhões de registros**

## 🚀 Como Usar

### Instalação de Dependências

```bash
pip install httpx beautifulsoup4 asyncpg psycopg2-binary
```

### Rodar ETL Manual

```bash
# Processar mês atual (2025-11)
python run_etl.py

# Processar mês específico
python run_etl.py 2025-10

# Com truncate (limpa tabelas antes)
python run_etl.py --truncate

# Manter arquivos (não deletar após processar)
python run_etl.py --no-clean

# Ajustar chunk size
python run_etl.py --chunk-size 50000

# Modo verbose
python run_etl.py -v
```

### Aplicar Migration (Criar Tabelas)

```bash
cd backend
alembic upgrade head
```

## 📊 Estrutura de Tabelas

### Tabelas Auxiliares
- `cnaes` - Códigos CNAE
- `municipios` - Códigos IBGE de municípios
- `naturezas` - Naturezas jurídicas
- `paises` - Códigos de países
- `qualificacoes` - Qualificações de sócios
- `motivos` - Motivos de situação cadastral

### Tabelas Principais
- `empresas` - Dados da matriz (CNPJ básico)
- `estabelecimentos` - Dados de filiais (CNPJ completo)
- `socios` - Quadro societário
- `simples` - Optantes do Simples Nacional

## ⚙️ Performance

**Hardware Recomendado:**
- CPU: 4+ cores
- RAM: 8GB+
- Disco: 100GB+ SSD
- Rede: 50+ Mbps

**Tempos Estimados:**
- Download: 30-60 minutos
- Processamento: 2-4 horas
- Total: 3-5 horas

**Otimizações Implementadas:**
- Async downloads
- Processamento em chunks (100K registros)
- PostgreSQL COPY bulk insert
- Índices criados após carga
- Limpeza automática de temporários

## 🔧 Troubleshooting

### Erro de conexão durante download
```bash
# Aumentar timeout e retry
python run_etl.py -v
```

### Memória insuficiente
```bash
# Reduzir chunk size
python run_etl.py --chunk-size 50000
```

### Disco cheio
```bash
# Limpar arquivos antigos
rm -rf ./data/receita/*

# Usar --clean para deletar após processar
python run_etl.py --clean
```

### Erro no PostgreSQL COPY
```bash
# Verificar encoding e permissões
psql -U postgres -d authbrasil_cnpj -c "SHOW client_encoding;"
```

## 📅 Agendamento (Futuro)

Com Celery Beat para rodar mensalmente:

```python
from celery import Celery
from celery.schedules import crontab

app = Celery('etl_tasks')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executar dia 10 de cada mês às 2h
    sender.add_periodic_task(
        crontab(day_of_month=10, hour=2, minute=0),
        run_etl_task.s(),
    )
```

## 🐛 Logs

Logs salvos em: `etl.log`

**Níveis de log:**
- INFO: Progresso geral
- WARNING: Arquivos não encontrados
- ERROR: Erros críticos
- DEBUG: Detalhes técnicos (usar -v)

## 📈 Monitoramento

**Estatísticas ao final:**
- Arquivos baixados/processados
- Total de registros inseridos
- Tempo de execução
- Erros ocorridos

**Exemplo de output:**
```
================================================================================
✅ ETL Pipeline Completed Successfully
Duration: 12847.3 seconds (214.1 minutes)
Files Downloaded: 37
Files Processed: 37
Total Records: 135,234,567
Errors: 0
================================================================================
```

## 🔐 Segurança

- Dados públicos (não há informações sensíveis)
- Validação de encoding (latin-1)
- Tratamento de caracteres especiais
- Logs não contêm dados pessoais

## 📚 Referências

- [Dados Abertos CNPJ - Receita Federal](https://dados.gov.br/dados/conjuntos-dados/cadastro-nacional-da-pessoa-juridica---cnpj)
- [Layout dos Arquivos](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/arquivos/NOVOLAYOUTDOSDADOSABERTOSDOCNPJ.pdf)

## 🤝 Contribuindo

1. Testar localmente antes de commitar
2. Documentar mudanças no código
3. Atualizar este README se necessário
4. Rodar `pytest` antes de push

---

**Desenvolvido para AuthBrasil CNPJ**  
**Última atualização: 2025-11-22**
