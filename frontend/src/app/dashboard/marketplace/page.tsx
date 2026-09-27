'use client'

import { useState } from 'react'

export default function MarketplacePage() {
  const [creators] = useState([
    { id: 1, name: 'Tech Reviews', earnings: 5200, followers: 12400, rating: 4.8 },
    { id: 2, name: 'Lifestyle Vlog', earnings: 3800, followers: 8900, rating: 4.6 },
    { id: 3, name: 'Gaming Pro', earnings: 7100, followers: 25600, rating: 4.9 },
    { id: 4, name: 'Travel Diaries', earnings: 2900, followers: 6200, rating: 4.5 }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Creator Marketplace</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Top Creators</h2>
          <div className="space-y-3">
            {creators.map(creator => (
              <div key={creator.id} className="border rounded-lg p-4 hover:shadow-md transition">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-semibold text-lg">{creator.name}</p>
                    <div className="flex items-center gap-4 text-sm text-gray-600 mt-1">
                      <span>👥 {creator.followers.toLocaleString()} followers</span>
                      <span>⭐ {creator.rating}/5</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-green-600">${creator.earnings.toLocaleString()}</p>
                    <p className="text-xs text-gray-600">Monthly earnings</p>
                  </div>
                </div>
                <button className="w-full mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
                  View Profile
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Marketplace Stats</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-blue-600">847</p>
              <p className="text-sm text-gray-600">Active Creators</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-green-600">$2.4M</p>
              <p className="text-sm text-gray-600">Monthly Revenue</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-purple-600">1.2M</p>
              <p className="text-sm text-gray-600">Total Followers</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
