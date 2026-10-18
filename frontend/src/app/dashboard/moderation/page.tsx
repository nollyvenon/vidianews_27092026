'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface QueueItem {
  id: number
  content_id: number
  content_type: string
  status: string
  reason: string
  confidence_score: number
  created_at: string
}

export default function ModerationPage() {
  const [items, setItems] = useState<QueueItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [note, setNote] = useState('')
  const [busyId, setBusyId] = useState<number | null>(null)

  const load = () =>
    ApiClient.get('/moderation/queue/pending')
      .then((data: QueueItem[]) => setItems(Array.isArray(data) ? data : []))
      .catch((err) => setError(errorMessage(err, 'The moderation queue could not be loaded.')))
      .finally(() => setLoading(false))

  useEffect(() => {
    load()
  }, [])

  const review = async (item: QueueItem, status: 'approved' | 'rejected') => {
    setBusyId(item.id)
    setError(null)
    try {
      await ApiClient.post(`/moderation/queue/${item.id}/review`, { status, decision: note.trim() })
      setNote('')
      setLoading(true)
      await load()
    } catch (err) {
      setError(errorMessage(err, 'The review could not be saved.'))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Content Moderation</h1>
      {error && <p role="alert" className="mb-4 bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}
      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Pending Reports</h2>
          <label className="block mb-4 text-sm">
            <span className="block mb-1">Decision note (required)</span>
            <input
              className="w-full border rounded px-3 py-2"
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="Why you approved or rejected this content"
            />
          </label>
          {loading ? (
            <p className="text-gray-500">Loading queue…</p>
          ) : items.length === 0 ? (
            <p className="text-gray-500">No content is waiting for review.</p>
          ) : (
            <div className="space-y-3">
              {items.map((item) => (
                <div key={item.id} className="border rounded-lg p-4">
                  <p className="font-semibold">{item.content_type} #{item.content_id}</p>
                  <p className="text-sm text-gray-600">Reason: {item.reason}</p>
                  <p className="text-sm text-gray-600">Confidence: {Math.round(item.confidence_score * 100)}%</p>
                  <div className="mt-3 flex gap-2">
                    <button
                      type="button"
                      disabled={!note.trim() || busyId === item.id}
                      onClick={() => review(item, 'approved')}
                      className="px-3 py-1 text-sm bg-green-600 text-white rounded disabled:opacity-50"
                    >
                      Approve
                    </button>
                    <button
                      type="button"
                      disabled={!note.trim() || busyId === item.id}
                      onClick={() => review(item, 'rejected')}
                      className="px-3 py-1 text-sm bg-red-600 text-white rounded disabled:opacity-50"
                    >
                      Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
