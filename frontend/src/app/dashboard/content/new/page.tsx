'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { ContentForm } from '@/components/content/content-form'
import { ApiClient } from '@/lib/api-client'
import { toContentPayload } from '@/lib/content-payload'

export default function NewContentPage() {
  const router = useRouter()

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">New content</h1>
        <Link href="/dashboard/content" className="text-blue-600 hover:underline">
          Back to content
        </Link>
      </div>
      <ContentForm
        submitLabel="Create content"
        onSubmit={async (values) => {
          const created = await ApiClient.post('/content', toContentPayload(values))
          router.push(`/dashboard/content/${created.id}`)
        }}
      />
    </div>
  )
}
