"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Header } from "@/components/layout/Header"
import { useAuth } from "@/contexts/AuthContext"
import { ArrowRight, Mail, Lock } from "lucide-react"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setLoading(true)
    
    try {
      await login({ email, password })
      router.push("/dashboard")
    } catch (err: any) {
      setError(err.message || "Erro ao fazer login")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="pt-24 pb-20 px-4">
        <div className="container mx-auto max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-emerald-800 to-blue-900 bg-clip-text text-transparent">
              Bem-vindo de volta
            </h1>
            <p className="text-gray-600">
              Acesse sua conta para continuar
            </p>
          </div>

          <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-200 shadow-xl">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="seu@email.com"
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Senha
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              {/* Forgot Password */}
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                  />
                  <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700">
                    Lembrar de mim
                  </label>
                </div>
                <Link href="/forgot-password" className="text-sm text-emerald-600 hover:text-emerald-700">
                  Esqueceu a senha?
                </Link>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-emerald-600 to-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:shadow-xl hover:scale-105 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                {loading ? "Entrando..." : "Entrar"}
                {!loading && <ArrowRight className="w-5 h-5" />}
              </button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Ou</span>
              </div>
            </div>

            {/* Sign Up Link */}
            <div className="text-center">
              <p className="text-sm text-gray-600">
                Não tem uma conta?{" "}
                <Link href="/signup" className="font-semibold text-emerald-600 hover:text-emerald-700">
                  Criar conta grátis
                </Link>
              </p>
            </div>
          </div>

          {/* Benefits */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600 mb-4">Ao fazer login, você terá acesso a:</p>
            <div className="flex flex-wrap justify-center gap-4 text-xs text-gray-600">
              <span className="bg-white/50 backdrop-blur-sm px-3 py-1.5 rounded-full border border-gray-200">
                📊 Painel completo
              </span>
              <span className="bg-white/50 backdrop-blur-sm px-3 py-1.5 rounded-full border border-gray-200">
                🔑 API Keys
              </span>
              <span className="bg-white/50 backdrop-blur-sm px-3 py-1.5 rounded-full border border-gray-200">
                📈 Estatísticas
              </span>
              <span className="bg-white/50 backdrop-blur-sm px-3 py-1.5 rounded-full border border-gray-200">
                💳 Faturamento
              </span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
