'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface MembershipTier {
  id: number
  name: string
  tier: string
  description: string | null
  price: number
  billing_cycle: string
  is_active: boolean
  subscriber_count: number
}

const TIERS = ['free', 'basic', 'premium', 'enterprise']
const BILLING_CYCLES = ['monthly', 'quarterly', 'annual']

export default function SubscriptionsPage() {
  const [tiers, setTiers] = useState<MembershipTier[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [creating, setCreating] = useState(false)
  const [name, setName] = useState('')
  const [tier, setTier] = useState('basic')
  const [price, setPrice] = useState(0)
  const [billingCycle, setBillingCycle] = useState('monthly')
  const [description, setDescription] = useState('')

  const load = () =>
    ApiClient.get('/membership-types')
      .then((data: MembershipTier[]) => setTiers(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'Subscription tiers could not be loaded.')))
      .finally(() => setLoading(false))

  useEffect(() => {
    load()
  }, [])

  const create = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    try {
      await ApiClient.post('/membership-types', {
        name: name.trim(),
        tier,
        description: description.trim() || null,
        price,
        billing_cycle: billingCycle,
      })
      setName('')
      setDescription('')
      setPrice(0)
      setCreating(false)
      setLoading(true)
      await load()
    } catch (err) {
      setError(errorMessage(err, 'The tier could not be created.'))
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Subscription Tiers</h1>
      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Your Tiers</h2>
            <button
              type="button"
              onClick={() => setCreating((open) => !open)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              + New Tier
            </button>
          </div>

          {creating && (
            <form onSubmit={create} className="mb-6 border rounded-lg p-4 space-y-3">
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Tier name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <label className="block text-sm">
                  <span className="block mb-1">Level</span>
                  <select className="w-full border rounded px-3 py-2" value={tier} onChange={(e) => setTier(e.target.value)}>
                    {TIERS.map((item) => (
                      <option key={item} value={item}>{item}</option>
                    ))}
                  </select>
                </label>
                <label className="block text-sm">
                  <span className="block mb-1">Price (USD)</span>
                  <input
                    type="number"
                    min={0}
                    step="0.01"
                    className="w-full border rounded px-3 py-2"
                    value={price}
                    onChange={(e) => setPrice(Number(e.target.value))}
                  />
                </label>
                <label className="block text-sm">
                  <span className="block mb-1">Billing</span>
                  <select className="w-full border rounded px-3 py-2" value={billingCycle} onChange={(e) => setBillingCycle(e.target.value)}>
                    {BILLING_CYCLES.map((item) => (
                      <option key={item} value={item}>{item}</option>
                    ))}
                  </select>
                </label>
              </div>
              <input
                className="w-full border rounded px-3 py-2"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
              <button type="submit" disabled={!name.trim()} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
                Create tier
              </button>
            </form>
          )}

          {loading ? (
            <p className="text-gray-500">Loading tiers…</p>
          ) : tiers.length === 0 ? (
            <p className="text-gray-500">No subscription tiers yet.</p>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {tiers.map((item) => (
                <div key={item.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-semibold text-lg">{item.name}</p>
                      <p className="text-2xl font-bold text-green-600">${item.price.toFixed(2)}/{item.billing_cycle}</p>
                      {item.description && <p className="text-sm text-gray-600">{item.description}</p>}
                    </div>
                    <div className="text-right text-sm">
                      <p className="text-gray-600">Level: {item.tier}</p>
                      <p className="text-gray-600">{item.is_active ? 'Active' : 'Inactive'}</p>
                      <p className="text-gray-600">{item.subscriber_count} active {item.subscriber_count === 1 ? 'subscriber' : 'subscribers'}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
