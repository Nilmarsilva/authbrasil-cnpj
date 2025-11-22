import Link from "next/link"
import { ArrowRight, CheckCircle, Zap, Shield, TrendingUp, Database, Code, BarChart3, Lock, Globe, Sparkles } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-lg border-b border-gray-200/50 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-2xl font-bold bg-gradient-to-r from-emerald-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
                AuthBrasil CNPJ
              </div>
              <a 
                href="https://authbrasil.com.br" 
                target="_blank"
                className="text-xs text-gray-500 hover:text-emerald-600 transition flex items-center gap-1"
              >
                <span className="hidden sm:inline">por</span> AuthBrasil
              </a>
            </div>
            <div className="hidden md:flex items-center gap-8">
              <Link href="#features" className="text-gray-600 hover:text-emerald-600 transition">Recursos</Link>
              <Link href="#pricing" className="text-gray-600 hover:text-emerald-600 transition">Preços</Link>
              <Link href="#docs" className="text-gray-600 hover:text-emerald-600 transition">Documentação</Link>
              <Link href="/login" className="text-gray-600 hover:text-emerald-600 transition">Login</Link>
              <Link 
                href="/signup"
                className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-6 py-2.5 rounded-full font-semibold hover:shadow-lg hover:scale-105 transition-all"
              >
                Começar Grátis
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="container mx-auto">
          <div className="max-w-5xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 bg-emerald-100/50 backdrop-blur-sm border border-emerald-200/50 rounded-full px-4 py-2 mb-8">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span className="text-sm font-medium text-emerald-700">Dados oficiais da Receita Federal</span>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-gray-900 via-emerald-800 to-blue-900 bg-clip-text text-transparent leading-tight">
              Consulta CNPJ
              <br />
              <span className="bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
                Profissional e Confiável
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Dados atualizados, completos e acessíveis via <span className="font-semibold text-emerald-600">painel web</span> e <span className="font-semibold text-blue-600">API REST</span>
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link 
                href="/signup"
                className="group bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-8 py-4 rounded-full font-semibold hover:shadow-2xl hover:scale-105 transition-all flex items-center justify-center gap-2"
              >
                Teste Grátis por 14 Dias
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link 
                href="#demo"
                className="bg-white/80 backdrop-blur-sm text-gray-700 px-8 py-4 rounded-full font-semibold border-2 border-gray-200 hover:border-emerald-300 hover:shadow-xl transition-all"
              >
                Ver Demonstração
              </Link>
            </div>

            <div className="flex items-center justify-center gap-8 text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span>Sem cartão de crédito</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span>Cancele quando quiser</span>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            {[
              { value: "50M+", label: "Empresas cadastradas" },
              { value: "<100ms", label: "Tempo de resposta" },
              { value: "99.9%", label: "Uptime garantido" },
              { value: "Mensal", label: "Atualização de dados" },
            ].map((stat, i) => (
              <div key={i} className="text-center">
                <div className="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600 mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
              Recursos Profissionais
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tudo que você precisa para consultas corporativas eficientes
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Zap,
                title: "Consultas Instantâneas",
                description: "Respostas em menos de 100ms com cache inteligente e otimizado",
                color: "from-yellow-500 to-orange-500"
              },
              {
                icon: Shield,
                title: "Dados Oficiais",
                description: "Sincronização mensal automática com a base da Receita Federal",
                color: "from-green-500 to-emerald-500"
              },
              {
                icon: Code,
                title: "API REST Completa",
                description: "Documentação detalhada e SDKs para fácil integração",
                color: "from-blue-500 to-indigo-500"
              },
              {
                icon: Database,
                title: "50M+ Empresas",
                description: "Base completa com CNPJ, sócios, atividades e muito mais",
                color: "from-purple-500 to-pink-500"
              },
              {
                icon: Lock,
                title: "Segurança Total",
                description: "HTTPS, autenticação JWT e rate limiting inteligente",
                color: "from-red-500 to-pink-500"
              },
              {
                icon: BarChart3,
                title: "Painel Completo",
                description: "Interface web intuitiva com estatísticas e histórico",
                color: "from-cyan-500 to-blue-500"
              },
            ].map((feature, i) => (
              <div
                key={i}
                className="group bg-white/50 backdrop-blur-sm p-8 rounded-2xl border border-gray-200/50 hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-3 text-gray-900">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="bg-gradient-to-r from-emerald-600 to-blue-600 rounded-3xl p-12 md:p-16 text-center text-white relative overflow-hidden">
            <div className="absolute inset-0 bg-grid-white/10"></div>
            <div className="relative z-10">
              <h2 className="text-4xl md:text-5xl font-bold mb-6">
                Comece Hoje Mesmo
              </h2>
              <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
                Teste grátis por 14 dias. Sem compromisso, sem cartão de crédito.
              </p>
              <Link 
                href="/signup"
                className="inline-flex items-center gap-2 bg-white text-emerald-600 px-8 py-4 rounded-full font-semibold hover:shadow-2xl hover:scale-105 transition-all"
              >
                Criar Conta Grátis
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent mb-4">
                AuthBrasil CNPJ
              </div>
              <p className="text-sm mb-3">
                Consultas corporativas profissionais com dados oficiais da Receita Federal.
              </p>
              <a 
                href="https://authbrasil.com.br" 
                target="_blank"
                className="text-xs text-gray-500 hover:text-emerald-400 transition inline-flex items-center gap-1"
              >
                <Globe className="w-3 h-3" />
                Parte de AuthBrasil
              </a>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Produto</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white transition">Recursos</Link></li>
                <li><Link href="#" className="hover:text-white transition">Preços</Link></li>
                <li><Link href="#" className="hover:text-white transition">API</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Empresa</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white transition">Sobre</Link></li>
                <li><Link href="#" className="hover:text-white transition">Contato</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="#" className="hover:text-white transition">Privacidade</Link></li>
                <li><Link href="#" className="hover:text-white transition">Termos</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-sm">
            <p>&copy; 2024 AuthBrasil CNPJ. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
