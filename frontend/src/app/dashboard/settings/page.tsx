'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { ApiClient } from '@/lib/api-client'

type SettingsTab = 'notifications' | 'privacy' | 'display' | 'profile'

interface Settings {
  notifications: {
    email_on_activity: boolean
    push_enabled: boolean
    inapp_enabled: boolean
  }
  privacy: {
    profile_visibility: 'public' | 'private'
    allow_messages: 'everyone' | 'followers' | 'none'
  }
  display: {
    theme: 'light' | 'dark' | 'auto'
    language: string
  }
}

interface Profile {
  bio: string | null
  title: string | null
  location: string | null
  timezone: string
  is_public: boolean
}

const TABS: SettingsTab[] = ['notifications', 'privacy', 'display', 'profile']

export default function SettingsPage() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState<SettingsTab>('notifications')
  const [settings, setSettings] = useState<Settings | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [loadedSettings, loadedProfile] = await Promise.all([
          ApiClient.get('/settings/me'),
          ApiClient.get('/profiles/me'),
        ])
        setSettings(loadedSettings)
        setProfile(loadedProfile)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load settings')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const saveSection = async (section: 'notifications' | 'privacy' | 'display', values: object) => {
    setSaving(true)
    setError(null)
    setMessage(null)
    try {
      const updated = await ApiClient.put(`/settings/me/${section}`, values)
      setSettings((prev) => (prev ? { ...prev, [section]: updated[section] ?? { ...prev[section], ...values } } : prev))
      setMessage('Settings saved')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const saveProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!profile) return
    setSaving(true)
    setError(null)
    setMessage(null)
    try {
      const updated: Profile = await ApiClient.put('/profiles/me', {
        bio: profile.bio,
        title: profile.title,
        location: profile.location,
        timezone: profile.timezone,
        is_public: profile.is_public,
      })
      setProfile(updated)
      setMessage('Profile saved')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save profile')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="p-8">Loading...</div>
  if (!settings) return <div className="p-8 text-red-700">{error ?? 'Settings not found'}</div>

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Settings</h1>

      {error && <div role="alert" className="bg-red-50 text-red-700 rounded-lg p-4 mb-6">{error}</div>}
      {message && <div role="status" className="bg-green-50 text-green-700 rounded-lg p-4 mb-6">{message}</div>}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow">
          <div className="border-b border-gray-200 flex space-x-8 px-6">
            {TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                  activeTab === tab ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="p-6 space-y-4">
            {activeTab === 'notifications' && (
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault()
                  saveSection('notifications', settings.notifications)
                }}
              >
                {(
                  [
                    ['email_on_activity', 'Activity email notifications'],
                    ['push_enabled', 'Push notifications'],
                    ['inapp_enabled', 'In-app notifications'],
                  ] as const
                ).map(([key, label]) => (
                  <label key={key} className="flex justify-between items-center">
                    <span className="font-medium">{label}</span>
                    <input
                      type="checkbox"
                      checked={settings.notifications[key]}
                      onChange={(e) =>
                        setSettings({
                          ...settings,
                          notifications: { ...settings.notifications, [key]: e.target.checked },
                        })
                      }
                      className="w-4 h-4"
                    />
                  </label>
                ))}
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  Save notifications
                </button>
              </form>
            )}

            {activeTab === 'privacy' && (
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault()
                  saveSection('privacy', settings.privacy)
                }}
              >
                <label className="flex justify-between items-center">
                  <span className="font-medium">Profile visibility</span>
                  <select
                    value={settings.privacy.profile_visibility}
                    onChange={(e) =>
                      setSettings({
                        ...settings,
                        privacy: { ...settings.privacy, profile_visibility: e.target.value as 'public' | 'private' },
                      })
                    }
                    className="border rounded px-2 py-1"
                  >
                    <option value="private">Private</option>
                    <option value="public">Public</option>
                  </select>
                </label>
                <label className="flex justify-between items-center">
                  <span className="font-medium">Who can message you</span>
                  <select
                    value={settings.privacy.allow_messages}
                    onChange={(e) =>
                      setSettings({
                        ...settings,
                        privacy: { ...settings.privacy, allow_messages: e.target.value as Settings['privacy']['allow_messages'] },
                      })
                    }
                    className="border rounded px-2 py-1"
                  >
                    <option value="everyone">Everyone</option>
                    <option value="followers">Followers</option>
                    <option value="none">No one</option>
                  </select>
                </label>
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  Save privacy
                </button>
              </form>
            )}

            {activeTab === 'display' && (
              <form
                className="space-y-4"
                onSubmit={(e) => {
                  e.preventDefault()
                  saveSection('display', settings.display)
                }}
              >
                <label className="flex justify-between items-center">
                  <span className="font-medium">Theme</span>
                  <select
                    value={settings.display.theme}
                    onChange={(e) =>
                      setSettings({
                        ...settings,
                        display: { ...settings.display, theme: e.target.value as Settings['display']['theme'] },
                      })
                    }
                    className="border rounded px-2 py-1"
                  >
                    <option value="light">Light</option>
                    <option value="dark">Dark</option>
                    <option value="auto">Auto</option>
                  </select>
                </label>
                <label className="flex justify-between items-center">
                  <span className="font-medium">Language</span>
                  <select
                    value={settings.display.language}
                    onChange={(e) =>
                      setSettings({ ...settings, display: { ...settings.display, language: e.target.value } })
                    }
                    className="border rounded px-2 py-1"
                  >
                    <option value="en">English</option>
                    <option value="es">Español</option>
                    <option value="fr">Français</option>
                  </select>
                </label>
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  Save display
                </button>
              </form>
            )}

            {activeTab === 'profile' && profile && (
              <form onSubmit={saveProfile} className="space-y-4">
                <div>
                  <span className="block text-sm font-medium text-gray-700 mb-1">Name</span>
                  <p className="text-gray-900">{user?.name ?? '—'}</p>
                </div>
                <div>
                  <span className="block text-sm font-medium text-gray-700 mb-1">Email</span>
                  <p className="text-gray-900">{user?.email ?? '—'}</p>
                </div>
                <label className="block">
                  <span className="block text-sm font-medium text-gray-700 mb-1">Title</span>
                  <input
                    type="text"
                    value={profile.title ?? ''}
                    onChange={(e) => setProfile({ ...profile, title: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md"
                  />
                </label>
                <label className="block">
                  <span className="block text-sm font-medium text-gray-700 mb-1">Bio</span>
                  <textarea
                    value={profile.bio ?? ''}
                    onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                    rows={4}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md"
                  />
                </label>
                <label className="block">
                  <span className="block text-sm font-medium text-gray-700 mb-1">Location</span>
                  <input
                    type="text"
                    value={profile.location ?? ''}
                    onChange={(e) => setProfile({ ...profile, location: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md"
                  />
                </label>
                <label className="block">
                  <span className="block text-sm font-medium text-gray-700 mb-1">Timezone</span>
                  <input
                    type="text"
                    value={profile.timezone}
                    onChange={(e) => setProfile({ ...profile, timezone: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md"
                  />
                </label>
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={profile.is_public}
                    onChange={(e) => setProfile({ ...profile, is_public: e.target.checked })}
                  />
                  <span className="text-sm">Public profile</span>
                </label>
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  {saving ? 'Saving...' : 'Save profile'}
                </button>
              </form>
            )}
          </div>
        </div>

        <div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Danger Zone</h2>
            <p className="text-sm text-gray-600 mb-4">
              Account deletion is not yet available. It needs a backend endpoint before it can be enabled.
            </p>
            <button disabled className="w-full px-4 py-2 bg-red-600 text-white rounded-md text-sm opacity-50 cursor-not-allowed">
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
