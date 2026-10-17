'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { ApiClient } from '@/lib/api-client'

interface Notification {
  id: number
  title: string
  message: string
  is_read: boolean
  created_at: string
}

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refresh = useCallback(async () => {
    setError(null)
    try {
      const [items, count] = await Promise.all([
        ApiClient.get('/notifications/me?limit=50'),
        ApiClient.get('/notifications/me/unread-count'),
      ])
      setNotifications(items)
      setUnreadCount(count.unread_count)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load notifications')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  const runAction = async (action: () => Promise<unknown>) => {
    setError(null)
    try {
      await action()
      await refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Action failed')
    }
  }

  if (loading) return <div className="p-8">Loading...</div>

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Notifications</h1>
        {unreadCount > 0 && (
          <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm">{unreadCount} unread</span>
        )}
      </div>

      {error && <div role="alert" className="bg-red-50 text-red-700 rounded-lg p-4 mb-6">{error}</div>}

      {unreadCount > 0 && (
        <button
          onClick={() => runAction(() => ApiClient.post('/notifications/me/read-all', {}))}
          className="mb-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Mark all as read
        </button>
      )}

      <div className="space-y-4 mb-10">
        {notifications.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No notifications</p>
        ) : (
          notifications.map((notif) => (
            <div
              key={notif.id}
              className={`p-4 bg-white rounded-lg border ${notif.is_read ? 'border-gray-200' : 'border-blue-300 bg-blue-50'}`}
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h2 className="font-semibold text-lg">{notif.title}</h2>
                  <p className="text-gray-600 mt-1">{notif.message}</p>
                  <p className="text-xs text-gray-400 mt-2">{new Date(notif.created_at).toLocaleString()}</p>
                </div>
                <div className="flex gap-2 ml-4">
                  {!notif.is_read && (
                    <button
                      onClick={() => runAction(() => ApiClient.post(`/notifications/me/${notif.id}/read`, {}))}
                      className="text-sm px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                    >
                      Mark read
                    </button>
                  )}
                  <button
                    onClick={() => runAction(() => ApiClient.post(`/notifications/me/${notif.id}/archive`, {}))}
                    className="text-sm px-3 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                  >
                    Archive
                  </button>
                  <button
                    onClick={() => runAction(() => ApiClient.delete(`/notifications/me/${notif.id}`))}
                    className="text-sm px-3 py-1 bg-red-300 text-red-700 rounded hover:bg-red-400"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6 space-y-3">
        <h2 className="text-xl font-semibold">Preferences and devices</h2>
        <p className="text-sm text-gray-600">
          Choose which notifications you receive in{' '}
          <Link href="/dashboard/settings" className="text-blue-600 hover:underline">
            Settings
          </Link>
          .
        </p>
        <p className="text-sm text-gray-600">
          Registered push devices are not yet available. Device registration needs a backend endpoint first.
        </p>
      </div>
    </div>
  )
}
