'use client'

import { useState, useEffect } from 'react'

export default function RealtimePage() {
  const [messages, setMessages] = useState([
    { id: 1, user: 'John', content: 'Just uploaded a new video!', timestamp: 'now' },
    { id: 2, user: 'Jane', content: 'Great content', timestamp: '2 min ago' },
    { id: 3, user: 'Mike', content: 'Love your channel', timestamp: '5 min ago' }
  ])
  const [newMessage, setNewMessage] = useState('')

  const handleSend = () => {
    if (newMessage.trim()) {
      setMessages([{ id: messages.length + 1, user: 'You', content: newMessage, timestamp: 'now' }, ...messages])
      setNewMessage('')
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Live Feed</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center mb-4">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></div>
            <span className="font-semibold">Live Updates</span>
          </div>

          <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
            {messages.map(msg => (
              <div key={msg.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex justify-between items-start">
                  <p className="font-semibold text-sm">{msg.user}</p>
                  <p className="text-xs text-gray-500">{msg.timestamp}</p>
                </div>
                <p className="text-gray-700 text-sm mt-1">{msg.content}</p>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type a message..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded focus:outline-none"
            />
            <button
              onClick={handleSend}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Send
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Connected Users</h2>
          <div className="space-y-2">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span>45 users online</span>
            </div>
            <div className="flex items-center">
              <div className="w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
              <span>12 users idle</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
