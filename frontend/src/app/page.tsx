import Link from "next/link"
import { ArrowRight, CheckCircle, Zap, Shield, TrendingUp } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Consulta CNPJ instantânea, completa e atualizada
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Dados oficiais da Receita Federal, processados e organizados para uso profissional
          </p>
          <div className="flex gap-4 justify-center">
            <Link 
              href="/signup"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition flex items-center gap-2"
            >
              Começar Grátis
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              href="/pricing"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition"
            >
              Ver Planos
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid md:grid-3 gap-8">
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="bg-blue-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold mb-2">Consultas Instantâneas</h3>
            <p className="text-gray-600">
              Respostas em menos de 100ms com cache otimizado
            </p>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <Shield className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-bold mb-2">Dados Oficiais</h3>
            <p className="text-gray-600">
              Sincronizados mensalmente com a Receita Federal
            </p>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="bg-purple-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold mb-2">API REST Robusta</h3>
            <p className="text-gray-600">
              Documentação completa e fácil integração
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-blue-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Comece hoje mesmo
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Teste grátis por 14 dias. Sem cartão de crédito necessário.
          </p>
          <Link 
            href="/signup"
            className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition inline-block"
          >
            Criar Conta Grátis
          </Link>
        </div>
      </section>
    </div>
  )
}
