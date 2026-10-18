'use client'

import { FormEvent, useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

type SettingsTab = 'notifications' | 'privacy' | 'display' | 'profile'
type SectionName = 'notifications' | 'privacy' | 'display'

interface NotificationSettings {
  email_on_activity: boolean
  email_on_mention: boolean
  email_on_message: boolean
  email_digest: string
  push_enabled: boolean
  push_on_activity: boolean
  push_on_message: boolean
  inapp_enabled: boolean
  inapp_sound: boolean
  dnd_enabled: boolean
  dnd_start_time: string | null
  dnd_end_time: string | null
}

interface PrivacySettings {
  profile_visibility: string
  show_email: boolean
  show_phone: boolean
  show_activity: boolean
  show_last_seen: boolean
  allow_messages: string
  allow_search: boolean
  allow_analytics: boolean
  allow_marketing_emails: boolean
  allow_third_party_sharing: boolean
}

interface DisplaySettings {
  theme: string
  language: string
  timezone: string
  date_format: string
  time_format: string
  sidebar_collapsed: boolean
  compact_mode: boolean
  animations_enabled: boolean
  font_size: string
}

interface Settings {
  notifications: NotificationSettings
  privacy: PrivacySettings
  display: DisplaySettings
}

interface Profile {
  bio: string | null
  title: string | null
  location: string | null
  timezone: string
  is_public: boolean
}

const TABS: SettingsTab[] = ['notifications', 'privacy', 'display', 'profile']

const NOTIFICATION_TOGGLES: Array<[keyof NotificationSettings, string]> = [
  ['email_on_activity', 'Activity email notifications'],
  ['email_on_mention', 'Mention email notifications'],
  ['email_on_message', 'Message email notifications'],
  ['push_enabled', 'Push notifications'],
  ['push_on_activity', 'Push for activity'],
  ['push_on_message', 'Push for messages'],
  ['inapp_enabled', 'In-app notifications'],
  ['inapp_sound', 'In-app sound'],
  ['dnd_enabled', 'Do not disturb'],
]

const PRIVACY_TOGGLES: Array<[keyof PrivacySettings, string]> = [
  ['show_email', 'Show email on profile'],
  ['show_phone', 'Show phone on profile'],
  ['show_activity', 'Show activity on profile'],
  ['show_last_seen', 'Show last seen'],
  ['allow_search', 'Appear in search'],
  ['allow_analytics', 'Allow usage analytics'],
  ['allow_marketing_emails', 'Marketing emails'],
  ['allow_third_party_sharing', 'Share data with third parties'],
]

const DISPLAY_TOGGLES: Array<[keyof DisplaySettings, string]> = [
  ['sidebar_collapsed', 'Collapsed sidebar'],
  ['compact_mode', 'Compact layout'],
  ['animations_enabled', 'Animations'],
]

const SECTION_KEYS: Record<SectionName, string[]> = {
  notifications: [
    'email_on_activity', 'email_on_mention', 'email_on_message', 'email_digest',
    'push_enabled', 'push_on_activity', 'push_on_message',
    'inapp_enabled', 'inapp_sound', 'dnd_enabled', 'dnd_start_time', 'dnd_end_time',
  ],
  privacy: [
    'profile_visibility', 'show_email', 'show_phone', 'show_activity', 'show_last_seen',
    'allow_messages', 'allow_search', 'allow_analytics', 'allow_marketing_emails', 'allow_third_party_sharing',
  ],
  display: [
    'theme', 'language', 'timezone', 'date_format', 'time_format',
    'sidebar_collapsed', 'compact_mode', 'animations_enabled', 'font_size',
  ],
}

const EMAIL_DIGESTS: Array<[string, string]> = [['never', 'Never'], ['daily', 'Daily'], ['weekly', 'Weekly'], ['realtime', 'Real time']]
const PROFILE_VISIBILITY: Array<[string, string]> = [['public', 'Public'], ['friends_only', 'Friends only'], ['private', 'Private']]
const ALLOW_MESSAGES: Array<[string, string]> = [['everyone', 'Everyone'], ['friends_only', 'Friends only'], ['nobody', 'No one']]
const THEMES: Array<[string, string]> = [['light', 'Light'], ['dark', 'Dark'], ['auto', 'Auto']]
const LANGUAGES: Array<[string, string]> = [['en', 'English'], ['es', 'Español'], ['fr', 'Français']]
const DATE_FORMATS: Array<[string, string]> = [['YYYY-MM-DD', 'YYYY-MM-DD'], ['DD/MM/YYYY', 'DD/MM/YYYY'], ['MM/DD/YYYY', 'MM/DD/YYYY']]
const TIME_FORMATS: Array<[string, string]> = [['24h', '24-hour'], ['12h', '12-hour']]
const FONT_SIZES: Array<[string, string]> = [['small', 'Small'], ['medium', 'Medium'], ['large', 'Large']]

/** Values for PUT /settings/me/{section}: every editable field, with empty optional times sent as null. */
function payloadFor(section: SectionName, values: object): Record<string, unknown> {
  const source = values as Record<string, unknown>
  const payload: Record<string, unknown> = {}
  for (const key of SECTION_KEYS[section]) {
    const value = source[key]
    payload[key] = value === '' ? null : value
  }
  return payload
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: Array<[string, string]>; onChange: (value: string) => void }) {
  return (
    <label className="flex justify-between items-center gap-4">
      <span className="font-medium">{label}</span>
      <select value={value} onChange={(e) => onChange(e.target.value)} className="border rounded px-2 py-1">
        {options.map(([optionValue, optionLabel]) => (
          <option key={optionValue} value={optionValue}>{optionLabel}</option>
        ))}
      </select>
    </label>
  )
}

function ToggleField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex justify-between items-center">
      <span className="font-medium">{label}</span>
      <input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} className="w-4 h-4" />
    </label>
  )
}

export default function SettingsPage() {
  const { user } = useAuth()
  const [activeTab, setActiveTab] = useState<SettingsTab>('notifications')
  const [settings, setSettings] = useState<Settings | null>(null)
  const [settingsError, setSettingsError] = useState<string | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [profileError, setProfileError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)

  const loadSettings = () =>
    ApiClient.get('/settings/me')
      .then((loaded: Settings) => {
        setSettings(loaded)
        setSettingsError(null)
      })
      .catch((err) => setSettingsError(errorMessage(err, 'Settings could not be loaded.')))

  useEffect(() => {
    const loadProfile = () =>
      ApiClient.get('/profiles/me')
        .then((loaded: Profile) => setProfile(loaded))
        .catch((err) => setProfileError(errorMessage(err, 'Your profile could not be loaded.')))

    Promise.all([loadSettings(), loadProfile()]).finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const updateSection = <K extends SectionName>(section: K, changes: Partial<Settings[K]>) => {
    setSettings((current) => (current ? { ...current, [section]: { ...current[section], ...changes } } : current))
  }

  const saveSection = async (event: FormEvent, section: SectionName) => {
    event.preventDefault()
    if (!settings) return
    setSaving(true)
    setError(null)
    setMessage(null)
    try {
      await ApiClient.put(`/settings/me/${section}`, payloadFor(section, settings[section]))
      await loadSettings()
      setMessage('Settings saved')
    } catch (err) {
      setError(errorMessage(err, 'Settings could not be saved.'))
    } finally {
      setSaving(false)
    }
  }

  const saveProfile = async (event: FormEvent) => {
    event.preventDefault()
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
      setError(errorMessage(err, 'Your profile could not be saved.'))
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="p-8">Loading...</div>
  if (!settings) return <div role="alert" className="p-8 text-red-700">{settingsError ?? 'Settings not found'}</div>

  const notifications = settings.notifications
  const privacy = settings.privacy
  const display = settings.display

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Settings</h1>

      {error && <div role="alert" className="bg-red-50 text-red-700 rounded-lg p-4 mb-6">{error}</div>}
      {message && <div role="status" className="bg-green-50 text-green-700 rounded-lg p-4 mb-6">{message}</div>}
      {settingsError && <div role="alert" className="bg-red-50 text-red-700 rounded-lg p-4 mb-6">{settingsError}</div>}

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
              <form className="space-y-4" onSubmit={(e) => saveSection(e, 'notifications')}>
                {NOTIFICATION_TOGGLES.map(([key, label]) => (
                  <ToggleField
                    key={key}
                    label={label}
                    checked={notifications[key] as boolean}
                    onChange={(checked) => updateSection('notifications', { [key]: checked })}
                  />
                ))}
                <SelectField
                  label="Email digest"
                  value={notifications.email_digest}
                  options={EMAIL_DIGESTS}
                  onChange={(value) => updateSection('notifications', { email_digest: value })}
                />
                <label className="flex justify-between items-center">
                  <span className="font-medium">Do not disturb from</span>
                  <input
                    type="time"
                    value={notifications.dnd_start_time ?? ''}
                    onChange={(e) => updateSection('notifications', { dnd_start_time: e.target.value })}
                    className="border rounded px-2 py-1"
                  />
                </label>
                <label className="flex justify-between items-center">
                  <span className="font-medium">Do not disturb until</span>
                  <input
                    type="time"
                    value={notifications.dnd_end_time ?? ''}
                    onChange={(e) => updateSection('notifications', { dnd_end_time: e.target.value })}
                    className="border rounded px-2 py-1"
                  />
                </label>
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  Save notifications
                </button>
              </form>
            )}

            {activeTab === 'privacy' && (
              <form className="space-y-4" onSubmit={(e) => saveSection(e, 'privacy')}>
                <SelectField
                  label="Profile visibility"
                  value={privacy.profile_visibility}
                  options={PROFILE_VISIBILITY}
                  onChange={(value) => updateSection('privacy', { profile_visibility: value })}
                />
                <SelectField
                  label="Who can message you"
                  value={privacy.allow_messages}
                  options={ALLOW_MESSAGES}
                  onChange={(value) => updateSection('privacy', { allow_messages: value })}
                />
                {PRIVACY_TOGGLES.map(([key, label]) => (
                  <ToggleField
                    key={key}
                    label={label}
                    checked={privacy[key] as boolean}
                    onChange={(checked) => updateSection('privacy', { [key]: checked })}
                  />
                ))}
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  Save privacy
                </button>
              </form>
            )}

            {activeTab === 'display' && (
              <form className="space-y-4" onSubmit={(e) => saveSection(e, 'display')}>
                <SelectField label="Theme" value={display.theme} options={THEMES} onChange={(value) => updateSection('display', { theme: value })} />
                <SelectField label="Language" value={display.language} options={LANGUAGES} onChange={(value) => updateSection('display', { language: value })} />
                <label className="flex justify-between items-center">
                  <span className="font-medium">Timezone</span>
                  <input
                    type="text"
                    value={display.timezone}
                    onChange={(e) => updateSection('display', { timezone: e.target.value })}
                    className="border rounded px-2 py-1"
                  />
                </label>
                <SelectField label="Date format" value={display.date_format} options={DATE_FORMATS} onChange={(value) => updateSection('display', { date_format: value })} />
                <SelectField label="Time format" value={display.time_format} options={TIME_FORMATS} onChange={(value) => updateSection('display', { time_format: value })} />
                <SelectField label="Font size" value={display.font_size} options={FONT_SIZES} onChange={(value) => updateSection('display', { font_size: value })} />
                {DISPLAY_TOGGLES.map(([key, label]) => (
                  <ToggleField
                    key={key}
                    label={label}
                    checked={display[key] as boolean}
                    onChange={(checked) => updateSection('display', { [key]: checked })}
                  />
                ))}
                <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
                  Save display
                </button>
              </form>
            )}

            {activeTab === 'profile' && (
              profile ? (
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
              ) : (
                <p role="alert" className="text-red-700">{profileError ?? 'Your profile could not be loaded.'}</p>
              )
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
