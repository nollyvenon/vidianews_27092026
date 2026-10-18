import { render, screen } from '@testing-library/react'
import AnalyticsPage from '@/app/dashboard/analytics/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/analytics page', () => {
  it('shows a loading message until both analytics requests finish', async () => {
    mockFetch({ 'GET /analytics/revenue': [], 'GET /analytics/engagement': [] })
    render(<AnalyticsPage />)

    expect(screen.getByText('Loading analytics...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Analytics Dashboard' })).toBeInTheDocument()
  })

  it('totals revenue and uses the latest active-user count from the API', async () => {
    mockFetch({
      'GET /analytics/revenue': [{ total_revenue: 100 }, { total_revenue: 50.5 }],
      'GET /analytics/engagement': [{ active_users: 5 }, { active_users: 42 }],
    })
    render(<AnalyticsPage />)

    expect(await screen.findByRole('heading', { name: 'Analytics Dashboard' })).toBeInTheDocument()
    expect(screen.getByText('$150.50')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
    expect(screen.getByText('1250')).toBeInTheDocument()
    expect(screen.getByText('342')).toBeInTheDocument()
  })

  it('shows zero revenue and active users when the API returns no usable rows', async () => {
    mockFetch({
      'GET /analytics/revenue': reply({ detail: 'unavailable' }, 500),
      'GET /analytics/engagement': [],
    })
    render(<AnalyticsPage />)

    expect(await screen.findByRole('heading', { name: 'Analytics Dashboard' })).toBeInTheDocument()
    expect(screen.getByText('$0.00')).toBeInTheDocument()
    expect(screen.getByText('0')).toBeInTheDocument()
  })

  it('treats unreadable response bodies as empty data', async () => {
    global.fetch = jest.fn(async () => ({
      json: () => Promise.reject(new SyntaxError('Unexpected token')),
    })) as unknown as typeof fetch
    render(<AnalyticsPage />)

    expect(await screen.findByRole('heading', { name: 'Analytics Dashboard' })).toBeInTheDocument()
    expect(screen.getByText('$0.00')).toBeInTheDocument()
  })

  it('still renders the dashboard with zero metrics when the requests cannot be made', async () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<AnalyticsPage />)

    expect(await screen.findByRole('heading', { name: 'Analytics Dashboard' })).toBeInTheDocument()
    expect(screen.getByText('$0.00')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to load analytics', expect.any(Error))
    consoleError.mockRestore()
  })
})
