import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import RecommendationsTab from '@/app/dashboard/publishing-distribution/components/RecommendationsTab'
import { mockFetch, reply } from '@/test-utils'

const engines = [{ id: 1, name: 'Main engine', recommendation_type: 'hybrid', is_active: true }]
const pool = { items: [{ id: 7, title: 'Storm report', status: 'published', content_type: 'article' }, { id: 8, title: 'Launch notes', status: 'draft', content_type: 'article' }], total: 2 }

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).includes(suffix) && init?.method === method)
}

describe('RecommendationsTab', () => {
  it('lists the organization engines', async () => {
    mockFetch({ 'GET /content-recommendations/engines': engines, 'GET /content': pool })
    render(<RecommendationsTab />)

    expect((await screen.findAllByText('Main engine'))[0]).toBeInTheDocument()
    expect(screen.getByRole('listitem')).toHaveTextContent('Main engine · hybrid')
  })

  it('says when there are no engines yet', async () => {
    mockFetch({ 'GET /content-recommendations/engines': [], 'GET /content': pool })
    render(<RecommendationsTab />)

    expect(await screen.findByText('No engines yet. Create one below.')).toBeInTheDocument()
  })

  it('shows the server reason when engines cannot be loaded', async () => {
    mockFetch({ 'GET /content-recommendations/engines': reply({ detail: 'Your account has no organization yet.' }, 422), 'GET /content': pool })
    render(<RecommendationsTab />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
  })

  it('creates an engine of the chosen type', async () => {
    const fetchMock = mockFetch({
      'GET /content-recommendations/engines': engines,
      'GET /content': pool,
      'POST /content-recommendations/engines': { id: 2, name: 'Trending', recommendation_type: 'trending', is_active: true },
    })
    render(<RecommendationsTab />)
    expect((await screen.findAllByText('Main engine'))[0]).toBeInTheDocument()

    fireEvent.change(screen.getByPlaceholderText('Engine name'), { target: { value: ' Trending ' } })
    fireEvent.change(screen.getByRole('combobox', { name: 'Engine type' }), { target: { value: 'trending' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create engine' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/content-recommendations/engines')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/content-recommendations/engines')![1].body as string)).toEqual({
      name: 'Trending',
      recommendation_type: 'trending',
    })
    expect(await screen.findByRole('status')).toHaveTextContent('Engine created')
  })

  it('saves a preference with its weight', async () => {
    const fetchMock = mockFetch({
      'GET /content-recommendations/engines': engines,
      'GET /content': pool,
      'POST /content-recommendations/preferences': { id: 4, category: 'topic', value: 'Weather', weight: 1.5 },
    })
    render(<RecommendationsTab />)
    expect((await screen.findAllByText('Main engine'))[0]).toBeInTheDocument()

    fireEvent.change(screen.getByPlaceholderText('Value'), { target: { value: 'Weather' } })
    fireEvent.change(screen.getByLabelText('Weight'), { target: { value: '1.5' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save preference' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/content-recommendations/preferences')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/content-recommendations/preferences')![1].body as string)).toEqual({
      category: 'topic',
      value: 'Weather',
      weight: 1.5,
    })
  })

  it('generates recommendations from the chosen content and shows the ranked result', async () => {
    const fetchMock = mockFetch({
      'GET /content-recommendations/engines': engines,
      'GET /content': pool,
      'POST /content-recommendations/generate': { id: 9, recommended_content_ids: [7], recommendation_scores: [0.91] },
    })
    render(<RecommendationsTab />)
    expect((await screen.findAllByText('Main engine'))[0]).toBeInTheDocument()

    const generate = screen.getByRole('button', { name: 'Generate' })
    expect(generate).toBeDisabled()
    fireEvent.click(await screen.findByRole('checkbox', { name: 'Storm report' }))
    expect(generate).toBeEnabled()
    fireEvent.click(generate)

    expect(await screen.findByText('score 0.91')).toBeInTheDocument()
    expect(screen.getAllByText('Storm report')).toHaveLength(2)
    const post = requestTo(fetchMock, 'POST', '/content-recommendations/generate')!
    expect(String(post[0])).toContain('engine_id=1')
    expect(JSON.parse(post[1].body as string)).toEqual({ content_pool: [7], num_recommendations: 1 })
  })

  it('shows the server reason when recommendations cannot be generated', async () => {
    mockFetch({
      'GET /content-recommendations/engines': engines,
      'GET /content': pool,
      'POST /content-recommendations/generate': reply({ detail: 'Recommendation engine not found' }, 404),
    })
    render(<RecommendationsTab />)
    expect((await screen.findAllByText('Main engine'))[0]).toBeInTheDocument()

    fireEvent.click(await screen.findByRole('checkbox', { name: 'Launch notes' }))
    fireEvent.click(screen.getByRole('button', { name: 'Generate' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Recommendation engine not found')
  })

  it('says when there is no content to recommend', async () => {
    mockFetch({ 'GET /content-recommendations/engines': [], 'GET /content': { items: [], total: 0 } })
    render(<RecommendationsTab />)

    expect(await screen.findByText('You have no content to recommend yet.')).toBeInTheDocument()
  })
})
