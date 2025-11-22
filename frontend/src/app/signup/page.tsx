"use client"

import { useState } from "react"
import Link from "next/link"
import { Header } from "@/components/layout/Header"
import { ArrowRight, Mail, Lock, User, Building2, CheckCircle } from "lucide-react"

export default function SignupPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    password: "",
    confirmPassword: "",
    acceptTerms: false
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implementar cadastro com backend
    console.log("Signup:", formData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="pt-24 pb-20 px-4">
        <div className="container mx-auto max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-gray-900 via-emerald-800 to-blue-900 bg-clip-text text-transparent">
              Criar Conta
            </h1>
            <p className="text-gray-600">
              Teste grátis por 14 dias. Sem cartão de crédito.
            </p>
          </div>

          <div className="bg-white/50 backdrop-blur-sm rounded-2xl p-8 border border-gray-200 shadow-xl">
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Nome */}
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                  Nome completo
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="name"
                    name="name"
                    type="text"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="João Silva"
                  />
                </div>
              </div>

              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email profissional
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="joao@empresa.com.br"
                  />
                </div>
              </div>

              {/* Empresa (Opcional) */}
              <div>
                <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                  Empresa (opcional)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Building2 className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="company"
                    name="company"
                    type="text"
                    value={formData.company}
                    onChange={handleChange}
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="Minha Empresa Ltda"
                  />
                </div>
              </div>

              {/* Senha */}
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
                    name="password"
                    type="password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="••••••••"
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">Mínimo 8 caracteres</p>
              </div>

              {/* Confirmar Senha */}
              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">
                  Confirmar senha
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    id="confirmPassword"
                    name="confirmPassword"
                    type="password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition"
                    placeholder="••••••••"
                  />
                </div>
              </div>

              {/* Termos */}
              <div className="flex items-start">
                <div className="flex items-center h-5">
                  <input
                    id="acceptTerms"
                    name="acceptTerms"
                    type="checkbox"
                    checked={formData.acceptTerms}
                    onChange={handleChange}
                    required
                    className="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
                  />
                </div>
                <div className="ml-3 text-sm">
                  <label htmlFor="acceptTerms" className="text-gray-700">
                    Eu aceito os{" "}
                    <Link href="/termos" className="text-emerald-600 hover:text-emerald-700 font-medium">
                      termos de serviço
                    </Link>
                    {" "}e a{" "}
                    <Link href="/privacidade" className="text-emerald-600 hover:text-emerald-700 font-medium">
                      política de privacidade
                    </Link>
                  </label>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={!formData.acceptTerms}
                className="w-full bg-gradient-to-r from-emerald-600 to-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:shadow-xl hover:scale-105 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              >
                Criar Conta Grátis
                <ArrowRight className="w-5 h-5" />
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

            {/* Login Link */}
            <div className="text-center">
              <p className="text-sm text-gray-600">
                Já tem uma conta?{" "}
                <Link href="/login" className="font-semibold text-emerald-600 hover:text-emerald-700">
                  Fazer login
                </Link>
              </p>
            </div>
          </div>

          {/* Benefits */}
          <div className="mt-8">
            <p className="text-sm text-gray-600 mb-4 text-center font-medium">O que você ganha:</p>
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center gap-2 text-sm text-gray-700 bg-white/50 backdrop-blur-sm p-3 rounded-lg border border-gray-200">
                <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                <span>14 dias grátis</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-700 bg-white/50 backdrop-blur-sm p-3 rounded-lg border border-gray-200">
                <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                <span>Sem cartão</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-700 bg-white/50 backdrop-blur-sm p-3 rounded-lg border border-gray-200">
                <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                <span>API completa</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-700 bg-white/50 backdrop-blur-sm p-3 rounded-lg border border-gray-200">
                <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                <span>Cancele a qualquer momento</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
