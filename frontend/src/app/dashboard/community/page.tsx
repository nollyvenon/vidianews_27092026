'use client'
import { useState, useEffect } from 'react'

export default function CommunityPage() {
  const [threads, setThreads] = useState([])
  const [title, setTitle] = useState('')
  const [category, setCategory] = useState('general')

  useEffect(() => {
    fetchThreads()
  }, [])

  const fetchThreads = async () => {
    try {
      const res = await fetch('/api/v1/forum/threads')
      if (res.ok) {
        const data = await res.json()
        setThreads(data)
      }
    } catch (err) {
      console.error('Failed to fetch threads:', err)
    }
  }

  const handleCreateThread = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/v1/forum/thread', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, title })
      })
      if (res.ok) {
        setTitle('')
        fetchThreads()
      }
    } catch (err) {
      console.error('Failed to create thread:', err)
    }
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Community Forums</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">New Thread</h2>
        <form onSubmit={handleCreateThread} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Category</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
            >
              <option>general</option>
              <option>announcements</option>
              <option>support</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Thread title"
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            Create Thread
          </button>
        </form>
      </div>

      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Threads</h2>
        {threads.map(thread => (
          <div key={thread.id} className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold text-lg">{thread.title}</h3>
            <p className="text-sm text-gray-600">Replies: {thread.replies || 0}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
