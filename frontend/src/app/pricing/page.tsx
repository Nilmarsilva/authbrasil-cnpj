import { Header } from "@/components/layout/Header"
import { Footer } from "@/components/layout/Footer"
import { PricingCard } from "@/components/pricing/PricingCard"
import { CheckCircle } from "lucide-react"

export default function PricingPage() {
  const plans = [
    {
      name: "Starter",
      price: "R$ 29",
      description: "Ideal para MEI e pequenos negócios",
      features: [
        "500 consultas/mês",
        "Acesso ao painel web",
        "API REST completa",
        "Suporte por email",
        "Dados atualizados mensalmente"
      ]
    },
    {
      name: "Pro",
      price: "R$ 79",
      description: "Para contadores e despachantes",
      features: [
        "5.000 consultas/mês",
        "Acesso ao painel web",
        "API REST completa",
        "Múltiplas API keys",
        "Suporte prioritário",
        "Webhooks (em breve)",
        "Dados atualizados mensalmente"
      ],
      highlighted: true
    },
    {
      name: "Enterprise",
      price: "R$ 249",
      description: "Para softwares e agências",
      features: [
        "50.000 consultas/mês",
        "Acesso ao painel web",
        "API REST completa",
        "API keys ilimitadas",
        "Suporte 24/7",
        "Webhooks personalizados",
        "SLA garantido",
        "Dados atualizados mensalmente"
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="pt-24 pb-20 px-4">
        <div className="container mx-auto">
          {/* Hero */}
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-gray-900 via-emerald-800 to-blue-900 bg-clip-text text-transparent">
              Planos e Preços
            </h1>
            <p className="text-xl text-gray-600">
              Escolha o plano ideal para o seu negócio. Teste grátis por 14 dias.
            </p>
          </div>

          {/* Pricing Cards */}
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
            {plans.map((plan, index) => (
              <PricingCard key={index} {...plan} />
            ))}
          </div>

          {/* On Demand */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white/50 backdrop-blur-sm border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center">
              <h3 className="text-2xl font-bold text-gray-900 mb-3">On Demand</h3>
              <p className="text-gray-600 mb-4">
                Pague apenas pelo que usar. Ideal para sistemas com uso variável.
              </p>
              <div className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent mb-6">
                R$ 0,09 <span className="text-xl text-gray-600">/consulta</span>
              </div>
              <a 
                href="mailto:contato@authbrasil.com.br"
                className="inline-block bg-gradient-to-r from-emerald-600 to-blue-600 text-white px-8 py-3 rounded-full font-semibold hover:shadow-xl hover:scale-105 transition-all"
              >
                Falar com Vendas
              </a>
            </div>
          </div>

          {/* FAQ */}
          <div className="mt-20 max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
              Perguntas Frequentes
            </h2>
            <div className="space-y-6">
              {[
                {
                  q: "Posso cancelar a qualquer momento?",
                  a: "Sim! Você pode cancelar sua assinatura a qualquer momento sem custo adicional."
                },
                {
                  q: "O que acontece se eu exceder o limite?",
                  a: "Você receberá uma notificação e poderá fazer upgrade do plano ou aguardar a renovação mensal."
                },
                {
                  q: "Os dados são atualizados?",
                  a: "Sim! Sincronizamos mensalmente com a base oficial da Receita Federal."
                },
                {
                  q: "Posso usar a API em produção?",
                  a: "Sim! Nossa API é robusta e preparada para ambientes de produção com alta disponibilidade."
                }
              ].map((faq, index) => (
                <div key={index} className="bg-white/50 backdrop-blur-sm rounded-xl p-6 border border-gray-200">
                  <h3 className="font-semibold text-gray-900 mb-2 flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                    {faq.q}
                  </h3>
                  <p className="text-gray-600 pl-8">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}
