import { fireEvent, render, screen } from '@testing-library/react'
import AnalyticsTab from '@/app/dashboard/publishing-distribution/components/AnalyticsTab'
import { mockFetch, reply } from '@/test-utils'

const content = { id: 7, title: 'Storm report', status: 'published', content_type: 'article' }

async function chooseContent() {
  fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })
}

describe('AnalyticsTab', () => {
  it('asks for a content item before showing any engagement', async () => {
    mockFetch({ 'GET /content': { items: [content], total: 1 }, 'GET /content/7': { id: 7, body: 'Text' } })
    render(<AnalyticsTab />)

    expect(screen.getByText('Select content to see its engagement.')).toBeInTheDocument()
    expect(await screen.findByRole('combobox')).toBeInTheDocument()
  })

  it('shows the engagement recorded for the chosen content', async () => {
    const fetchMock = mockFetch({
      'GET /content': { items: [content], total: 1 },
      'GET /content/7': { id: 7, body: 'Text' },
      'GET /analytics/metrics/7': {
        content_id: 7,
        total_views: 1200,
        total_clicks: 60,
        total_shares: 9,
        engagement_score: 72.5,
        engagement_trend: 'increasing',
      },
    })
    render(<AnalyticsTab />)
    await chooseContent()

    expect(await screen.findByText('1,200')).toBeInTheDocument()
    expect(screen.getByText('5.0%')).toBeInTheDocument()
    expect(screen.getByText('60 clicks')).toBeInTheDocument()
    expect(screen.getByText('9')).toBeInTheDocument()
    expect(screen.getByText('72.5')).toBeInTheDocument()
    expect(screen.getByText('increasing')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/analytics/metrics/7'))).toBe(true)
  })

  it('shows a zero click-through rate when nothing has been viewed', async () => {
    mockFetch({
      'GET /content': { items: [content], total: 1 },
      'GET /content/7': { id: 7, body: 'Text' },
      'GET /analytics/metrics/7': { content_id: 7, total_views: 0, total_clicks: 0, total_shares: 0, engagement_score: 0, engagement_trend: null },
    })
    render(<AnalyticsTab />)
    await chooseContent()

    expect(await screen.findByText('0.0%')).toBeInTheDocument()
  })

  it('explains when no engagement has been recorded for the content', async () => {
    mockFetch({
      'GET /content': { items: [content], total: 1 },
      'GET /content/7': { id: 7, body: 'Text' },
      'GET /analytics/metrics/7': reply({ detail: 'Metrics not found' }, 404),
    })
    render(<AnalyticsTab />)
    await chooseContent()

    expect(await screen.findByRole('alert')).toHaveTextContent('Metrics not found')
  })
})
