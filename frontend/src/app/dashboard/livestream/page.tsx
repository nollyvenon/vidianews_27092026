'use client'

import { useState } from 'react'

export default function LivestreamPage() {
  const [isLive, setIsLive] = useState(false)
  const [viewers] = useState(245)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Livestream</h1>
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Stream Status</h2>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              isLive ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
            }`}>
              {isLive ? '🔴 LIVE' : 'OFFLINE'}
            </span>
          </div>
          {isLive && (
            <div className="mb-4">
              <p className="text-lg font-semibold text-red-600">{viewers} viewers</p>
            </div>
          )}
          <button 
            onClick={() => setIsLive(!isLive)}
            className={`px-6 py-3 rounded font-medium text-white ${
              isLive ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {isLive ? 'End Stream' : 'Start Stream'}
          </button>
        </div>
      </div>
    </div>
  )
}
