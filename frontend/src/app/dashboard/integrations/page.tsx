'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Integration {
  id: number
  integration_type: string
  name: string
  is_active: boolean
  config: Record<string, unknown>
  created_at: string | null
}

const INTEGRATION_TYPES = [
  { value: 'slack', label: 'Slack' },
  { value: 'webhook', label: 'Webhook' },
  { value: 'zapier', label: 'Zapier' },
  { value: 'stripe', label: 'Stripe' },
  { value: 'sendgrid', label: 'SendGrid' },
  { value: 'twilio', label: 'Twilio' },
]

const ICONS: Record<string, string> = {
  slack: '💬',
  webhook: '🔗',
  zapier: '⚡',
  stripe: '💳',
  sendgrid: '📧',
  twilio: '📱',
}

/** Connects the organization to external services. Credentials are stored on the server and shown masked. */
export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<Integration[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [integrationType, setIntegrationType] = useState(INTEGRATION_TYPES[0].value)
  const [name, setName] = useState('')
  const [configText, setConfigText] = useState('{}')
  const [saved, setSaved] = useState<string | null>(null)

  const load = () =>
    ApiClient.get('/system/integrations')
      .then((data: Integration[]) => {
        setIntegrations(Array.isArray(data) ? data : [])
        setError(null)
      })
      .catch((err) => setError(errorMessage(err, 'Integrations could not be loaded.')))

  useEffect(() => {
    load()
  }, [])

  const connect = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    setSaved(null)
    let config: unknown
    try {
      config = JSON.parse(configText || '{}')
    } catch {
      setError('The configuration must be valid JSON.')
      return
    }
    if (typeof config !== 'object' || config === null || Array.isArray(config)) {
      setError('The configuration must be a JSON object.')
      return
    }
    try {
      await ApiClient.post('/system/integrations', {
        integration_type: integrationType,
        name: name.trim(),
        config,
      })
      setSaved(`${name.trim()} is connected.`)
      setName('')
      setConfigText('{}')
      await load()
    } catch (err) {
      setError(errorMessage(err, 'The integration could not be connected.'))
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Integrations</h1>
      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      {saved && <p role="status" className="mb-4 text-green-700">{saved}</p>}

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Connected Integrations</h2>
        {integrations === null ? (
          <div className="text-gray-600">Loading integrations…</div>
        ) : integrations.length === 0 ? (
          <div className="text-gray-600">No integrations connected yet.</div>
        ) : (
          <div className="space-y-2">
            {integrations.map((integration) => (
              <div key={integration.id} className="p-3 bg-green-50 rounded border border-green-200">
                <span className="font-medium">✓ {integration.name}</span>
                <span className="text-sm text-gray-600"> · {INTEGRATION_TYPES.find((t) => t.value === integration.integration_type)?.label ?? integration.integration_type}</span>
                {Object.keys(integration.config).length > 0 && (
                  <pre className="mt-2 text-xs text-gray-700 whitespace-pre-wrap">{JSON.stringify(integration.config, null, 2)}</pre>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">Connect an integration</h2>
        <form onSubmit={connect} className="bg-white rounded-lg shadow p-6 space-y-4 max-w-2xl">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
            {INTEGRATION_TYPES.map((type) => (
              <button
                key={type.value}
                type="button"
                onClick={() => setIntegrationType(type.value)}
                aria-pressed={integrationType === type.value}
                className={`p-4 rounded-lg border text-left ${integrationType === type.value ? 'border-blue-600 bg-blue-50' : 'border-gray-200'}`}
              >
                <div className="text-3xl mb-1">{ICONS[type.value]}</div>
                <div className="font-medium">{type.label}</div>
              </button>
            ))}
          </div>
          <label className="block text-sm">
            <span className="block mb-1">Name</span>
            <input className="w-full border rounded px-3 py-2" value={name} onChange={(e) => setName(e.target.value)} required />
          </label>
          <label className="block text-sm">
            <span className="block mb-1">Configuration (JSON object, e.g. {'{"webhook_url": "https://…"}'})</span>
            <textarea className="w-full border rounded px-3 py-2 font-mono text-sm" rows={4} value={configText} onChange={(e) => setConfigText(e.target.value)} />
          </label>
          <button type="submit" disabled={!name.trim()} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
            Connect
          </button>
        </form>
      </div>
    </div>
  )
}
