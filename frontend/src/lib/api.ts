/**
 * API Service
 * HTTP client for backend API calls
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.authbrasil.app.br/api/v1'

export interface LoginCredentials {
  email: string
  password: string
}

export interface SignupData {
  email: string
  password: string
  full_name: string
  company?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  email: string
  full_name: string
  is_active: boolean
  is_superuser: boolean
  is_verified: boolean
}

export interface ETLStartRequest {
  force?: boolean
  skip_download?: boolean
  tables?: string[]
}

export interface ETLValidationResponse {
  can_proceed: boolean
  warnings: string[]
  errors: string[]
  disk_free_gb: number
  disk_used_gb: number
  postgres_running: boolean
  tables_exist: boolean
}

export interface ETLStatusResponse {
  job_id: string
  status: string
  current_step?: string
  current_file?: string
  current_table?: string
  progress_percent: number
  files_processed: number
  files_total: number
  records_imported: number
  disk_free_gb?: number
  disk_used_gb?: number
  started_at?: string
  completed_at?: string
  elapsed_seconds: number
  estimated_remaining_seconds?: number
  error_message?: string
  warnings: string[]
}

export interface ETLStartResponse {
  status: string
  job_id: string
  message: string
}

export interface ETLLogsResponse {
  logs: string[]
  total_lines: number
}

class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    // Add auth token if available
    const token = localStorage.getItem('access_token')
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: 'Erro na requisição'
      }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
  }

  // Auth endpoints
  async login(credentials: LoginCredentials): Promise<TokenResponse> {
    return this.request<TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })
  }

  async signup(data: SignupData): Promise<UserResponse> {
    return this.request<UserResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getCurrentUser(): Promise<UserResponse> {
    return this.request<UserResponse>('/auth/me')
  }

  // CNPJ endpoints
  async consultarCNPJ(cnpj: string): Promise<any> {
    return this.request(`/cnpj/${cnpj}`)
  }

  // ETL endpoints (admin only)
  async validateETL(): Promise<ETLValidationResponse> {
    return this.request<ETLValidationResponse>('/etl/validate')
  }

  async startETL(data: ETLStartRequest): Promise<ETLStartResponse> {
    return this.request<ETLStartResponse>('/etl/start', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async getETLStatus(): Promise<ETLStatusResponse> {
    return this.request<ETLStatusResponse>('/etl/status')
  }

  async getETLLogs(lines: number = 100): Promise<ETLLogsResponse> {
    return this.request<ETLLogsResponse>(`/etl/logs?lines=${lines}`)
  }
}

export const api = new ApiClient(API_BASE_URL)
