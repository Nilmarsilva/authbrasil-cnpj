# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Em Desenvolvimento
- Importação manual de dados da Receita Federal (ETL)
- Sistema de autenticação JWT
- Rate limiting
- Cache Redis
- Testes unitários

### Implementado (não lançado)
- Estrutura completa do backend FastAPI
- Modelos SQLAlchemy para todas as tabelas
- Endpoints básicos (/health, /cnpj)
- Configuração Alembic para migrations
- Docker Compose para desenvolvimento local

## [0.1.0] - 2024-11-22

### Adicionado
- Especificação completa do projeto (Projeto.md)
- Estrutura de diretórios do repositório
- Documentação inicial (README.md)
- Definição de metodologia ágil
- Planejamento de fases de implementação
- Stack tecnológico definido
- Arquitetura do sistema documentada
- Backlog priorizado
- Decisões técnicas (ADRs) iniciais
- Este arquivo CHANGELOG

### Decisões Técnicas
- ADR-001: FastAPI como framework backend
- ADR-002: PostgreSQL como banco de dados principal
- ADR-003: Next.js para frontend

---

## Tipos de Mudanças

- **Adicionado** - para novas funcionalidades
- **Modificado** - para mudanças em funcionalidades existentes
- **Descontinuado** - para funcionalidades que serão removidas
- **Removido** - para funcionalidades removidas
- **Corrigido** - para correções de bugs
- **Segurança** - para vulnerabilidades corrigidas
