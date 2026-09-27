'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'

export default function NotificationsCenterPage() {
  const [notifications, setNotifications] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchNotifications()
  }, [])

  const fetchNotifications = async () => {
    try {
      const data = await ApiClient.get('/system/notifications')
      setNotifications(data)
    } catch (err) {
      console.error('Failed to fetch notifications', err)
    } finally {
      setLoading(false)
    }
  }

  const markAsRead = async (id: number) => {
    try {
      await ApiClient.post(`/system/notifications/${id}/read`, {})
      setNotifications(notifications.map(n => n.id === id ? { ...n, is_read: true } : n))
    } catch (err) {
      console.error('Failed to mark as read', err)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Notifications</h1>

      {loading ? (
        <div className="text-gray-600">Loading...</div>
      ) : (
        <div className="space-y-3">
          {notifications.map((notif) => (
            <div
              key={notif.id}
              className={`p-4 border rounded-lg cursor-pointer ${
                notif.is_read ? 'bg-white' : 'bg-blue-50 border-blue-300'
              }`}
              onClick={() => !notif.is_read && markAsRead(notif.id)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold">{notif.title}</h3>
                  <p className="text-sm text-gray-600">{notif.message}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(notif.created_at).toLocaleString()}
                  </p>
                </div>
                <span className="text-xs px-2 py-1 bg-gray-200 rounded">
                  {notif.notification_type}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {notifications.length === 0 && !loading && (
        <div className="text-center text-gray-600 py-8">
          No notifications
        </div>
      )}
    </div>
  )
}
