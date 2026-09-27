'use client'

import { useState } from 'react'

export default function NotificationsPage() {
  const [devices] = useState([
    { id: 1, name: 'iPhone 14 Pro', platform: 'ios', active: true },
    { id: 2, name: 'Android Phone', platform: 'android', active: true }
  ])
  const [notifications] = useState([
    { id: 1, title: 'New Comment', body: 'Someone commented on your video', read: false, time: '2 hours ago' },
    { id: 2, title: 'Upload Complete', body: 'Your video has been processed', read: true, time: '1 day ago' }
  ])
  const [preferences, setPreferences] = useState({
    comments: true,
    likes: true,
    followers: false,
    system: true
  })

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Notifications</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Registered Devices</h2>
          <div className="space-y-3">
            {devices.map(device => (
              <div key={device.id} className="flex justify-between items-center p-3 border rounded">
                <div>
                  <p className="font-medium">{device.name}</p>
                  <p className="text-sm text-gray-600">{device.platform}</p>
                </div>
                <span className={`px-3 py-1 rounded text-sm ${device.active ? 'bg-green-100 text-green-800' : 'bg-gray-100'}`}>
                  {device.active ? 'Active' : 'Inactive'}
                </span>
              </div>
            ))}
          </div>
          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ Add Device</button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Notification Preferences</h2>
          <div className="space-y-3">
            {Object.entries(preferences).map(([key, value]) => (
              <div key={key} className="flex items-center">
                <input
                  type="checkbox"
                  checked={value}
                  onChange={(e) => setPreferences({...preferences, [key]: e.target.checked})}
                  className="mr-3"
                />
                <label className="capitalize">{key} notifications</label>
              </div>
            ))}
          </div>
          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save Preferences</button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Notifications</h2>
          <div className="space-y-3">
            {notifications.map(notif => (
              <div key={notif.id} className={`p-4 border rounded ${notif.read ? 'bg-gray-50' : 'bg-blue-50'}`}>
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium">{notif.title}</p>
                    <p className="text-sm text-gray-600">{notif.body}</p>
                    <p className="text-xs text-gray-500 mt-1">{notif.time}</p>
                  </div>
                  {!notif.read && <span className="w-3 h-3 bg-blue-600 rounded-full"></span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
