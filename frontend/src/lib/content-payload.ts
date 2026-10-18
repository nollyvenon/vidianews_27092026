import type { ContentValues } from '@/components/content/content-form'

/** Shape of GET /content/{id} that the editor reads back into form values. */
export interface ContentDetail {
  id: number
  title: string
  slug: string
  description: string | null
  body: string | null
  content_type: ContentValues['content_type']
  status: ContentValues['status']
  access_level: ContentValues['access_level']
  thumbnail_url: string | null
}

/** Form values for an existing item. */
export function toFormValues(detail: ContentDetail): ContentValues {
  return {
    title: detail.title,
    slug: detail.slug,
    description: detail.description ?? '',
    body: detail.body ?? '',
    content_type: detail.content_type,
    status: detail.status,
    access_level: detail.access_level,
    thumbnail_url: detail.thumbnail_url ?? '',
  }
}

/** Request body for POST /content and PUT /content/{id}; empty optional fields are sent as null. */
export function toContentPayload(values: ContentValues) {
  return {
    title: values.title.trim(),
    slug: values.slug.trim(),
    description: values.description.trim() || null,
    body: values.body || null,
    content_type: values.content_type,
    status: values.status,
    access_level: values.access_level,
    thumbnail_url: values.thumbnail_url.trim() || null,
  }
}
