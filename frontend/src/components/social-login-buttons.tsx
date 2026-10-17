'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

export interface SocialProvider {
  provider: string
  display_name: string
}

interface AuthorizationResponse {
  authorization_url: string
}

/** Sign-in buttons for the providers an administrator has enabled. Renders nothing when none are enabled. */
export function SocialLoginButtons() {
  const [providers, setProviders] = useState<SocialProvider[]>([])
  const [error, setError] = useState('')
  const [pending, setPending] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/auth/social/providers')
      .then((list: SocialProvider[]) => setProviders(list))
      .catch(() => setProviders([]))
  }, [])

  const startLogin = async (provider: string) => {
    setError('')
    setPending(provider)
    try {
      const response: AuthorizationResponse = await ApiClient.get(`/auth/social/${provider}/authorize`)
      window.location.assign(response.authorization_url)
    } catch (err: any) {
      setError(err.message || 'Could not start social sign-in')
      setPending(null)
    }
  }

  if (providers.length === 0) {
    return null
  }

  return (
    <div className="mt-6" aria-label="Social sign-in">
      <div className="relative my-4">
        <div className="absolute inset-0 flex items-center" aria-hidden="true">
          <div className="w-full border-t border-gray-200" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="bg-white px-2 text-gray-500">Or continue with</span>
        </div>
      </div>

      {error && (
        <p role="alert" className="mb-3 text-sm text-red-700">
          {error}
        </p>
      )}

      <div className="space-y-2">
        {providers.map((item) => (
          <button
            key={item.provider}
            type="button"
            onClick={() => startLogin(item.provider)}
            disabled={pending !== null}
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            {pending === item.provider ? 'Redirecting...' : `Continue with ${item.display_name}`}
          </button>
        ))}
      </div>
    </div>
  )
}
