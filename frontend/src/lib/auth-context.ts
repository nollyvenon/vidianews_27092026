import { createContext } from 'react'

export interface User {
  id: number
  email: string
  name: string
  role: string
  organization_id: number
  tenant_id: number
  avatar_url?: string
  created_at: string
}

/** Fields accepted by POST /auth/register (backend RegisterRequest). */
export interface SignupDetails {
  email: string
  password: string
  first_name: string
  last_name: string
}

export interface AuthContextType {
  token: string | null
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<any>
  logout: () => void
  signup: (details: SignupDetails) => Promise<any>
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)
