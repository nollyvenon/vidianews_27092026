'use client'

import { useState } from 'react'

export default function CreatorPage() {
  const [profile, setProfile] = useState({ followers: 0, earnings: 0 })

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Creator Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-blue-600">{profile.followers}</div>
          <div className="text-gray-600">Followers</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">${profile.earnings}</div>
          <div className="text-gray-600">Total Earnings</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-purple-600">Pro</div>
          <div className="text-gray-600">Status</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Earnings</h2>
          <div className="h-40 bg-gray-100 rounded flex items-center justify-center">
            Chart would go here
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Actions</h2>
          <ul className="space-y-2 text-sm">
            <li>✓ Video published 2 hours ago</li>
            <li>✓ 50 new followers today</li>
            <li>✓ $125 earned this week</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
