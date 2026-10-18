'use client'

import { useEffect, useState } from 'react'
import axios from 'axios'
import { errorMessage } from '@/lib/api-error'

export interface OrderItem {
  product_name: string
  product_sku: string
  quantity: number
  unit_price: string | number
  line_total: string | number
}

export interface Order {
  id: number
  order_number: string
  email: string
  subtotal: string | number
  tax: string | number
  shipping: string | number
  discount: string | number
  total: string | number
  order_status: string
  shipping_status: string
  shipping_method: string | null
  created_at: string
  items: OrderItem[]
}

const STATUS_COLOURS: Record<string, string> = {
  pending: 'bg-yellow-100 text-yellow-800',
  confirmed: 'bg-blue-100 text-blue-800',
  processing: 'bg-blue-100 text-blue-800',
  shipped: 'bg-purple-100 text-purple-800',
  delivered: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
}

function money(value: string | number): string {
  return `$${Number(value).toFixed(2)}`
}

/** Loads one of the signed-in user's orders and renders its details. */
export function OrderSummary({ orderId }: { orderId: string }) {
  const [order, setOrder] = useState<Order | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    axios
      .get(`/api/v1/orders/${orderId}`)
      .then((response) => {
        if (active) setOrder(response.data)
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'This order could not be loaded.'))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [orderId])

  if (loading) return <div className="p-6">Loading order…</div>
  if (error || !order) return <div role="alert" className="p-6 text-red-700">{error ?? 'Order not found.'}</div>

  const statusClass = STATUS_COLOURS[order.order_status] ?? 'bg-gray-100 text-gray-800'

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6 space-y-2">
        <h1 className="text-2xl font-bold text-gray-900">Order {order.order_number}</h1>
        <p className="text-sm text-gray-600">Placed {new Date(order.created_at).toLocaleDateString()} for {order.email}</p>
        <div className="flex gap-3 items-center">
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${statusClass}`}>{order.order_status}</span>
          <span className="px-3 py-1 rounded-full text-sm bg-gray-100 text-gray-800">Shipping: {order.shipping_status}</span>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left">Item</th>
              <th className="px-6 py-3 text-left">Qty</th>
              <th className="px-6 py-3 text-left">Price</th>
              <th className="px-6 py-3 text-left">Total</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {order.items.map((item) => (
              <tr key={item.product_sku}>
                <td className="px-6 py-3">
                  <div className="font-medium">{item.product_name}</div>
                  <div className="text-xs text-gray-500">SKU {item.product_sku}</div>
                </td>
                <td className="px-6 py-3">{item.quantity}</td>
                <td className="px-6 py-3">{money(item.unit_price)}</td>
                <td className="px-6 py-3">{money(item.line_total)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-white rounded-lg shadow p-6 max-w-sm ml-auto space-y-2">
        <div className="flex justify-between"><span>Subtotal</span><span>{money(order.subtotal)}</span></div>
        <div className="flex justify-between"><span>Tax</span><span>{money(order.tax)}</span></div>
        <div className="flex justify-between">
          <span>Shipping{order.shipping_method ? ` (${order.shipping_method})` : ''}</span>
          <span>{money(order.shipping)}</span>
        </div>
        {Number(order.discount) > 0 && (
          <div className="flex justify-between text-green-700"><span>Discount</span><span>-{money(order.discount)}</span></div>
        )}
        <div className="flex justify-between font-bold border-t pt-2"><span>Total</span><span>{money(order.total)}</span></div>
      </div>
    </div>
  )
}
