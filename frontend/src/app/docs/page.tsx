import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { Code, Key, Lock, Zap, CheckCircle, Database, Shield } from "lucide-react"
import Link from "next/link"

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <main className="pt-24 pb-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            {/* Breadcrumb */}
            <nav className="mb-8 text-sm text-gray-600">
              <Link href="/" className="hover:text-emerald-600">Home</Link>
              <span className="mx-2">/</span>
              <span className="text-gray-900 font-medium">Documentação</span>
            </nav>

            {/* Visão Geral */}
            <section className="mb-16">
              <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">
                AuthBrasil CNPJ API
              </h1>
              
              <p className="text-xl text-gray-600 mb-12">
                API completa para consultas de CNPJ automatizadas no Brasil
              </p>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">Visão Geral</h2>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-4">O que é a AuthBrasil CNPJ API?</h3>
              
              <p className="text-gray-700 mb-6 leading-relaxed">
                A AuthBrasil CNPJ API fornece acesso programático a dados oficiais da Receita Federal sobre empresas brasileiras. 
                Com ela, você pode consultar informações completas de CNPJ, incluindo dados cadastrais, sócios, atividades econômicas e muito mais.
              </p>

              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700"><strong>Consultas por CNPJ:</strong> Busque dados completos de qualquer empresa brasileira</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700"><strong>Dados atualizados:</strong> Sincronização mensal com a base da Receita Federal</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700"><strong>Performance otimizada:</strong> Respostas em menos de 100ms com cache inteligente</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700"><strong>API REST:</strong> Fácil integração com qualquer linguagem de programação</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-700"><strong>Dados estruturados:</strong> Respostas em JSON padronizadas e completas</span>
                </li>
              </ul>
            </section>

            {/* Casos de Uso */}
            <section className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Casos de Uso Principais</h3>
              
              <div className="space-y-6">
                <div className="border-l-4 border-emerald-500 pl-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">1. Escritórios de Contabilidade</h4>
                  <ul className="space-y-1 text-gray-700">
                    <li>• Validação de dados de clientes</li>
                    <li>• Consulta rápida de informações fiscais</li>
                    <li>• Verificação de situação cadastral</li>
                  </ul>
                </div>

                <div className="border-l-4 border-blue-500 pl-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">2. Fintechs e Bureaus de Crédito</h4>
                  <ul className="space-y-1 text-gray-700">
                    <li>• Verificação de empresas para análise de risco</li>
                    <li>• Consultas em massa para due diligence</li>
                    <li>• Validação de dados cadastrais</li>
                  </ul>
                </div>

                <div className="border-l-4 border-purple-500 pl-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">3. Softwares Empresariais</h4>
                  <ul className="space-y-1 text-gray-700">
                    <li>• Preenchimento automático de formulários</li>
                    <li>• Integração com sistemas de gestão</li>
                    <li>• Enriquecimento de base de dados</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* Primeiros Passos */}
            <section className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Primeiros Passos</h3>
              
              <div className="space-y-4">
                <div className="flex items-start gap-4 p-6 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="bg-emerald-100 p-2 rounded-lg">
                    <Key className="w-6 h-6 text-emerald-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-2">1. Obtenha sua API Key</h4>
                    <p className="text-gray-700 mb-2">
                      <Link href="/signup" className="text-emerald-600 hover:text-emerald-700 font-medium">
                        Crie sua conta
                      </Link> e acesse o painel para gerar sua chave de API.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-6 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <Code className="w-6 h-6 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-2">2. Configure a Autenticação</h4>
                    <p className="text-gray-700">
                      Implemente a autenticação usando Bearer Token em suas requisições.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-6 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="bg-purple-100 p-2 rounded-lg">
                    <Zap className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900 mb-2">3. Faça sua primeira consulta</h4>
                    <p className="text-gray-700">
                      Teste a API consultando um CNPJ de exemplo.
                    </p>
                  </div>
                </div>
              </div>
            </section>

            {/* Exemplo de Requisição */}
            <section className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Exemplo de Requisição</h3>
              
              <div className="bg-gray-900 text-gray-100 rounded-lg p-6 overflow-x-auto mb-4">
                <pre className="text-sm">
{`curl -X GET https://api.authbrasil.app.br/api/v1/cnpj/12345678000190 \\
  -H "Authorization: Bearer SUA_API_KEY" \\
  -H "Content-Type: application/json"`}
                </pre>
              </div>

              <h4 className="font-semibold text-gray-900 mb-3">Resposta de Sucesso (200 OK):</h4>
              <div className="bg-gray-900 text-gray-100 rounded-lg p-6 overflow-x-auto">
                <pre className="text-sm">
{`{
  "success": true,
  "data": {
    "cnpj": "12.345.678/0001-90",
    "razao_social": "EMPRESA EXEMPLO LTDA",
    "nome_fantasia": "Exemplo",
    "situacao": "ATIVA",
    "data_situacao": "2020-01-15",
    "tipo": "MATRIZ",
    "porte": "MICRO EMPRESA",
    "natureza_juridica": {
      "codigo": "206-2",
      "descricao": "Sociedade Empresária Limitada"
    },
    "cnae_principal": {
      "codigo": "6201-5/00",
      "descricao": "Desenvolvimento de programas de computador sob encomenda"
    },
    "endereco": {
      "logradouro": "RUA EXEMPLO",
      "numero": "123",
      "complemento": "SALA 1",
      "bairro": "CENTRO",
      "municipio": "São Paulo",
      "uf": "SP",
      "cep": "01234-567"
    },
    "socios": [
      {
        "nome": "FULANO DE TAL",
        "qualificacao": "Sócio-Administrador",
        "data_entrada": "2020-01-01"
      }
    ]
  },
  "metadata": {
    "cached": true,
    "timestamp": "2024-11-22T14:30:00Z"
  }
}`}
                </pre>
              </div>
            </section>

            {/* Vantagens */}
            <section className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Vantagens da AuthBrasil CNPJ API</h3>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="p-6 bg-gradient-to-br from-emerald-50 to-green-50 rounded-lg border border-emerald-200">
                  <div className="flex items-center gap-3 mb-3">
                    <Zap className="w-6 h-6 text-emerald-600" />
                    <h4 className="font-semibold text-gray-900">Performance Superior</h4>
                  </div>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Cache inteligente com TTL configurável</li>
                    <li>• Respostas otimizadas &lt;100ms</li>
                    <li>• Infraestrutura distribuída</li>
                  </ul>
                </div>

                <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                  <div className="flex items-center gap-3 mb-3">
                    <Shield className="w-6 h-6 text-blue-600" />
                    <h4 className="font-semibold text-gray-900">Segurança Avançada</h4>
                  </div>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Autenticação via API Key</li>
                    <li>• HTTPS obrigatório</li>
                    <li>• Rate limiting inteligente</li>
                  </ul>
                </div>

                <div className="p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg border border-purple-200">
                  <div className="flex items-center gap-3 mb-3">
                    <Database className="w-6 h-6 text-purple-600" />
                    <h4 className="font-semibold text-gray-900">Dados Estruturados</h4>
                  </div>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Respostas padronizadas em JSON</li>
                    <li>• Metadados ricos para cada consulta</li>
                    <li>• Fácil de integrar</li>
                  </ul>
                </div>

                <div className="p-6 bg-gradient-to-br from-orange-50 to-red-50 rounded-lg border border-orange-200">
                  <div className="flex items-center gap-3 mb-3">
                    <Lock className="w-6 h-6 text-orange-600" />
                    <h4 className="font-semibold text-gray-900">Dados Oficiais</h4>
                  </div>
                  <ul className="space-y-1 text-sm text-gray-700">
                    <li>• Sincronização mensal com Receita</li>
                    <li>• 50M+ empresas cadastradas</li>
                    <li>• Sempre atualizado</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* Autenticação */}
            <section className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Autenticação</h3>
              
              <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                <p className="text-gray-700 mb-4">
                  Todas as requisições autenticadas devem incluir o header:
                </p>
                <div className="bg-gray-900 text-gray-100 rounded-lg p-4">
                  <code className="text-sm">Authorization: Bearer SUA_API_KEY</code>
                </div>
              </div>
            </section>

            {/* Rate Limits */}
            <section className="mb-16">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Rate Limits</h3>
              
              <p className="text-gray-700 mb-4">
                Os limites de requisições variam conforme seu plano:
              </p>

              <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                <ul className="space-y-3">
                  <li className="flex items-center gap-3">
                    <span className="w-3 h-3 bg-emerald-500 rounded-full"></span>
                    <span className="text-gray-700"><strong>Starter:</strong> 500 requisições/mês</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
                    <span className="text-gray-700"><strong>Pro:</strong> 5.000 requisições/mês</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <span className="w-3 h-3 bg-purple-500 rounded-full"></span>
                    <span className="text-gray-700"><strong>Enterprise:</strong> 50.000 requisições/mês</span>
                  </li>
                </ul>
                
                <p className="text-sm text-gray-600 mt-4">
                  Limite padrão: 60 requisições por minuto por API key
                </p>
              </div>
            </section>

            {/* Suporte */}
            <section>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Suporte e Documentação</h3>
              
              <div className="grid md:grid-cols-3 gap-4">
                <Link 
                  href="/pricing"
                  className="p-6 bg-white rounded-lg border-2 border-gray-200 hover:border-emerald-500 transition-all hover:shadow-lg group"
                >
                  <div className="text-2xl mb-2">📊</div>
                  <h4 className="font-semibold text-gray-900 mb-2 group-hover:text-emerald-600 transition">Ver Planos</h4>
                  <p className="text-sm text-gray-600">Escolha o plano ideal para você</p>
                </Link>

                <a 
                  href="mailto:suporte@authbrasil.com.br"
                  className="p-6 bg-white rounded-lg border-2 border-gray-200 hover:border-blue-500 transition-all hover:shadow-lg group"
                >
                  <div className="text-2xl mb-2">💬</div>
                  <h4 className="font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition">Suporte Técnico</h4>
                  <p className="text-sm text-gray-600">Equipe especializada para ajudar</p>
                </a>

                <Link 
                  href="/signup"
                  className="p-6 bg-white rounded-lg border-2 border-gray-200 hover:border-purple-500 transition-all hover:shadow-lg group"
                >
                  <div className="text-2xl mb-2">🚀</div>
                  <h4 className="font-semibold text-gray-900 mb-2 group-hover:text-purple-600 transition">Começar Agora</h4>
                  <p className="text-sm text-gray-600">Teste grátis por 14 dias</p>
                </Link>
              </div>
            </section>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
