'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface PendingReturn {
  id: number
  order_id: number
  rma_number: string | null
  reason: string
  status: string
  quantity_requested: number
  quantity_received: number | null
  refund_amount: number | null
}

export interface StockRow {
  id: number
  product_id: number
  quantity_on_hand: number
  quantity_available: number
  reorder_level: number
  status: string
}

const CARRIERS = ['ups', 'fedex', 'usps', 'dhl', 'local']

type Notice = { kind: 'success' | 'error'; text: string } | null

export default function FulfilmentPage() {
  const [pending, setPending] = useState<PendingReturn[]>([])
  const [lowStock, setLowStock] = useState<StockRow[]>([])
  const [outOfStock, setOutOfStock] = useState<StockRow[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)
  const [notice, setNotice] = useState<Notice>(null)

  const [shipOrderId, setShipOrderId] = useState('')
  const [carrier, setCarrier] = useState(CARRIERS[0])
  const [trackingNumber, setTrackingNumber] = useState('')
  const [baseRate, setBaseRate] = useState('')
  const [totalCost, setTotalCost] = useState('')
  const [shipError, setShipError] = useState<string | null>(null)

  const [eventShipmentId, setEventShipmentId] = useState('')
  const [eventStatus, setEventStatus] = useState('')
  const [eventLocation, setEventLocation] = useState('')
  const [eventDescription, setEventDescription] = useState('')
  const [eventError, setEventError] = useState<string | null>(null)

  const [refundAmounts, setRefundAmounts] = useState<Record<number, string>>({})
  const [receivedCounts, setReceivedCounts] = useState<Record<number, string>>({})

  useEffect(() => {
    load()
  }, [])

  async function load() {
    try {
      const [returns, low, out] = await Promise.all([
        ApiClient.get('/returns/pending') as Promise<PendingReturn[]>,
        ApiClient.get('/inventory/low-stock') as Promise<StockRow[]>,
        ApiClient.get('/inventory/out-of-stock') as Promise<StockRow[]>,
      ])
      setPending(returns)
      setLowStock(low)
      setOutOfStock(out)
      setLoadError(null)
    } catch (err) {
      setLoadError(errorMessage(err, 'Fulfilment data could not be loaded.'))
    }
  }

  async function createShipment(event: FormEvent) {
    event.preventDefault()
    const orderId = Number(shipOrderId)
    if (!Number.isInteger(orderId) || orderId <= 0) {
      setShipError('Enter a valid order number.')
      return
    }
    setShipError(null)
    try {
      const shipment = (await ApiClient.post(`/orders/${orderId}/shipment`, {
        carrier,
        tracking_number: trackingNumber.trim(),
        base_rate: Number(baseRate),
        total_cost: Number(totalCost),
      })) as { id: number }
      setNotice({ kind: 'success', text: `Shipment ${shipment.id} created for order ${orderId}.` })
      setTrackingNumber('')
      setBaseRate('')
      setTotalCost('')
      setEventShipmentId(String(shipment.id))
    } catch (err) {
      setShipError(errorMessage(err, 'The shipment could not be created.'))
    }
  }

  async function addTrackingEvent(event: FormEvent) {
    event.preventDefault()
    const shipmentId = Number(eventShipmentId)
    if (!Number.isInteger(shipmentId) || shipmentId <= 0) {
      setEventError('Enter a valid shipment number.')
      return
    }
    setEventError(null)
    try {
      await ApiClient.post(`/shipments/${shipmentId}/tracking`, {
        status: eventStatus.trim(),
        location: eventLocation.trim() || null,
        description: eventDescription.trim() || null,
      })
      setEventStatus('')
      setEventLocation('')
      setEventDescription('')
      setNotice({ kind: 'success', text: `Tracking update added to shipment ${shipmentId}.` })
    } catch (err) {
      setEventError(errorMessage(err, 'The tracking update could not be added.'))
    }
  }

  async function runReturnAction(returnId: number, action: string, query: Record<string, string>, success: string) {
    const params = new URLSearchParams(Object.entries(query).filter(([, value]) => value !== ''))
    const suffix = params.toString() ? `?${params.toString()}` : ''
    try {
      await ApiClient.post(`/returns/${returnId}/${action}${suffix}`, {})
      setNotice({ kind: 'success', text: success })
      await load()
    } catch (err) {
      setNotice({ kind: 'error', text: errorMessage(err, 'The return could not be updated.') })
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Fulfilment</h1>

      {notice && (
        <p role={notice.kind === 'error' ? 'alert' : 'status'} className={notice.kind === 'error' ? 'text-red-700' : 'text-green-700'}>
          {notice.text}
        </p>
      )}
      {loadError && <p role="alert" className="text-red-700">{loadError}</p>}

      <section aria-label="Create shipment" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Create a shipment</h2>
        <form onSubmit={createShipment} className="grid gap-4 md:grid-cols-3">
          <label className="flex flex-col text-sm text-gray-700">
            Order number
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="numeric" value={shipOrderId} onChange={(e) => setShipOrderId(e.target.value)} required />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Carrier
            <select className="mt-1 rounded border border-gray-300 px-3 py-2" value={carrier} onChange={(e) => setCarrier(e.target.value)}>
              {CARRIERS.map((c) => (
                <option key={c} value={c}>{c.toUpperCase()}</option>
              ))}
            </select>
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Tracking number
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" value={trackingNumber} onChange={(e) => setTrackingNumber(e.target.value)} required />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Base rate
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="decimal" value={baseRate} onChange={(e) => setBaseRate(e.target.value)} required />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Total cost
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="decimal" value={totalCost} onChange={(e) => setTotalCost(e.target.value)} required />
          </label>
          <div className="flex items-end">
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Create shipment</button>
          </div>
          {shipError && <p role="alert" className="md:col-span-3 text-sm text-red-700">{shipError}</p>}
        </form>
      </section>

      <section aria-label="Tracking update" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Add a tracking update</h2>
        <form onSubmit={addTrackingEvent} className="grid gap-4 md:grid-cols-2">
          <label className="flex flex-col text-sm text-gray-700">
            Shipment number
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="numeric" value={eventShipmentId} onChange={(e) => setEventShipmentId(e.target.value)} required />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Status
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" value={eventStatus} onChange={(e) => setEventStatus(e.target.value)} required />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Location
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" value={eventLocation} onChange={(e) => setEventLocation(e.target.value)} />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Description
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" value={eventDescription} onChange={(e) => setEventDescription(e.target.value)} />
          </label>
          <div>
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Add update</button>
          </div>
          {eventError && <p role="alert" className="md:col-span-2 text-sm text-red-700">{eventError}</p>}
        </form>
      </section>

      <section aria-label="Stock alerts" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Stock alerts</h2>
        {lowStock.length === 0 && outOfStock.length === 0 ? (
          <p className="text-gray-600">Every product is above its reorder level.</p>
        ) : (
          <ul className="divide-y divide-gray-200">
            {outOfStock.map((row) => (
              <li key={`out-${row.id}`} className="py-2 text-sm text-red-700">
                Product #{row.product_id} is out of stock (on hand {row.quantity_on_hand})
              </li>
            ))}
            {lowStock.map((row) => (
              <li key={`low-${row.id}`} className="py-2 text-sm text-amber-800">
                Product #{row.product_id} is low on stock (on hand {row.quantity_on_hand}, reorder at {row.reorder_level})
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-label="Pending returns" className="bg-white rounded-lg shadow p-6 space-y-4">
        <h2 className="text-xl font-semibold text-gray-900">Pending returns</h2>
        {pending.length === 0 ? (
          <p className="text-gray-600">No returns are waiting for a decision.</p>
        ) : (
          <ul className="space-y-4">
            {pending.map((item) => (
              <li key={item.id} className="rounded border border-gray-200 p-4 space-y-3">
                <p className="text-sm text-gray-900">
                  <span className="font-medium">{item.rma_number ?? `Return #${item.id}`}</span> · order #{item.order_id} · {item.reason} · {item.status}
                </p>
                <div className="flex flex-wrap items-end gap-3">
                  {item.status === 'initiated' && (
                    <>
                      <label className="flex flex-col text-xs text-gray-700">
                        Approved refund
                        <input
                          aria-label={`Approved refund for return ${item.id}`}
                          className="mt-1 rounded border border-gray-300 px-2 py-1"
                          inputMode="decimal"
                          value={refundAmounts[item.id] ?? ''}
                          onChange={(e) => setRefundAmounts((current) => ({ ...current, [item.id]: e.target.value }))}
                        />
                      </label>
                      <button
                        type="button"
                        className="px-3 py-1 rounded bg-green-600 text-white text-sm"
                        onClick={() => runReturnAction(item.id, 'approve', { refund_amount: refundAmounts[item.id] ?? '' }, 'Return approved.')}
                      >
                        Approve
                      </button>
                      <button
                        type="button"
                        className="px-3 py-1 rounded bg-red-600 text-white text-sm"
                        onClick={() => runReturnAction(item.id, 'reject', {}, 'Return rejected.')}
                      >
                        Reject
                      </button>
                    </>
                  )}
                  {(item.status === 'approved' || item.status === 'shipped') && (
                    <>
                      <label className="flex flex-col text-xs text-gray-700">
                        Items received
                        <input
                          aria-label={`Items received for return ${item.id}`}
                          className="mt-1 rounded border border-gray-300 px-2 py-1"
                          inputMode="numeric"
                          value={receivedCounts[item.id] ?? String(item.quantity_requested)}
                          onChange={(e) => setReceivedCounts((current) => ({ ...current, [item.id]: e.target.value }))}
                        />
                      </label>
                      <button
                        type="button"
                        className="px-3 py-1 rounded bg-blue-600 text-white text-sm"
                        onClick={() => runReturnAction(item.id, 'receive', { quantity_received: receivedCounts[item.id] ?? String(item.quantity_requested) }, 'Return received.')}
                      >
                        Mark received
                      </button>
                    </>
                  )}
                  {item.status === 'received' && (
                    <button
                      type="button"
                      className="px-3 py-1 rounded bg-green-700 text-white text-sm"
                      onClick={() => runReturnAction(item.id, 'refund', {}, 'Refund processed.')}
                    >
                      Refund
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
