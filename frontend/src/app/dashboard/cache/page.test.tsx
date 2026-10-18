import { fireEvent, screen, waitFor } from '@testing-library/react'
import CachePage from '@/app/dashboard/cache/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const stats = {
  total_entries: 120,
  hot_entries: 30,
  warm_entries: 50,
  cold_entries: 40,
  total_hits: 980,
  avg_hits_per_entry: 8.2,
  hit_rate: 0.982,
}
const policies = [
  { resource_type: 'content', cache_type: 'redis', ttl_seconds: 3600, max_size_mb: 100, is_active: true, hits: 90, misses: 10, hit_rate: 90 },
]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /cache/stats/summary': stats,
    'GET /cache/policies': policies,
    ...extra,
  })
}

function bodyOf(fetchMock: jest.Mock, method: string, suffix: string) {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
  return JSON.parse(call![1].body as string)
}

describe('/dashboard/cache page', () => {
  it('shows a loading message until the statistics arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<CachePage />)

    expect(screen.getByText('Loading cache statistics…')).toBeInTheDocument()
  })

  it('shows the cache statistics from the backend', async () => {
    base()
    renderWithQuery(<CachePage />)

    expect(await screen.findByText('98.2%')).toBeInTheDocument()
    expect(screen.getByText('120')).toBeInTheDocument()
    expect(screen.getByText('980')).toBeInTheDocument()
    expect(screen.getByText('8.2')).toBeInTheDocument()
  })

  it('lists each policy with its hit rate, type, TTL and traffic', async () => {
    base()
    renderWithQuery(<CachePage />)

    expect(await screen.findByText('content')).toBeInTheDocument()
    expect(screen.getByText('Type: redis | TTL: 3600s | Max: 100 MB | Active')).toBeInTheDocument()
    expect(screen.getByText('90.0%')).toBeInTheDocument()
    expect(screen.getByText('90 hits')).toBeInTheDocument()
  })

  it('edits a policy and saves its new values', async () => {
    const fetchMock = base({ 'PUT /cache/policies/content': { ...policies[0], ttl_seconds: 600 } })
    renderWithQuery(<CachePage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Edit policy' }))
    fireEvent.change(screen.getByLabelText('TTL (seconds)'), { target: { value: '600' } })
    fireEvent.change(screen.getByLabelText('Cache type'), { target: { value: 'local' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save policy' }))

    await waitFor(() =>
      expect(bodyOf(fetchMock, 'PUT', '/cache/policies/content')).toEqual({
        cache_type: 'local',
        ttl_seconds: 600,
        max_size_mb: 100,
        is_active: true,
      }),
    )
  })

  it('shows the server reason when a policy cannot be saved', async () => {
    base({ 'PUT /cache/policies/content': reply({ detail: 'Only administrators can change cache policies' }, 403) })
    renderWithQuery(<CachePage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Edit policy' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save policy' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Only administrators can change cache policies')
  })

  it('flushes the cache and reports how many entries were removed', async () => {
    const fetchMock = base({ 'POST /cache/flush': { removed: 120 } })
    renderWithQuery(<CachePage />)
    await screen.findByText('98.2%')

    fireEvent.click(screen.getByRole('button', { name: 'Flush All Cache' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Removed 120 cache entries.')
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/cache/flush') && init?.method === 'POST')).toBe(true)
  })

  it('optimizes the cache and reports the expired entries removed and those that remain', async () => {
    base({ 'POST /cache/optimize': { removed: 7, remaining: 113 } })
    renderWithQuery(<CachePage />)
    await screen.findByText('98.2%')

    fireEvent.click(screen.getByRole('button', { name: 'Optimize Cache' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Removed 7 expired entries; 113 remain.')
  })

  it('shows the server reason when a cache action is refused', async () => {
    base({ 'POST /cache/flush': reply({ detail: 'Admin access required' }, 403) })
    renderWithQuery(<CachePage />)
    await screen.findByText('98.2%')

    fireEvent.click(screen.getByRole('button', { name: 'Flush All Cache' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Admin access required')
  })

  it('says when no policies exist and shows the statistics error', async () => {
    mockFetch({
      'GET /cache/stats/summary': reply({ detail: 'Cache is offline' }, 503),
      'GET /cache/policies': [],
    })
    renderWithQuery(<CachePage />)

    expect(await screen.findByText('No cache policies are defined yet.')).toBeInTheDocument()
    expect(await screen.findByText('Cache is offline')).toBeInTheDocument()
  })
})
