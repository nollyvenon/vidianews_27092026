'use client'

import { useState } from 'react'

export default function ErrorsPage() {
  const [errors] = useState([
    { id: 1, type: 'ValueError', message: 'Invalid input parameter', severity: 'high', count: 12, lastSeen: '5 min ago' },
    { id: 2, type: 'DatabaseError', message: 'Connection timeout', severity: 'critical', count: 8, lastSeen: '2 min ago' },
    { id: 3, type: 'TypeError', message: 'Unexpected type conversion', severity: 'medium', count: 3, lastSeen: '1 hour ago' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Error Tracking</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Unresolved Errors</h2>
          <div className="space-y-3">
            {errors.map(err => (
              <div key={err.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold">{err.type}</p>
                    <p className="text-sm text-gray-600">{err.message}</p>
                  </div>
                  <span className={`px-3 py-1 rounded text-xs font-medium ${
                    err.severity === 'critical' ? 'bg-red-200 text-red-800' :
                    err.severity === 'high' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {err.severity}
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-600">{err.count} occurrences</span>
                  <span className="text-gray-500">Last: {err.lastSeen}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Error Trends</h2>
          <div className="text-center py-8">
            <p className="text-gray-600">Error rate trending down ✓</p>
          </div>
        </div>
      </div>
    </div>
  )
}
