import Link from "next/link"

export function Header() {
  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-lg border-b border-gray-200/50 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/">
              <div className="text-2xl font-bold bg-gradient-to-r from-emerald-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent cursor-pointer">
                AuthBrasil CNPJ
              </div>
            </Link>
            <a 
              href="https://authbrasil.com.br" 
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-gray-500 hover:text-emerald-600 transition flex items-center gap-1"
            >
              <span className="hidden sm:inline">por</span> AuthBrasil
            </a>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <Link href="/#features" className="text-gray-600 hover:text-emerald-600 transition">
              Recursos
            </Link>
            <Link href="/pricing" className="text-gray-600 hover:text-emerald-600 transition">
              Preços
            </Link>
            <Link href="/docs" className="text-gray-600 hover:text-emerald-600 transition">
              Documentação
            </Link>
            <Link href="/login" className="text-gray-600 hover:text-emerald-600 transition">
              Login
            </Link>
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
  )
}
