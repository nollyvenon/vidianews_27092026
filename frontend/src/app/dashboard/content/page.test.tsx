import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import ContentPage from '@/app/dashboard/content/page'
import * as toastModule from '@/hooks/use-toast'
import { mockFetch, reply } from '@/test-utils'

// The toast is asserted through the mocked hook; the real Toaster is not rendered in page tests.
jest.mock('@/hooks/use-toast', () => {
  const toast = jest.fn()
  return { __toast: toast, useToast: () => ({ toast, dismiss: jest.fn(), toasts: [] }) }
})

const item = (overrides: Record<string, unknown> = {}) => ({
  id: 1,
  title: 'Evening bulletin',
  slug: 'evening-bulletin',
  description: 'Top stories tonight',
  content_type: 'video',
  status: 'published',
  views_count: 1200,
  likes_count: 34,
  created_at: '2026-10-01T10:00:00Z',
  published_at: '2026-10-02T10:00:00Z',
  thumbnail_url: null,
  ...overrides,
})

function toastMock(): jest.Mock {
  return (toastModule as unknown as { __toast: jest.Mock }).__toast
}

describe('/dashboard/content page', () => {
  beforeEach(() => {
    localStorage.setItem('token', 'content-token')
    jest.spyOn(window, 'confirm').mockReturnValue(true)
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('shows a spinner while loading, then the content with badges and engagement', async () => {
    mockFetch({ 'GET /content': { items: [item()], total: 1 } })
    const { container } = render(<ContentPage />)

    expect(container.querySelector('.animate-spin')).not.toBeNull()
    expect(await screen.findByRole('heading', { name: 'Evening bulletin' })).toBeInTheDocument()
    expect(screen.getByText('Top stories tonight')).toBeInTheDocument()
    expect(screen.getByText('published')).toHaveClass('bg-green-100')
    expect(screen.getByText('1200')).toBeInTheDocument()
    expect(screen.getByText('❤️ 34')).toBeInTheDocument()
    expect(screen.getByText('🎥')).toBeInTheDocument()
  })

  it('sends the stored token and the paging parameters with each list request', async () => {
    const fetchMock = mockFetch({ 'GET /content': { items: [item()], total: 1 } })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    const [url, init] = fetchMock.mock.calls[0]
    expect(String(url)).toContain('page=1')
    expect(String(url)).toContain('page_size=20')
    expect(init.headers).toMatchObject({ Authorization: 'Bearer content-token' })
  })

  it('shows an image thumbnail when the item has one', async () => {
    mockFetch({ 'GET /content': { items: [item({ thumbnail_url: 'https://cdn.example.com/t.jpg' })], total: 1 } })
    render(<ContentPage />)

    expect(await screen.findByRole('img', { name: 'Evening bulletin' })).toHaveAttribute('src', expect.stringContaining('t.jpg'))
  })

  it('shows the publication date badge only for published items', async () => {
    mockFetch({
      'GET /content': {
        items: [item(), item({ id: 2, title: 'Draft piece', status: 'draft', published_at: null, content_type: 'newsletter' })],
        total: 2,
      },
    })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Draft piece' })

    expect(screen.getByText('draft')).toHaveClass('bg-gray-100')
    expect(screen.getByText('📧')).toBeInTheDocument()
    expect(screen.getAllByText(new Date('2026-10-02T10:00:00Z').toLocaleDateString())).toHaveLength(1)
  })

  it('shows the empty state with a call to create content', async () => {
    mockFetch({ 'GET /content': { items: [], total: 0 } })
    render(<ContentPage />)

    expect(await screen.findByText('No content found')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Create First Content' })).toBeInTheDocument()
  })

  it('reports a failed load through a destructive toast', async () => {
    mockFetch({ 'GET /content': reply({ detail: 'down' }, 500) })
    render(<ContentPage />)

    await waitFor(() =>
      expect(toastMock()).toHaveBeenCalledWith({
        title: 'Error',
        description: 'Failed to fetch content',
        variant: 'destructive',
      })
    )
  })

  it('filters by status and by type, going back to the first page each time', async () => {
    const fetchMock = mockFetch({ 'GET /content': { items: [item()], total: 1 } })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    const [statusSelect, typeSelect] = screen.getAllByRole('combobox')
    fireEvent.change(statusSelect, { target: { value: 'archived' } })
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes('status=archived'))).toBe(true))

    fireEvent.change(typeSelect, { target: { value: 'article' } })
    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes('content_type=article'))).toBe(true))
    const lastCall = fetchMock.mock.calls[fetchMock.mock.calls.length - 1]
    expect(String(lastCall[0])).toContain('page=1')
  })

  it('pages forward and back through the results', async () => {
    const fetchMock = mockFetch({ 'GET /content': { items: [item()], total: 25 } })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    expect(screen.getByText('Page 1 of 2')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Previous' })).toBeDisabled()

    fireEvent.click(screen.getByRole('button', { name: 'Next' }))
    await waitFor(() => expect(screen.getByText('Page 2 of 2')).toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Next' })).toBeDisabled()
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('page=2'))).toBe(true)

    fireEvent.click(screen.getByRole('button', { name: 'Previous' }))
    await waitFor(() => expect(screen.getByText('Page 1 of 2')).toBeInTheDocument())
  })

  it('searches by title and shows the matching items', async () => {
    const fetchMock = mockFetch({
      'GET /content': { items: [item()], total: 1 },
      'GET /content/search': [item({ id: 9, title: 'Storm coverage' })],
    })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    fireEvent.change(screen.getByPlaceholderText('Search content by title...'), { target: { value: 'storm' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(await screen.findByRole('heading', { name: 'Storm coverage' })).toBeInTheDocument()
    const lastCall = fetchMock.mock.calls[fetchMock.mock.calls.length - 1]
    expect(String(lastCall[0])).toMatch(/content\/search\?query=storm$/)
  })

  it('reloads the full list when the search box is cleared', async () => {
    const fetchMock = mockFetch({ 'GET /content': { items: [item()], total: 1 } })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })
    const before = fetchMock.mock.calls.length

    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() => expect(fetchMock.mock.calls.length).toBeGreaterThan(before))
  })

  it('reports a failed search through a toast', async () => {
    mockFetch({
      'GET /content': { items: [item()], total: 1 },
      'GET /content/search': reply({ detail: 'down' }, 500),
    })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    fireEvent.change(screen.getByPlaceholderText('Search content by title...'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() =>
      expect(toastMock()).toHaveBeenCalledWith({ title: 'Error', description: 'Search failed', variant: 'destructive' })
    )
  })

  it('deletes an item after confirmation, announces it and reloads the list', async () => {
    const fetchMock = mockFetch({
      'GET /content': { items: [item()], total: 1 },
      'DELETE /content/1': { ok: true },
    })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    await waitFor(() =>
      expect(toastMock()).toHaveBeenCalledWith({ title: 'Success', description: 'Content deleted successfully' })
    )
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/content/1') && init?.method === 'DELETE')).toBe(true)
  })

  it('does not delete when the confirmation is declined', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(false)
    const fetchMock = mockFetch({ 'GET /content': { items: [item()], total: 1 } })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === 'DELETE')).toHaveLength(0)
  })

  it('reports a failed delete through a toast', async () => {
    mockFetch({
      'GET /content': { items: [item()], total: 1 },
      'DELETE /content/1': reply({ detail: 'locked' }, 423),
    })
    render(<ContentPage />)
    await screen.findByRole('heading', { name: 'Evening bulletin' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    await waitFor(() =>
      expect(toastMock()).toHaveBeenCalledWith({
        title: 'Error',
        description: 'Failed to delete content',
        variant: 'destructive',
      })
    )
  })

  it('shows the icon and colour for each content type and status', async () => {
    mockFetch({
      'GET /content': {
        items: [
          item({ id: 1, title: 'Scheduled post', status: 'scheduled', content_type: 'article' }),
          item({ id: 2, title: 'Archived post', status: 'archived', content_type: 'blog_post' }),
          item({ id: 3, title: 'Unknown state', status: 'paused', content_type: 'unknown_type' }),
        ],
        total: 3,
      },
    })
    render(<ContentPage />)

    expect(await screen.findByRole('heading', { name: 'Scheduled post' })).toBeInTheDocument()
    expect(screen.getByText('scheduled')).toHaveClass('bg-blue-100')
    expect(screen.getByText('archived')).toHaveClass('bg-red-100')
    expect(screen.getByText('paused')).toHaveClass('bg-gray-100')
    expect(screen.getByText('📝')).toBeInTheDocument()
    expect(screen.getAllByText('📄')).toHaveLength(2)
  })
})
