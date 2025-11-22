# Estrutura dos Dados da Receita Federal

**Análise baseada em amostras de 50 linhas**  
**Data: 22/11/2024**

---

## 📋 TABELAS AUXILIARES (Lookup)

### 1. CNAEs (1.359 registros)
**Colunas:** 2
```csv
"0111301";"Cultivo de arroz"
```
- Coluna 1: Código CNAE (7 dígitos)
- Coluna 2: Descrição da Atividade

---

### 2. Municípios (5.572 registros)
**Colunas:** 2
```csv
"0001";"GUAJARA-MIRIM"
```
- Coluna 1: Código IBGE (4 dígitos)
- Coluna 2: Nome do Município

---

### 3. Naturezas Jurídicas (91 registros)
**Colunas:** 2
```csv
"0000";"Natureza Jurídica não informada"
```
- Coluna 1: Código (4 dígitos)
- Coluna 2: Descrição

---

### 4. Países (255 registros)
**Colunas:** 2
```csv
"000";"COLIS POSTAUX"
```
- Coluna 1: Código (3 dígitos)
- Coluna 2: Nome do País

---

### 5. Qualificações (68 registros)
**Colunas:** 2
```csv
"00";"Não informada"
```
- Coluna 1: Código (2 dígitos)
- Coluna 2: Descrição da Qualificação

---

### 6. Motivos (63 registros)
**Colunas:** 2
```csv
"00";"SEM MOTIVO"
```
- Coluna 1: Código (2 dígitos)
- Coluna 2: Descrição do Motivo

---

## 📊 TABELAS PRINCIPAIS

### 7. EMPRESAS (24.8 milhões de registros)
**Colunas:** 7  
**Tamanho:** 1.9GB

```csv
"41273590";"MARIA DAS MERCES SOARES LEMOS";"4014";"34";"0,00";"05";""
```

| # | Campo | Exemplo | Descrição |
|---|-------|---------|-----------|
| 1 | cnpj_basico | 41273590 | CNPJ Básico (8 dígitos) |
| 2 | razao_social | MARIA DAS MERCES SOARES LEMOS | Razão Social |
| 3 | natureza_juridica | 4014 | Código da Natureza Jurídica |
| 4 | qualificacao_responsavel | 34 | Código Qualificação do Responsável |
| 5 | capital_social | 0,00 | Capital Social (formato BR: vírgula) |
| 6 | porte_empresa | 05 | Código do Porte |
| 7 | ente_federativo_responsavel | "" | Ente Federativo (geralmente vazio) |

---

### 8. ESTABELECIMENTOS (25.6 milhões de registros)
**Colunas:** 30  
**Tamanho:** 6GB

```csv
"08636546";"0001";"45";"1";"******";"04";"20181016";"63";"";"";"20070207";"8599604";"";"ALAMEDA";"RIO CLARO";"95";"SALA 183";"BELA VISTA";"01332010";"SP";"7107";"11";"31166305";"";"";"";"";"email@example.com";"";""
```

| # | Campo | Exemplo | Descrição |
|---|-------|---------|-----------|
| 1 | cnpj_basico | 08636546 | CNPJ Básico (8 dígitos) |
| 2 | cnpj_ordem | 0001 | Ordem do CNPJ (4 dígitos) |
| 3 | cnpj_dv | 45 | Dígito Verificador (2 dígitos) |
| 4 | identificador_matriz_filial | 1 | 1=Matriz, 2=Filial |
| 5 | nome_fantasia | ****** | Nome Fantasia (asteriscos quando vazio) |
| 6 | situacao_cadastral | 04 | Código Situação Cadastral |
| 7 | data_situacao_cadastral | 20181016 | Data (YYYYMMDD) |
| 8 | motivo_situacao_cadastral | 63 | Código do Motivo |
| 9 | cidade_exterior | "" | Cidade no Exterior |
| 10 | pais | "" | Código do País |
| 11 | data_inicio_atividade | 20070207 | Data (YYYYMMDD) |
| 12 | cnae_fiscal_principal | 8599604 | CNAE Principal |
| 13 | cnae_fiscal_secundaria | "" | CNAEs Secundários (separados por vírgula) |
| 14 | tipo_logradouro | ALAMEDA | Tipo (RUA, AVENIDA, etc) |
| 15 | logradouro | RIO CLARO | Nome do Logradouro |
| 16 | numero | 95 | Número |
| 17 | complemento | SALA 183 | Complemento |
| 18 | bairro | BELA VISTA | Bairro |
| 19 | cep | 01332010 | CEP (8 dígitos) |
| 20 | uf | SP | UF (2 letras) |
| 21 | municipio | 7107 | Código IBGE do Município |
| 22 | ddd_1 | 11 | DDD Telefone 1 |
| 23 | telefone_1 | 31166305 | Telefone 1 |
| 24 | ddd_2 | "" | DDD Telefone 2 |
| 25 | telefone_2 | "" | Telefone 2 |
| 26 | ddd_fax | "" | DDD Fax |
| 27 | fax | "" | Fax |
| 28 | email | email@example.com | E-mail |
| 29 | situacao_especial | "" | Situação Especial |
| 30 | data_situacao_especial | "" | Data (YYYYMMDD) |

**CNPJ Completo = cnpj_basico + cnpj_ordem + cnpj_dv**  
Exemplo: `08636546` + `0001` + `45` = `08636546000145`

---

### 9. SÓCIOS (8.4 milhões de registros)
**Colunas:** 11  
**Tamanho:** 868MB

```csv
"46010391";"2";"RICARDO HENRIQUE DA ROCHA";"***556256**";"49";"20220412";"";"***000000**";"";"00";"6"
```

| # | Campo | Exemplo | Descrição |
|---|-------|---------|-----------|
| 1 | cnpj_basico | 46010391 | CNPJ Básico (8 dígitos) |
| 2 | identificador_socio | 2 | Tipo: 1=PJ, 2=PF, 3=Estrangeiro |
| 3 | nome_socio | RICARDO HENRIQUE DA ROCHA | Nome/Razão Social |
| 4 | cpf_cnpj_socio | ***556256** | CPF/CNPJ (com asteriscos) |
| 5 | qualificacao_socio | 49 | Código da Qualificação |
| 6 | data_entrada_sociedade | 20220412 | Data (YYYYMMDD) |
| 7 | pais | "" | Código do País (se estrangeiro) |
| 8 | representante_legal | ***000000** | CPF do Representante |
| 9 | nome_representante | "" | Nome do Representante |
| 10 | qualificacao_representante | 00 | Código da Qualificação |
| 11 | faixa_etaria | 6 | Código da Faixa Etária |

---

### 10. SIMPLES NACIONAL (45.7 milhões de registros)
**Colunas:** 7  
**Tamanho:** 2.8GB

```csv
"00000000";"N";"20070701";"20070701";"N";"20090701";"20090701"
```

| # | Campo | Exemplo | Descrição |
|---|-------|---------|-----------|
| 1 | cnpj_basico | 00000000 | CNPJ Básico (8 dígitos) |
| 2 | opcao_simples | N | S=Sim, N=Não |
| 3 | data_opcao_simples | 20070701 | Data (YYYYMMDD) |
| 4 | data_exclusao_simples | 20070701 | Data (YYYYMMDD) |
| 5 | opcao_mei | N | S=Sim, N=Não |
| 6 | data_opcao_mei | 20090701 | Data (YYYYMMDD) |
| 7 | data_exclusao_mei | 20090701 | Data (YYYYMMDD) |

---

## 🔗 RELACIONAMENTOS

```
EMPRESAS (1) ----< (N) ESTABELECIMENTOS
   |                       |
   |                       |
   └----< (N) SÓCIOS      |
   |                       |
   └----< (1) SIMPLES     |
                           |
Natureza Jurídica >--------┘
Qualificações >-------------┘
Municípios >----------------┘
CNAEs >---------------------┘
Motivos >-------------------┘
Países >--------------------┘
```

---

## 📝 OBSERVAÇÕES IMPORTANTES

1. **Encoding:** `latin-1` (padrão da Receita)
2. **Delimiter:** `;` (ponto-e-vírgula)
3. **Quote:** `"` (aspas duplas)
4. **Valores vazios:** `""` (string vazia entre aspas)
5. **Dados mascarados:** Asteriscos `***` em CPFs
6. **Datas:** Formato `YYYYMMDD` (ex: 20220412)
7. **Capital Social:** Formato brasileiro com vírgula `0,00`
8. **CNAEs Secundários:** Separados por vírgula sem espaço
9. **Nome Fantasia vazio:** Asteriscos `******`

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Ajustar modelos SQLAlchemy com campos corretos
2. ✅ Criar migrations para todas as tabelas
3. ✅ Ajustar processor.py com mapeamento correto
4. ⏳ Testar ETL com arquivos pequenos
5. ⏳ Rodar ETL completo
