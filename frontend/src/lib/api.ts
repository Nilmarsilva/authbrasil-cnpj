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
}

export const api = new ApiClient(API_BASE_URL)
