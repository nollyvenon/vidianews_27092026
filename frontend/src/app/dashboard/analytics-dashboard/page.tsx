'use client'

import { useState } from 'react'

export default function AnalyticsDashboardPage() {
  const [metrics] = useState({
    views: 125420,
    watchHours: 5230,
    subscribers: 3450,
    revenue: 1240.50
  })

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Analytics Dashboard</h1>
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Views</p>
          <p className="text-3xl font-bold text-blue-600">{(metrics.views/1000).toFixed(1)}K</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Watch Hours</p>
          <p className="text-3xl font-bold text-green-600">{(metrics.watchHours/1000).toFixed(1)}K</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Subscribers</p>
          <p className="text-3xl font-bold text-purple-600">{(metrics.subscribers/1000).toFixed(1)}K</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Revenue</p>
          <p className="text-3xl font-bold text-orange-600">${metrics.revenue.toFixed(2)}</p>
        </div>
      </div>
    </div>
  )
}
