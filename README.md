# AuthBrasil CNPJ

Plataforma de Consulta Corporativa Avançada - Dados atualizados, confiáveis e acessíveis via painel e API.

## Sobre o Projeto

O AuthBrasil CNPJ é uma plataforma SaaS que oferece consulta profissional de dados corporativos brasileiros através de um painel web intuitivo e API REST robusta. Os dados são sincronizados mensalmente com a base oficial da Receita Federal, contendo CNPJ e também MEI.

## Proposta de Valor

- Dados oficiais da Receita Federal processados e estruturados
- Acesso via painel web e API REST
- Atualizações mensais automáticas
- Performance otimizada com cache
- Planos flexíveis por volume de consultas

## Stack Tecnológico

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL 16
- Redis 7
- Celery
- SQLAlchemy 2.0

### Frontend
- Next.js 14
- TailwindCSS
- shadcn/ui
- React Hook Form

### Infraestrutura
- Docker + Docker Swarm
- Nginx Proxy Manager
- Cloudflare (CDN/DNS)
- GitHub Actions (CI/CD)

## Estrutura do Projeto

```
authbrasil-cnpj/
├── backend/          # API FastAPI
├── frontend/         # Dashboard Next.js
├── docs/            # Documentação técnica
├── infra/           # Docker, scripts de deploy
├── scripts/         # Utilitários e ETL
├── .github/         # GitHub Actions workflows
├── Projeto.md       # Especificação completa do projeto
├── CHANGELOG.md     # Histórico de mudanças
└── README.md        # Este arquivo
```

## Status do Projeto

**Versão:** 0.1.0  
**Status:** Planejamento Inicial  
**Última atualização:** 22/11/2024

## Fases de Desenvolvimento

- **Fase 1 (MVP):** 4-6 semanas - Validação técnica e primeiras receitas
- **Fase 2 (Produto Completo):** 6-8 semanas - Features core e escalabilidade
- **Fase 3 (Otimização):** 4 semanas - Performance e estabilidade
- **Fase 4 (Growth):** Ongoing - Novas features e crescimento

## Documentação

Para documentação completa, consulte:
- [Projeto.md](./Projeto.md) - Especificação técnica completa
- [CHANGELOG.md](./CHANGELOG.md) - Histórico de desenvolvimento

## Contato

**Projeto pessoal** - Desenvolvimento em andamento

## Licença

Proprietary - Todos os direitos reservados
