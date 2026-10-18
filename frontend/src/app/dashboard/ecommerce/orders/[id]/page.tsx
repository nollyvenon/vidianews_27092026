'use client'

import Link from 'next/link'
import { useParams } from 'next/navigation'
import { OrderSummary } from '@/components/ecommerce/order-summary'

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="space-y-6">
      <Link href="/dashboard/ecommerce/orders" className="text-blue-600 hover:underline">
        ← Back to orders
      </Link>
      <OrderSummary orderId={id} />
    </div>
  )
}
