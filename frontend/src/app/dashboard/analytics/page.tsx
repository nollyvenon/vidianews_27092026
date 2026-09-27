'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

export default function AnalyticsPage() {
  const [stats, setStats] = useState({
    total_views: 0,
    total_engagement: 0,
    avg_watch_time: 0,
    retention_rate: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const data = await ApiClient.get('/content/stats')
      setStats(data || stats)
    } catch (err) {
      console.error('Failed to fetch analytics', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-gray-600">Loading analytics...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Analytics</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-blue-600">{stats.total_views}</div>
          <div className="text-gray-600">Total Views</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">{stats.total_engagement}</div>
          <div className="text-gray-600">Total Engagement</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-purple-600">{stats.avg_watch_time}s</div>
          <div className="text-gray-600">Avg Watch Time</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-orange-600">{stats.retention_rate}%</div>
          <div className="text-gray-600">Retention Rate</div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Detailed Reports</h2>
        <div className="space-y-2">
          <div className="p-3 bg-gray-50 rounded">Video Performance Report</div>
          <div className="p-3 bg-gray-50 rounded">User Engagement Report</div>
          <div className="p-3 bg-gray-50 rounded">Content ROI Analysis</div>
          <div className="p-3 bg-gray-50 rounded">AI Feature Usage</div>
        </div>
      </div>
    </div>
  )
}
