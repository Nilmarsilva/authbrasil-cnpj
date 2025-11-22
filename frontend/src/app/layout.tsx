import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { AuthProvider } from "@/contexts/AuthContext"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AuthBrasil CNPJ - Consulta Corporativa Profissional",
  description: "Dados atualizados, confiáveis e acessíveis via painel e API. Consultas CNPJ oficiais da Receita Federal.",
  keywords: ["CNPJ", "Consulta CNPJ", "API CNPJ", "Dados empresariais", "Receita Federal"],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
