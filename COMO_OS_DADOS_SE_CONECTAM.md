# 🔗 Como os Dados da Receita Federal se Conectam

## 📊 VISÃO GERAL

Imagine que você tem uma empresa chamada **"PADARIA DO ZÉ LTDA"**:

```
PADARIA DO ZÉ LTDA
├── CNPJ: 12.345.678/0001-90 (Matriz em São Paulo)
├── CNPJ: 12.345.678/0002-71 (Filial 1 em Campinas)
└── CNPJ: 12.345.678/0003-52 (Filial 2 no Rio)
```

Os dados da Receita separam isso em **4 arquivos diferentes**:

---

## 🎯 A TABELA CENTRAL: EMPRESAS

**Arquivo:** `Empresas0.zip` (e Empresas1, Empresas2... até Empresas9)

```
┌─────────────────────────────────────────────────────┐
│              TABELA: EMPRESAS                       │
│                                                     │
│  cnpj_basico: 12345678  ◄──── CHAVE PRINCIPAL     │
│  razao_social: PADARIA DO ZÉ LTDA                  │
│  natureza_juridica: 2062 (LTDA)                    │
│  capital_social: 50000,00                          │
│  porte_empresa: 01 (Micro Empresa)                 │
└─────────────────────────────────────────────────────┘
```

**✅ REGRA:** Uma linha em EMPRESAS = Uma razão social (matriz)  
**🔑 CHAVE:** `cnpj_basico` (8 primeiros dígitos do CNPJ)

---

## 🏢 AS FILIAIS: ESTABELECIMENTOS

**Arquivo:** `Estabelecimentos0.zip` até `Estabelecimentos9.zip`

Aqui ficam **TODOS os endereços** (matriz + filiais):

```
┌────────────────────────────────────────────────────────────────┐
│           TABELA: ESTABELECIMENTOS (Matriz)                   │
│                                                                │
│  cnpj_basico: 12345678  ◄──── Liga com EMPRESAS              │
│  cnpj_ordem:  0001                                            │
│  cnpj_dv:     90                                              │
│  matriz_filial: 1 (Matriz)                                    │
│  nome_fantasia: PADARIA DO ZÉ - CENTRO                       │
│  logradouro: RUA DAS FLORES                                   │
│  numero: 123                                                   │
│  municipio: 7107 ◄──── Liga com MUNICIPIOS                   │
│  cnae_principal: 1091201 ◄──── Liga com CNAES                │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│         TABELA: ESTABELECIMENTOS (Filial 1)                   │
│                                                                │
│  cnpj_basico: 12345678  ◄──── MESMO cnpj_basico!             │
│  cnpj_ordem:  0002      ◄──── Ordem diferente                │
│  cnpj_dv:     71                                              │
│  matriz_filial: 2 (Filial)                                    │
│  nome_fantasia: PADARIA DO ZÉ - CAMPINAS                     │
│  logradouro: AV BRASIL                                        │
│  numero: 456                                                   │
│  municipio: 6291 ◄──── Código diferente (Campinas)           │
└────────────────────────────────────────────────────────────────┘
```

**✅ REGRA:** Várias linhas em ESTABELECIMENTOS = Vários CNPJs da mesma empresa  
**🔑 CHAVE:** `cnpj_basico` + `cnpj_ordem` + `cnpj_dv`  
**🔗 RELACIONAMENTO:** `cnpj_basico` conecta com EMPRESAS

---

## 👥 OS DONOS: SÓCIOS

**Arquivo:** `Socios0.zip` até `Socios9.zip`

```
┌────────────────────────────────────────────────────────────────┐
│              TABELA: SÓCIOS (Sócio 1)                         │
│                                                                │
│  cnpj_basico: 12345678  ◄──── Liga com EMPRESAS              │
│  nome_socio: JOSÉ DA SILVA                                    │
│  cpf_cnpj_socio: ***123456**                                  │
│  qualificacao_socio: 49 ◄──── Liga com QUALIFICACOES         │
│  data_entrada: 20200115                                       │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│              TABELA: SÓCIOS (Sócio 2)                         │
│                                                                │
│  cnpj_basico: 12345678  ◄──── MESMO cnpj_basico!             │
│  nome_socio: MARIA OLIVEIRA                                   │
│  cpf_cnpj_socio: ***789012**                                  │
│  qualificacao_socio: 22 ◄──── Código diferente               │
│  data_entrada: 20200115                                       │
└────────────────────────────────────────────────────────────────┘
```

**✅ REGRA:** Várias linhas em SÓCIOS = Vários donos da mesma empresa  
**🔗 RELACIONAMENTO:** `cnpj_basico` conecta com EMPRESAS

---

## 📋 SIMPLES NACIONAL

**Arquivo:** `Simples.zip`

```
┌────────────────────────────────────────────────────────────────┐
│              TABELA: SIMPLES                                  │
│                                                                │
│  cnpj_basico: 12345678  ◄──── Liga com EMPRESAS              │
│  opcao_simples: S (É optante do Simples)                     │
│  data_opcao_simples: 20200201                                │
│  opcao_mei: N (Não é MEI)                                     │
└────────────────────────────────────────────────────────────────┘
```

**✅ REGRA:** Uma linha em SIMPLES = Uma empresa (pode ou não ser optante)  
**🔗 RELACIONAMENTO:** `cnpj_basico` conecta com EMPRESAS

---

## 📚 TABELAS AUXILIARES (Dicionários)

Essas tabelas são como **dicionários** que traduzem códigos em descrições:

### 1. CNAES - Traduz atividade econômica
```
Código: 1091201
         ↓
"Fabricação de produtos de panificação"
```

### 2. MUNICIPIOS - Traduz código IBGE
```
Código: 7107
         ↓
"São Paulo/SP"
```

### 3. NATUREZAS - Traduz tipo de empresa
```
Código: 2062
         ↓
"Sociedade Empresária Limitada"
```

### 4. QUALIFICACOES - Traduz cargo do sócio
```
Código: 49
         ↓
"Sócio-Administrador"
```

### 5. MOTIVOS - Traduz situação cadastral
```
Código: 63
         ↓
"Omissão Contumaz"
```

### 6. PAISES - Traduz país
```
Código: 105
         ↓
"Brasil"
```

---

## 🎨 DIAGRAMA COMPLETO

```
                    ┌─────────────────────┐
                    │      EMPRESAS       │
                    │ (Dados da Matriz)   │
                    │                     │
                    │ PK: cnpj_basico     │
                    └──────────┬──────────┘
                               │
                               │ cnpj_basico
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           │                   │                   │
           ▼                   ▼                   ▼
   ┌───────────────┐   ┌──────────────┐   ┌──────────────┐
   │ESTABELECIMENTOS│  │    SÓCIOS    │   │   SIMPLES    │
   │ (Filiais)      │  │   (Donos)    │   │  (Regime)    │
   │                │  │              │   │              │
   │FK: cnpj_basico │  │FK:cnpj_basico│   │FK:cnpj_basico│
   └───────┬────────┘  └──────┬───────┘   └──────────────┘
           │                  │
           │                  │
           ▼                  ▼
    ┌──────────────┐   ┌─────────────────┐
    │  MUNICIPIOS  │   │  QUALIFICACOES  │
    │   (Lookup)   │   │    (Lookup)     │
    └──────────────┘   └─────────────────┘
           │                  
           ▼                  
    ┌──────────────┐   
    │    CNAES     │   
    │   (Lookup)   │   
    └──────────────┘   
           │
           ▼
    ┌──────────────┐
    │  NATUREZAS   │
    │   (Lookup)   │
    └──────────────┘
           │
           ▼
    ┌──────────────┐
    │   MOTIVOS    │
    │   (Lookup)   │
    └──────────────┘
           │
           ▼
    ┌──────────────┐
    │    PAISES    │
    │   (Lookup)   │
    └──────────────┘
```

**Legenda:**
- `PK` = Primary Key (Chave Primária)
- `FK` = Foreign Key (Chave Estrangeira)
- `┌──┐` = Tabela
- `│` e `─` = Relacionamento

---

## 🔍 EXEMPLO PRÁTICO: Consultando CNPJ Completo

Vamos buscar o CNPJ **12.345.678/0001-90**:

### PASSO 1: Separar o CNPJ
```
12.345.678 / 0001 - 90
    ↓         ↓     ↓
 básico    ordem   DV
```

### PASSO 2: Buscar na EMPRESAS
```sql
SELECT * FROM empresas WHERE cnpj_basico = '12345678'
```
**Retorna:** Razão social, natureza jurídica, capital social

### PASSO 3: Buscar no ESTABELECIMENTOS
```sql
SELECT * FROM estabelecimentos 
WHERE cnpj_basico = '12345678' 
  AND cnpj_ordem = '0001' 
  AND cnpj_dv = '90'
```
**Retorna:** Endereço, telefone, email, CNAEs

### PASSO 4: Buscar SÓCIOS
```sql
SELECT * FROM socios WHERE cnpj_basico = '12345678'
```
**Retorna:** Todos os sócios da empresa (podem ser vários)

### PASSO 5: Buscar SIMPLES
```sql
SELECT * FROM simples WHERE cnpj_basico = '12345678'
```
**Retorna:** Se é optante do Simples/MEI

### PASSO 6: Traduzir códigos (JOINS)
```sql
SELECT 
    e.razao_social,
    n.descricao as natureza_juridica_nome,
    est.logradouro,
    m.descricao as municipio_nome,
    c.descricao as cnae_descricao
FROM empresas e
JOIN estabelecimentos est ON e.cnpj_basico = est.cnpj_basico
JOIN naturezas n ON e.natureza_juridica = n.codigo
JOIN municipios m ON est.municipio = m.codigo
JOIN cnaes c ON est.cnae_principal = c.codigo
WHERE e.cnpj_basico = '12345678'
  AND est.cnpj_ordem = '0001'
  AND est.cnpj_dv = '90'
```

---

## 💡 RESUMO SIMPLES

1. **EMPRESAS** = A empresa (razão social)
   - Chave: `cnpj_basico` (8 dígitos)

2. **ESTABELECIMENTOS** = Os endereços (matriz + filiais)
   - Chave: `cnpj_basico` + `cnpj_ordem` + `cnpj_dv`
   - Conecta com EMPRESAS via `cnpj_basico`

3. **SÓCIOS** = Os donos
   - Conecta com EMPRESAS via `cnpj_basico`

4. **SIMPLES** = Regime tributário
   - Conecta com EMPRESAS via `cnpj_basico`

5. **Tabelas auxiliares** = Traduzem códigos em textos legíveis

---

## 🎯 IMPORTANTE!

**Todos os arquivos compartilham o mesmo `cnpj_basico`!**

```
┌─────────────────────────────────────────────────┐
│  cnpj_basico = 12345678                         │
│                                                 │
│  ├── EMPRESAS: 1 linha (a empresa)             │
│  ├── ESTABELECIMENTOS: 3 linhas (matriz+filiais)│
│  ├── SÓCIOS: 2 linhas (2 donos)                │
│  └── SIMPLES: 1 linha (dados do regime)        │
└─────────────────────────────────────────────────┘
```

É como se o `cnpj_basico` fosse um **RG da empresa** que aparece em todas as fichas!

---

**Agora ficou claro como tudo se conecta?** 🚀
