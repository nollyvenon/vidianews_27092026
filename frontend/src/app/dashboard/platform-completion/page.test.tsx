import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import PlatformCompletionDashboard from '@/app/dashboard/platform-completion/page'
import { mockFetch, reply } from '@/test-utils'

const summary = {
  totalInteractions: 320,
  totalFollows: 45,
  totalComments: 88,
  totalMessages: 12,
  totalNotifications: 7,
  timestamp: '2026-10-01T00:00:00Z',
}
const platformStats = [
  { id: 1, metricName: 'Page views', metricValue: 1500.5, metricType: 'counter', createdAt: '2026-10-01T10:00:00Z' },
]
const notifications = [
  { id: 4, title: 'Maintenance', message: 'Tonight at 22:00', notificationType: 'system', createdAt: '2026-10-01T09:00:00Z' },
]

function baseRoutes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /platform/dashboard-summary': summary,
    'GET /platform/statistics': platformStats,
    'GET /platform/system/notifications': notifications,
    ...extra,
  })
}

describe('/dashboard/platform-completion page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows the social and system counters from the dashboard summary', async () => {
    baseRoutes()
    render(<PlatformCompletionDashboard />)

    expect(await screen.findByText('320')).toBeInTheDocument()
    expect(screen.getByText('Follows')).toBeInTheDocument()
    expect(screen.getByText('45')).toBeInTheDocument()
    expect(screen.getByText('88')).toBeInTheDocument()
    expect(screen.getByText('12')).toBeInTheDocument()
    expect(screen.getByText('7')).toBeInTheDocument()
  })

  it('shows zero counters while the summary has not arrived', () => {
    baseRoutes({ 'GET /platform/dashboard-summary': reply({ detail: 'down' }, 500) })
    render(<PlatformCompletionDashboard />)

    expect(screen.getAllByText('0')).toHaveLength(5)
  })

  it('lists the platform metrics with their value and type', async () => {
    baseRoutes()
    render(<PlatformCompletionDashboard />)

    expect(await screen.findByText('Page views')).toBeInTheDocument()
    expect(screen.getByText('1500.50')).toBeInTheDocument()
    expect(screen.getByText('counter')).toBeInTheDocument()
    expect(screen.getByText('Last 7 days metrics')).toBeInTheDocument()
  })

  it('reloads the statistics for the selected period', async () => {
    const fetchMock = baseRoutes()
    render(<PlatformCompletionDashboard />)
    await screen.findByText('Page views')

    fireEvent.click(screen.getByRole('button', { name: '30d' }))

    expect(await screen.findByText('Last 30 days metrics')).toBeInTheDocument()
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/platform/statistics?days=30'))).toBe(true)
    )
  })

  it('runs a content search and lists the results', async () => {
    const fetchMock = baseRoutes({
      'GET /platform/search': [
        { id: 9, contentId: 3, indexType: 'article', title: 'Flood update', content: 'Water levels rising', createdAt: '2026-10-01T10:00:00Z' },
      ],
    })
    render(<PlatformCompletionDashboard />)
    await screen.findByText('Page views')

    fireEvent.click(screen.getByRole('tab', { name: 'Search' }))
    fireEvent.change(screen.getByPlaceholderText('Search content...'), { target: { value: 'flood' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(await screen.findByRole('heading', { name: 'Flood update' })).toBeInTheDocument()
    expect(screen.getByText('article')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/platform/search?query=flood&limit=20'))).toBe(true)
  })

  it('does not search for a blank query', async () => {
    const fetchMock = baseRoutes()
    render(<PlatformCompletionDashboard />)
    await screen.findByText('Page views')
    fireEvent.click(screen.getByRole('tab', { name: 'Search' }))
    const before = fetchMock.mock.calls.length

    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(fetchMock.mock.calls.length).toBe(before)
  })

  it('logs a failed search', async () => {
    baseRoutes({ 'GET /platform/search': reply({ detail: 'down' }, 500) })
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<PlatformCompletionDashboard />)
    fireEvent.click(screen.getByRole('tab', { name: 'Search' }))
    fireEvent.change(screen.getByPlaceholderText('Search content...'), { target: { value: 'x' } })

    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Search failed:', expect.any(Error)))
  })

  it('lists system notifications and shows the empty state when there are none', async () => {
    baseRoutes()
    render(<PlatformCompletionDashboard />)
    fireEvent.click(screen.getByRole('tab', { name: 'Notifications' }))

    expect(await screen.findByText('Maintenance')).toBeInTheDocument()
    expect(screen.getByText('Tonight at 22:00')).toBeInTheDocument()
    expect(screen.getByText('system')).toBeInTheDocument()
  })

  it('shows the no-notifications message when the system has none', async () => {
    baseRoutes({ 'GET /platform/system/notifications': [] })
    render(<PlatformCompletionDashboard />)
    fireEvent.click(screen.getByRole('tab', { name: 'Notifications' }))

    expect(await screen.findByText('No notifications')).toBeInTheDocument()
  })

  it('logs the failure when the dashboard data cannot be requested', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<PlatformCompletionDashboard />)

    await waitFor(() =>
      expect(consoleError).toHaveBeenCalledWith('Failed to fetch dashboard data:', expect.any(Error))
    )
  })

  it('shows the social and admin area actions', async () => {
    baseRoutes()
    render(<PlatformCompletionDashboard />)
    await screen.findByText('Page views')

    fireEvent.click(screen.getByRole('tab', { name: 'Social' }))
    expect(screen.getByRole('button', { name: 'Moderate Comments' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'View Messages' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Security Settings' })).toBeInTheDocument()
  })
})
