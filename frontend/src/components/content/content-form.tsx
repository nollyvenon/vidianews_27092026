'use client'

import { FormEvent, useState } from 'react'
import { errorMessage } from '@/lib/api-error'

export interface ContentValues {
  title: string
  slug: string
  description: string
  body: string
  content_type: 'video' | 'article' | 'blog_post' | 'newsletter'
  status: 'draft' | 'scheduled' | 'published' | 'archived'
  access_level: 'public' | 'members_only' | 'premium' | 'private'
  thumbnail_url: string
}

export const EMPTY_CONTENT: ContentValues = {
  title: '',
  slug: '',
  description: '',
  body: '',
  content_type: 'article',
  status: 'draft',
  access_level: 'public',
  thumbnail_url: '',
}

/** URL-safe slug from a title, used until the author edits the slug field. */
export function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 500)
}

interface ContentFormProps {
  initial?: ContentValues
  submitLabel: string
  onSubmit: (values: ContentValues) => Promise<void>
}

export function ContentForm({ initial = EMPTY_CONTENT, submitLabel, onSubmit }: ContentFormProps) {
  const [values, setValues] = useState<ContentValues>(initial)
  const [slugEdited, setSlugEdited] = useState(Boolean(initial.slug))
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const update = (field: keyof ContentValues, value: string) => {
    setValues((prev) => {
      const next = { ...prev, [field]: value }
      if (field === 'title' && !slugEdited) next.slug = slugify(value)
      return next
    })
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    setSaving(true)
    try {
      await onSubmit(values)
    } catch (err) {
      setError(errorMessage(err, 'The content could not be saved.'))
    } finally {
      setSaving(false)
    }
  }

  const inputClass = 'w-full border rounded-md px-3 py-2'

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white rounded-lg shadow p-6">
      {error && (
        <div role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">
          {error}
        </div>
      )}

      <label className="block">
        <span className="block text-sm font-medium mb-1">Title</span>
        <input className={inputClass} value={values.title} onChange={(e) => update('title', e.target.value)} required />
      </label>

      <label className="block">
        <span className="block text-sm font-medium mb-1">Slug</span>
        <input
          className={inputClass}
          value={values.slug}
          onChange={(e) => {
            setSlugEdited(true)
            update('slug', e.target.value)
          }}
          required
        />
      </label>

      <label className="block">
        <span className="block text-sm font-medium mb-1">Summary</span>
        <textarea className={inputClass} rows={2} value={values.description} onChange={(e) => update('description', e.target.value)} />
      </label>

      <label className="block">
        <span className="block text-sm font-medium mb-1">Body</span>
        <textarea className={inputClass} rows={10} value={values.body} onChange={(e) => update('body', e.target.value)} />
      </label>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <label className="block">
          <span className="block text-sm font-medium mb-1">Type</span>
          <select className={inputClass} value={values.content_type} onChange={(e) => update('content_type', e.target.value)}>
            <option value="article">Article</option>
            <option value="video">Video</option>
            <option value="blog_post">Blog post</option>
            <option value="newsletter">Newsletter</option>
          </select>
        </label>
        <label className="block">
          <span className="block text-sm font-medium mb-1">Status</span>
          <select className={inputClass} value={values.status} onChange={(e) => update('status', e.target.value)}>
            <option value="draft">Draft</option>
            <option value="scheduled">Scheduled</option>
            <option value="published">Published</option>
            <option value="archived">Archived</option>
          </select>
        </label>
        <label className="block">
          <span className="block text-sm font-medium mb-1">Access</span>
          <select className={inputClass} value={values.access_level} onChange={(e) => update('access_level', e.target.value)}>
            <option value="public">Public</option>
            <option value="members_only">Members only</option>
            <option value="premium">Premium</option>
            <option value="private">Private</option>
          </select>
        </label>
      </div>

      <label className="block">
        <span className="block text-sm font-medium mb-1">Thumbnail URL</span>
        <input className={inputClass} type="url" value={values.thumbnail_url} onChange={(e) => update('thumbnail_url', e.target.value)} />
      </label>

      <button type="submit" disabled={saving} className="px-6 py-2 bg-blue-600 text-white rounded-md disabled:opacity-50">
        {saving ? 'Saving…' : submitLabel}
      </button>
    </form>
  )
}
