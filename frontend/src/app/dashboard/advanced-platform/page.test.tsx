import { fireEvent, render, screen } from '@testing-library/react'
import AdvancedPlatformPage from '@/app/dashboard/advanced-platform/page'
import { mockFetch, reply } from '@/test-utils'

const health = {
  metrics: { cpu_percent: 12.5, memory_percent: 40, disk_percent: 55, database_latency_ms: 3.2 },
  checks: [
    { name: 'Database', status: 'healthy', latency_ms: 3.2 },
    { name: 'Background jobs', status: 'degraded', pending: 4, running: 1, failed: 2 },
  ],
}

const jobs = [
  { id: 1, job_type: 'email_notification', status: 'pending', priority: 2, user_id: null, created_at: '2026-10-18T09:00:00Z' },
  { id: 2, job_type: 'data_export', status: 'pending', priority: 1, user_id: null, created_at: '2026-10-18T09:05:00Z' },
]

const pipelines = [
  { id: 1, name: 'User Sync', source_type: 'database', destination_type: 'warehouse', status: 'active', is_active: true, failure_count: 0, last_run: '2026-10-18T08:00:00Z' },
  { id: 2, name: 'Event Pipeline', source_type: 'events', destination_type: 'analytics', status: 'draft', is_active: false, failure_count: 3, last_run: null },
]

const usage = [
  { id: 1, endpoint: '/users', method: 'GET', call_count: 12345, error_count: 23, average_response_time_ms: 41.5 },
  { id: 2, endpoint: '/content', method: 'GET', call_count: 54321, error_count: 12, average_response_time_ms: 18 },
]

function workingRoutes(extra: Record<string, unknown> = {}) {
  return {
    'GET /websocket/presence': { online: 234, idle: 7 },
    'GET /system/health/checks': health,
    'GET /jobs/pending': jobs,
    'GET /pipelines/': pipelines,
    'GET /cache-summary': { entries: 42, total_hits: 1078, memory_usage_mb: 2.5 },
    'GET /api-docs/usage': usage,
    ...extra,
  }
}

describe('/dashboard/advanced-platform page', () => {
  it('shows the live statistics and opens on the overview tab', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedPlatformPage />)

    expect(screen.getByRole('heading', { name: 'Advanced Platform' })).toBeInTheDocument()
    expect(screen.getByText('Active WebSockets')).toBeInTheDocument()
    expect(await screen.findByText('234')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: 'Overview' })).toHaveAttribute('aria-selected', 'true')
    expect(await screen.findByText('12.5%')).toBeInTheDocument()
    expect(screen.getByText('3.2ms')).toBeInTheDocument()
  })

  it('shows the state of each health check', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedPlatformPage />)

    expect(await screen.findByText('Background jobs')).toBeInTheDocument()
    expect(screen.getByText('degraded')).toHaveClass('bg-yellow-100')
    expect(screen.getByText('healthy')).toHaveClass('bg-green-100')
  })

  it('lists the pending background jobs with their priority', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Jobs' }))

    expect(await screen.findByText('email_notification')).toBeInTheDocument()
    expect(screen.getByText(/Priority 2/)).toBeInTheDocument()
    expect(screen.getAllByText('pending')).toHaveLength(2)
  })

  it('says when no jobs are waiting', async () => {
    mockFetch(workingRoutes({ 'GET /jobs/pending': [] }))
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Jobs' }))

    expect(await screen.findByText('No jobs are waiting.')).toBeInTheDocument()
  })

  it('lists the data pipelines with their routes, last run and failures', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Pipelines' }))

    expect(await screen.findByText('User Sync')).toBeInTheDocument()
    expect(screen.getByText(/database → warehouse/)).toBeInTheDocument()
    expect(screen.getByText(/· never run · 3 failures/)).toBeInTheDocument()
    expect(screen.getByText('active')).toHaveClass('bg-green-100')
    expect(screen.getByText('draft')).toHaveClass('bg-gray-100')
  })

  it('says when no pipelines exist', async () => {
    mockFetch(workingRoutes({ 'GET /pipelines/': [] }))
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Pipelines' }))

    expect(await screen.findByText('No pipelines have been created.')).toBeInTheDocument()
  })

  it('shows the cached entries, the hits they served and their memory', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Cache' }))

    expect(await screen.findByText('Hits Served')).toBeInTheDocument()
    expect(screen.getByText('1,078')).toBeInTheDocument()
    expect(screen.getByText('2.50MB')).toBeInTheDocument()
  })

  it('shows API endpoint usage with calls, errors and average response time', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'API' }))

    expect(await screen.findByText('GET /users')).toBeInTheDocument()
    expect(screen.getByText('12,345 calls · 23 errors · 41.5ms avg')).toBeInTheDocument()
    expect(screen.getByText('54,321 calls · 12 errors · 18ms avg')).toBeInTheDocument()
  })

  it('says when no API calls have been measured', async () => {
    mockFetch(workingRoutes({ 'GET /api-docs/usage': [] }))
    render(<AdvancedPlatformPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'API' }))

    expect(await screen.findByText('No API calls have been measured yet.')).toBeInTheDocument()
  })

  it('reports each failed source in its own section, without hiding the others', async () => {
    mockFetch(workingRoutes({
      'GET /websocket/presence': reply({ detail: 'Connections offline' }, 503),
      'GET /system/health/checks': reply({ detail: 'Health offline' }, 500),
      'GET /jobs/pending': reply({ detail: 'Jobs offline' }, 500),
    }))
    render(<AdvancedPlatformPage />)

    expect(await screen.findByText('Connections offline')).toBeInTheDocument()
    expect(screen.getByText('Health offline')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Jobs' }))
    expect(await screen.findByText('Jobs offline')).toBeInTheDocument()
  })

  it('uses generic messages when the requests fail without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<AdvancedPlatformPage />)

    expect(await screen.findByText('Connection figures could not be loaded.')).toBeInTheDocument()
    expect(await screen.findByText('Health figures could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Cache' }))
    expect(await screen.findByText('Cache figures could not be loaded.')).toBeInTheDocument()
  })

  it('shows loading placeholders while the figures are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<AdvancedPlatformPage />)

    expect(screen.getAllByText('—').length).toBeGreaterThanOrEqual(4)
  })
})
