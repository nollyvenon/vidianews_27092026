'use client'

import { useState } from 'react'

export default function SecurityPage() {
  const [rateLimit] = useState({ endpoint: '/api/content', requests: 850, limit: 1000 })
  const [oauthProviders] = useState([
    { id: 1, name: 'Google', connected: true },
    { id: 2, name: 'GitHub', connected: false }
  ])
  const [mfa, setMfa] = useState({ enabled: false, method: 'totp' })

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Security Settings</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Rate Limiting</h2>
          <div className="space-y-2">
            <p className="text-sm text-gray-600">{rateLimit.endpoint}</p>
            <div className="w-full bg-gray-200 rounded h-2">
              <div className="bg-blue-600 h-2 rounded" style={{ width: `${(rateLimit.requests / rateLimit.limit) * 100}%` }}></div>
            </div>
            <p className="text-sm">{rateLimit.requests} / {rateLimit.limit} requests</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">OAuth Providers</h2>
          <div className="space-y-3">
            {oauthProviders.map(p => (
              <div key={p.id} className="flex justify-between items-center">
                <span>{p.name}</span>
                <span className={`px-3 py-1 rounded text-sm ${p.connected ? 'bg-green-100 text-green-800' : 'bg-gray-100'}`}>
                  {p.connected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            ))}
          </div>
          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ Add Provider</button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Two-Factor Authentication</h2>
          <div className="flex justify-between items-center">
            <div>
              <p className="font-medium">MFA Status</p>
              <p className="text-sm text-gray-600">{mfa.enabled ? 'Enabled' : 'Disabled'}</p>
            </div>
            <button
              onClick={() => setMfa({...mfa, enabled: !mfa.enabled})}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {mfa.enabled ? 'Disable' : 'Enable'} MFA
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
