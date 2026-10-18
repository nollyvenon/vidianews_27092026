import { contentService } from '@/services/content-service'
import { mockFetch, reply } from '@/test-utils'

const content = { id: 7, title: 'Story', slug: 'story', description: '', content_type: 'article', status: 'draft' }

describe('contentService', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    localStorage.setItem('token', 'svc-token')
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  describe('writes', () => {
    it('creates content with the stored token and returns the created record', async () => {
      const fetchMock = mockFetch({ 'POST /content': content })

      const created = await contentService.createContent({ title: 'Story', slug: 'story', content_type: 'article' })

      expect(created).toEqual(content)
      const [url, init] = fetchMock.mock.calls[0]
      expect(url).toBe('/api/v1/content')
      expect(init).toMatchObject({
        method: 'POST',
        headers: { Authorization: 'Bearer svc-token', 'Content-Type': 'application/json' },
      })
      expect(JSON.parse(init.body)).toEqual({ title: 'Story', slug: 'story', content_type: 'article' })
    })

    it('updates content by id with a partial payload', async () => {
      const fetchMock = mockFetch({ 'PUT /content/7': { ...content, title: 'New' } })

      const updated = await contentService.updateContent(7, { title: 'New' })

      expect(updated.title).toBe('New')
      expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/content/7')
      expect(fetchMock.mock.calls[0][1].method).toBe('PUT')
    })

    it('rejects when an update is refused', async () => {
      mockFetch({ 'PUT /content/7': reply({ detail: 'nope' }, 403) })

      await expect(contentService.updateContent(7, { title: 'x' })).rejects.toThrow('Failed to update content')
    })

    it('rejects when creation is refused', async () => {
      mockFetch({ 'POST /content': reply({ detail: 'nope' }, 422) })

      await expect(contentService.createContent({ title: 'x', slug: 'x', content_type: 'video' })).rejects.toThrow(
        'Failed to create content'
      )
    })

    it('deletes content and resolves without a body', async () => {
      const fetchMock = mockFetch({ 'DELETE /content/7': { ok: true } })

      await expect(contentService.deleteContent(7)).resolves.toBeUndefined()
      expect(fetchMock.mock.calls[0][1]).toMatchObject({ method: 'DELETE' })
    })

    it('rejects when deletion is refused', async () => {
      mockFetch({ 'DELETE /content/7': reply({ detail: 'locked' }, 423) })

      await expect(contentService.deleteContent(7)).rejects.toThrow('Failed to delete content')
    })

    it('publishes with the public access level by default', async () => {
      const fetchMock = mockFetch({ 'POST /content/7/publish': { ...content, status: 'published' } })

      const published = await contentService.publishContent(7)

      expect(published.status).toBe('published')
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ access_level: 'public' })
    })

    it('publishes with a chosen access level', async () => {
      const fetchMock = mockFetch({ 'POST /content/7/publish': content })

      await contentService.publishContent(7, 'members_only')

      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ access_level: 'members_only' })
    })

    it('rejects when publishing fails', async () => {
      mockFetch({ 'POST /content/7/publish': reply({ detail: 'x' }, 409) })

      await expect(contentService.publishContent(7)).rejects.toThrow('Failed to publish content')
    })

    it('schedules publication at an ISO timestamp', async () => {
      const when = new Date('2026-11-01T09:00:00Z')
      const fetchMock = mockFetch({ 'POST /content/7/schedule': { ...content, status: 'scheduled' } })

      const scheduled = await contentService.scheduleContent(7, when)

      expect(scheduled.status).toBe('scheduled')
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ scheduled_at: '2026-11-01T09:00:00.000Z' })
    })

    it('rejects when scheduling fails', async () => {
      mockFetch({ 'POST /content/7/schedule': reply({ detail: 'x' }, 400) })

      await expect(contentService.scheduleContent(7, new Date())).rejects.toThrow('Failed to schedule content')
    })

    it('archives content with an empty body', async () => {
      const fetchMock = mockFetch({ 'POST /content/7/archive': { ...content, status: 'archived' } })

      const archived = await contentService.archiveContent(7)

      expect(archived.status).toBe('archived')
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({})
    })

    it('rejects when archiving fails', async () => {
      mockFetch({ 'POST /content/7/archive': reply({ detail: 'x' }, 500) })

      await expect(contentService.archiveContent(7)).rejects.toThrow('Failed to archive content')
    })

    it('attaches a video source to content', async () => {
      const fetchMock = mockFetch({ 'POST /content/7/videos': { id: 3 } })

      await expect(contentService.addVideo(7, 'https://cdn.example.com/v.mp4')).resolves.toEqual({ id: 3 })
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ source_url: 'https://cdn.example.com/v.mp4' })
    })

    it('rejects when a video cannot be attached', async () => {
      mockFetch({ 'POST /content/7/videos': reply({ detail: 'x' }, 400) })

      await expect(contentService.addVideo(7, 'bad')).rejects.toThrow('Failed to add video')
    })

    it('attaches a media file to content', async () => {
      const fetchMock = mockFetch({ 'POST /content/7/media': { id: 4 } })

      await expect(contentService.addMediaFile(7, { name: 'cover.png' })).resolves.toEqual({ id: 4 })
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ name: 'cover.png' })
    })

    it('rejects when a media file cannot be attached', async () => {
      mockFetch({ 'POST /content/7/media': reply({ detail: 'x' }, 400) })

      await expect(contentService.addMediaFile(7, {})).rejects.toThrow('Failed to add media file')
    })

    it('records an engagement with the stored token', async () => {
      const fetchMock = mockFetch({ 'POST /content/7/engage': { ok: true } })

      await contentService.recordEngagement(7, 'like')

      expect(fetchMock.mock.calls[0][1]).toMatchObject({
        method: 'POST',
        headers: { Authorization: 'Bearer svc-token', 'Content-Type': 'application/json' },
      })
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ engagement_type: 'like' })
      expect(consoleError).not.toHaveBeenCalled()
    })

    it('logs, without throwing, when an engagement is refused', async () => {
      mockFetch({ 'POST /content/7/engage': reply({ detail: 'x' }, 401) })

      await expect(contentService.recordEngagement(7, 'share')).resolves.toBeUndefined()
      expect(consoleError).toHaveBeenCalledWith('Failed to record engagement')
    })

    it('runs bulk updates and bulk deletes over the given ids', async () => {
      const fetchMock = mockFetch({
        'POST /content/bulk/update': { updated: 2 },
        'POST /content/bulk/delete': { deleted: 2 },
      })

      await expect(contentService.bulkUpdateContent([1, 2], { status: 'archived' })).resolves.toEqual({ updated: 2 })
      expect(JSON.parse(fetchMock.mock.calls[0][1].body)).toEqual({ content_ids: [1, 2], status: 'archived' })

      await expect(contentService.bulkDeleteContent([1, 2])).resolves.toEqual({ deleted: 2 })
      expect(JSON.parse(fetchMock.mock.calls[1][1].body)).toEqual({ content_ids: [1, 2] })
    })

    it('rejects when a bulk update or bulk delete fails', async () => {
      mockFetch({
        'POST /content/bulk/update': reply({ detail: 'x' }, 500),
        'POST /content/bulk/delete': reply({ detail: 'x' }, 500),
      })

      await expect(contentService.bulkUpdateContent([1], {})).rejects.toThrow('Failed to bulk update')
      await expect(contentService.bulkDeleteContent([1])).rejects.toThrow('Failed to bulk delete')
    })
  })

  describe('reads', () => {
    it('fetches one item and its stats by id, and one by slug', async () => {
      const fetchMock = mockFetch({
        'GET /content/7': content,
        'GET /content/7/stats': { views: 10 },
        'GET /content/by-slug/story': content,
      })

      await expect(contentService.getContent(7)).resolves.toEqual(content)
      await expect(contentService.getContentStats(7)).resolves.toEqual({ views: 10 })
      await expect(contentService.getContentBySlug('story')).resolves.toEqual(content)
      expect(fetchMock.mock.calls[2][0]).toBe('/api/v1/content/by-slug/story')
    })

    it('rejects when a single item, its slug, or its stats cannot be fetched', async () => {
      mockFetch({
        'GET /content/7': reply({ detail: 'x' }, 404),
        'GET /content/by-slug/missing': reply({ detail: 'x' }, 404),
        'GET /content/7/stats': reply({ detail: 'x' }, 500),
      })

      await expect(contentService.getContent(7)).rejects.toThrow('Failed to fetch content')
      await expect(contentService.getContentBySlug('missing')).rejects.toThrow('Failed to fetch content')
      await expect(contentService.getContentStats(7)).rejects.toThrow('Failed to fetch stats')
    })

    it('builds the list query from only the filters that are set', async () => {
      const fetchMock = mockFetch({ 'GET /content': { items: [], total: 0 } })

      await contentService.listContent({ page: 2, page_size: 10, status: 'draft', content_type: 'video', category_id: 4 })
      await contentService.listContent()

      expect(fetchMock.mock.calls[0][0]).toBe(
        '/api/v1/content?page=2&page_size=10&status=draft&content_type=video&category_id=4'
      )
      expect(fetchMock.mock.calls[1][0]).toBe('/api/v1/content?')
    })

    it('rejects when the list cannot be fetched', async () => {
      mockFetch({ 'GET /content': reply({ detail: 'x' }, 500) })

      await expect(contentService.listContent()).rejects.toThrow('Failed to fetch content list')
    })

    it('searches with the query and an optional limit', async () => {
      const fetchMock = mockFetch({ 'GET /content/search': [content] })

      await expect(contentService.searchContent('storm', 5)).resolves.toEqual([content])
      await contentService.searchContent('storm')

      expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/content/search?query=storm&limit=5')
      expect(fetchMock.mock.calls[1][0]).toBe('/api/v1/content/search?query=storm')
    })

    it('rejects when a search fails', async () => {
      mockFetch({ 'GET /content/search': reply({ detail: 'x' }, 500) })

      await expect(contentService.searchContent('x')).rejects.toThrow('Failed to search content')
    })

    it('fetches featured content with an optional limit', async () => {
      const fetchMock = mockFetch({ 'GET /content/featured': [content] })

      await expect(contentService.getFeaturedContent(3)).resolves.toEqual([content])
      await contentService.getFeaturedContent()

      expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/content/featured?limit=3')
      expect(fetchMock.mock.calls[1][0]).toBe('/api/v1/content/featured?')
    })

    it('rejects when featured content cannot be fetched', async () => {
      mockFetch({ 'GET /content/featured': reply({ detail: 'x' }, 500) })

      await expect(contentService.getFeaturedContent()).rejects.toThrow('Failed to fetch featured content')
    })

    it('fetches trending content over an optional window and limit', async () => {
      const fetchMock = mockFetch({ 'GET /content/trending': [content] })

      await expect(contentService.getTrendingContent(7, 10)).resolves.toEqual([content])
      await contentService.getTrendingContent()

      expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/content/trending?days=7&limit=10')
      expect(fetchMock.mock.calls[1][0]).toBe('/api/v1/content/trending?')
    })

    it('rejects when trending content cannot be fetched', async () => {
      mockFetch({ 'GET /content/trending': reply({ detail: 'x' }, 500) })

      await expect(contentService.getTrendingContent()).rejects.toThrow('Failed to fetch trending content')
    })
  })
})
