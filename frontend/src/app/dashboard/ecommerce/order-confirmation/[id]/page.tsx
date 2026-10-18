'use client'

import Link from 'next/link'
import { useParams } from 'next/navigation'
import { OrderSummary } from '@/components/ecommerce/order-summary'

export default function OrderConfirmationPage() {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="space-y-6">
      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <h1 className="text-2xl font-bold text-green-900">Thank you — your payment was received</h1>
        <p className="text-green-800 mt-1">Your order is being prepared. You can follow its progress below.</p>
        <div className="mt-4 flex gap-3">
          <Link href={`/dashboard/ecommerce/orders/${id}`} className="px-4 py-2 bg-blue-600 text-white rounded-md">
            View order
          </Link>
          <Link href="/dashboard/ecommerce/products" className="px-4 py-2 border border-gray-300 rounded-md">
            Continue shopping
          </Link>
        </div>
      </div>
      <OrderSummary orderId={id} />
    </div>
  )
}
