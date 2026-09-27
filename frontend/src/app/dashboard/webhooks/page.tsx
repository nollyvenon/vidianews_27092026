'use client'

import { useState } from 'react'

export default function WebhooksPage() {
  const [webhooks, setWebhooks] = useState<any[]>([])
  const [newUrl, setNewUrl] = useState('')
  const [selectedEvent, setSelectedEvent] = useState('content.published')

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newUrl) return
    setWebhooks([...webhooks, { id: Date.now(), event_type: selectedEvent, url: newUrl, is_active: true }])
    setNewUrl('')
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Webhooks</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Create Webhook</h2>
        <form onSubmit={handleCreate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Event Type</label>
            <select value={selectedEvent} onChange={(e) => setSelectedEvent(e.target.value)} className="w-full px-4 py-2 border rounded-md">
              <option value="content.published">Content Published</option>
              <option value="content.updated">Content Updated</option>
              <option value="user.login">User Login</option>
              <option value="payment.completed">Payment Completed</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">URL</label>
            <input type="url" value={newUrl} onChange={(e) => setNewUrl(e.target.value)} placeholder="https://example.com/webhook" className="w-full px-4 py-2 border rounded-md" required />
          </div>
          <button type="submit" className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Create</button>
        </form>
      </div>

      <div className="space-y-4">
        {webhooks.map((webhook) => (
          <div key={webhook.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="font-semibold">{webhook.event_type}</h3>
                <p className="text-sm text-gray-600">{webhook.url}</p>
              </div>
              <div className="text-right">
                <span className={`px-3 py-1 rounded text-sm ${webhook.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100'}`}>
                  {webhook.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
