import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import AIMonitoringPage from '@/app/dashboard/ai/monitoring/page'
import { mockFetch, reply } from '@/test-utils'

const usage = { period_days: 30, total: 1500, average: 0.5, count: 3 }
const daily = [
  { date: '2026-10-11', total: 0 },
  { date: '2026-10-12', total: 300 },
  { date: '2026-10-13', total: 0 },
  { date: '2026-10-14', total: 0 },
  { date: '2026-10-15', total: 0 },
  { date: '2026-10-16', total: 600 },
  { date: '2026-10-17', total: 150 },
]

describe('/dashboard/ai/monitoring page', () => {
  it('shows a loading state until usage statistics arrive', async () => {
    mockFetch({ 'GET /ai/metrics/usage': usage, 'GET /ai/metrics/usage/daily': daily, 'GET /ai/alerts': [] })
    render(<AIMonitoringPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'AI Monitoring' })).toBeInTheDocument()
  })

  it('shows token totals, average cost, call count and period', async () => {
    mockFetch({ 'GET /ai/metrics/usage': usage, 'GET /ai/metrics/usage/daily': daily, 'GET /ai/alerts': [] })
    render(<AIMonitoringPage />)

    expect(await screen.findByText('1500')).toBeInTheDocument()
    expect(screen.getByText('$0.50')).toBeInTheDocument()
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText('30d')).toBeInTheDocument()
  })

  it('draws one bar per day, scaled to the busiest day, with the recorded tokens as tooltips', async () => {
    mockFetch({ 'GET /ai/metrics/usage': usage, 'GET /ai/metrics/usage/daily': daily, 'GET /ai/alerts': [] })
    const { container } = render(<AIMonitoringPage />)
    await screen.findByRole('heading', { name: 'AI Monitoring' })

    const bars = container.querySelectorAll('[title$="tokens"]')
    expect(bars).toHaveLength(7)
    expect(bars[5]).toHaveStyle({ height: '100%' })
    expect(bars[1]).toHaveStyle({ height: '50%' })
    expect(bars[0]).toHaveStyle({ height: '0%' })
    expect(bars[5]).toHaveAttribute('title', '2026-10-16: 600 tokens')
  })

  it('says so when there is no usage to chart', async () => {
    mockFetch({ 'GET /ai/metrics/usage': { ...usage, total: 0, count: 0 }, 'GET /ai/metrics/usage/daily': [], 'GET /ai/alerts': [] })
    render(<AIMonitoringPage />)

    expect(await screen.findByText('No usage recorded yet.')).toBeInTheDocument()
  })

  it('shows zero-height bars when every day is empty', async () => {
    const empty = daily.map((point) => ({ ...point, total: 0 }))
    mockFetch({ 'GET /ai/metrics/usage': usage, 'GET /ai/metrics/usage/daily': empty, 'GET /ai/alerts': [] })
    const { container } = render(<AIMonitoringPage />)
    await screen.findByRole('heading', { name: 'AI Monitoring' })

    const bars = container.querySelectorAll('[title$="tokens"]')
    expect(bars[0]).toHaveStyle({ height: '0%' })
  })

  it('lists the configured cost alerts', async () => {
    mockFetch({
      'GET /ai/metrics/usage': usage,
      'GET /ai/metrics/usage/daily': daily,
      'GET /ai/alerts': [{ id: 1, threshold: 50, period: 'monthly' }],
    })
    render(<AIMonitoringPage />)

    expect(await screen.findByText('$50 / month')).toBeInTheDocument()
    expect(screen.getByText('monthly')).toBeInTheDocument()
  })

  it('creates a monthly cost alert at the entered threshold and reloads the alerts', async () => {
    const fetchMock = mockFetch({
      'GET /ai/metrics/usage': usage,
      'GET /ai/metrics/usage/daily': daily,
      'GET /ai/alerts': [],
      'POST /ai/alerts/cost': { id: 2 },
    })
    render(<AIMonitoringPage />)
    await screen.findByRole('heading', { name: 'AI Monitoring' })

    fireEvent.change(screen.getByPlaceholderText('Threshold ($)'), { target: { value: '75' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add Alert' }))

    await waitFor(() => expect(screen.getByPlaceholderText('Threshold ($)')).toHaveValue(100))
    const postCall = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/ai/alerts/cost') && init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({ threshold: 75, period: 'monthly' })
    expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith('/ai/alerts')).length).toBe(2)
  })

  it('shows the server reason and keeps the entered threshold when an alert cannot be created', async () => {
    mockFetch({
      'GET /ai/metrics/usage': usage,
      'GET /ai/metrics/usage/daily': daily,
      'GET /ai/alerts': [],
      'POST /ai/alerts/cost': reply({ detail: 'Threshold must be positive' }, 422),
    })
    render(<AIMonitoringPage />)
    await screen.findByRole('heading', { name: 'AI Monitoring' })

    fireEvent.change(screen.getByPlaceholderText('Threshold ($)'), { target: { value: '20' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add Alert' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Threshold must be positive')
    expect(screen.getByPlaceholderText('Threshold ($)')).toHaveValue(20)
  })

  it('shows the server reason when the statistics cannot be loaded', async () => {
    mockFetch({
      'GET /ai/metrics/usage': reply({ detail: 'AI usage is unavailable' }, 500),
      'GET /ai/metrics/usage/daily': daily,
      'GET /ai/alerts': [],
    })
    render(<AIMonitoringPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('AI usage is unavailable')
  })

  it('shows a generic message when the data cannot be loaded without a server reason', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Failed to fetch')) as unknown as typeof fetch
    render(<AIMonitoringPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('AI usage could not be loaded.')
  })
})
