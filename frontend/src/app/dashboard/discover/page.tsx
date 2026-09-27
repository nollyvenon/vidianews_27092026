'use client'

import { useState } from 'react'

export default function DiscoverPage() {
  const [recommendations] = useState([
    { id: 1, title: 'Amazing Travel Vlog', creator: 'travelbug', views: '2.3K' },
    { id: 2, title: 'Cooking Tutorial', creator: 'foodie', views: '1.8K' }
  ])

  const [trending] = useState([
    { tag: 'python', count: '12.5K' },
    { tag: 'webdesign', count: '8.3K' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Discover</h1>
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recommended</h2>
          <div className="space-y-3">
            {recommendations.map(r => (
              <div key={r.id} className="border rounded-lg p-4">
                <p className="font-semibold">{r.title}</p>
                <p className="text-xs text-gray-600">{r.creator} - {r.views} views</p>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Trending</h2>
          <div className="space-y-2">
            {trending.map((t, i) => (
              <div key={i} className="flex justify-between">
                <span>#{t.tag}</span>
                <span className="text-sm text-gray-600">{t.count} posts</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
