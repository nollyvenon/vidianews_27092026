'use client'

import { useState } from 'react'

export default function CachePage() {
  const [policies] = useState([
    { id: 1, resource: 'content', type: 'redis', ttl: 3600, hits: 4850, misses: 320 },
    { id: 2, resource: 'users', type: 'cloudflare', ttl: 1800, hits: 2100, misses: 85 },
    { id: 3, resource: 'analytics', type: 'redis', ttl: 7200, hits: 1230, misses: 45 }
  ])

  const hitRate = policies.map(p => (p.hits / (p.hits + p.misses) * 100).toFixed(1))

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Cache Configuration</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Cache Policies</h2>
          <div className="space-y-4">
            {policies.map((policy, idx) => (
              <div key={policy.id} className="border rounded p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-lg">{policy.resource}</p>
                    <p className="text-sm text-gray-600">Type: {policy.type} | TTL: {policy.ttl}s</p>
                  </div>
                  <span className="text-2xl font-bold text-blue-600">{hitRate[idx]}%</span>
                </div>
                <div className="flex justify-between text-sm text-gray-600">
                  <span>{policy.hits} hits</span>
                  <span>{policy.misses} misses</span>
                </div>
                <div className="w-full bg-gray-200 rounded h-2 mt-2">
                  <div className="bg-green-600 h-2 rounded" style={{ width: `${parseFloat(hitRate[idx])}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Performance Metrics</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-blue-600">45ms</p>
              <p className="text-sm text-gray-600">Avg Response Time</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-green-600">98.2%</p>
              <p className="text-sm text-gray-600">Overall Hit Rate</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-purple-600">2.3GB</p>
              <p className="text-sm text-gray-600">Cache Size</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Cache Management</h2>
          <div className="space-y-2">
            <button className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">Flush All Cache</button>
            <button className="w-full px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">Optimize Cache</button>
          </div>
        </div>
      </div>
    </div>
  )
}
