'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface AuditLogEntry {
  id: number
  user_id: number
  action: string
  resource_type: string | null
  status: string | null
  ip_address: string | null
  severity: string
  created_at: string
}

interface RateLimit {
  id: number
  endpoint: string
  requests_per_minute: number
  requests_per_hour: number
  requests_per_day: number
  burst_limit: number
}

interface SocialProvider {
  provider: string
  display_name: string
  enabled: boolean
  client_id: string | null
  client_secret_set: boolean
  redirect_uri: string | null
}

interface MfaSetup {
  secret: string
  otpauth_uri: string
}

/** Security settings: audit trail, rate limits, sign-in providers and two-factor authentication. */
export default function SecurityPage() {
  const [logs, setLogs] = useState<AuditLogEntry[]>([])
  const [logsError, setLogsError] = useState<string | null>(null)
  const [limits, setLimits] = useState<RateLimit[] | null>(null)
  const [limitsError, setLimitsError] = useState<string | null>(null)
  const [endpoint, setEndpoint] = useState('')
  const [perMinute, setPerMinute] = useState('60')
  const [providers, setProviders] = useState<SocialProvider[] | null>(null)
  const [providersError, setProvidersError] = useState<string | null>(null)
  const [mfaEnabled, setMfaEnabled] = useState<boolean | null>(null)
  const [mfaSetup, setMfaSetup] = useState<MfaSetup | null>(null)
  const [mfaCode, setMfaCode] = useState('')
  const [mfaError, setMfaError] = useState<string | null>(null)
  const [mfaNotice, setMfaNotice] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const loadLimits = () =>
    ApiClient.get('/rate-limits/configs')
      .then((data: RateLimit[]) => {
        setLimits(Array.isArray(data) ? data : [])
        setLimitsError(null)
      })
      .catch((err) => setLimitsError(errorMessage(err, 'Rate limits could not be loaded.')))

  const loadProviders = () =>
    ApiClient.get('/admin/social-providers')
      .then((data: SocialProvider[]) => {
        setProviders(Array.isArray(data) ? data : [])
        setProvidersError(null)
      })
      .catch((err) => setProvidersError(errorMessage(err, 'Sign-in providers could not be loaded.')))

  useEffect(() => {
    ApiClient.get('/security/audit-logs')
      .then((data: AuditLogEntry[]) => setLogs(Array.isArray(data) ? data : []))
      .catch((err) => setLogsError(errorMessage(err, 'Audit logs could not be loaded.')))
    loadLimits()
    loadProviders()
    ApiClient.get('/auth/mfa')
      .then((data: { enabled: boolean }) => setMfaEnabled(data.enabled))
      .catch((err) => setMfaError(errorMessage(err, 'Two-factor status could not be loaded.')))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const addRateLimit = async (event: FormEvent) => {
    event.preventDefault()
    setLimitsError(null)
    try {
      await ApiClient.post('/rate-limits/config', {
        endpoint: endpoint.trim(),
        requests_per_minute: Number(perMinute),
      })
      setEndpoint('')
      await loadLimits()
    } catch (err) {
      setLimitsError(errorMessage(err, 'The rate limit could not be saved.'))
    }
  }

  const toggleProvider = async (provider: SocialProvider) => {
    setProvidersError(null)
    try {
      await ApiClient.put(`/admin/social-providers/${provider.provider}`, { enabled: !provider.enabled })
      await loadProviders()
    } catch (err) {
      setProvidersError(errorMessage(err, 'The provider could not be changed.'))
    }
  }

  const startSetup = async () => {
    setMfaError(null)
    setMfaNotice(null)
    setBusy(true)
    try {
      setMfaSetup(await ApiClient.post('/auth/mfa/setup', {}))
    } catch (err) {
      setMfaError(errorMessage(err, 'Two-factor setup could not start.'))
    } finally {
      setBusy(false)
    }
  }

  const confirmMfa = async (action: 'enable' | 'disable') => {
    setMfaError(null)
    setMfaNotice(null)
    setBusy(true)
    try {
      const result: { enabled: boolean } = await ApiClient.post(`/auth/mfa/${action}`, { code: mfaCode })
      setMfaEnabled(result.enabled)
      setMfaSetup(null)
      setMfaCode('')
      setMfaNotice(action === 'enable' ? 'Two-factor authentication is on.' : 'Two-factor authentication is off.')
    } catch (err) {
      setMfaError(errorMessage(err, 'The code was not accepted.'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Security Settings</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Audit Log</h2>
          {logsError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{logsError}</p>}
          {!logsError && logs.length === 0 && <p className="text-gray-500">No security events recorded yet.</p>}
          {logs.length > 0 && (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 text-sm">
                <thead className="bg-gray-50 text-left text-gray-600">
                  <tr>
                    <th className="px-3 py-2">When</th>
                    <th className="px-3 py-2">Action</th>
                    <th className="px-3 py-2">User</th>
                    <th className="px-3 py-2">Status</th>
                    <th className="px-3 py-2">Severity</th>
                    <th className="px-3 py-2">IP address</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {logs.map((log) => (
                    <tr key={log.id}>
                      <td className="px-3 py-2">{new Date(log.created_at).toLocaleString()}</td>
                      <td className="px-3 py-2">{log.action}{log.resource_type ? ` (${log.resource_type})` : ''}</td>
                      <td className="px-3 py-2">#{log.user_id}</td>
                      <td className="px-3 py-2">{log.status ?? '—'}</td>
                      <td className="px-3 py-2">{log.severity}</td>
                      <td className="px-3 py-2">{log.ip_address ?? '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Rate Limiting</h2>
          {limitsError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{limitsError}</p>}
          {limits && limits.length === 0 && <p className="text-gray-500">No rate limits are configured.</p>}
          {limits && limits.length > 0 && (
            <ul className="space-y-2 text-sm mb-4">
              {limits.map((limit) => (
                <li key={limit.id} className="border rounded p-3">
                  <span className="font-medium">{limit.endpoint}</span> · {limit.requests_per_minute}/min · {limit.requests_per_hour}/hour · {limit.requests_per_day}/day · burst {limit.burst_limit}
                </li>
              ))}
            </ul>
          )}
          {limits !== null && (
            <form onSubmit={addRateLimit} className="flex flex-wrap gap-2 items-end">
              <label className="text-sm">
                <span className="block text-xs text-gray-600">Endpoint</span>
                <input
                  className="border rounded px-2 py-1"
                  value={endpoint}
                  onChange={(e) => setEndpoint(e.target.value)}
                  placeholder="/api/v1/content"
                  required
                />
              </label>
              <label className="text-sm">
                <span className="block text-xs text-gray-600">Requests per minute</span>
                <input
                  type="number"
                  min={1}
                  className="border rounded px-2 py-1 w-28"
                  value={perMinute}
                  onChange={(e) => setPerMinute(e.target.value)}
                  required
                />
              </label>
              <button type="submit" disabled={!endpoint.trim()} className="px-3 py-1 border border-blue-600 text-blue-600 rounded disabled:opacity-50">
                Save limit
              </button>
            </form>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">OAuth Providers</h2>
          {providersError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{providersError}</p>}
          {providers && providers.length === 0 && <p className="text-gray-500">No sign-in providers are available.</p>}
          {providers && providers.length > 0 && (
            <div className="space-y-3">
              {providers.map((provider) => (
                <div key={provider.provider} className="flex justify-between items-center">
                  <div>
                    <span className="font-medium">{provider.display_name}</span>
                    {!provider.client_secret_set && <p className="text-xs text-gray-500">Needs a client ID, secret and redirect URI before it can be enabled</p>}
                  </div>
                  <button
                    type="button"
                    onClick={() => toggleProvider(provider)}
                    className={`px-3 py-1 rounded text-sm ${provider.enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}
                  >
                    {provider.enabled ? 'Enabled — disable' : 'Disabled — enable'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Two-Factor Authentication</h2>
          {mfaError && <p role="alert" className="mb-3 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{mfaError}</p>}
          {mfaNotice && <p role="status" className="mb-3 text-green-700">{mfaNotice}</p>}
          {mfaEnabled === null ? (
            <p className="text-gray-500">Loading…</p>
          ) : mfaEnabled ? (
            <div className="space-y-3">
              <p className="text-sm">Status: <strong>Enabled</strong>. Sign-in asks for a code from your authenticator app.</p>
              <div className="flex gap-2 items-end">
                <input className="border rounded px-2 py-1 w-32 tracking-widest" inputMode="numeric" maxLength={6} aria-label="Authentication code" value={mfaCode} onChange={(e) => setMfaCode(e.target.value.replace(/\D/g, ''))} />
                <button type="button" disabled={busy || mfaCode.length !== 6} onClick={() => confirmMfa('disable')} className="px-4 py-2 bg-red-600 text-white rounded disabled:opacity-50">
                  Disable 2FA
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-sm">Status: <strong>Disabled</strong>.</p>
              {!mfaSetup ? (
                <button type="button" disabled={busy} onClick={startSetup} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
                  Set up 2FA
                </button>
              ) : (
                <div className="space-y-3">
                  <p className="text-sm">Add this key to your authenticator app, then enter the 6-digit code it shows.</p>
                  <p className="font-mono text-sm break-all bg-gray-50 rounded p-2" data-testid="mfa-secret">{mfaSetup.secret}</p>
                  <a className="text-sm text-blue-600 hover:underline break-all" href={mfaSetup.otpauth_uri}>Open in authenticator app</a>
                  <div className="flex gap-2 items-end">
                    <input className="border rounded px-2 py-1 w-32 tracking-widest" inputMode="numeric" maxLength={6} aria-label="Authentication code" value={mfaCode} onChange={(e) => setMfaCode(e.target.value.replace(/\D/g, ''))} />
                    <button type="button" disabled={busy || mfaCode.length !== 6} onClick={() => confirmMfa('enable')} className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50">
                      Turn on 2FA
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
