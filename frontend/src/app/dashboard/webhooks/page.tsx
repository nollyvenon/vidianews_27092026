'use client'

import { useState } from 'react'

export default function WebhooksPage() {
  const [webhooks] = useState([
    { id: 1, url: 'https://example.com/hook', event: 'user.created', status: 'active', lastFired: '2 min ago' },
    { id: 2, url: 'https://api.service.com/events', event: 'content.uploaded', status: 'active', lastFired: '5 min ago' },
    { id: 3, url: 'https://old-service.com/hook', event: 'payment.received', status: 'failed', lastFired: '1 hour ago' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Webhooks</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Active Webhooks</h2>
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ Add Webhook</button>
          </div>

          <div className="space-y-3">
            {webhooks.map(w => (
              <div key={w.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-sm break-all">{w.url}</p>
                    <p className="text-xs text-gray-600 mt-1">{w.event}</p>
                  </div>
                  <span className={`px-3 py-1 rounded text-xs font-medium ${
                    w.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {w.status}
                  </span>
                </div>
                <p className="text-xs text-gray-500">Last fired: {w.lastFired}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Webhook Events</h2>
          <div className="space-y-2 text-sm">
            <p>✓ user.created</p>
            <p>✓ content.uploaded</p>
            <p>✓ payment.received</p>
            <p>✓ subscription.changed</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Event Log</h2>
          <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 text-sm">
            View Full Event Log
          </button>
        </div>
      </div>
    </div>
  )
}
