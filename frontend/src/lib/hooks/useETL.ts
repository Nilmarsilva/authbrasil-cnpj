/**
 * useETL Hook
 * Manages ETL state and polling
 */

import { useState, useEffect, useCallback } from 'react'
import { api, ETLStatusResponse, ETLValidationResponse, ETLStartRequest } from '../api'

const POLL_INTERVAL = 5000 // 5 seconds

export function useETL() {
  const [status, setStatus] = useState<ETLStatusResponse | null>(null)
  const [validation, setValidation] = useState<ETLValidationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [polling, setPolling] = useState(false)

  // Fetch validation
  const validateETL = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      const result = await api.validateETL()
      setValidation(result)
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Erro ao validar ETL'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  // Fetch status
  const fetchStatus = useCallback(async () => {
    try {
      const result = await api.getETLStatus()
      setStatus(result)
      
      // Auto-enable polling if running
      if (result.status === 'running' && !polling) {
        setPolling(true)
      }
      
      // Auto-disable polling if completed/error
      if ((result.status === 'completed' || result.status === 'error') && polling) {
        setPolling(false)
      }
      
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Erro ao buscar status'
      setError(message)
      throw err
    }
  }, [polling])

  // Start ETL
  const startETL = useCallback(async (data: ETLStartRequest) => {
    setLoading(true)
    setError(null)
    
    try {
      const result = await api.startETL(data)
      
      // Immediately fetch status
      await fetchStatus()
      
      // Enable polling
      setPolling(true)
      
      return result
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Erro ao iniciar ETL'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [fetchStatus])

  // Polling effect
  useEffect(() => {
    if (!polling) return

    const interval = setInterval(() => {
      fetchStatus()
    }, POLL_INTERVAL)

    return () => clearInterval(interval)
  }, [polling, fetchStatus])

  // Initial fetch
  useEffect(() => {
    fetchStatus()
  }, [])

  return {
    status,
    validation,
    loading,
    error,
    validateETL,
    startETL,
    refresh: fetchStatus,
  }
}
