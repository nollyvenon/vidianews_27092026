import { fireEvent, render, screen } from '@testing-library/react'
import APIVersionsPage from '@/app/dashboard/api-versions/page'
import { mockFetch, reply } from '@/test-utils'

const versions = [
  { id: 1, endpoint: '/api/content', version: 'v2', deprecated: false, sunset_date: null },
  { id: 2, endpoint: '/api/content', version: 'v1', deprecated: true, sunset_date: '2026-12-31T00:00:00+00:00' },
]

describe('/dashboard/api-versions page', () => {
  it('lists each registered version with its deprecation state and sunset date', async () => {
    mockFetch({ 'GET /versions': versions, 'GET /versions/migrations': [] })
    render(<APIVersionsPage />)

    expect(await screen.findByText('Version v2')).toBeInTheDocument()
    expect(screen.getByText('Active')).toBeInTheDocument()
    expect(screen.getByText('Deprecated')).toBeInTheDocument()
    expect(screen.getByText(/Sunset:/)).toBeInTheDocument()
    expect(screen.getAllByText('Usage: not tracked yet')).toHaveLength(2)
  })

  it('says when no versions are registered', async () => {
    mockFetch({ 'GET /versions': [], 'GET /versions/migrations': [] })
    render(<APIVersionsPage />)

    expect(await screen.findByText('No endpoint versions are registered yet.')).toBeInTheDocument()
  })

  it('shows the planned and completed migrations when asked', async () => {
    mockFetch({
      'GET /versions': versions,
      'GET /versions/migrations': [
        { id: 1, old_version: 'v1', new_version: 'v2', status: 'completed', executed_at: '2026-06-01T00:00:00+00:00' },
      ],
    })
    render(<APIVersionsPage />)
    await screen.findByText('Version v2')

    fireEvent.click(screen.getByRole('button', { name: 'View migrations' }))

    expect(await screen.findByText(/v1 → v2 · completed/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Hide migrations' })).toBeInTheDocument()
  })

  it('says when no migrations are planned', async () => {
    mockFetch({ 'GET /versions': versions, 'GET /versions/migrations': [] })
    render(<APIVersionsPage />)
    await screen.findByText('Version v2')

    fireEvent.click(screen.getByRole('button', { name: 'View migrations' }))

    expect(await screen.findByText('No migrations are planned.')).toBeInTheDocument()
  })

  it('shows the server reason when versions cannot be loaded', async () => {
    mockFetch({ 'GET /versions': reply({ detail: 'Versions offline' }, 503), 'GET /versions/migrations': [] })
    render(<APIVersionsPage />)

    expect(await screen.findByText('Versions offline')).toBeInTheDocument()
  })

  it('reports a migrations failure when the migrations are opened', async () => {
    mockFetch({ 'GET /versions': versions, 'GET /versions/migrations': reply({ detail: 'Migrations offline' }, 500) })
    render(<APIVersionsPage />)
    await screen.findByText('Version v2')

    fireEvent.click(screen.getByRole('button', { name: 'View migrations' }))

    expect(await screen.findByText('Migrations offline')).toBeInTheDocument()
  })

  it('uses generic messages when the requests fail without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<APIVersionsPage />)

    expect(await screen.findByText('API versions could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'View migrations' }))
    expect(await screen.findByText('Migrations could not be loaded.')).toBeInTheDocument()
  })

  it('shows loading placeholders while the requests are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<APIVersionsPage />)

    expect(screen.getByText('Loading versions…')).toBeInTheDocument()
  })
})
