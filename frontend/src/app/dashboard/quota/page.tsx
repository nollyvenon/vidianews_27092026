'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface QuotaUsage {
  api_calls: number
  storage_gb: number
  bandwidth_gb: number
}

/** Usage recorded for the signed-in user. No plan limits are configured on the server, so none are shown. */
export default function QuotaPage() {
  const [usage, setUsage] = useState<QuotaUsage | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/quota/usage')
      .then((data: QuotaUsage) => setUsage(data))
      .catch((err) => setError(errorMessage(err, 'Usage could not be loaded.')))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Usage & Quotas</h1>

      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        {!usage && !error && <p className="text-gray-500">Loading usage…</p>}
        {usage && (
          <dl className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <dt className="text-sm text-gray-600">API calls</dt>
              <dd className="text-3xl font-bold">{usage.api_calls.toLocaleString()}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Storage</dt>
              <dd className="text-3xl font-bold">{usage.storage_gb.toFixed(2)} GB</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Bandwidth</dt>
              <dd className="text-3xl font-bold">{usage.bandwidth_gb.toFixed(2)} GB</dd>
            </div>
          </dl>
        )}
        <p className="text-xs text-gray-500 mt-6">Usage is recorded as it happens. Plan limits are not set on this server.</p>
      </div>
    </div>
  )
}
