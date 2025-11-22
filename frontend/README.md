# AuthBrasil CNPJ - Frontend

Frontend Next.js 14 para a plataforma AuthBrasil CNPJ.

## 🚀 Tecnologias

- **Next.js 14** (App Router)
- **TypeScript**
- **TailwindCSS**
- **shadcn/ui**
- **Lucide React** (ícones)
- **React Hook Form + Zod**

## 📦 Instalação

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Iniciar produção
npm start
```

## 🌐 Variáveis de Ambiente

Copie `.env.example` para `.env.local`:

```bash
cp .env.example .env.local
```

Edite `.env.local` com suas configurações:

```
NEXT_PUBLIC_API_URL=https://api.authbrasil.app.br
```

## 📁 Estrutura

```
frontend/
├── src/
│   ├── app/              # Pages (App Router)
│   ├── components/       # Componentes reutilizáveis
│   ├── lib/             # Utilit\u00e1rios e configs
│   └── hooks/           # Custom hooks
├── public/              # Assets est\u00e1ticos
└── ...configs
```

## 🎨 Páginas

### Landing Page
- `/` - Homepage com Hero, Features, Pricing, CTA

### Dashboard  
- `/app` - Overview do dashboard
- `/app/consultas` - Busca de CNPJ
- `/app/api` - Gerenciamento de API keys
- `/app/faturamento` - Histórico de cobranças
- `/app/configuracoes` - Configurações do usuário

### Autenticação
- `/login` - Login de usuário
- `/signup` - Cadastro de novo usuário

## 🧪 Testes

```bash
npm test
```

## 📝 Lint

```bash
npm run lint
```

## 🚀 Deploy

O frontend será deployado via Docker Swarm na VPS junto com o backend.

Ver `DEPLOY_COMMANDS.md` na raiz do projeto para instruções.
