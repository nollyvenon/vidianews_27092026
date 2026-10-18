'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface ContentOption {
  id: number
  title: string
  status: string
  content_type: string
  body?: string | null
}

interface ContentPickerProps {
  value: number | null
  onChange: (content: ContentOption | null) => void
  label?: string
}

/** Lets the author choose which of their content items a quality check or publication applies to. */
export function ContentPicker({ value, onChange, label = 'Content item' }: ContentPickerProps) {
  const [options, setOptions] = useState<ContentOption[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    ApiClient.get('/content?page=1&page_size=100')
      .then((data: { items?: ContentOption[] }) => {
        if (active) setOptions(Array.isArray(data?.items) ? data.items : [])
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'Your content could not be loaded.'))
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const handleSelect = async (id: string) => {
    if (!id) {
      onChange(null)
      return
    }
    const summary = options.find((option) => String(option.id) === id)
    if (!summary) return
    try {
      // The list omits the body; fetch the full item so the check runs on the real text.
      const detail: ContentOption = await ApiClient.get(`/content/${summary.id}`)
      onChange({ ...summary, body: detail.body ?? '' })
    } catch (err) {
      setError(errorMessage(err, 'That content could not be opened.'))
    }
  }

  if (loading) return <p className="text-sm text-gray-500">Loading your content…</p>
  if (error) return <p role="alert" className="text-sm text-red-700">{error}</p>

  if (options.length === 0) {
    return (
      <p className="text-sm text-gray-600">
        You have no content yet.{' '}
        <Link href="/dashboard/content/new" className="text-blue-600 hover:underline">
          Create a content item
        </Link>{' '}
        to check it.
      </p>
    )
  }

  return (
    <label className="block">
      <span className="block text-sm font-medium mb-1">{label}</span>
      <select
        className="w-full border rounded-md px-3 py-2"
        value={value ?? ''}
        onChange={(e) => handleSelect(e.target.value)}
      >
        <option value="">Select content…</option>
        {options.map((option) => (
          <option key={option.id} value={option.id}>
            {option.title} ({option.status})
          </option>
        ))}
      </select>
    </label>
  )
}
