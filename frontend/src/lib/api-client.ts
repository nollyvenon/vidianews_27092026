const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

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
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || `API Error: ${response.status}`)
    }

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
