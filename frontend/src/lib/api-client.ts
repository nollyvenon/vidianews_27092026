import { ApiError, messageFromDetail } from '@/lib/api-error'

// Same-origin base: next.config.js rewrites /api/v1/* to the backend (NEXT_PUBLIC_API_URL).
const BASE_URL = '/api/v1'

class ApiClientClass {
  private token: string | null = null

  setToken(token: string | null) {
    this.token = token
  }

  private async request(method: string, endpoint: string, body?: any) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    const options: RequestInit = {
      method,
      headers,
    }

    if (body) {
      options.body = JSON.stringify(body)
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, options)

    if (!response.ok) {
      const body = await response.json().catch(() => ({}))
      throw new ApiError(messageFromDetail(body?.detail) ?? `API Error: ${response.status}`)
    }

    // 204 No Content (for example DELETE) has no body to parse.
    if (response.status === 204) return null
    return response.json()
  }

  async get(endpoint: string) {
    return this.request('GET', endpoint)
  }

  async post(endpoint: string, body: any) {
    return this.request('POST', endpoint, body)
  }

  async put(endpoint: string, body: any) {
    return this.request('PUT', endpoint, body)
  }

  async patch(endpoint: string, body: any) {
    return this.request('PATCH', endpoint, body)
  }

  async delete(endpoint: string) {
    return this.request('DELETE', endpoint)
  }
}

export const ApiClient = new ApiClientClass()
