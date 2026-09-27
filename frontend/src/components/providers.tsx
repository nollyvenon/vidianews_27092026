'use client'

import { ReactNode, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { AuthContext } from '@/lib/auth-context'
import { ApiClient } from '@/lib/api-client'

export function Providers({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState({ token: null, user: null, loading: true })
  const router = useRouter()

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          const response = await fetch('/api/v1/auth/me', {
            headers: { Authorization: `Bearer ${token}` }
          })
          if (response.ok) {
            const user = await response.json()
            setAuthState({ token, user, loading: false })
            ApiClient.setToken(token)
          } else {
            localStorage.removeItem('token')
            setAuthState({ token: null, user: null, loading: false })
          }
        } catch {
          setAuthState({ token: null, user: null, loading: false })
        }
      } else {
        setAuthState({ token: null, user: null, loading: false })
      }
    }

    checkAuth()
  }, [])

  const login = async (email: string, password: string) => {
    const response = await ApiClient.post('/auth/login', { email, password })
    const { access_token, user } = response
    localStorage.setItem('token', access_token)
    ApiClient.setToken(access_token)
    setAuthState({ token: access_token, user, loading: false })
    router.push('/dashboard')
    return response
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('tenant_id')
    ApiClient.setToken(null)
    setAuthState({ token: null, user: null, loading: false })
    router.push('/auth/login')
  }

  const signup = async (email: string, password: string, name: string) => {
    const response = await ApiClient.post('/auth/register', { email, password, name })
    const { access_token, user } = response
    localStorage.setItem('token', access_token)
    ApiClient.setToken(access_token)
    setAuthState({ token: access_token, user, loading: false })
    router.push('/dashboard')
    return response
  }

  return (
    <AuthContext.Provider value={{ ...authState, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  )
}
