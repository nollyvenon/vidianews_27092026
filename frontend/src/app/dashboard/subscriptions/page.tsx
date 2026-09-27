'use client'

import { useState } from 'react'

export default function SubscriptionsPage() {
  const [tiers] = useState([
    { id: 1, name: 'Silver', price: 4.99, subscribers: 245 },
    { id: 2, name: 'Gold', price: 9.99, subscribers: 152 },
    { id: 3, name: 'Platinum', price: 19.99, subscribers: 48 }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Subscription Tiers</h1>
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Your Tiers</h2>
            <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">+ New Tier</button>
          </div>
          <div className="grid grid-cols-1 gap-4">
            {tiers.map(tier => (
              <div key={tier.id} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-lg">{tier.name}</p>
                    <p className="text-2xl font-bold text-green-600">${tier.price}/mo</p>
                  </div>
                  <span className="text-sm text-gray-600">{tier.subscribers} subscribers</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
