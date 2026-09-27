'use client'

import { useState } from 'react'

export default function PrivacyPage() {
  const [settings, setSettings] = useState({
    profileVisibility: 'public',
    contentVisibility: 'public',
    allowAnalytics: true,
    allowMarketing: false
  })
  const [deletionRequest, setDeletionRequest] = useState(null)

  const handleUpdateSettings = (key: string, value: any) => {
    setSettings({ ...settings, [key]: value })
  }

  const requestDataDeletion = () => {
    setDeletionRequest({
      id: 1,
      status: 'pending',
      scheduledFor: '2026-10-27'
    })
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Privacy & GDPR Settings</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Privacy Preferences</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Profile Visibility</label>
              <select
                value={settings.profileVisibility}
                onChange={(e) => handleUpdateSettings('profileVisibility', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none"
              >
                <option>public</option>
                <option>private</option>
                <option>friends_only</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Content Visibility</label>
              <select
                value={settings.contentVisibility}
                onChange={(e) => handleUpdateSettings('contentVisibility', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none"
              >
                <option>public</option>
                <option>private</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.allowAnalytics}
                onChange={(e) => handleUpdateSettings('allowAnalytics', e.target.checked)}
                className="mr-3"
              />
              <label>Allow analytics tracking</label>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.allowMarketing}
                onChange={(e) => handleUpdateSettings('allowMarketing', e.target.checked)}
                className="mr-3"
              />
              <label>Allow marketing emails</label>
            </div>
          </div>
          <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Save Changes</button>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Data Management</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-600 mb-2">Download your data</p>
              <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">Export Data</button>
            </div>

            <div>
              <p className="text-sm text-gray-600 mb-2">Request data deletion (30-day notice)</p>
              <button
                onClick={requestDataDeletion}
                className={`px-4 py-2 rounded ${deletionRequest ? 'bg-red-100 text-red-800' : 'border border-red-600 text-red-600'}`}
              >
                {deletionRequest ? 'Deletion Pending' : 'Request Deletion'}
              </button>
            </div>

            {deletionRequest && (
              <div className="bg-red-50 border border-red-200 rounded p-4">
                <p className="text-sm text-red-800">Your account will be deleted on {deletionRequest.scheduledFor}</p>
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Consent History</h2>
          <div className="space-y-2 text-sm">
            <p>✓ Terms of Service - Sept 27, 2026</p>
            <p>✓ Privacy Policy - Sept 27, 2026</p>
            <p>✓ Cookie Policy - Sept 27, 2026</p>
          </div>
        </div>
      </div>
    </div>
  )
}
