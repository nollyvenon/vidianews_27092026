'use client'

import { useState } from 'react'

export default function AlertsPage() {
  const [notifications] = useState([
    { id: 1, message: 'Sarah followed you', time: '5 min ago' },
    { id: 2, message: 'You were mentioned', time: '1 hour ago' },
    { id: 3, message: 'Someone liked your video', time: '3 hours ago' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Alerts</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Alerts</h2>
        <div className="space-y-3">
          {notifications.map(n => (
            <div key={n.id} className="border-l-4 border-blue-500 pl-4 py-3">
              <p className="font-medium text-sm">{n.message}</p>
              <p className="text-xs text-gray-500">{n.time}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
