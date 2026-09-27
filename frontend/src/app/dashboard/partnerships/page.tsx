'use client'

import { useState } from 'react'

export default function PartnershipsPage() {
  const [partnerships] = useState([
    { id: 1, name: 'Brand XYZ', type: 'Brand Deal', status: 'Active' },
    { id: 2, name: 'Creator ABC', type: 'Collaboration', status: 'Active' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Partnerships</h1>
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Active Partnerships</h2>
            <button className="px-4 py-2 bg-blue-600 text-white rounded text-sm">+ New</button>
          </div>
          <div className="space-y-3">
            {partnerships.map(p => (
              <div key={p.id} className="border rounded-lg p-4">
                <p className="font-semibold">{p.name}</p>
                <p className="text-sm text-gray-600">{p.type}</p>
                <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 rounded text-xs">{p.status}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
