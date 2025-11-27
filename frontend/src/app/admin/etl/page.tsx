'use client'

/**
 * Admin ETL Page
 * Protected route - only superusers can access
 */

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { ETLPanel } from '@/components/admin/ETLPanel'

export default function AdminETLPage() {
  const { user, isLoading, isAuthenticated } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading) {
      // Redirect to login if not authenticated
      if (!isAuthenticated) {
        router.push('/login?redirect=/admin/etl')
        return
      }
      
      // Redirect to dashboard if not superuser
      if (user && !user.is_superuser) {
        alert('Acesso negado. Apenas administradores podem acessar esta página.')
        router.push('/dashboard')
      }
    }
  }, [isLoading, isAuthenticated, user, router])

  // Show loading
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando...</p>
        </div>
      </div>
    )
  }

  // Show access denied if not superuser
  if (!user?.is_superuser) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-2">❌ Acesso Negado</h1>
          <p className="text-gray-600">Apenas administradores podem acessar esta página.</p>
        </div>
      </div>
    )
  }

  // Show ETL panel for superusers
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200 mb-6">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-bold">🛠️ Painel Administrativo</h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                {user?.email}
              </span>
              <button
                onClick={() => router.push('/dashboard')}
                className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-md"
              >
                ← Voltar ao Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <ETLPanel />
    </div>
  )
}
