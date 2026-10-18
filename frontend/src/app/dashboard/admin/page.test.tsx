import { render, screen } from '@testing-library/react'
import AdminPage from '@/app/dashboard/admin/page'
import { mockFetch } from '@/test-utils'

describe('/dashboard/admin page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state until the admin data arrives', async () => {
    mockFetch({ 'GET /admin/logs': [], 'GET /system/alerts': [] })
    render(<AdminPage />)

    expect(screen.getByText('Loading admin dashboard...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Admin Dashboard' })).toBeInTheDocument()
  })

  it('lists system alerts with their severity', async () => {
    mockFetch({
      'GET /admin/logs': [],
      'GET /system/alerts': [
        { id: 1, alert_type: 'Disk', message: 'Disk almost full', severity: 'critical' },
        { id: 2, alert_type: 'Latency', message: 'Slow responses', severity: 'warning' },
      ],
    })
    render(<AdminPage />)

    expect(await screen.findByText('Disk almost full')).toBeInTheDocument()
    expect(screen.getByText('CRITICAL')).toHaveClass('text-red-600')
    expect(screen.getByText('WARNING')).toHaveClass('text-yellow-600')
  })

  it('hides the alerts panel when there are no alerts', async () => {
    mockFetch({ 'GET /admin/logs': [], 'GET /system/alerts': [] })
    render(<AdminPage />)

    await screen.findByRole('heading', { name: 'Admin Dashboard' })
    expect(screen.queryByRole('heading', { name: 'System Alerts' })).not.toBeInTheDocument()
  })

  it('shows the 10 most recent admin actions', async () => {
    const logs = Array.from({ length: 12 }, (_, i) => ({
      id: i + 1,
      admin_id: 1,
      action: `ACTION_${i + 1}`,
      resource_type: 'user',
      created_at: '2026-10-01T10:00:00Z',
    }))
    mockFetch({ 'GET /admin/logs': logs, 'GET /system/alerts': [] })
    render(<AdminPage />)

    expect(await screen.findByText('ACTION_10')).toBeInTheDocument()
    expect(screen.queryByText('ACTION_11')).not.toBeInTheDocument()
  })

  it('ignores responses that are not lists', async () => {
    mockFetch({ 'GET /admin/logs': { detail: 'forbidden' }, 'GET /system/alerts': { detail: 'forbidden' } })
    render(<AdminPage />)

    expect(await screen.findByRole('heading', { name: 'Admin Dashboard' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'System Alerts' })).not.toBeInTheDocument()
  })

  it('shows the dashboard with empty panels when the requests fail', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<AdminPage />)

    expect(await screen.findByRole('heading', { name: 'Admin Dashboard' })).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to load admin dashboard', expect.any(Error))
  })

  it('offers the quick actions and system status figures', async () => {
    mockFetch({ 'GET /admin/logs': [], 'GET /system/alerts': [] })
    render(<AdminPage />)
    await screen.findByRole('heading', { name: 'Admin Dashboard' })

    expect(screen.getByRole('button', { name: 'Suspend User' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Generate Report' })).toBeInTheDocument()
    expect(screen.getByText('45.5%')).toBeInTheDocument()
    expect(screen.getByText('99.8%')).toHaveClass('text-green-600')
  })
})
