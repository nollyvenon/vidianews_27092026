'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { ApiError, errorMessage } from '@/lib/api-error'

export interface WebhookEndpoint {
  id: number
  url: string
  description: string | null
  events: string[]
  is_active: boolean
  created_at: string | null
  updated_at: string | null
}

export interface WebhookEventType {
  event: string
  description: string
}

export interface WebhookDelivery {
  id: number
  webhook_id: number
  event: string
  status: 'delivered' | 'failed'
  response_status: number | null
  error: string | null
  created_at: string | null
}

type Notice = { kind: 'success' | 'error'; text: string }

const URL_PATTERN = /^https:\/\/[^\s/]+\S*$/

function formatTime(value: string | null): string {
  return value ? new Date(value).toLocaleString() : '—'
}

/** Registration, signing secrets, test delivery and delivery history for outbound webhooks. */
export default function WebhooksPage() {
  const [endpoints, setEndpoints] = useState<WebhookEndpoint[]>([])
  const [eventTypes, setEventTypes] = useState<WebhookEventType[]>([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const [notice, setNotice] = useState<Notice | null>(null)

  const [url, setUrl] = useState('')
  const [description, setDescription] = useState('')
  const [selectedEvents, setSelectedEvents] = useState<string[]>([])
  const [creating, setCreating] = useState(false)
  const [formError, setFormError] = useState('')
  const [revealedSecret, setRevealedSecret] = useState<{ id: number; secret: string } | null>(null)

  const load = async () => {
    try {
      const [list, events] = await Promise.all([
        ApiClient.get('/outbound-webhooks') as Promise<WebhookEndpoint[]>,
        ApiClient.get('/outbound-webhooks/events') as Promise<WebhookEventType[]>,
      ])
      setEndpoints(list)
      setEventTypes(events)
      setLoadError('')
    } catch (err) {
      setLoadError(errorMessage(err, 'Webhooks could not be loaded.'))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const toggleEvent = (event: string) => {
    setSelectedEvents((current) =>
      current.includes(event) ? current.filter((item) => item !== event) : [...current, event],
    )
  }

  const create = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError('')
    setNotice(null)
    if (!URL_PATTERN.test(url.trim())) {
      setFormError('The endpoint must be an https:// address on a public host.')
      return
    }
    if (selectedEvents.length === 0) {
      setFormError('Select at least one event.')
      return
    }
    setCreating(true)
    try {
      const { secret, ...endpoint }: WebhookEndpoint & { secret: string } = await ApiClient.post('/outbound-webhooks', {
        url: url.trim(),
        description: description.trim() || null,
        events: selectedEvents,
      })
      setEndpoints((current) => [...current, endpoint])
      setRevealedSecret({ id: endpoint.id, secret })
      setUrl('')
      setDescription('')
      setSelectedEvents([])
    } catch (err) {
      setFormError(errorMessage(err, 'The endpoint could not be created.'))
    } finally {
      setCreating(false)
    }
  }

  const replaceEndpoint = (updated: WebhookEndpoint) => {
    setEndpoints((current) => current.map((item) => (item.id === updated.id ? updated : item)))
  }

  const runAction = async (action: () => Promise<void>, success: string) => {
    setNotice(null)
    try {
      await action()
      setNotice({ kind: 'success', text: success })
    } catch (err) {
      setNotice({ kind: 'error', text: errorMessage(err, 'That action could not be completed.') })
    }
  }

  const togglePaused = (endpoint: WebhookEndpoint) =>
    runAction(async () => {
      const updated: WebhookEndpoint = await ApiClient.patch(`/outbound-webhooks/${endpoint.id}`, {
        is_active: !endpoint.is_active,
      })
      replaceEndpoint(updated)
    }, endpoint.is_active ? 'Endpoint paused.' : 'Endpoint resumed.')

  const sendTest = (endpoint: WebhookEndpoint) =>
    runAction(async () => {
      const delivery: WebhookDelivery = await ApiClient.post(`/outbound-webhooks/${endpoint.id}/test`, {})
      if (delivery.status !== 'delivered') {
        throw new ApiError(delivery.error ?? 'The test event was not accepted.')
      }
    }, 'Test event delivered.')

  const rotateSecret = (endpoint: WebhookEndpoint) => {
    if (!window.confirm('Rotate the signing secret? Receivers still using the old secret will reject events.')) return
    runAction(async () => {
      const result: { secret: string } = await ApiClient.post(`/outbound-webhooks/${endpoint.id}/rotate-secret`, {})
      setRevealedSecret({ id: endpoint.id, secret: result.secret })
    }, 'New signing secret generated.')
  }

  const remove = (endpoint: WebhookEndpoint) => {
    if (!window.confirm(`Delete the endpoint ${endpoint.url}? Its delivery history is deleted too.`)) return
    runAction(async () => {
      await ApiClient.delete(`/outbound-webhooks/${endpoint.id}`)
      setEndpoints((current) => current.filter((item) => item.id !== endpoint.id))
    }, 'Endpoint deleted.')
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Webhooks</h1>
        <p className="mt-1 text-sm text-gray-600">
          Receive signed HTTPS notifications when events happen. Each request carries an
          <code className="mx-1">X-Webhook-Signature</code> header computed with the endpoint&apos;s secret.
        </p>
      </div>

      {notice && (
        <p role={notice.kind === 'error' ? 'alert' : 'status'}
          className={notice.kind === 'error' ? 'text-sm text-red-700' : 'text-sm text-green-700'}>
          {notice.text}
        </p>
      )}

      {revealedSecret && (
        <div role="region" aria-label="Signing secret" className="rounded-lg border border-amber-300 bg-amber-50 p-4">
          <p className="font-semibold text-amber-900">Copy this signing secret now. It will not be shown again.</p>
          <code className="mt-2 block break-all rounded bg-white p-2 text-sm">{revealedSecret.secret}</code>
          <button className="mt-3 text-sm text-amber-900 underline" onClick={() => setRevealedSecret(null)}>
            I have saved it
          </button>
        </div>
      )}

      <section className="rounded-lg bg-white p-6 shadow">
        <h2 className="mb-4 text-xl font-semibold">Add an endpoint</h2>
        <form onSubmit={create} className="space-y-4">
          <div>
            <label htmlFor="webhook-url" className="block text-sm font-medium text-gray-700">Endpoint URL</label>
            <input
              id="webhook-url"
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/webhooks"
              maxLength={500}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
              required
            />
          </div>
          <div>
            <label htmlFor="webhook-description" className="block text-sm font-medium text-gray-700">Description</label>
            <input
              id="webhook-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              maxLength={255}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2"
            />
          </div>
          <fieldset>
            <legend className="text-sm font-medium text-gray-700">Events</legend>
            <div className="mt-2 grid gap-2 md:grid-cols-2">
              {eventTypes.map((item) => (
                <label key={item.event} className="flex items-start gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={selectedEvents.includes(item.event)}
                    onChange={() => toggleEvent(item.event)}
                    className="mt-1"
                  />
                  <span>
                    <span className="font-mono">{item.event}</span>
                    <span className="block text-gray-600">{item.description}</span>
                  </span>
                </label>
              ))}
            </div>
          </fieldset>
          {formError && <p role="alert" className="text-sm text-red-700">{formError}</p>}
          <button
            type="submit"
            disabled={creating}
            className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {creating ? 'Adding...' : 'Add endpoint'}
          </button>
        </form>
      </section>

      <section className="rounded-lg bg-white p-6 shadow">
        <h2 className="mb-4 text-xl font-semibold">Endpoints</h2>
        {loading ? (
          <p role="status" className="text-sm text-gray-600">Loading endpoints...</p>
        ) : loadError ? (
          <p role="alert" className="text-sm text-red-700">{loadError}</p>
        ) : endpoints.length === 0 ? (
          <p className="text-sm text-gray-600">No endpoints yet. Add one above to start receiving events.</p>
        ) : (
          <ul className="space-y-4">
            {endpoints.map((endpoint) => (
              <EndpointCard
                key={endpoint.id}
                endpoint={endpoint}
                onTogglePaused={() => togglePaused(endpoint)}
                onTest={() => sendTest(endpoint)}
                onRotate={() => rotateSecret(endpoint)}
                onDelete={() => remove(endpoint)}
              />
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}

interface EndpointCardProps {
  endpoint: WebhookEndpoint
  onTogglePaused: () => void
  onTest: () => void
  onRotate: () => void
  onDelete: () => void
}

function EndpointCard({ endpoint, onTogglePaused, onTest, onRotate, onDelete }: EndpointCardProps) {
  const [showDeliveries, setShowDeliveries] = useState(false)
  const [deliveries, setDeliveries] = useState<WebhookDelivery[] | null>(null)
  const [deliveryError, setDeliveryError] = useState('')

  const toggleDeliveries = async () => {
    const next = !showDeliveries
    setShowDeliveries(next)
    if (next && deliveries === null) {
      try {
        setDeliveries(await ApiClient.get(`/outbound-webhooks/${endpoint.id}/deliveries?limit=20`))
      } catch (err) {
        setDeliveryError(errorMessage(err, 'Deliveries could not be loaded.'))
      }
    }
  }

  return (
    <li className="rounded-lg border p-4">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="break-all font-semibold">{endpoint.url}</p>
          {endpoint.description && <p className="text-sm text-gray-600">{endpoint.description}</p>}
          <p className="mt-1 text-xs text-gray-600">{endpoint.events.join(', ')}</p>
        </div>
        <span className={`rounded px-3 py-1 text-xs font-medium ${
          endpoint.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-200 text-gray-800'
        }`}>
          {endpoint.is_active ? 'Active' : 'Paused'}
        </span>
      </div>

      <div className="mt-3 flex flex-wrap gap-2 text-sm">
        <button onClick={onTest} className="rounded border px-3 py-1 hover:bg-gray-50">Send test</button>
        <button onClick={onTogglePaused} className="rounded border px-3 py-1 hover:bg-gray-50">
          {endpoint.is_active ? 'Pause' : 'Resume'}
        </button>
        <button onClick={onRotate} className="rounded border px-3 py-1 hover:bg-gray-50">Rotate secret</button>
        <button onClick={toggleDeliveries} className="rounded border px-3 py-1 hover:bg-gray-50">
          {showDeliveries ? 'Hide deliveries' : 'Deliveries'}
        </button>
        <button onClick={onDelete} className="rounded border border-red-300 px-3 py-1 text-red-700 hover:bg-red-50">
          Delete
        </button>
      </div>

      {showDeliveries && (
        <div className="mt-4">
          {deliveryError ? (
            <p role="alert" className="text-sm text-red-700">{deliveryError}</p>
          ) : deliveries === null ? (
            <p role="status" className="text-sm text-gray-600">Loading deliveries...</p>
          ) : deliveries.length === 0 ? (
            <p className="text-sm text-gray-600">No deliveries yet.</p>
          ) : (
            <table className="min-w-full text-left text-sm">
              <thead className="text-gray-600">
                <tr>
                  <th className="py-1 pr-3">When</th>
                  <th className="py-1 pr-3">Event</th>
                  <th className="py-1 pr-3">Result</th>
                  <th className="py-1">Detail</th>
                </tr>
              </thead>
              <tbody>
                {deliveries.map((item) => (
                  <tr key={item.id} className="border-t">
                    <td className="py-1 pr-3">{formatTime(item.created_at)}</td>
                    <td className="py-1 pr-3 font-mono">{item.event}</td>
                    <td className="py-1 pr-3">{item.status === 'delivered' ? 'Delivered' : 'Failed'}</td>
                    <td className="py-1">{item.error ?? (item.response_status ? `HTTP ${item.response_status}` : '—')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </li>
  )
}
