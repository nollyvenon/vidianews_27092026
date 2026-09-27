'use client'

import { useState } from 'react'

export default function PremiumPage() {
  const [isPremium] = useState(true)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Premium Features</h1>
      <div className="grid gap-6">
        <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg shadow p-8 text-white">
          <h2 className="text-2xl font-bold mb-2">VidiNews Premium</h2>
          <p className="opacity-90">Ad-free streaming, exclusive content, and more</p>
          {isPremium ? (
            <div className="mt-4">
              <span className="inline-block px-4 py-2 bg-white text-purple-600 rounded font-bold">Active</span>
            </div>
          ) : (
            <button className="mt-4 px-6 py-2 bg-white text-purple-600 rounded font-bold hover:bg-gray-100">Subscribe Now</button>
          )}
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold mb-4">Included Features</h3>
          <ul className="space-y-2 text-sm">
            <li>✓ HD Streaming</li>
            <li>✓ Ad-Free</li>
            <li>✓ Early Access</li>
            <li>✓ Exclusive Content</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
