'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface PrivacySettings {
  profile_visibility: string
  content_visibility: string
  allow_analytics: boolean
  allow_marketing: boolean
}

interface ConsentEntry {
  id: number
  consent_type: string
  granted: boolean
  version: string | null
}

const VISIBILITY = [
  { value: 'public', label: 'Public' },
  { value: 'friends_only', label: 'Friends only' },
  { value: 'private', label: 'Private' },
]

/** Privacy preferences, consent history, a copy of the personal data, and account deletion. */
export default function PrivacyPage() {
  const [settings, setSettings] = useState<PrivacySettings | null>(null)
  const [consents, setConsents] = useState<ConsentEntry[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const loadConsents = () =>
    ApiClient.get('/privacy/consents')
      .then((data: ConsentEntry[]) => setConsents(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Consent history could not be loaded.')))

  useEffect(() => {
    ApiClient.get('/privacy/settings')
      .then((data: PrivacySettings) => setSettings(data))
      .catch((err) => setError(errorMessage(err, 'Privacy settings could not be loaded.')))
    loadConsents()
  }, [])

  const save = async (event: FormEvent) => {
    event.preventDefault()
    if (!settings) return
    setBusy(true)
    setError(null)
    setNotice(null)
    try {
      const query = new URLSearchParams({
        profile_visibility: settings.profile_visibility,
        content_visibility: settings.content_visibility,
        allow_analytics: String(settings.allow_analytics),
        allow_marketing: String(settings.allow_marketing),
      }).toString()
      const saved: PrivacySettings = await ApiClient.put(`/privacy/settings?${query}`, {})
      setSettings(saved)
      await ApiClient.post(`/privacy/consent-log?consent_type=analytics&granted=${saved.allow_analytics}`, {})
      await ApiClient.post(`/privacy/consent-log?consent_type=marketing&granted=${saved.allow_marketing}`, {})
      await loadConsents()
      setNotice('Privacy preferences saved.')
    } catch (err) {
      setError(errorMessage(err, 'Privacy preferences could not be saved.'))
    } finally {
      setBusy(false)
    }
  }

  const exportData = async () => {
    setError(null)
    try {
      const data = await ApiClient.get('/privacy/export')
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'my-data.json'
      link.click()
      URL.revokeObjectURL(url)
      setNotice('Your data export has been downloaded.')
    } catch (err) {
      setError(errorMessage(err, 'Your data could not be exported.'))
    }
  }

  const requestDeletion = async () => {
    if (!window.confirm('Request deletion of your account and data? This is scheduled, not immediate.')) return
    setError(null)
    try {
      const request: { scheduled_for: string } = await ApiClient.post('/privacy/request-deletion', {})
      setNotice(`Deletion scheduled for ${new Date(request.scheduled_for).toLocaleDateString()}.`)
    } catch (err) {
      setError(errorMessage(err, 'The deletion request could not be recorded.'))
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Privacy</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Privacy Preferences</h2>
        {!settings ? (
          <p className="text-gray-500">Loading preferences…</p>
        ) : (
          <form onSubmit={save} className="space-y-4">
            <label className="block text-sm font-medium">
              Profile Visibility
              <select
                className="mt-1 w-full border rounded px-3 py-2"
                value={settings.profile_visibility}
                onChange={(e) => setSettings({ ...settings, profile_visibility: e.target.value })}
              >
                {VISIBILITY.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </label>
            <label className="block text-sm font-medium">
              Content Visibility
              <select
                className="mt-1 w-full border rounded px-3 py-2"
                value={settings.content_visibility}
                onChange={(e) => setSettings({ ...settings, content_visibility: e.target.value })}
              >
                {VISIBILITY.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={settings.allow_analytics} onChange={(e) => setSettings({ ...settings, allow_analytics: e.target.checked })} />
              Allow analytics tracking
            </label>
            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={settings.allow_marketing} onChange={(e) => setSettings({ ...settings, allow_marketing: e.target.checked })} />
              Allow marketing emails
            </label>
            <button type="submit" disabled={busy} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
              Save Changes
            </button>
          </form>
        )}
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Data Management</h2>
        <div className="flex flex-wrap gap-3">
          <button type="button" onClick={exportData} className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">
            Export Data
          </button>
          <button type="button" onClick={requestDeletion} className="px-4 py-2 border border-red-600 text-red-600 rounded hover:bg-red-50">
            Request Account Deletion
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Consent History</h2>
        {consents === null ? (
          <p className="text-gray-500">Loading consent history…</p>
        ) : consents.length === 0 ? (
          <p className="text-gray-500">No consent decisions recorded yet.</p>
        ) : (
          <ul className="space-y-2 text-sm">
            {consents.map((entry) => (
              <li key={entry.id} className="border rounded p-3">
                <span className="font-medium">{entry.consent_type}</span> · {entry.granted ? 'granted' : 'withdrawn'}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
