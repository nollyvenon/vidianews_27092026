'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface UsageStats {
  period_days: number
  total: number
  average: number
  count: number
}

interface DailyUsage {
  date: string
  total: number
}

interface CostAlert {
  id: number
  threshold: number
  period: string
}

export default function MonitoringPage() {
  const [stats, setStats] = useState<UsageStats>({
    period_days: 30,
    total: 0,
    average: 0,
    count: 0,
  })
  const [daily, setDaily] = useState<DailyUsage[]>([])
  const [alerts, setAlerts] = useState<CostAlert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [newAlertThreshold, setNewAlertThreshold] = useState('100')

  const loadAlerts = () =>
    ApiClient.get('/ai/alerts')
      .then((data: CostAlert[]) => setAlerts(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Cost alerts could not be loaded.')))

  useEffect(() => {
    let active = true
    Promise.all([
      ApiClient.get('/ai/metrics/usage?days=30'),
      ApiClient.get('/ai/metrics/usage/daily?days=7'),
      ApiClient.get('/ai/alerts'),
    ])
      .then(([usage, days, alertRows]) => {
        if (!active) return
        setStats(usage)
        setDaily(Array.isArray(days) ? days : [])
        setAlerts(Array.isArray(alertRows) ? alertRows : [])
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'AI usage could not be loaded.'))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const createAlert = async () => {
    setError(null)
    try {
      await ApiClient.post('/ai/alerts/cost', {
        threshold: parseFloat(newAlertThreshold),
        period: 'monthly',
      })
      setNewAlertThreshold('100')
      await loadAlerts()
    } catch (err) {
      setError(errorMessage(err, 'The cost alert could not be created.'))
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  const peak = Math.max(0, ...daily.map((point) => point.total))

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">AI Monitoring</h1>
      {error && <p role="alert" className="mb-6 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold">{stats.total}</div>
          <div className="text-gray-600">Total Tokens</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold">${stats.average.toFixed(2)}</div>
          <div className="text-gray-600">Avg Cost</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold">{stats.count}</div>
          <div className="text-gray-600">API Calls</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold">{stats.period_days}d</div>
          <div className="text-gray-600">Period</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Cost Alerts</h2>
          <div className="mb-4 flex gap-2">
            <input
              type="number"
              value={newAlertThreshold}
              onChange={(e) => setNewAlertThreshold(e.target.value)}
              placeholder="Threshold ($)"
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md"
            />
            <button
              onClick={createAlert}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Add Alert
            </button>
          </div>
          <div className="space-y-2">
            {alerts.map((alert) => (
              <div key={alert.id} className="p-3 bg-gray-50 rounded">
                <div className="font-medium">${alert.threshold} / month</div>
                <div className="text-sm text-gray-600">{alert.period}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Usage Trends (last 7 days)</h2>
          {daily.length === 0 ? (
            <p className="text-sm text-gray-500">No usage recorded yet.</p>
          ) : (
            <div className="h-48 flex items-end justify-around gap-2">
              {daily.map((point) => (
                <div key={point.date} className="flex-1 flex flex-col items-center justify-end h-full">
                  <div
                    className="w-full bg-blue-200 rounded"
                    style={{ height: peak > 0 ? `${(point.total / peak) * 100}%` : '0%' }}
                    title={`${point.date}: ${point.total} tokens`}
                  />
                  <span className="mt-1 text-xs text-gray-500">{point.date.slice(5)}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
