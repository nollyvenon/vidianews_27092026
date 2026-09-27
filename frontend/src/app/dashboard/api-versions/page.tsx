'use client'

import { useState } from 'react'

export default function APIVersionsPage() {
  const [versions] = useState([
    { id: 1, endpoint: '/api/users', version: 'v3', deprecated: false, usage: 8500 },
    { id: 2, endpoint: '/api/posts', version: 'v2', deprecated: false, usage: 3200 },
    { id: 3, endpoint: '/api/content', version: 'v1', deprecated: true, sunsetDate: '2026-12-31', usage: 120 }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">API Versions</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Active Versions</h2>
          <div className="space-y-3">
            {versions.map(v => (
              <div key={v.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-lg">{v.endpoint}</p>
                    <p className="text-sm text-gray-600">Version {v.version}</p>
                  </div>
                  <span className={`px-3 py-1 rounded text-sm font-medium ${
                    v.deprecated ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                  }`}>
                    {v.deprecated ? 'Deprecated' : 'Active'}
                  </span>
                </div>
                <p className="text-sm text-gray-600">Usage: {v.usage.toLocaleString()} calls/day</p>
                {v.deprecated && (
                  <p className="text-xs text-red-600 mt-2">Sunset: {v.sunsetDate}</p>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Migration Path</h2>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-900">
              Migrate from v1 → v2 → v3 for latest features and performance improvements.
            </p>
            <button className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
              View Migration Guide
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
