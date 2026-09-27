'use client'

import { useState } from 'react'

export default function FeaturesPage() {
  const [flags] = useState([
    { id: 1, name: 'dark_mode', status: 'enabled', rollout: 100 },
    { id: 2, name: 'new_ui', status: 'rollout', rollout: 50 },
    { id: 3, name: 'beta_search', status: 'disabled', rollout: 0 }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Feature Flags</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Active Flags</h2>
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">+ New Flag</button>
          </div>

          <div className="space-y-3">
            {flags.map(flag => (
              <div key={flag.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <p className="font-semibold">{flag.name}</p>
                  <span className={`px-3 py-1 rounded text-sm font-medium ${
                    flag.status === 'enabled' ? 'bg-green-100 text-green-800' :
                    flag.status === 'rollout' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {flag.status}
                  </span>
                </div>
                {flag.rollout > 0 && (
                  <div className="text-sm text-gray-600 mb-2">Rollout: {flag.rollout}%</div>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">A/B Tests</h2>
          <div className="border rounded-lg p-4">
            <p className="font-medium mb-2">New UI Test</p>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Variant A: 1.2K conversions</p>
              </div>
              <div>
                <p className="text-gray-600">Variant B: 1.5K conversions</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
