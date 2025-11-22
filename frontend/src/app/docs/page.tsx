import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { Code, Key, Lock, Zap } from "lucide-react"

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="pt-24 pb-20 px-4">
        <div className="container mx-auto max-w-5xl">
          {/* Hero */}
          <div className="text-center mb-16">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-gray-900 via-emerald-800 to-blue-900 bg-clip-text text-transparent">
              Documentação da API
            </h1>
            <p className="text-xl text-gray-600">
              Integre rapidamente com nossa API REST. Simples, rápida e confiável.
            </p>
          </div>

          {/* Quick Start */}
          <section className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Quick Start</h2>
            
            <div className="bg-white/50 backdrop-blur-sm rounded-xl p-8 border border-gray-200 mb-6">
              <div className="flex items-start gap-4 mb-4">
                <div className="bg-emerald-100 p-3 rounded-lg">
                  <Key className="w-6 h-6 text-emerald-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">1. Obtenha sua API Key</h3>
                  <p className="text-gray-600">
                    Após criar sua conta, acesse o painel e gere sua chave de API.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white/50 backdrop-blur-sm rounded-xl p-8 border border-gray-200 mb-6">
              <div className="flex items-start gap-4 mb-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <Code className="w-6 h-6 text-blue-600" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">2. Faça sua primeira requisição</h3>
                  <p className="text-gray-600 mb-4">
                    Use sua API key no header de autorização:
                  </p>
                  <div className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto">
                    <pre className="text-sm">
{`curl -X GET https://api.authbrasil.app.br/api/v1/cnpj/12345678000190 \\
  -H "Authorization: Bearer SUA_API_KEY"`}
                    </pre>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/50 backdrop-blur-sm rounded-xl p-8 border border-gray-200">
              <div className="flex items-start gap-4 mb-4">
                <div className="bg-purple-100 p-3 rounded-lg">
                  <Zap className="w-6 h-6 text-purple-600" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">3. Receba os dados</h3>
                  <p className="text-gray-600 mb-4">
                    Resposta em JSON com todos os dados da empresa:
                  </p>
                  <div className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto">
                    <pre className="text-sm">
{`{
  "success": true,
  "data": {
    "cnpj": "12.345.678/0001-90",
    "razao_social": "EMPRESA EXEMPLO LTDA",
    "nome_fantasia": "Exemplo",
    "situacao": "ATIVA",
    "tipo": "MATRIZ",
    "porte": "MICRO EMPRESA",
    "natureza_juridica": "206-2 - Sociedade Empresária Limitada",
    "cnae_principal": {
      "codigo": "6201-5/00",
      "descricao": "Desenvolvimento de programas de computador sob encomenda"
    },
    "endereco": { ... },
    "socios": [ ... ]
  }
}`}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Endpoints */}
          <section className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Principais Endpoints</h2>
            
            <div className="space-y-4">
              {[
                {
                  method: "GET",
                  endpoint: "/api/v1/cnpj/{cnpj}",
                  description: "Consulta completa de CNPJ com todos os dados"
                },
                {
                  method: "GET",
                  endpoint: "/api/v1/health",
                  description: "Status da API"
                },
                {
                  method: "GET",
                  endpoint: "/api/v1/user/usage",
                  description: "Estatísticas de uso da sua conta"
                },
              ].map((endpoint, index) => (
                <div key={index} className="bg-white/50 backdrop-blur-sm rounded-xl p-6 border border-gray-200">
                  <div className="flex items-center gap-4 mb-2">
                    <span className="bg-emerald-100 text-emerald-700 text-xs font-mono font-semibold px-3 py-1 rounded">
                      {endpoint.method}
                    </span>
                    <code className="text-sm font-mono text-gray-700">{endpoint.endpoint}</code>
                  </div>
                  <p className="text-gray-600 text-sm">{endpoint.description}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Authentication */}
          <section className="mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Autenticação</h2>
            
            <div className="bg-white/50 backdrop-blur-sm rounded-xl p-8 border border-gray-200">
              <div className="flex items-start gap-4">
                <div className="bg-red-100 p-3 rounded-lg">
                  <Lock className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">Bearer Token</h3>
                  <p className="text-gray-600 mb-4">
                    Todas as requisições autenticadas devem incluir o header:
                  </p>
                  <div className="bg-gray-900 text-gray-100 rounded-lg p-4">
                    <code className="text-sm">Authorization: Bearer SUA_API_KEY</code>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Rate Limiting */}
          <section>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Rate Limiting</h2>
            
            <div className="bg-white/50 backdrop-blur-sm rounded-xl p-8 border border-gray-200">
              <p className="text-gray-600 mb-4">
                Os limites de requisições variam conforme seu plano:
              </p>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full"></span>
                  <strong>Starter:</strong> 500 requisições/mês
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                  <strong>Pro:</strong> 5.000 requisições/mês
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                  <strong>Enterprise:</strong> 50.000 requisições/mês
                </li>
              </ul>
            </div>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  )
}
