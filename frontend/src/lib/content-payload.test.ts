import { ContentValues } from '@/components/content/content-form'
import { ContentDetail, toContentPayload, toFormValues } from '@/lib/content-payload'

describe('toFormValues', () => {
  it('maps a full content item onto form values', () => {
    const detail: ContentDetail = {
      id: 7,
      title: 'Storm report',
      slug: 'storm-report',
      description: 'Summary',
      body: 'The storm arrived early.',
      content_type: 'article',
      status: 'published',
      access_level: 'members_only',
      thumbnail_url: 'https://cdn.example.com/a.png',
    }

    expect(toFormValues(detail)).toEqual({
      title: 'Storm report',
      slug: 'storm-report',
      description: 'Summary',
      body: 'The storm arrived early.',
      content_type: 'article',
      status: 'published',
      access_level: 'members_only',
      thumbnail_url: 'https://cdn.example.com/a.png',
    })
  })

  it('turns null optional fields into empty strings', () => {
    const values = toFormValues({
      id: 8,
      title: 'Draft',
      slug: 'draft',
      description: null,
      body: null,
      content_type: 'video',
      status: 'draft',
      access_level: 'public',
      thumbnail_url: null,
    })

    expect(values.description).toBe('')
    expect(values.body).toBe('')
    expect(values.thumbnail_url).toBe('')
  })
})

describe('toContentPayload', () => {
  const base: ContentValues = {
    title: '  Storm report  ',
    slug: ' storm-report ',
    description: '  ',
    body: 'Body text',
    content_type: 'newsletter',
    status: 'scheduled',
    access_level: 'premium',
    thumbnail_url: ' https://cdn.example.com/a.png ',
  }

  it('trims text fields and keeps the enumerated choices', () => {
    expect(toContentPayload(base)).toEqual({
      title: 'Storm report',
      slug: 'storm-report',
      description: null,
      body: 'Body text',
      content_type: 'newsletter',
      status: 'scheduled',
      access_level: 'premium',
      thumbnail_url: 'https://cdn.example.com/a.png',
    })
  })

  it('sends empty optional fields as null', () => {
    const payload = toContentPayload({ ...base, description: '', body: '', thumbnail_url: '   ' })

    expect(payload.description).toBeNull()
    expect(payload.body).toBeNull()
    expect(payload.thumbnail_url).toBeNull()
  })
})
