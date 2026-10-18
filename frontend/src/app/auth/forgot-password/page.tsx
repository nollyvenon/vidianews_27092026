'use client'

import { FormEvent, useState } from 'react'
import Link from 'next/link'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

/** Starts a password reset. The answer is the same whether or not the address has an account. */
export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const response = await ApiClient.post('/auth/forgot-password', { email: email.trim() })
      setMessage(response.message)
    } catch (err) {
      setError(errorMessage(err, 'The reset link could not be requested. Try again shortly.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-6 space-y-4">
        <h1 className="text-2xl font-bold text-center">Reset your password</h1>

        {message ? (
          <p role="status" className="text-gray-700">{message}</p>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <p role="alert" className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">{error}</p>}
            <label className="block text-sm font-medium text-gray-700">
              Email address
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
                placeholder="your@email.com"
                required
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white font-medium py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Sending...' : 'Send reset link'}
            </button>
          </form>
        )}

        <p className="text-center text-sm">
          <Link href="/auth/login" className="text-blue-600 hover:underline">Back to sign in</Link>
        </p>
      </div>
    </div>
  )
}
