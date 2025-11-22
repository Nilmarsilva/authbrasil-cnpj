# AuthBrasil CNPJ
## Plataforma de Consulta Corporativa Avançada

**Tagline:** Dados atualizados, confiáveis e acessíveis via painel e API.

**Última atualização:** 22/11/2024  
**Status:** Planejamento Inicial  
**Versão do documento:** 1.0

---

## Índice

1. [Visão Geral do Produto](#1-visão-geral-do-produto)
2. [Metodologia de Desenvolvimento](#2-metodologia-de-desenvolvimento)
3. [Fases de Implementação](#3-fases-de-implementação)
4. [Stack Tecnológico](#4-stack-tecnológico)
5. [Arquitetura do Sistema](#5-arquitetura-do-sistema)
6. [Infraestrutura](#6-infraestrutura)
7. [Backend e API](#7-backend-e-api)
8. [Banco de Dados](#8-banco-de-dados)
9. [ETL e Atualização de Dados](#9-etl-e-atualização-de-dados)
10. [Faturamento](#10-faturamento)
11. [Landing Page](#11-landing-page)
12. [Documentação da API](#12-documentação-da-api)
13. [Dashboard do Cliente](#13-dashboard-do-cliente)
14. [Autenticação e Autorização](#14-autenticação-e-autorização)
15. [Domínios e DNS](#15-domínios-e-dns)
16. [Segurança](#16-segurança)
17. [Backlog Priorizado](#17-backlog-priorizado)
18. [Decisões Técnicas (ADR)](#18-decisões-técnicas-adr)
19. [Changelog de Desenvolvimento](#19-changelog-de-desenvolvimento)

---

## 1. Visão Geral do Produto

O AuthBrasil CNPJ é uma plataforma SaaS que oferece consulta profissional de dados corporativos brasileiros através de um painel web intuitivo e API REST robusta. Os dados são sincronizados mensalmente com a base oficial da Receita Federal.

**Proposta de valor:**
- Dados oficiais da Receita Federal processados e estruturados
- Acesso via painel web e API REST
- Atualizações mensais automáticas
- Performance otimizada com cache
- Planos flexíveis por volume de consultas

---

## 2. Metodologia de Desenvolvimento

### 2.1. Abordagem Ágil
- **Sprints semanais** com revisão aos domingos
- **Daily tracking** via documento único (este)
- **MVP-first approach** com entregas incrementais
- **Documentação contínua** no Projeto.md

### 2.2. Controle de Qualidade
- Testes unitários obrigatórios (pytest)
- Testes E2E para fluxos críticos (Playwright)
- Code review antes de merge
- CI/CD com GitHub Actions

### 2.3. Gestão de Código
- Repositório Git com branches protegidas
- Conventional Commits
- Versionamento semântico
- Changelog atualizado a cada release

---

## 3. Fases de Implementação

### Fase 1: MVP (4-6 semanas)
**Objetivo:** Validar viabilidade técnica e gerar primeiras receitas

- [ ] Importação manual de dados da Receita (Nov/2024)
- [ ] Backend FastAPI com endpoint GET /cnpj/{cnpj}
- [ ] Autenticação básica (email/senha)
- [ ] Dashboard simples com busca de CNPJ
- [ ] Landing page estática
- [ ] Stripe com 1 plano único (R$ 49/mês - 1000 consultas)
- [ ] Deploy em VPS com Docker

### Fase 2: Produto Completo (6-8 semanas)
**Objetivo:** Completar features core e escalar

- [ ] API REST completa com todos endpoints
- [ ] ETL automático mensal
- [ ] Sistema de múltiplos planos
- [ ] API keys e rate limiting
- [ ] Admin panel
- [ ] Documentação técnica da API
- [ ] Logs e monitoramento

### Fase 3: Otimização (4 semanas)
**Objetivo:** Performance e escalabilidade

- [ ] Cache Redis em todos endpoints
- [ ] Materialized views otimizadas
- [ ] CDN para assets estáticos
- [ ] Backup automático
- [ ] Testes de carga

### Fase 4: Growth (ongoing)
**Objetivo:** Crescimento e novas features

- [ ] Busca avançada com filtros
- [ ] Webhooks para clientes
- [ ] Exportação de relatórios
- [ ] Integrações (Zapier, etc)

---

## 4. Stack Tecnológico

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0
- **Validação:** Pydantic v2
- **Task Queue:** Celery + Redis
- **Testes:** pytest, pytest-asyncio

### Frontend
- **Framework:** Next.js 14 (App Router)
- **UI:** TailwindCSS + shadcn/ui
- **Ícones:** Lucide React
- **Forms:** React Hook Form + Zod
- **Testes:** Playwright

### Banco de Dados
- **Principal:** PostgreSQL 16
- **Cache:** Redis 7
- **Migrations:** Alembic

### DevOps
- **Containerização:** Docker + Docker Compose
- **Orquestração:** Docker Swarm
- **Proxy:** Nginx Proxy Manager
- **CI/CD:** GitHub Actions
- **Monitoramento:** Portainer, Logs centralizados

### Infraestrutura
- **Cloud:** VPS (Hostinger/Contabo/AWS Lightsail)
- **CDN/DNS:** Cloudflare
- **Pagamentos:** Stripe
- **Email:** SendGrid ou AWS SES

---

## 5. Arquitetura do Sistema

### 5.1. Módulos do Sistema

- Landing Page (marketing/vendas)
- Sistema de autenticação
- Dashboard do Cliente
- Módulo de consultas via painel
- API REST autenticada
- ETL mensal automático (importação dos dados da Receita)
- Admin Panel (gestão interna)
- Faturamento (Stripe)
- Logs e monitoramento
- Sistema de cache (Redis)

---

## 6. Infraestrutura

### 6.1. Especificações do Servidor

**VPS Recomendado:** Hostinger, Contabo ou AWS Lightsail

- **CPU:** 4 vCPUs
- **RAM:** 8 GB
- **Storage:** 150-200 GB SSD
- **OS:** Ubuntu 22.04 LTS

### 6.2. Componentes

- Docker + Docker Swarm
- Portainer (gestão de containers)
- Redis (cache)
- PostgreSQL (banco principal)
- Nginx Proxy Manager / Traefik
- Cloudflare DNS + WAF

### 6.3. Backup Strategy

- **Banco de dados:** Daily dump automático (retenção 30 dias)
- **Arquivos:** Backup semanal para S3-compatible storage
- **Disaster recovery:** Plano de restore testado mensalmente

---

## 7. Backend e API

### 7.1. Endpoints Principais

| Endpoint | Método | Descrição | Auth |
|----------|--------|-----------|------|
| `/auth/login` | POST | Login de usuário | Não |
| `/auth/signup` | POST | Cadastro de novo usuário | Não |
| `/auth/refresh` | POST | Renovar token JWT | Sim |
| `/cnpj/{cnpj}` | GET | Consulta completa de CNPJ | Sim |
| `/empresas/search` | GET | Busca avançada com filtros | Sim |
| `/socios/{cnpj}` | GET | Lista de sócios | Sim |
| `/atividade/{cnae}` | GET | Informações de CNAE | Sim |
| `/health` | GET | Status da API | Não |
| `/stripe/webhook` | POST | Webhook de pagamentos | Webhook |
| `/user/profile` | GET | Dados do usuário logado | Sim |
| `/user/usage` | GET | Estatísticas de uso | Sim |
| `/user/api-keys` | POST | Gerar nova API key | Sim |

### 7.2. Rate Limiting

- **Por IP (não autenticado):** 10 req/min
- **Por usuário (painel):** 60 req/min
- **Por API key:** Conforme plano contratado

### 7.3. Respostas Padrão

**Sucesso (200):**
```json
{
  "success": true,
  "data": {...},
  "metadata": {
    "cached": true,
    "timestamp": "2024-11-22T12:00:00Z"
  }
}
```

**Erro (4xx/5xx):**
```json
{
  "success": false,
  "error": {
    "code": "CNPJ_NOT_FOUND",
    "message": "CNPJ não encontrado na base de dados"
  }
}
```

---

## 8. Banco de Dados

### 8.1. Tabelas de Dados da Receita

**Tabelas principais (estrutura conforme dados abertos CNPJ):**

- `empresas` - Dados da matriz (CNPJ raiz)
- `estabelecimentos` - Dados de cada estabelecimento (filiais)
- `socios` - Quadro societário
- `simples` - Optantes pelo Simples Nacional
- `cnaes` - Códigos e descrições de atividades econômicas
- `municipios` - Códigos e nomes de municípios (IBGE)
- `paises` - Códigos e nomes de países
- `qualificacoes` - Qualificações de sócios

### 8.2. Tabelas do Sistema

- `users` - Usuários cadastrados
- `plans` - Planos disponíveis
- `subscriptions` - Assinaturas ativas/canceladas
- `api_keys` - Chaves de API geradas
- `usage_logs` - Log de uso por usuário/API key
- `billing_logs` - Histórico de cobranças

### 8.3. Views Materializadas

- `empresas_full` - Join otimizado de empresas + estabelecimentos + sócios
  - Atualizada após cada ETL
  - Indexada para busca rápida

---

## 9. ETL e Atualização de Dados

### 9.1. Fonte de Dados

**URL oficial da Receita Federal:**
- Base: `https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/`
- Mensal: `https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/<ANO-MES>/`
- Exemplo: `2025-11`

### 9.2. Pipeline do ETL

1. **Download**
   - Listar arquivos disponíveis na pasta do mês
   - Validar integridade (checksum quando disponível)
   - Baixar ZIPs em stream com progress bar

2. **Processamento**
   - Extrair arquivos em diretório temporário
   - Ler CSVs em chunks (100k registros)
   - Transformar e validar dados

3. **Carga**
   - Inserir no PostgreSQL em batches otimizados
   - Atualizar VIEW `empresas_full`
   - Criar índices se necessário

4. **Pós-processamento**
   - Limpar cache Redis
   - Registrar log de atualização em tabela
   - Enviar email interno com relatório de sucesso/erro
   - Limpar arquivos temporários

### 9.3. Agendamento

- **Scheduler:** Celery Beat
- **Frequência:** Mensal
- **Data:** Dia 10 de cada mês
- **Horário:** 02:00 AM (baixa demanda)
- **Retry:** 3 tentativas com backoff exponencial

---

## 10. Faturamento

### 10.1. Planos e Precificação

| Nome | Preço | Limite Mensal | Público-alvo |
|------|-------|---------------|--------------|
| **Starter** | R$ 29/mês | 500 consultas | MEI e pequenos negócios |
| **Pro** | R$ 79/mês | 5.000 consultas | Contadores e despachantes |
| **Enterprise** | R$ 249/mês | 50.000 consultas | Softwares e agências |
| **On Demand** | R$ 0,09/consulta | Ilimitado | Sistemas internos com uso variável |

### 10.2. Fluxo de Pagamento (Stripe)

1. Cliente clica em "Assinar" na landing page
2. Redirecionamento para Stripe Checkout
3. Stripe processa o pagamento
4. Webhook POST `/stripe/webhook` notifica o sistema
5. Sistema cria registro em `subscriptions`
6. Sistema gera `api_key` automaticamente
7. Cliente recebe email de boas-vindas com credenciais
8. Painel liberado para uso

### 10.3. Gestão de Cobranças

- Cobrança recorrente automática via Stripe
- Notificação 3 dias antes da renovação
- Suspensão automática em caso de falha de pagamento
- Histórico completo em `billing_logs`
- Notas fiscais emitidas via integração (Emitte ou similar)

---

## 11. Landing Page

### 11.1. Estrutura de Seções

1. **Hero Section**
   - Headline forte e clara
   - Subtítulo com proposta de valor
   - CTA principal (Teste Grátis / Ver Planos)
   - Screenshot do painel

2. **Sobre o Produto**
   - O que é o AuthBrasil CNPJ
   - Principais benefícios em bullet points
   - Trust indicators (dados oficiais, HTTPS, etc)

3. **Demonstração do Painel**
   - GIF ou vídeo curto mostrando busca de CNPJ
   - Destaque para UX limpa e rápida

4. **Demonstração da API**
   - Code snippet de exemplo
   - Botão "Ver Documentação"

5. **Planos e Preços**
   - Cards de planos lado a lado
   - CTAs "Assinar Agora"
   - Destaque para plano recomendado

6. **Comparação com Concorrentes**
   - Tabela simples: Nós vs Outros
   - Foco em: preço, atualização, performance, suporte

7. **Garantia e Confiabilidade**
   - Uptime garantido
   - Dados oficiais
   - Suporte por email

8. **FAQ**
   - 5-7 perguntas frequentes

9. **Footer**
   - Links: Documentação, API, Termos, Privacidade
   - Redes sociais (se houver)
   - Contato

### 11.2. Copy Sugerido

**Hero Headline:**
> "Consulta CNPJ instantânea, completa e atualizada — via API e Painel"

**Subheadline:**
> "Dados oficiais da Receita Federal, processados e organizados para uso profissional"

---

## 12. Documentação da API

### 12.1. Estrutura do Developer Portal

1. **Introdução**
   - Overview da API
   - Casos de uso
   - Quick start

2. **Autenticação**
   - Como obter API key
   - Header de autenticação
   - Segurança

3. **Endpoints**
   - Lista completa com exemplos
   - Request/response schemas
   - Códigos de erro

4. **Exemplos de Código**
   - Python
   - JavaScript/Node.js
   - PHP
   - C#
   - cURL

5. **Rate Limiting**
   - Limites por plano
   - Headers de controle
   - Throttling

6. **Webhooks** (futuro)
   - Configuração
   - Eventos disponíveis

7. **Versionamento**
   - Política de versões
   - Changelog da API

### 12.2. Exemplo de Consulta

```bash
GET https://api.authbrasil.com/cnpj/12345678000190
Headers:
  Authorization: Bearer SUA_API_KEY
```

---

## 13. Dashboard do Cliente

### 13.1. Funcionalidades

**Página: Overview**
- Resumo da assinatura (plano, validade)
- Gráfico de consumo mensal
- Alertas (limite próximo, renovação, etc)

**Página: Consultas**
- Busca de CNPJ via painel web
- Visualização de dados completos
- Download de relatórios (CSV/PDF)
- Histórico de consultas recentes

**Página: API**
- Visualizar API key atual
- Gerar nova API key
- Revogar keys antigas
- Estatísticas de uso da API

**Página: Faturamento**
- Histórico de cobranças
- Próxima cobrança
- Alterar método de pagamento
- Download de notas fiscais

**Página: Configurações**
- Dados cadastrais
- Alterar senha
- 2FA (opcional)
- Preferências de notificação

**Página: Suporte**
- Formulário de contato
- FAQ integrado
- Link para documentação

---

## 14. Autenticação e Autorização

### 14.1. Sistema RBAC (Role-Based Access Control)

**Níveis de acesso:**
- **Admin** - Acesso total ao sistema e admin panel
- **Cliente** - Acesso ao próprio dashboard e API
- **ETL Worker** - Token interno para jobs automatizados

### 14.2. Tecnologias

- **JWT** (JSON Web Tokens)
  - Access token: 15 minutos de validade
  - Refresh token: 7 dias de validade
  
- **Password hashing:** bcrypt ou Argon2

- **2FA opcional:** TOTP (Google Authenticator, Authy)

### 14.3. Fluxo de Autenticação

1. Login (email + senha)
2. Sistema valida credenciais
3. Retorna access_token e refresh_token
4. Cliente usa access_token em todas as requisições
5. Quando expirar, usa refresh_token para renovar
6. Logout invalida refresh_token

---

## 15. Domínios e DNS

### 15.1. Estrutura de Domínios

- **Principal:** `authbrasil.com.br`
- **API:** `api.authbrasil.com.br` ou `cnpj.authbrasil.com.br`
- **Dashboard:** `painel.authbrasil.com.br` ou `app.authbrasil.com.br`
- **Docs:** `docs.authbrasil.com.br`

### 15.2. Configuração DNS (Cloudflare)

- Proxied: Sim (CDN + WAF + DDoS protection)
- SSL/TLS: Full (strict)
- Always HTTPS: Habilitado
- HTTP/3: Habilitado
- Auto Minify: JS, CSS, HTML

---

## 16. Segurança

### 16.1. OWASP Top 10 Mitigations

- **Injection:** Prepared statements, validação de input
- **Broken Auth:** JWT + 2FA, rate limiting em login
- **Sensitive Data:** HTTPS everywhere, env vars para secrets
- **XXE:** Desabilitar XML entity processing
- **Broken Access Control:** RBAC implementado corretamente
- **Security Misconfiguration:** Headers de segurança configurados
- **XSS:** Content Security Policy, sanitização de output
- **Insecure Deserialization:** Validação com Pydantic
- **Components with Vulnerabilities:** Dependabot ativado
- **Logging & Monitoring:** Logs centralizados, alertas

### 16.2. Headers de Segurança

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### 16.3. Rate Limiting

- Por IP: 100 req/min (geral)
- Login: 5 tentativas / 15 min
- API: Conforme plano contratado
- Admin panel: Whitelist de IPs

### 16.4. Compliance

- **LGPD:** Mesmo sendo dados públicos, ter termo de uso claro
- **Logs:** Não armazenar dados sensíveis em logs
- **Backup:** Criptografado em repouso

---

## 17. Backlog Priorizado

### Sprint 1 (Semana 1-2)
- [ ] Estruturar repositório Git
- [ ] Configurar ambiente de desenvolvimento
- [ ] Criar modelos SQLAlchemy básicos
- [ ] Implementar ETL manual (importação inicial)
- [ ] Endpoint GET /cnpj/{cnpj}

### Sprint 2 (Semana 3-4)
- [ ] Sistema de autenticação completo
- [ ] Dashboard frontend básico (Next.js)
- [ ] Integração Stripe (1 plano)
- [ ] Landing page estática

### Sprint 3 (Semana 5-6)
- [ ] Deploy em VPS
- [ ] CI/CD com GitHub Actions
- [ ] Configuração de domínios
- [ ] Testes E2E básicos

### Backlog Futuro
- [ ] API REST completa
- [ ] ETL automático
- [ ] Admin panel
- [ ] Múltiplos planos
- [ ] Documentação da API
- [ ] Busca avançada
- [ ] Webhooks

---

## 18. Decisões Técnicas (ADR)

### ADR-001: Escolha de FastAPI sobre Flask/Django
**Data:** 22/11/2024  
**Status:** Aceito  
**Contexto:** Precisamos de performance e tipagem forte  
**Decisão:** FastAPI com Pydantic  
**Consequências:** Performance superior, documentação automática, async nativo

### ADR-002: PostgreSQL como banco principal
**Data:** 22/11/2024  
**Status:** Aceito  
**Contexto:** Dados relacionais complexos com milhões de registros  
**Decisão:** PostgreSQL 16  
**Consequências:** Suporte a JSON, materialized views, excelente performance

### ADR-003: Next.js para frontend
**Data:** 22/11/2024  
**Status:** Aceito  
**Contexto:** Precisa de SEO para landing page e app dinâmico  
**Decisão:** Next.js 14 com App Router  
**Consequências:** SSR/SSG para SEO, React para dashboard interativo

---

## 19. Changelog de Desenvolvimento

### 2024-11-22 - Inicialização do Projeto
- Criação do documento de especificação
- Definição da arquitetura
- Planejamento de fases
- Estruturação de metodologia

