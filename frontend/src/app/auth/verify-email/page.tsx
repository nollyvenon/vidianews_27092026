'use client'

import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

type VerificationState = 'confirming' | 'confirmed' | 'failed'

function VerifyEmailContent() {
  const token = useSearchParams().get('token')
  const [state, setState] = useState<VerificationState>(token ? 'confirming' : 'failed')
  const [message, setMessage] = useState(token ? '' : 'This link is missing its confirmation token.')

  useEffect(() => {
    if (!token) return
    ApiClient.post('/auth/verify-email', { token })
      .then(() => setState('confirmed'))
      .catch((error) => {
        setMessage(errorMessage(error, 'We could not confirm this address. The link may have expired.'))
        setState('failed')
      })
  }, [token])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-6 text-center space-y-4">
        <h1 className="text-2xl font-bold">Confirm your email</h1>
        {state === 'confirming' && <p className="text-gray-600">Confirming your address…</p>}
        {state === 'confirmed' && (
          <>
            <p className="text-green-700">Your email is confirmed. You can sign in now.</p>
            <Link href="/auth/login" className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md">
              Sign in
            </Link>
          </>
        )}
        {state === 'failed' && (
          <>
            <p role="alert" className="text-red-700">{message}</p>
            <Link href="/auth/signup" className="text-blue-600 hover:underline">
              Create an account again
            </Link>
          </>
        )}
      </div>
    </div>
  )
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading…</div>}>
      <VerifyEmailContent />
    </Suspense>
  )
}
