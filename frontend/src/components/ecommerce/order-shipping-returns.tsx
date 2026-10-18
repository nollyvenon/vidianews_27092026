'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface Shipment {
  id: number
  order_id: number
  carrier: string
  tracking_number: string | null
  status: string | null
  shipped_at: string | null
  delivered_at: string | null
}

export interface TrackingEvent {
  id: number
  shipment_id: number
  status: string
  description: string | null
  location: string | null
  timestamp: string
}

export interface ReturnRequest {
  id: number
  rma_number: string | null
  reason: string
  status: string
  quantity_requested: number
  quantity_received: number | null
  refund_amount: number | null
  refund_method: string | null
}

export const RETURN_REASONS: { value: string; label: string }[] = [
  { value: 'damaged', label: 'Arrived damaged' },
  { value: 'defective', label: 'Defective' },
  { value: 'not_as_described', label: 'Not as described' },
  { value: 'wrong_item', label: 'Wrong item' },
  { value: 'no_longer_needed', label: 'No longer needed' },
  { value: 'size_issue', label: 'Size does not fit' },
  { value: 'color_issue', label: 'Colour is different' },
  { value: 'other', label: 'Other' },
]

interface Props {
  orderId: string
}

export function OrderShippingReturns({ orderId }: Props) {
  const [shipments, setShipments] = useState<Shipment[]>([])
  const [events, setEvents] = useState<Record<number, TrackingEvent[]>>({})
  const [returns, setReturns] = useState<ReturnRequest[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)

  const [reason, setReason] = useState(RETURN_REASONS[0].value)
  const [quantity, setQuantity] = useState('1')
  const [details, setDetails] = useState('')
  const [formError, setFormError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  useEffect(() => {
    load()
    // The page is keyed by order, so loading once per order id is enough.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [orderId])

  async function load() {
    try {
      const [shipmentRows, returnRows] = await Promise.all([
        ApiClient.get(`/orders/${orderId}/shipments`) as Promise<Shipment[]>,
        ApiClient.get(`/orders/${orderId}/returns`) as Promise<ReturnRequest[]>,
      ])
      const tracking = await Promise.all(
        shipmentRows.map(async (shipment) => [
          shipment.id,
          (await ApiClient.get(`/shipments/${shipment.id}/tracking`)) as TrackingEvent[],
        ] as const),
      )
      setShipments(shipmentRows)
      setEvents(Object.fromEntries(tracking))
      setReturns(returnRows)
      setLoadError(null)
    } catch (err) {
      setLoadError(errorMessage(err, 'Shipping and return details could not be loaded.'))
    }
  }

  async function requestReturn(event: FormEvent) {
    event.preventDefault()
    const count = Number(quantity)
    if (!Number.isInteger(count) || count < 1) {
      setFormError('Enter how many items you are returning.')
      return
    }
    setFormError(null)
    try {
      await ApiClient.post(`/orders/${orderId}/return`, {
        reason,
        quantity_requested: count,
        reason_details: details.trim() || null,
      })
      setDetails('')
      setQuantity('1')
      setNotice('Your return request has been submitted.')
      await load()
    } catch (err) {
      setFormError(errorMessage(err, 'The return could not be requested.'))
    }
  }

  return (
    <div className="space-y-6">
      {loadError && <p role="alert" className="text-red-700">{loadError}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      <section aria-label="Shipments" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Shipping</h2>
        {shipments.length === 0 ? (
          <p className="text-gray-600">This order has not shipped yet.</p>
        ) : (
          <ul className="space-y-4">
            {shipments.map((shipment) => (
              <li key={shipment.id} className="rounded border border-gray-200 p-4">
                <p className="font-medium text-gray-900">
                  {shipment.carrier.toUpperCase()} {shipment.tracking_number ?? ''}
                </p>
                <p className="text-sm text-gray-600">Status: {shipment.status ?? 'unknown'}</p>
                {(events[shipment.id] ?? []).length === 0 ? (
                  <p className="mt-2 text-sm text-gray-600">No tracking updates yet.</p>
                ) : (
                  <ol className="mt-3 space-y-2 border-l border-gray-300 pl-4">
                    {(events[shipment.id] ?? []).map((event) => (
                      <li key={event.id} className="text-sm text-gray-700">
                        <span className="font-medium">{event.status}</span>
                        {event.location ? ` · ${event.location}` : ''}
                        {event.description ? ` — ${event.description}` : ''}
                        <span className="block text-xs text-gray-500">{new Date(event.timestamp).toLocaleString()}</span>
                      </li>
                    ))}
                  </ol>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-label="Returns" className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Returns</h2>
        {returns.length === 0 ? (
          <p className="text-gray-600">No return requests for this order.</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {returns.map((item) => (
              <li key={item.id} className="py-3 text-sm text-gray-700">
                <span className="font-medium text-gray-900">{item.rma_number ?? `Return #${item.id}`}</span>
                {' · '}
                {item.status}
                {' · '}
                {item.quantity_requested} item(s)
                {item.refund_amount !== null && item.refund_amount !== undefined
                  ? ` · refund ${item.refund_amount}${item.refund_method ? ` (${item.refund_method})` : ''}`
                  : ''}
              </li>
            ))}
          </ul>
        )}

        <form onSubmit={requestReturn} className="grid gap-4 md:grid-cols-2 border-t border-gray-200 pt-4">
          <label className="flex flex-col text-sm text-gray-700">
            Reason
            <select className="mt-1 rounded border border-gray-300 px-3 py-2" value={reason} onChange={(e) => setReason(e.target.value)}>
              {RETURN_REASONS.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Items to return
            <input
              className="mt-1 rounded border border-gray-300 px-3 py-2"
              inputMode="numeric"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
          </label>
          <label className="flex flex-col text-sm text-gray-700 md:col-span-2">
            Details
            <textarea
              className="mt-1 rounded border border-gray-300 px-3 py-2"
              rows={3}
              value={details}
              onChange={(e) => setDetails(e.target.value)}
            />
          </label>
          <div>
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
              Request a return
            </button>
          </div>
          {formError && <p role="alert" className="md:col-span-2 text-sm text-red-700">{formError}</p>}
        </form>
      </section>
    </div>
  )
}
