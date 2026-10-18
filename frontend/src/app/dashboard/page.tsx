'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface DashboardSummary {
  videos: number
  articles: number
  chats: number
  monthly_spend: number
}

export interface ActivityEntry {
  id: number
  action: string
  entity_type: string
  description: string | null
  created_at: string
}

/** Dashboard home: the signed-in user's own totals and their most recent activity. */
export default function DashboardPage() {
  const { user } = useAuth()
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [summaryError, setSummaryError] = useState<string | null>(null)
  const [activity, setActivity] = useState<ActivityEntry[] | null>(null)
  const [activityError, setActivityError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    ApiClient.get('/dashboard/summary')
      .then((data) => {
        if (active) setSummary(data as DashboardSummary)
      })
      .catch((err) => {
        if (active) setSummaryError(errorMessage(err, 'Your totals could not be loaded.'))
      })
    ApiClient.get('/activity/me?limit=5')
      .then((data) => {
        if (active) setActivity(data as ActivityEntry[])
      })
      .catch((err) => {
        if (active) setActivityError(errorMessage(err, 'Your recent activity could not be loaded.'))
      })
    return () => {
      active = false
    }
  }, [])

  const count = (value: number | undefined) => (summary ? String(value ?? 0) : summaryError ? '–' : '…')
  const spend = summary ? `$${summary.monthly_spend.toFixed(2)}` : summaryError ? '–' : '…'

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Welcome, {user?.name}!</h1>

      {summaryError && <p role="alert" className="mb-4 text-red-700">{summaryError}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-blue-600">{count(summary?.videos)}</div>
          <div className="text-gray-600">Videos</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">{count(summary?.articles)}</div>
          <div className="text-gray-600">Articles</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-purple-600">{count(summary?.chats)}</div>
          <div className="text-gray-600">Chats</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-orange-600">{spend}</div>
          <div className="text-gray-600">Monthly Spend</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="space-y-2">
            <Link href="/dashboard/content" className="block p-3 bg-blue-50 rounded hover:bg-blue-100">
              📹 Manage Content
            </Link>
            <Link href="/dashboard/ai" className="block p-3 bg-purple-50 rounded hover:bg-purple-100">
              🤖 AI Features
            </Link>
            <Link href="/dashboard/analytics" className="block p-3 bg-green-50 rounded hover:bg-green-100">
              📈 View Analytics
            </Link>
            <Link href="/dashboard/ecommerce" className="block p-3 bg-amber-50 rounded hover:bg-amber-100">
              🛒 Ecommerce
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          {activityError && <p role="alert" className="text-red-700">{activityError}</p>}
          {!activityError && activity === null && <p className="text-gray-600">Loading activity...</p>}
          {activity !== null && activity.length === 0 && <div className="text-gray-600">No recent activity yet.</div>}
          {activity !== null && activity.length > 0 && (
            <ul className="divide-y divide-gray-200">
              {activity.map((entry) => (
                <li key={entry.id} className="py-2 text-sm text-gray-700">
                  <span className="font-medium text-gray-900">{entry.description ?? entry.action}</span>
                  <span className="block text-xs text-gray-500">{new Date(entry.created_at).toLocaleString()}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
