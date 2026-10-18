'use client'

import { useCallback, useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface ContentItem {
  id: number
  title: string
  slug: string
  description: string | null
  body: string | null
  content_type: string
  status: string
  access_level: string
  views_count: number
  likes_count: number
  comments_count: number
  shares_count: number
  published_at: string | null
  created_at: string
  updated_at: string
}

export default function ContentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const router = useRouter()
  const [item, setItem] = useState<ContentItem | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  const load = useCallback(() => {
    ApiClient.get(`/content/${id}`)
      .then((data: ContentItem) => setItem(data))
      .catch((err) => setError(errorMessage(err, 'This content could not be loaded.')))
  }, [id])

  useEffect(() => {
    load()
  }, [load])

  const run = async (action: () => Promise<unknown>, onDone?: () => void) => {
    setBusy(true)
    setError(null)
    try {
      await action()
      onDone?.()
    } catch (err) {
      setError(errorMessage(err, 'That action could not be completed.'))
    } finally {
      setBusy(false)
    }
  }

  if (error && !item) return <p role="alert" className="text-red-700">{error}</p>
  if (!item) return <p className="text-gray-600">Loading content…</p>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Link href="/dashboard/content" className="text-blue-600 hover:underline">
          ← Back to content
        </Link>
        <Link href={`/dashboard/content/${id}/edit`} className="px-4 py-2 bg-blue-600 text-white rounded-md">
          Edit
        </Link>
      </div>

      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <h1 className="text-3xl font-bold">{item.title}</h1>
        <div className="flex flex-wrap gap-2 text-sm">
          <span className="px-2 py-1 rounded bg-gray-100">{item.content_type}</span>
          <span className="px-2 py-1 rounded bg-gray-100">{item.status}</span>
          <span className="px-2 py-1 rounded bg-gray-100">{item.access_level}</span>
        </div>
        {item.description && <p className="text-gray-600">{item.description}</p>}
        <div className="whitespace-pre-wrap text-gray-900">{item.body || 'No body text yet.'}</div>
        <p className="text-sm text-gray-500">
          {item.views_count} views · {item.likes_count} likes · {item.comments_count} comments · {item.shares_count} shares
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-6 flex flex-wrap gap-3">
        {item.status !== 'published' && (
          <button
            type="button"
            disabled={busy}
            onClick={() => run(() => ApiClient.post(`/content/${id}/publish`, { access_level: item.access_level }), load)}
            className="px-4 py-2 bg-green-600 text-white rounded-md disabled:opacity-50"
          >
            Publish
          </button>
        )}
        {item.status !== 'archived' && (
          <button
            type="button"
            disabled={busy}
            onClick={() => run(() => ApiClient.post(`/content/${id}/archive`, {}), load)}
            className="px-4 py-2 border border-gray-300 rounded-md disabled:opacity-50"
          >
            Archive
          </button>
        )}
        <button
          type="button"
          disabled={busy}
          onClick={() => {
            if (window.confirm('Delete this content? This cannot be undone.')) {
              run(() => ApiClient.delete(`/content/${id}`), () => router.push('/dashboard/content'))
            }
          }}
          className="px-4 py-2 bg-red-600 text-white rounded-md disabled:opacity-50"
        >
          Delete
        </button>
      </div>
    </div>
  )
}
