import { render, screen } from '@testing-library/react'
import MonitoringPage from '@/app/dashboard/monitoring/page'
import { mockFetch, reply } from '@/test-utils'

const report = {
  metrics: { cpu_percent: 85, memory_percent: 64, disk_percent: 40, database_latency_ms: 4.2 },
  checks: [
    { name: 'Database', status: 'healthy', latency_ms: 4.2 },
    { name: 'Background jobs', status: 'degraded', pending: 3, running: 1, failed: 2 },
  ],
}
const alerts = [
  { id: 1, alert_type: 'database', severity: 'high', message: 'Database connection latency increased', created_at: '2026-10-17T09:55:00Z' },
  { id: 2, alert_type: 'cache', severity: 'medium', message: 'Cache hit rate below threshold', created_at: '2026-10-17T09:48:00Z' },
]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({ 'GET /system/health/checks': report, 'GET /system/alerts': [], ...extra })
}

describe('/dashboard/monitoring page', () => {
  it('shows a loading message before the live figures arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<MonitoringPage />)

    expect(screen.getByText('Loading metrics…')).toBeInTheDocument()
  })

  it('shows the live server figures and flags those over threshold', async () => {
    base()
    render(<MonitoringPage />)

    expect(await screen.findByText('85%')).toBeInTheDocument()
    expect(screen.getByText('85%').parentElement).toHaveTextContent('warning')
    expect(screen.getByText('64%')).toBeInTheDocument()
    expect(screen.getByText('4.2ms')).toBeInTheDocument()
    expect(screen.getAllByText('good')).toHaveLength(3)
  })

  it('reports each dependency check with its status and job counts', async () => {
    base()
    render(<MonitoringPage />)

    expect(await screen.findByText('Database')).toBeInTheDocument()
    expect(screen.getByText(/✓ Healthy · 4\.2ms/)).toBeInTheDocument()
    expect(screen.getByText(/⚠ Degraded · 3 pending · 1 running · 2 failed/)).toBeInTheDocument()
  })

  it('lists active alerts with the high-severity ones highlighted', async () => {
    const { container } = (() => {
      base({ 'GET /system/alerts': alerts })
      return render(<MonitoringPage />)
    })()

    expect(await screen.findByText('Database connection latency increased')).toBeInTheDocument()
    expect(screen.getByText('Cache hit rate below threshold')).toBeInTheDocument()
    expect(container.querySelector('.border-red-500')).not.toBeNull()
    expect(container.querySelector('.border-yellow-500')).not.toBeNull()
  })

  it('says when there are no active alerts', async () => {
    base()
    render(<MonitoringPage />)

    expect(await screen.findByText('No active alerts.')).toBeInTheDocument()
  })

  it('shows the server reason when the live figures cannot be loaded', async () => {
    base({ 'GET /system/health/checks': reply({ detail: 'Monitoring is unavailable' }, 503) })
    render(<MonitoringPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Monitoring is unavailable')
  })

  it('shows the server reason when the alerts cannot be loaded', async () => {
    base({ 'GET /system/alerts': reply({ detail: 'Admin access required' }, 403) })
    render(<MonitoringPage />)

    expect(await screen.findByText('Admin access required')).toBeInTheDocument()
  })
})
