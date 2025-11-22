import Link from "next/link"
import { Globe } from "lucide-react"

export function Footer() {
  return (
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
              rel="noopener noreferrer"
              className="text-xs text-gray-500 hover:text-emerald-400 transition inline-flex items-center gap-1"
            >
              <Globe className="w-3 h-3" />
              Parte de AuthBrasil
            </a>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-4">Produto</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/#features" className="hover:text-white transition">Recursos</Link></li>
              <li><Link href="/pricing" className="hover:text-white transition">Preços</Link></li>
              <li><Link href="/docs" className="hover:text-white transition">API</Link></li>
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
  )
}
