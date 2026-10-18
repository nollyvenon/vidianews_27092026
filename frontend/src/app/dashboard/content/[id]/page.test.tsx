import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useParams, useRouter } from 'next/navigation'
import ContentDetailPage from '@/app/dashboard/content/[id]/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const item = {
  id: 1,
  title: 'Storm report',
  slug: 'storm-report',
  description: 'What happened',
  body: 'The storm arrived early.',
  content_type: 'article',
  status: 'draft',
  access_level: 'public',
  views_count: 12,
  likes_count: 3,
  comments_count: 2,
  shares_count: 1,
  published_at: null,
  created_at: '2026-10-01T10:00:00Z',
  updated_at: '2026-10-01T10:00:00Z',
}

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && (init?.method ?? 'GET') === method)
}

describe('/dashboard/content/[id] page', () => {
  let confirmSpy: jest.SpyInstance

  beforeEach(() => {
    ;(useParams as jest.Mock).mockReturnValue({ id: '1' })
    confirmSpy = jest.spyOn(window, 'confirm').mockReturnValue(true)
  })

  afterEach(() => {
    confirmSpy.mockRestore()
  })

  it('shows a loading message until the item arrives', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<ContentDetailPage />)

    expect(screen.getByText('Loading content…')).toBeInTheDocument()
  })

  it('renders the item with its type, status, body and engagement counts', async () => {
    mockFetch({ 'GET /content/1': item })
    renderWithQuery(<ContentDetailPage />)

    expect(await screen.findByRole('heading', { name: 'Storm report' })).toBeInTheDocument()
    expect(screen.getByText('What happened')).toBeInTheDocument()
    expect(screen.getByText('The storm arrived early.')).toBeInTheDocument()
    expect(screen.getByText('12 views · 3 likes · 2 comments · 1 shares')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Edit' })).toHaveAttribute('href', '/dashboard/content/1/edit')
  })

  it('says so when the item has no body text', async () => {
    mockFetch({ 'GET /content/1': { ...item, description: null, body: null } })
    renderWithQuery(<ContentDetailPage />)

    expect(await screen.findByText('No body text yet.')).toBeInTheDocument()
  })

  it('publishes a draft with its access level and reloads the item', async () => {
    const fetchMock = mockFetch({ 'GET /content/1': item, 'POST /content/1/publish': { ...item, status: 'published' } })
    renderWithQuery(<ContentDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Publish' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/content/1/publish')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/content/1/publish')![1].body as string)).toEqual({ access_level: 'public' })
  })

  it('archives the item', async () => {
    const fetchMock = mockFetch({ 'GET /content/1': item, 'POST /content/1/archive': {} })
    renderWithQuery(<ContentDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Archive' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/content/1/archive')).toBeDefined())
  })

  it('omits the publish action for a published item and keeps archive available', async () => {
    mockFetch({ 'GET /content/1': { ...item, status: 'published' } })
    renderWithQuery(<ContentDetailPage />)

    await screen.findByRole('heading', { name: 'Storm report' })
    expect(screen.queryByRole('button', { name: 'Publish' })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Archive' })).toBeInTheDocument()
  })

  it('hides the archive action for an archived item', async () => {
    mockFetch({ 'GET /content/1': { ...item, status: 'archived' } })
    renderWithQuery(<ContentDetailPage />)

    await screen.findByRole('heading', { name: 'Storm report' })
    expect(screen.queryByRole('button', { name: 'Archive' })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Publish' })).toBeInTheDocument()
  })

  it('deletes the item after confirmation and returns to the list', async () => {
    const fetchMock = mockFetch({ 'GET /content/1': item, 'DELETE /content/1': null })
    renderWithQuery(<ContentDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Delete' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/content'))
    expect(window.confirm).toHaveBeenCalledWith('Delete this content? This cannot be undone.')
    expect(requestTo(fetchMock, 'DELETE', '/content/1')).toBeDefined()
  })

  it('does nothing when the author cancels the delete confirmation', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(false)
    const fetchMock = mockFetch({ 'GET /content/1': item })
    renderWithQuery(<ContentDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Delete' }))

    expect(requestTo(fetchMock, 'DELETE', '/content/1')).toBeUndefined()
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('shows the server reason when an action fails and keeps the item visible', async () => {
    mockFetch({
      'GET /content/1': item,
      'POST /content/1/publish': reply({ detail: 'Publishing needs a body' }, 422),
    })
    renderWithQuery(<ContentDetailPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Publish' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Publishing needs a body')
    expect(screen.getByRole('heading', { name: 'Storm report' })).toBeInTheDocument()
  })

  it('shows the server reason when the item cannot be loaded', async () => {
    mockFetch({ 'GET /content/1': reply({ detail: 'Content not found' }, 404) })
    renderWithQuery(<ContentDetailPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Content not found')
  })
})
