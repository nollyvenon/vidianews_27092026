'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

export default function MonitoringPage() {
  const [stats, setStats] = useState({
    period_days: 30,
    total: 0,
    average: 0,
    count: 0,
  })
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)
  const [newAlertThreshold, setNewAlertThreshold] = useState('100')

  useEffect(() => {
    fetchStats()
    fetchAlerts()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await ApiClient.get('/ai/metrics/usage?days=30')
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchAlerts = async () => {
    try {
      const data = await ApiClient.get('/ai/alerts')
      setAlerts(data)
    } catch (err) {
      console.error('Failed to fetch alerts', err)
    }
  }

  const createAlert = async () => {
    try {
      await ApiClient.post('/ai/alerts/cost', {
        threshold: parseFloat(newAlertThreshold),
        period: 'monthly',
      })
      setNewAlertThreshold('100')
      fetchAlerts()
    } catch (err) {
      console.error('Failed to create alert', err)
    }
  }

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">AI Monitoring</h1>

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
            {alerts.map((alert: any) => (
              <div key={alert.id} className="p-3 bg-gray-50 rounded">
                <div className="font-medium">${alert.threshold} / month</div>
                <div className="text-sm text-gray-600">{alert.period}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Usage Trends</h2>
          <div className="h-48 flex items-end justify-around gap-2">
            {[...Array(7)].map((_, i) => (
              <div
                key={i}
                className="flex-1 bg-blue-200 rounded"
                style={{ height: `${Math.random() * 100}%` }}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
