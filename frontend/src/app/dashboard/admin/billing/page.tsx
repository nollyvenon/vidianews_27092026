'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ApiClient } from '@/lib/api-client'

const SUBSCRIPTION_TIERS = ['free', 'starter', 'pro', 'enterprise'] as const

export interface SubscriptionRow {
  id: number
  user_id: number
  user_email: string | null
  organization_id: number
  tier: string | null
  billing_cycle: string | null
  amount: number
  is_active: boolean
  started_at: string | null
  renews_at: string | null
  canceled_at: string | null
}

export interface TransactionRow {
  source: 'subscription' | 'checkout'
  id: number
  user_id: number | null
  user_email: string | null
  amount: number
  currency: string
  status: string | null
  payment_method: string | null
  reference: string | null
  created_at: string | null
}

interface Page<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

const PAGE_SIZE = 20

function formatDate(value: string | null): string {
  return value ? new Date(value).toLocaleString() : '—'
}

function formatMoney(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount)
}

/** Administrators review subscriptions (change tier, cancel) and all payment transactions. */
export default function BillingAdminPage() {
  return (
    <div className="mx-auto max-w-6xl space-y-8 p-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Subscriptions &amp; transactions</h1>
        <p className="mt-1 text-sm text-gray-600">Manage customer subscriptions and review payments.</p>
      </div>
      <SubscriptionsSection />
      <TransactionsSection />
    </div>
  )
}

function SubscriptionsSection() {
  const [rows, setRows] = useState<SubscriptionRow[]>([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [activeFilter, setActiveFilter] = useState<'all' | 'active' | 'canceled'>('all')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState<number | null>(null)
  const [tierDrafts, setTierDrafts] = useState<Record<number, string>>({})

  const load = async () => {
    setLoading(true)
    setError('')
    const query = new URLSearchParams({ skip: String(skip), limit: String(PAGE_SIZE) })
    if (activeFilter !== 'all') query.set('is_active', String(activeFilter === 'active'))
    try {
      const page: Page<SubscriptionRow> = await ApiClient.get(`/admin/subscriptions?${query.toString()}`)
      setRows(page.items)
      setTotal(page.total)
    } catch (err: any) {
      setError(err.message || 'Could not load subscriptions')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [skip, activeFilter])

  const saveTier = async (row: SubscriptionRow) => {
    const tier = tierDrafts[row.id] ?? row.tier
    setBusy(row.id)
    setError('')
    try {
      const updated: SubscriptionRow = await ApiClient.patch(`/admin/subscriptions/${row.id}`, { tier })
      setRows((current) => current.map((item) => (item.id === updated.id ? updated : item)))
    } catch (err: any) {
      setError(err.message || 'Could not change the tier')
    } finally {
      setBusy(null)
    }
  }

  const cancel = async (row: SubscriptionRow) => {
    if (!window.confirm(`Cancel the subscription for ${row.user_email ?? 'this customer'}?`)) return
    setBusy(row.id)
    setError('')
    try {
      const updated: SubscriptionRow = await ApiClient.post(`/admin/subscriptions/${row.id}/cancel`, {})
      setRows((current) => current.map((item) => (item.id === updated.id ? updated : item)))
    } catch (err: any) {
      setError(err.message || 'Could not cancel the subscription')
    } finally {
      setBusy(null)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Subscriptions</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-3">
          <label htmlFor="sub-filter" className="text-sm text-gray-700">Show</label>
          <select
            id="sub-filter"
            className="rounded-md border border-gray-300 px-2 py-1 text-sm"
            value={activeFilter}
            onChange={(e) => {
              setSkip(0)
              setActiveFilter(e.target.value as 'all' | 'active' | 'canceled')
            }}
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="canceled">Canceled</option>
          </select>
        </div>

        {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
        {loading ? (
          <p role="status" className="text-sm text-gray-600">Loading subscriptions...</p>
        ) : rows.length === 0 ? (
          <p className="text-sm text-gray-600">No subscriptions found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50 text-left text-gray-600">
                <tr>
                  <th className="px-3 py-2">Customer</th>
                  <th className="px-3 py-2">Tier</th>
                  <th className="px-3 py-2">Amount</th>
                  <th className="px-3 py-2">Renews</th>
                  <th className="px-3 py-2">Status</th>
                  <th className="px-3 py-2">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {rows.map((row) => (
                  <tr key={row.id}>
                    <td className="px-3 py-2">{row.user_email ?? `User #${row.user_id}`}</td>
                    <td className="px-3 py-2">
                      <label className="sr-only" htmlFor={`tier-${row.id}`}>Tier for subscription {row.id}</label>
                      <select
                        id={`tier-${row.id}`}
                        className="rounded-md border border-gray-300 px-2 py-1"
                        value={tierDrafts[row.id] ?? row.tier ?? 'free'}
                        onChange={(e) => setTierDrafts((current) => ({ ...current, [row.id]: e.target.value }))}
                      >
                        {SUBSCRIPTION_TIERS.map((tier) => (
                          <option key={tier} value={tier}>{tier}</option>
                        ))}
                      </select>
                    </td>
                    <td className="px-3 py-2">{formatMoney(row.amount)}</td>
                    <td className="px-3 py-2">{formatDate(row.renews_at)}</td>
                    <td className="px-3 py-2">{row.is_active ? 'Active' : `Canceled ${formatDate(row.canceled_at)}`}</td>
                    <td className="px-3 py-2 space-x-2">
                      <Button size="sm" variant="outline" onClick={() => saveTier(row)} disabled={busy === row.id}>
                        Save tier
                      </Button>
                      {row.is_active && (
                        <Button size="sm" variant="destructive" onClick={() => cancel(row)} disabled={busy === row.id}>
                          Cancel
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <Pager skip={skip} total={total} onChange={setSkip} />
      </CardContent>
    </Card>
  )
}

function TransactionsSection() {
  const [rows, setRows] = useState<TransactionRow[]>([])
  const [total, setTotal] = useState(0)
  const [skip, setSkip] = useState(0)
  const [source, setSource] = useState<'all' | 'subscription' | 'checkout'>('all')
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setLoading(true)
    setError('')
    const query = new URLSearchParams({ source, skip: String(skip), limit: String(PAGE_SIZE) })
    if (status) query.set('status', status)
    ApiClient.get(`/admin/transactions?${query.toString()}`)
      .then((page: Page<TransactionRow>) => {
        setRows(page.items)
        setTotal(page.total)
      })
      .catch((err: Error) => setError(err.message || 'Could not load transactions'))
      .finally(() => setLoading(false))
  }, [skip, source, status])

  return (
    <Card>
      <CardHeader>
        <CardTitle>Transactions</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex flex-wrap items-center gap-3 text-sm">
          <label htmlFor="tx-source" className="text-gray-700">Source</label>
          <select
            id="tx-source"
            className="rounded-md border border-gray-300 px-2 py-1"
            value={source}
            onChange={(e) => {
              setSkip(0)
              setSource(e.target.value as 'all' | 'subscription' | 'checkout')
            }}
          >
            <option value="all">All</option>
            <option value="subscription">Subscriptions</option>
            <option value="checkout">Checkout</option>
          </select>
          <label htmlFor="tx-status" className="text-gray-700">Status</label>
          <select
            id="tx-status"
            className="rounded-md border border-gray-300 px-2 py-1"
            value={status}
            onChange={(e) => {
              setSkip(0)
              setStatus(e.target.value)
            }}
          >
            <option value="">Any</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
            <option value="refunded">Refunded</option>
          </select>
        </div>

        {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
        {loading ? (
          <p role="status" className="text-sm text-gray-600">Loading transactions...</p>
        ) : rows.length === 0 ? (
          <p className="text-sm text-gray-600">No transactions found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50 text-left text-gray-600">
                <tr>
                  <th className="px-3 py-2">Date</th>
                  <th className="px-3 py-2">Source</th>
                  <th className="px-3 py-2">Customer</th>
                  <th className="px-3 py-2">Amount</th>
                  <th className="px-3 py-2">Method</th>
                  <th className="px-3 py-2">Status</th>
                  <th className="px-3 py-2">Reference</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {rows.map((row) => (
                  <tr key={`${row.source}-${row.id}`}>
                    <td className="px-3 py-2">{formatDate(row.created_at)}</td>
                    <td className="px-3 py-2 capitalize">{row.source}</td>
                    <td className="px-3 py-2">{row.user_email ?? '—'}</td>
                    <td className="px-3 py-2">{formatMoney(row.amount, row.currency)}</td>
                    <td className="px-3 py-2">{row.payment_method ?? '—'}</td>
                    <td className="px-3 py-2">{row.status ?? '—'}</td>
                    <td className="px-3 py-2 font-mono text-xs">{row.reference ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <Pager skip={skip} total={total} onChange={setSkip} />
      </CardContent>
    </Card>
  )
}

function Pager({ skip, total, onChange }: { skip: number; total: number; onChange: (skip: number) => void }) {
  const hasPrev = skip > 0
  const hasNext = skip + PAGE_SIZE < total
  return (
    <nav aria-label="Pagination" className="flex items-center justify-between text-sm text-gray-600">
      <span>{total} total</span>
      <div className="space-x-2">
        <Button size="sm" variant="outline" onClick={() => onChange(Math.max(0, skip - PAGE_SIZE))} disabled={!hasPrev}>
          Previous
        </Button>
        <Button size="sm" variant="outline" onClick={() => onChange(skip + PAGE_SIZE)} disabled={!hasNext}>
          Next
        </Button>
      </div>
    </nav>
  )
}
