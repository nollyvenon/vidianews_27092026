'use client'

import { ReactNode, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthContext, SignupDetails } from '@/lib/auth-context'
import { ApiClient } from '@/lib/api-client'
import { Toaster } from '@/components/toaster'

interface AuthState {
  token: string | null
  user: any
  loading: boolean
}

/** Shape of POST /auth/login responses (backend TokenResponse). */
interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

/** Shape of POST /auth/register responses (backend RegisterResponse). */
export interface RegisterResult {
  requires_verification: boolean
  message: string
  access_token?: string | null
  refresh_token?: string | null
  token_type?: string
}

export function Providers({ children }: { children: ReactNode }) {
  // One client per browser session, created on mount so server rendering never shares state.
  const [queryClient] = useState(() => new QueryClient())
  const [authState, setAuthState] = useState<AuthState>({ token: null, user: null, loading: true })
  const router = useRouter()

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      if (!token) {
        setAuthState({ token: null, user: null, loading: false })
        return
      }
      ApiClient.setToken(token)
      try {
        const user = await ApiClient.get('/auth/me')
        setAuthState({ token, user, loading: false })
      } catch {
        // An expired or revoked token is treated as signed out.
        ApiClient.setToken(null)
        localStorage.removeItem('token')
        setAuthState({ token: null, user: null, loading: false })
      }
    }

    checkAuth()
  }, [])

  // Stores the issued tokens, loads the user (the token response does not include it), and
  // enters the dashboard. Shared by login and signup so both routes produce the same session.
  const startSession = async (tokens: TokenResponse) => {
    localStorage.setItem('token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
    ApiClient.setToken(tokens.access_token)
    const user = await ApiClient.get('/auth/me')
    setAuthState({ token: tokens.access_token, user, loading: false })
    router.push('/dashboard')
    return tokens
  }

  // otpCode is sent only when the account has two-factor authentication on.
  const login = async (email: string, password: string, otpCode?: string) => {
    const tokens: TokenResponse = await ApiClient.post('/auth/login', { email, password, otp_code: otpCode })
    return startSession(tokens)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('tenant_id')
    ApiClient.setToken(null)
    setAuthState({ token: null, user: null, loading: false })
    router.push('/auth/login')
  }

  // Returns the backend's registration outcome. When the account needs email confirmation no
  // session is started; the caller shows the "check your email" state instead.
  const signup = async (details: SignupDetails): Promise<RegisterResult> => {
    // Callers validate the password confirmation before calling; the backend requires the field.
    const result: RegisterResult = await ApiClient.post('/auth/register', {
      ...details,
      password_confirm: details.password,
    })
    if (result.requires_verification || !result.access_token) {
      return result
    }
    await startSession({
      access_token: result.access_token,
      refresh_token: result.refresh_token ?? '',
      token_type: result.token_type ?? 'bearer',
    })
    return result
  }

  return (
    <QueryClientProvider client={queryClient}>
      <AuthContext.Provider value={{ ...authState, login, logout, signup }}>
        {children}
        <Toaster />
      </AuthContext.Provider>
    </QueryClientProvider>
  )
}
