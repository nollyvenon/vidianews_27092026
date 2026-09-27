'use client'

import { useState } from 'react'

export default function FollowersPage() {
  const [followers] = useState([
    { id: 1, name: 'John Doe', username: 'johndoe', followers: '1.2K' },
    { id: 2, name: 'Jane Smith', username: 'janesmith', followers: '2.5K' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">My Network</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Followers</h2>
        <div className="space-y-3">
          {followers.map(f => (
            <div key={f.id} className="border rounded-lg p-4">
              <p className="font-semibold">{f.name}</p>
              <p className="text-sm text-gray-600">{f.followers} followers</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
