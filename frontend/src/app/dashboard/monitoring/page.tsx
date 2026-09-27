'use client'

import { useState } from 'react'

export default function MonitoringPage() {
  const [metrics] = useState([
    { type: 'Response Time', value: '45ms', status: 'good' },
    { type: 'Error Rate', value: '0.2%', status: 'good' },
    { type: 'CPU Usage', value: '32%', status: 'good' },
    { type: 'Memory Usage', value: '64%', status: 'warning' }
  ])

  const [alerts] = useState([
    { id: 1, severity: 'high', message: 'Database connection latency increased', time: '5 min ago' },
    { id: 2, severity: 'medium', message: 'Cache hit rate below threshold', time: '12 min ago' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">System Monitoring</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Key Metrics</h2>
          <div className="grid grid-cols-2 gap-4">
            {metrics.map((m, i) => (
              <div key={i} className="border rounded-lg p-4">
                <p className="text-sm text-gray-600">{m.type}</p>
                <p className="text-2xl font-bold mt-1">{m.value}</p>
                <span className={`inline-block mt-2 px-2 py-1 rounded text-xs ${
                  m.status === 'good' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {m.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Active Alerts</h2>
          <div className="space-y-3">
            {alerts.map(a => (
              <div key={a.id} className={`border-l-4 pl-4 py-2 ${
                a.severity === 'high' ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'
              }`}>
                <div className="flex justify-between items-start">
                  <p className="font-medium text-sm">{a.message}</p>
                  <span className="text-xs text-gray-500">{a.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Health Checks</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Database</span>
              <span className="text-green-600">✓ Healthy</span>
            </div>
            <div className="flex justify-between">
              <span>API Gateway</span>
              <span className="text-green-600">✓ Healthy</span>
            </div>
            <div className="flex justify-between">
              <span>Cache Service</span>
              <span className="text-green-600">✓ Healthy</span>
            </div>
            <div className="flex justify-between">
              <span>Message Queue</span>
              <span className="text-yellow-600">⚠ Degraded</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
