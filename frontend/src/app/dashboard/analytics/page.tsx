'use client'

import { useState } from 'react'

export default function AnalyticsPage() {
  const [events] = useState([
    { type: 'page_view', count: 45230, percentage: 45 },
    { type: 'click', count: 23450, percentage: 23 },
    { type: 'video_play', count: 18900, percentage: 19 },
    { type: 'signup', count: 12340, percentage: 12 }
  ])

  const totalEvents = events.reduce((sum, e) => sum + e.count, 0)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Analytics</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Event Distribution</h2>
          <div className="space-y-4">
            {events.map((event, idx) => (
              <div key={idx}>
                <div className="flex justify-between mb-1">
                  <p className="text-sm font-medium">{event.type}</p>
                  <span className="text-sm text-gray-600">{event.count.toLocaleString()} ({event.percentage}%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${event.percentage}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Key Metrics</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{(totalEvents / 1000).toFixed(1)}K</p>
              <p className="text-xs text-gray-600">Total Events</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">2.3K</p>
              <p className="text-xs text-gray-600">Active Users</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">4.2m</p>
              <p className="text-xs text-gray-600">Session Time</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">User Sessions</h2>
          <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 text-sm">
            View Session Details
          </button>
        </div>
      </div>
    </div>
  )
}
