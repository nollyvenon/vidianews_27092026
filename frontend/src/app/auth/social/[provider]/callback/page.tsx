'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams } from 'next/navigation'
import { ApiClient } from '@/lib/api-client'

interface SocialTokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

/** Receives the provider redirect, exchanges the code for local tokens and enters the dashboard. */
export default function SocialLoginCallbackPage() {
  const params = useParams<{ provider: string }>()
  const [error, setError] = useState('')

  useEffect(() => {
    const query = new URLSearchParams(window.location.search)
    const providerError = query.get('error_description') || query.get('error')
    const code = query.get('code')
    const state = query.get('state')

    if (providerError) {
      setError(`Sign-in was cancelled: ${providerError}`)
      return
    }
    if (!code || !state) {
      setError('The sign-in response is incomplete. Please try again.')
      return
    }

    ApiClient.post(`/auth/social/${params.provider}/exchange`, { code, state })
      .then((tokens: SocialTokenResponse) => {
        localStorage.setItem('token', tokens.access_token)
        localStorage.setItem('refresh_token', tokens.refresh_token)
        // Full navigation so the auth provider re-reads the stored session on load.
        window.location.replace('/dashboard')
      })
      .catch((err: Error) => {
        setError(err.message || 'Social sign-in failed')
      })
  }, [params.provider])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div className="w-full max-w-md rounded-lg bg-white p-8 shadow">
          <h1 className="text-xl font-semibold text-gray-900">Sign-in failed</h1>
          <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>
          <Link href="/auth/login" className="mt-6 inline-block text-sm text-blue-600 hover:underline">
            Back to sign in
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <p className="text-sm text-gray-600" role="status">Completing sign-in...</p>
    </div>
  )
}
