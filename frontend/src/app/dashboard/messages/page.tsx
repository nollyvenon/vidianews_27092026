'use client'

import { useState } from 'react'

export default function MessagesPage() {
  const [conversations] = useState([
    { id: 1, name: 'Sarah Johnson', message: 'Thanks for the update', time: '2 min ago' },
    { id: 2, name: 'Mike Chen', message: 'See you tomorrow', time: '1 hour ago' }
  ])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Messages</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold">Conversations</h2>
        </div>
        <div className="divide-y">
          {conversations.map(c => (
            <div key={c.id} className="p-4 hover:bg-gray-50">
              <p className="font-semibold">{c.name}</p>
              <p className="text-sm text-gray-600">{c.message}</p>
              <p className="text-xs text-gray-500">{c.time}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
