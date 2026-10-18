'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useParams, useRouter } from 'next/navigation'
import { ContentForm, ContentValues } from '@/components/content/content-form'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'
import { ContentDetail, toContentPayload, toFormValues } from '@/lib/content-payload'

export default function EditContentPage() {
  const { id } = useParams<{ id: string }>()
  const router = useRouter()
  const [initial, setInitial] = useState<ContentValues | null>(null)
  const [loadError, setLoadError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    ApiClient.get(`/content/${id}`)
      .then((detail: ContentDetail) => {
        if (active) setInitial(toFormValues(detail))
      })
      .catch((err) => {
        if (active) setLoadError(errorMessage(err, 'This content could not be loaded.'))
      })
    return () => {
      active = false
    }
  }, [id])

  if (loadError) return <p role="alert" className="text-red-700">{loadError}</p>
  if (!initial) return <p className="text-gray-600">Loading content…</p>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Edit content</h1>
        <Link href={`/dashboard/content/${id}`} className="text-blue-600 hover:underline">
          Back to content
        </Link>
      </div>
      <ContentForm
        initial={initial}
        submitLabel="Save changes"
        onSubmit={async (values) => {
          await ApiClient.put(`/content/${id}`, toContentPayload(values))
          router.push(`/dashboard/content/${id}`)
        }}
      />
    </div>
  )
}
