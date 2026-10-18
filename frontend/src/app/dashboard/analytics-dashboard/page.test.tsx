import { render, screen } from '@testing-library/react'
import AnalyticsDashboardPage from '@/app/dashboard/analytics-dashboard/page'
import { mockFetch, reply } from '@/test-utils'

const revenue = [
  { date: '2026-10-01T00:00:00', total_revenue: 10.5, course_revenue: 0, membership_revenue: 0, transaction_count: 2, average_transaction: 5.25 },
  { date: '2026-10-02T00:00:00', total_revenue: 4.25, course_revenue: 0, membership_revenue: 0, transaction_count: 3, average_transaction: 1.41 },
]
const engagement = [
  { date: '2026-10-01T00:00:00', active_users: 30, new_users: 4 },
  { date: '2026-10-02T00:00:00', active_users: 42, new_users: 3 },
]
const summary = { days: 30, views: 1250, watch_hours: 12.5, subscribers: 48 }

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /analytics/revenue': revenue,
    'GET /analytics/engagement': engagement,
    'GET /analytics/summary': summary,
    ...extra,
  })
}

describe('/dashboard/analytics-dashboard page', () => {
  it('shows the views, watch hours and subscribers recorded for the organization', async () => {
    const fetchMock = base()
    render(<AnalyticsDashboardPage />)

    expect(await screen.findByText('1,250')).toBeInTheDocument()
    expect(screen.getByText('12.5')).toBeInTheDocument()
    expect(screen.getByText('48')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/analytics/summary?days=30'))).toBe(true)
  })

  it('sums the revenue and activity of the last 30 days from the backend', async () => {
    const fetchMock = base()
    render(<AnalyticsDashboardPage />)

    expect(await screen.findByText('$14.75')).toBeInTheDocument()
    expect(screen.getByText('5')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
    expect(screen.getByText('7')).toBeInTheDocument()

    const revenueCall = String(fetchMock.mock.calls.find(([url]) => String(url).includes('/analytics/revenue'))![0])
    expect(revenueCall).toMatch(/start_date=.+&end_date=/)
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/analytics/engagement?days=30'))).toBe(true)
  })

  it('shows zero revenue and a dash for active users when nothing is recorded', async () => {
    base({
      'GET /analytics/revenue': [],
      'GET /analytics/engagement': [],
      'GET /analytics/summary': { days: 30, views: 0, watch_hours: 0, subscribers: 0 },
    })
    render(<AnalyticsDashboardPage />)

    expect(await screen.findByText('$0.00')).toBeInTheDocument()
    expect(screen.getByText('—')).toBeInTheDocument()
  })

  it('shows the server reason when analytics cannot be loaded', async () => {
    base({
      'GET /analytics/revenue': reply({ detail: 'Your account has no workspace yet. Create a tenant first.' }, 422),
    })
    render(<AnalyticsDashboardPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no workspace yet.')
  })
})
