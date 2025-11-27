'use client'

/**
 * ETL Panel Component
 * Admin interface for managing CNPJ data imports
 */

import { useState } from 'react'
import { useETL } from '@/lib/hooks/useETL'

export function ETLPanel() {
  const { status, validation, loading, error, validateETL, startETL, refresh } = useETL()
  const [showConfirm, setShowConfirm] = useState(false)

  const handleStartClick = async () => {
    // Validate first
    const validationResult = await validateETL()
    
    if (!validationResult) return
    
    // If has errors, block
    if (validationResult.errors.length > 0) {
      alert('Não é possível iniciar o ETL:\n' + validationResult.errors.join('\n'))
      return
    }
    
    // If has warnings, show confirmation
    if (validationResult.warnings.length > 0) {
      setShowConfirm(true)
    } else {
      // No warnings, start directly
      await startETL({ force: false })
    }
  }

  const handleConfirmStart = async () => {
    setShowConfirm(false)
    await startETL({ force: true })
  }

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return hours > 0 ? `${hours}h ${minutes}min` : `${minutes}min`
  }

  const formatDate = (dateStr?: string): string => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleString('pt-BR')
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Atualização de Dados CNPJ</h2>
          <button
            onClick={refresh}
            disabled={loading}
            className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-md disabled:opacity-50"
          >
            🔄 Atualizar
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md text-red-800">
            ❌ {error}
          </div>
        )}

        {/* Status Card */}
        <div className="mb-6 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Status</p>
              <p className="text-2xl font-bold">
                {status?.status === 'idle' && '⏸️ Parado'}
                {status?.status === 'running' && '🔄 Rodando'}
                {status?.status === 'completed' && '✅ Concluído'}
                {status?.status === 'error' && '❌ Erro'}
              </p>
            </div>
            
            {status?.current_step && (
              <div>
                <p className="text-sm text-gray-600">Etapa Atual</p>
                <p className="text-lg font-semibold">{status.current_step}</p>
                {status.current_file && (
                  <p className="text-sm text-gray-500">{status.current_file}</p>
                )}
              </div>
            )}
            
            <div>
              <p className="text-sm text-gray-600">Progresso</p>
              <div className="flex items-center gap-2">
                <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                  <div
                    className="bg-blue-600 h-full transition-all duration-500"
                    style={{ width: `${status?.progress_percent || 0}%` }}
                  />
                </div>
                <span className="text-sm font-semibold">
                  {status?.progress_percent?.toFixed(1) || 0}%
                </span>
              </div>
            </div>
            
            <div>
              <p className="text-sm text-gray-600">Arquivos Processados</p>
              <p className="text-lg font-semibold">
                {status?.files_processed || 0} / {status?.files_total || 0}
              </p>
            </div>
            
            <div>
              <p className="text-sm text-gray-600">Registros Importados</p>
              <p className="text-lg font-semibold">
                {status?.records_imported?.toLocaleString('pt-BR') || 0}
              </p>
            </div>
            
            <div>
              <p className="text-sm text-gray-600">Espaço Livre</p>
              <p className="text-lg font-semibold">
                {status?.disk_free_gb?.toFixed(1) || '-'} GB
              </p>
            </div>
            
            {status?.elapsed_seconds && status.elapsed_seconds > 0 && (
              <div>
                <p className="text-sm text-gray-600">Tempo Decorrido</p>
                <p className="text-lg font-semibold">
                  {formatTime(status.elapsed_seconds)}
                </p>
              </div>
            )}
            
            {status?.estimated_remaining_seconds && status.estimated_remaining_seconds > 0 && (
              <div>
                <p className="text-sm text-gray-600">Tempo Restante (estimado)</p>
                <p className="text-lg font-semibold">
                  {formatTime(status.estimated_remaining_seconds)}
                </p>
              </div>
            )}
          </div>

          {/* Warnings */}
          {status?.warnings && status.warnings.length > 0 && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="font-semibold text-yellow-800 mb-1">⚠️ Avisos:</p>
              <ul className="text-sm text-yellow-700 list-disc list-inside">
                {status.warnings.map((warning, i) => (
                  <li key={i}>{warning}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Error */}
          {status?.error_message && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="font-semibold text-red-800 mb-1">❌ Erro:</p>
              <p className="text-sm text-red-700">{status.error_message}</p>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          {status?.status === 'idle' && (
            <button
              onClick={handleStartClick}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              🚀 Iniciar Atualização
            </button>
          )}
          
          {status?.status === 'running' && (
            <div className="px-6 py-3 bg-green-100 text-green-800 rounded-lg font-semibold flex items-center gap-2">
              <div className="w-3 h-3 bg-green-600 rounded-full animate-pulse"></div>
              Processando...
            </div>
          )}
          
          {status?.status === 'completed' && (
            <div className="px-6 py-3 bg-green-100 text-green-800 rounded-lg font-semibold">
              ✅ Atualização Concluída
            </div>
          )}
        </div>

        {/* Job Info */}
        {status?.job_id && status.job_id !== 'none' && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-600">
              <span className="font-semibold">Job ID:</span> {status.job_id}
            </p>
            {status.started_at && (
              <p className="text-sm text-gray-600">
                <span className="font-semibold">Iniciado em:</span> {formatDate(status.started_at)}
              </p>
            )}
            {status.completed_at && (
              <p className="text-sm text-gray-600">
                <span className="font-semibold">Concluído em:</span> {formatDate(status.completed_at)}
              </p>
            )}
          </div>
        )}
      </div>

      {/* Confirmation Modal */}
      {showConfirm && validation && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
            <h3 className="text-xl font-bold mb-4">⚠️ Atenção</h3>
            
            <div className="mb-4">
              <p className="font-semibold mb-2">Avisos:</p>
              <ul className="text-sm list-disc list-inside text-gray-700">
                {validation.warnings.map((warning, i) => (
                  <li key={i}>{warning}</li>
                ))}
              </ul>
            </div>
            
            <p className="text-sm text-gray-600 mb-6">
              Deseja continuar mesmo assim?
            </p>
            
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowConfirm(false)}
                className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md"
              >
                Cancelar
              </button>
              <button
                onClick={handleConfirmStart}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md"
              >
                Continuar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
