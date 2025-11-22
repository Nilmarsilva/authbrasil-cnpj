import Link from "next/link"
import { CheckCircle } from "lucide-react"

interface PricingCardProps {
  name: string
  price: string
  description: string
  features: string[]
  highlighted?: boolean
  ctaText?: string
  ctaLink?: string
}

export function PricingCard({ 
  name, 
  price, 
  description, 
  features, 
  highlighted = false,
  ctaText = "Começar Agora",
  ctaLink = "/signup"
}: PricingCardProps) {
  return (
    <div className={`
      relative p-8 rounded-2xl border-2 transition-all duration-300
      ${highlighted 
        ? 'border-emerald-500 bg-gradient-to-br from-emerald-50 to-blue-50 shadow-2xl scale-105' 
        : 'border-gray-200 bg-white hover:border-emerald-300 hover:shadow-xl'
      }
    `}>
      {highlighted && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2">
          <span className="bg-gradient-to-r from-emerald-600 to-blue-600 text-white text-sm font-semibold px-4 py-1.5 rounded-full">
            Mais Popular
          </span>
        </div>
      )}
      
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">{name}</h3>
        <p className="text-gray-600 text-sm">{description}</p>
      </div>

      <div className="mb-6">
        <div className="flex items-baseline gap-2">
          <span className="text-5xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
            {price}
          </span>
          {price !== "Grátis" && <span className="text-gray-600">/mês</span>}
        </div>
      </div>

      <ul className="space-y-3 mb-8">
        {features.map((feature, index) => (
          <li key={index} className="flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
            <span className="text-gray-700 text-sm">{feature}</span>
          </li>
        ))}
      </ul>

      <Link 
        href={ctaLink}
        className={`
          block w-full py-3 px-6 rounded-full font-semibold text-center transition-all
          ${highlighted
            ? 'bg-gradient-to-r from-emerald-600 to-blue-600 text-white hover:shadow-xl hover:scale-105'
            : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
          }
        `}
      >
        {ctaText}
      </Link>
    </div>
  )
}
