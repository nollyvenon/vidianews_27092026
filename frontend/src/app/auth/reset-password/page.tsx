'use client'

import { FormEvent, Suspense, useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

function ResetPasswordForm() {
  const token = useSearchParams().get('token') ?? ''
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(false)

  if (!token) {
    return <p role="alert" className="text-red-700">This link is missing its reset token. Request a new one.</p>
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    if (password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }
    if (password !== confirm) {
      setError('Passwords do not match')
      return
    }
    setLoading(true)
    try {
      await ApiClient.post('/auth/reset-password', { token, new_password: password, password_confirm: confirm })
      setDone(true)
    } catch (err) {
      setError(errorMessage(err, 'The password could not be reset. The link may have expired.'))
    } finally {
      setLoading(false)
    }
  }

  if (done) {
    return (
      <div className="space-y-4 text-center">
        <p role="status" className="text-green-700">Your password has been reset. You can sign in now.</p>
        <Link href="/auth/login" className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md">Sign in</Link>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <p role="alert" className="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">{error}</p>}
      <label className="block text-sm font-medium text-gray-700">
        New password (min 8 characters)
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
          required
        />
      </label>
      <label className="block text-sm font-medium text-gray-700">
        Confirm new password
        <input
          type="password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md"
          required
        />
      </label>
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white font-medium py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Saving...' : 'Set new password'}
      </button>
    </form>
  )
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow p-6 space-y-4">
        <h1 className="text-2xl font-bold text-center">Choose a new password</h1>
        <Suspense fallback={<p className="text-gray-600">Loading…</p>}>
          <ResetPasswordForm />
        </Suspense>
      </div>
    </div>
  )
}
