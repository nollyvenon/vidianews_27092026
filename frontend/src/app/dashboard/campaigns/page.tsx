'use client'

import { useState } from 'react'

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState([
    { id: 1, name: 'Welcome Series', status: 'sent', recipients: 1250 },
    { id: 2, name: 'Product Launch', status: 'draft', recipients: 0 },
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Email Campaigns</h1>

      <button className="mb-6 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        + New Campaign
      </button>

      <div className="space-y-4">
        {campaigns.map((c) => (
          <div key={c.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-lg">{c.name}</h3>
                <p className="text-sm text-gray-600">{c.recipients} recipients</p>
              </div>
              <span className={`px-3 py-1 rounded text-sm ${c.status === 'sent' ? 'bg-green-100 text-green-800' : 'bg-gray-100'}`}>
                {c.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
