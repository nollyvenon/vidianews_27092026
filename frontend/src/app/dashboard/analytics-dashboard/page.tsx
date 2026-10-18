'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface RevenueRow {
  date: string
  total_revenue: number
  transaction_count: number
}

interface EngagementRow {
  date: string
  active_users: number
  new_users: number
}

interface AnalyticsSummary {
  days: number
  views: number
  watch_hours: number
  subscribers: number
}

const WINDOW_DAYS = 30

export default function AnalyticsDashboardPage() {
  const [revenue, setRevenue] = useState<RevenueRow[]>([])
  const [engagement, setEngagement] = useState<EngagementRow[]>([])
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    const end = new Date()
    const start = new Date(end.getTime() - WINDOW_DAYS * 24 * 60 * 60 * 1000)
    Promise.all([
      ApiClient.get(
        `/analytics/revenue?start_date=${encodeURIComponent(start.toISOString())}&end_date=${encodeURIComponent(end.toISOString())}`,
      ),
      ApiClient.get(`/analytics/engagement?days=${WINDOW_DAYS}`),
      ApiClient.get(`/analytics/summary?days=${WINDOW_DAYS}`),
    ])
      .then(([revenueRows, engagementRows, summaryFigures]) => {
        if (!active) return
        setRevenue(Array.isArray(revenueRows) ? revenueRows : [])
        setEngagement(Array.isArray(engagementRows) ? engagementRows : [])
        setSummary(summaryFigures)
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'Analytics could not be loaded.'))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const totalRevenue = revenue.reduce((sum, row) => sum + Number(row.total_revenue || 0), 0)
  const transactions = revenue.reduce((sum, row) => sum + Number(row.transaction_count || 0), 0)
  const newUsers = engagement.reduce((sum, row) => sum + Number(row.new_users || 0), 0)
  const latestActive = engagement.length > 0 ? engagement[engagement.length - 1].active_users : null

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Analytics Dashboard</h1>
      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Views (last {WINDOW_DAYS} days)</p>
          <p className="text-3xl font-bold text-blue-600">{summary ? summary.views.toLocaleString() : loading ? '…' : '—'}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Watch Hours</p>
          <p className="text-3xl font-bold text-green-600">{summary ? summary.watch_hours.toFixed(1) : loading ? '…' : '—'}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Active Subscribers</p>
          <p className="text-3xl font-bold text-purple-600">{summary ? summary.subscribers.toLocaleString() : loading ? '…' : '—'}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Revenue (last {WINDOW_DAYS} days)</p>
          <p className="text-3xl font-bold text-orange-600">{loading ? '…' : `$${totalRevenue.toFixed(2)}`}</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Activity (last {WINDOW_DAYS} days)</h2>
        {loading ? (
          <p className="text-gray-500">Loading analytics…</p>
        ) : (
          <dl className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <dt className="text-sm text-gray-600">Transactions</dt>
              <dd className="text-2xl font-bold">{transactions}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">Active users (latest day)</dt>
              <dd className="text-2xl font-bold">{latestActive ?? '—'}</dd>
            </div>
            <div>
              <dt className="text-sm text-gray-600">New users</dt>
              <dd className="text-2xl font-bold">{newUsers}</dd>
            </div>
          </dl>
        )}
      </div>
    </div>
  )
}
