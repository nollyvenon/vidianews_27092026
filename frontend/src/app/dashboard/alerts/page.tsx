'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Notification {
  id: number
  title: string
  message: string
  is_read: boolean
  created_at: string
}

export default function AlertsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [busyId, setBusyId] = useState<number | null>(null)

  useEffect(() => {
    let active = true
    ApiClient.get('/notifications/me')
      .then((data: Notification[]) => {
        if (active) setNotifications(Array.isArray(data) ? data : [])
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'Alerts could not be loaded.'))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const markRead = async (id: number) => {
    setBusyId(id)
    setError(null)
    try {
      const updated: Notification = await ApiClient.post(`/notifications/me/${id}/read`, {})
      setNotifications((current) => current.map((item) => (item.id === id ? updated : item)))
    } catch (err) {
      setError(errorMessage(err, 'The alert could not be marked as read.'))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Alerts</h1>
      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Alerts</h2>
        {loading ? (
          <p className="text-gray-500">Loading alerts…</p>
        ) : notifications.length === 0 ? (
          <p className="text-gray-500">No alerts yet.</p>
        ) : (
          <div className="space-y-3">
            {notifications.map((n) => (
              <div key={n.id} className={`border-l-4 pl-4 py-3 ${n.is_read ? 'border-gray-300' : 'border-blue-500'}`}>
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <p className="font-medium text-sm">{n.title}</p>
                    <p className="text-sm text-gray-700">{n.message}</p>
                    <p className="text-xs text-gray-500">{new Date(n.created_at).toLocaleString()}</p>
                  </div>
                  {n.is_read ? (
                    <span className="text-xs text-gray-500">Read</span>
                  ) : (
                    <button
                      type="button"
                      disabled={busyId === n.id}
                      onClick={() => markRead(n.id)}
                      className="px-3 py-1 text-sm border border-blue-600 text-blue-600 rounded hover:bg-blue-50 disabled:opacity-50"
                    >
                      Mark as read
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
