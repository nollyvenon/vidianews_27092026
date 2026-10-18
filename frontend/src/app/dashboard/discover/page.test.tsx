import { render, screen } from '@testing-library/react'
import DiscoverPage from '@/app/dashboard/discover/page'
import { mockFetch, reply } from '@/test-utils'

const recommendations = [
  { id: 1, content_id: 10, score: 0.9, title: 'Amazing Travel Vlog', creator: 'Test Creator', views: 2300, reason: 'Matches your interests' },
  { id: 2, content_id: 11, score: 0.4, title: 'Cooking Tutorial', creator: null, views: 0, reason: null },
]

const trending = [
  { id: 1, topic: 'python', score: 9.5, mention_count: 12500 },
  { id: 2, topic: 'webdesign', score: 3.1, mention_count: 8300 },
]

describe('/dashboard/discover page', () => {
  it('lists the recommended content with its creator, views and reason', async () => {
    mockFetch({ 'GET /recommendations': recommendations, 'GET /trending': trending })
    render(<DiscoverPage />)

    expect(await screen.findByText('Amazing Travel Vlog')).toBeInTheDocument()
    expect(screen.getByText('Test Creator - 2,300 views')).toBeInTheDocument()
    expect(screen.getByText('Matches your interests')).toBeInTheDocument()
    expect(screen.getByText('Cooking Tutorial')).toBeInTheDocument()
    expect(screen.getByText('Unknown creator - 0 views')).toBeInTheDocument()
  })

  it('lists trending topics with their mention counts', async () => {
    mockFetch({ 'GET /recommendations': recommendations, 'GET /trending': trending })
    render(<DiscoverPage />)

    expect(await screen.findByText('#python')).toBeInTheDocument()
    expect(screen.getByText('12,500 mentions')).toBeInTheDocument()
    expect(screen.getByText('#webdesign')).toBeInTheDocument()
  })

  it('says when there is nothing recommended or trending yet', async () => {
    mockFetch({ 'GET /recommendations': [], 'GET /trending': [] })
    render(<DiscoverPage />)

    expect(await screen.findByText('No recommendations yet.')).toBeInTheDocument()
    expect(screen.getByText('No trending topics yet.')).toBeInTheDocument()
  })

  it('shows loading placeholders while the requests are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<DiscoverPage />)

    expect(screen.getByText('Loading recommendations…')).toBeInTheDocument()
    expect(screen.getByText('Loading trending topics…')).toBeInTheDocument()
  })

  it('shows the server reason when recommendations cannot be loaded, and still shows trending', async () => {
    mockFetch({ 'GET /recommendations': reply({ detail: 'Recommendations offline' }, 503), 'GET /trending': trending })
    render(<DiscoverPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Recommendations offline')
    expect(await screen.findByText('#python')).toBeInTheDocument()
  })

  it('shows the server reason when trending topics cannot be loaded', async () => {
    mockFetch({ 'GET /recommendations': recommendations, 'GET /trending': reply({ detail: 'Trends offline' }, 500) })
    render(<DiscoverPage />)

    expect(await screen.findByText('Trends offline')).toBeInTheDocument()
    expect(await screen.findByText('Amazing Travel Vlog')).toBeInTheDocument()
  })

  it('uses generic messages when the requests fail without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<DiscoverPage />)

    expect(await screen.findByText('Recommendations could not be loaded.')).toBeInTheDocument()
    expect(await screen.findByText('Trending topics could not be loaded.')).toBeInTheDocument()
  })
})
