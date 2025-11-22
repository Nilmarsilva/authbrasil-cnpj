# Próximos Passos - AuthBrasil CNPJ

## Status Atual

Repositório Git inicializado com sucesso.

**Commit inicial:** `df52a91 - chore: estrutura inicial do projeto AuthBrasil CNPJ`  
**Branch:** `main`

## Para Conectar ao GitHub

### 1. Criar Repositório no GitHub

Acesse: https://github.com/new

**Configurações recomendadas:**
- **Nome do repositório:** `authbrasil-cnpj`
- **Descrição:** "Plataforma SaaS de consulta de dados corporativos brasileiros via API e painel web"
- **Visibilidade:** Private (por ser projeto pessoal em desenvolvimento)
- **NÃO** marque nenhuma opção de inicialização (README, .gitignore, licença)

### 2. Conectar o Repositório Local ao GitHub

Após criar o repositório no GitHub, execute os seguintes comandos:

```powershell
# Substitua SEU_USERNAME pelo seu username do GitHub
git remote add origin https://github.com/SEU_USERNAME/authbrasil-cnpj.git

# Fazer push do commit inicial
git push -u origin main
```

**Ou via SSH (se configurado):**

```powershell
git remote add origin git@github.com:SEU_USERNAME/authbrasil-cnpj.git
git push -u origin main
```

### 3. Verificar Conexão

```powershell
git remote -v
```

Deve mostrar:
```
origin  https://github.com/SEU_USERNAME/authbrasil-cnpj.git (fetch)
origin  https://github.com/SEU_USERNAME/authbrasil-cnpj.git (push)
```

## Estrutura Criada

```
authbrasil-cnpj/
├── .github/
│   └── workflows/        # CI/CD workflows (a criar)
├── backend/              # API FastAPI (a implementar)
├── docs/                 # Documentação técnica
├── frontend/             # Dashboard Next.js (a implementar)
├── infra/
│   └── docker/          # Docker compose e configs
├── scripts/             # Scripts utilitários e ETL
├── .env.example         # Template de variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo Git
├── CHANGELOG.md         # Histórico de mudanças
├── Projeto.md           # Especificação completa
├── PROXIMOS_PASSOS.md   # Este arquivo
└── README.md            # Documentação principal
```

## Workflow de Desenvolvimento Recomendado

### Branches

- **main** - Branch principal (produção)
- **develop** - Branch de desenvolvimento
- **feature/** - Features em desenvolvimento
- **hotfix/** - Correções urgentes

### Conventional Commits

Utilize o padrão de commits semânticos:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Tarefas gerais

**Exemplos:**
```
feat(backend): adicionar endpoint de consulta CNPJ
fix(frontend): corrigir validação de formulário
docs: atualizar README com instruções de setup
```

## Próximas Ações Recomendadas

### Sprint 1 - Semana 1-2

1. **Configurar ambiente de desenvolvimento**
   - [ ] Instalar Python 3.11+
   - [ ] Instalar Node.js 18+
   - [ ] Instalar Docker
   - [ ] Instalar PostgreSQL local ou usar Docker

2. **Backend - Estrutura Base**
   - [ ] Criar `backend/requirements.txt`
   - [ ] Configurar FastAPI
   - [ ] Configurar SQLAlchemy
   - [ ] Criar modelos de dados básicos
   - [ ] Configurar Alembic (migrations)

3. **Banco de Dados**
   - [ ] Criar schema do PostgreSQL
   - [ ] Definir tabelas conforme Projeto.md seção 8
   - [ ] Criar migration inicial

4. **ETL Manual**
   - [ ] Criar script para download dos dados da Receita
   - [ ] Implementar parser de CSVs
   - [ ] Importar dados para PostgreSQL

5. **API Básica**
   - [ ] Endpoint GET /health
   - [ ] Endpoint GET /cnpj/{cnpj}
   - [ ] Documentação automática (Swagger)

### Sprint 2 - Semana 3-4

1. **Autenticação**
   - [ ] Implementar registro de usuário
   - [ ] Implementar login com JWT
   - [ ] Middleware de autenticação

2. **Frontend Base**
   - [ ] Inicializar projeto Next.js
   - [ ] Configurar TailwindCSS
   - [ ] Instalar shadcn/ui
   - [ ] Criar layout base

3. **Integração Stripe**
   - [ ] Configurar conta Stripe (modo test)
   - [ ] Implementar webhook
   - [ ] Criar fluxo de pagamento básico

## Recursos Úteis

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Stripe API](https://stripe.com/docs/api)
- [Conventional Commits](https://www.conventionalcommits.org/pt-br/)

## Observações Importantes

1. **Não commitar secrets:** Sempre use `.env` para variáveis sensíveis
2. **Testar antes de commitar:** Garanta que o código funciona
3. **Documentar mudanças:** Atualizar CHANGELOG.md regularmente
4. **Code review:** Mesmo sendo projeto pessoal, revisar código antes de merge
5. **Backup regular:** Fazer push para GitHub frequentemente

## Contato e Suporte

Este é um projeto pessoal em desenvolvimento ativo.

---

**Última atualização:** 22/11/2024  
**Versão:** 0.1.0
