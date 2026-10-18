'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'
import { useAuth } from '@/hooks/useAuth'

interface Message {
  id: number
  sender_id: number
  content: string
  is_read: boolean
}

/** Direct messages with another member, identified by their user id. */
export default function MessagesPage() {
  const { user } = useAuth()
  const [unread, setUnread] = useState<number | null>(null)
  const [otherId, setOtherId] = useState('')
  const [conversation, setConversation] = useState<Message[] | null>(null)
  const [draft, setDraft] = useState('')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/messages/unread/count')
      .then((data: { unread_count: number }) => setUnread(data.unread_count))
      .catch((err) => setError(errorMessage(err, 'Unread count could not be loaded.')))
  }, [])

  const openConversation = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    try {
      setConversation(await ApiClient.get(`/messages/${Number(otherId)}`))
    } catch (err) {
      setError(errorMessage(err, 'The conversation could not be loaded.'))
    }
  }

  const send = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    try {
      const query = new URLSearchParams({ recipient_id: otherId, content: draft.trim() }).toString()
      await ApiClient.post(`/messages/send?${query}`, {})
      setDraft('')
      setConversation(await ApiClient.get(`/messages/${Number(otherId)}`))
    } catch (err) {
      setError(errorMessage(err, 'The message could not be sent.'))
    }
  }

  const markRead = async (message: Message) => {
    setError(null)
    try {
      await ApiClient.put(`/messages/${message.id}/read`, {})
      setConversation((current) => (current ?? []).map((item) => (item.id === message.id ? { ...item, is_read: true } : item)))
      setUnread((count) => Math.max(0, (count ?? 0) - 1))
    } catch (err) {
      setError(errorMessage(err, 'The message could not be marked as read.'))
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Messages</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      <p className="text-gray-600">Unread messages: {unread ?? '…'}</p>

      <form onSubmit={openConversation} className="flex gap-2 items-end">
        <label className="text-sm">
          <span className="block text-xs text-gray-600">Member user ID</span>
          <input type="number" min={1} className="border rounded px-2 py-1" value={otherId} onChange={(e) => setOtherId(e.target.value)} required />
        </label>
        <button type="submit" className="px-3 py-1 border border-blue-600 text-blue-600 rounded">Open conversation</button>
      </form>

      {conversation !== null && (
        <div className="bg-white rounded-lg shadow p-6 space-y-4">
          {conversation.length === 0 ? (
            <p className="text-gray-500">No messages with this member yet.</p>
          ) : (
            <ul className="space-y-2">
              {conversation.map((message) => (
                <li key={message.id} className="border rounded p-3 flex justify-between gap-4">
                  <span>
                    <span className="text-xs text-gray-500">{message.sender_id === user?.id ? 'You' : `Member #${message.sender_id}`}: </span>
                    {message.content}
                  </span>
                  {!message.is_read && message.sender_id !== user?.id ? (
                    <button type="button" onClick={() => markRead(message)} className="text-sm text-blue-600 hover:underline">Mark read</button>
                  ) : (
                    <span className="text-xs text-gray-400">{message.is_read ? 'Read' : 'Sent'}</span>
                  )}
                </li>
              ))}
            </ul>
          )}
          <form onSubmit={send} className="flex gap-2">
            <input className="flex-1 border rounded px-3 py-2" placeholder="Write a message" value={draft} onChange={(e) => setDraft(e.target.value)} required />
            <button type="submit" disabled={!draft.trim() || !otherId} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">Send</button>
          </form>
        </div>
      )}
    </div>
  )
}
