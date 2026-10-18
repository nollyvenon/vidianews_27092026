import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import ABTestingTab from '@/app/dashboard/publishing-distribution/components/ABTestingTab'
import { mockFetch, reply } from '@/test-utils'

const campaigns = [
  {
    id: 1,
    name: 'Subject line test',
    content_id: 7,
    test_metric: 'clicks',
    status: 'running',
    winner: null,
    is_statistically_significant: false,
    variants: [
      { id: 10, variant_name: 'Current', variant_type: 'control', impressions: 100, clicks: 5, conversions: 2, ctr: 5, conversion_rate: 40 },
      { id: 11, variant_name: 'Test', variant_type: 'treatment', impressions: 100, clicks: 8, conversions: 4, ctr: 8, conversion_rate: 50 },
    ],
  },
]
const oneVariant = [{ ...campaigns[0], variants: [campaigns[0].variants[0]] }]
const content = { id: 7, title: 'Storm report', status: 'published', content_type: 'article' }

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).includes(suffix) && init?.method === method)
}

describe('ABTestingTab', () => {
  it('shows a loading message until the tests arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<ABTestingTab />)

    expect(screen.getByText('Loading A/B tests…')).toBeInTheDocument()
  })

  it('lists each test with its variants and their click-through and conversion rates', async () => {
    mockFetch({ 'GET /ab-testing/campaigns': campaigns, 'GET /content': { items: [content], total: 1 } })
    render(<ABTestingTab />)

    expect(await screen.findByText('Subject line test')).toBeInTheDocument()
    expect(screen.getByText('Measured by clicks')).toBeInTheDocument()
    expect(screen.getByText('running')).toBeInTheDocument()
    expect(screen.getByText('Current')).toBeInTheDocument()
    expect(screen.getByText('CTR 8.00% · Conversion 50.00%')).toBeInTheDocument()
  })

  it('says when there are no tests yet', async () => {
    mockFetch({ 'GET /ab-testing/campaigns': [], 'GET /content': { items: [], total: 0 } })
    render(<ABTestingTab />)

    expect(await screen.findByText('No A/B tests yet.')).toBeInTheDocument()
  })

  it('shows the server reason when the tests cannot be loaded', async () => {
    mockFetch({ 'GET /ab-testing/campaigns': reply({ detail: 'Your account has no organization yet.' }, 422), 'GET /content': { items: [], total: 0 } })
    render(<ABTestingTab />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
  })

  it('analyzes a test with two variants and shows the result', async () => {
    const fetchMock = mockFetch({
      'GET /ab-testing/campaigns': campaigns,
      'GET /content': { items: [content], total: 1 },
      'POST /ab-testing/campaigns/1/analyze': { id: 3, p_value: 0.021, is_significant: true, improvement_percent: 60, recommended_action: 'Ship the test variant' },
    })
    render(<ABTestingTab />)
    await screen.findByText('Subject line test')

    fireEvent.click(screen.getByRole('button', { name: 'Analyze results' }))

    expect(await screen.findByText(/p-value 0\.021 · statistically significant · 60\.0% change · Ship the test variant/)).toBeInTheDocument()
    expect(requestTo(fetchMock, 'POST', '/ab-testing/campaigns/1/analyze')).toBeDefined()
  })

  it('does not offer analysis until a test has two variants', async () => {
    mockFetch({ 'GET /ab-testing/campaigns': oneVariant, 'GET /content': { items: [], total: 0 } })
    render(<ABTestingTab />)
    await screen.findByText('Subject line test')

    expect(screen.getByRole('button', { name: 'Analyze results' })).toBeDisabled()
  })

  it('shows the server reason when a test cannot be analyzed', async () => {
    mockFetch({
      'GET /ab-testing/campaigns': campaigns,
      'GET /content': { items: [], total: 0 },
      'POST /ab-testing/campaigns/1/analyze': reply({ detail: 'Need at least 2 variants to analyze' }, 400),
    })
    render(<ABTestingTab />)
    await screen.findByText('Subject line test')

    fireEvent.click(screen.getByRole('button', { name: 'Analyze results' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Need at least 2 variants to analyze')
  })

  it('creates a test for the chosen content with its metric and hypothesis', async () => {
    const fetchMock = mockFetch({
      'GET /ab-testing/campaigns': [],
      'GET /content': { items: [content], total: 1 },
      'GET /content/7': { id: 7, body: 'Text' },
      'POST /ab-testing/campaigns': { id: 2, name: 'Headline', status: 'draft', test_metric: 'conversion' },
    })
    render(<ABTestingTab />)
    await screen.findByText('No A/B tests yet.')
    const create = screen.getByRole('button', { name: 'Create test' })
    expect(create).toBeDisabled()
    fireEvent.change(await screen.findByRole('combobox', { name: 'Content to test' }), { target: { value: '7' } })
    fireEvent.change(screen.getByPlaceholderText('Test name'), { target: { value: 'Headline' } })
    fireEvent.change(screen.getByRole('combobox', { name: 'Measured metric' }), { target: { value: 'conversion' } })
    fireEvent.change(screen.getByPlaceholderText('Hypothesis'), { target: { value: 'Shorter headlines convert better' } })
    await waitFor(() => expect(create).toBeEnabled())
    fireEvent.click(create)

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ab-testing/campaigns')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ab-testing/campaigns')![1].body as string)).toEqual({
      content_id: 7,
      name: 'Headline',
      test_metric: 'conversion',
      hypothesis: 'Shorter headlines convert better',
    })
  })

  it('records the results of a variant', async () => {
    const fetchMock = mockFetch({
      'GET /ab-testing/campaigns': campaigns,
      'GET /content': { items: [], total: 0 },
      'PATCH /ab-testing/variants/10/performance': { id: 10, ctr: 6, conversion_rate: 40, performance_score: 50 },
    })
    render(<ABTestingTab />)
    await screen.findByText('Subject line test')

    fireEvent.change(screen.getAllByLabelText('Impressions')[0], { target: { value: '150' } })
    fireEvent.click(screen.getAllByRole('button', { name: 'Save results' })[0])

    await waitFor(() => expect(requestTo(fetchMock, 'PATCH', '/ab-testing/variants/10/performance')).toBeDefined())
    expect(String(requestTo(fetchMock, 'PATCH', '/ab-testing/variants/10/performance')![0])).toContain('impressions=150&clicks=5&conversions=2')
  })

  it('adds a variant to a test', async () => {
    const fetchMock = mockFetch({
      'GET /ab-testing/campaigns': campaigns,
      'GET /content': { items: [], total: 0 },
      'POST /ab-testing/campaigns/1/variants': { id: 12, variant_name: 'Bold', variant_type: 'treatment' },
    })
    render(<ABTestingTab />)
    await screen.findByText('Subject line test')

    fireEvent.change(screen.getByLabelText('Variant name'), { target: { value: ' Bold ' } })
    fireEvent.change(screen.getAllByRole('combobox', { name: 'Role' })[0], { target: { value: 'treatment' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add variant' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ab-testing/campaigns/1/variants')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ab-testing/campaigns/1/variants')![1].body as string)).toEqual({
      variant_name: 'Bold',
      variant_type: 'treatment',
    })
  })

  it('shows the server reason when a variant cannot be added', async () => {
    mockFetch({
      'GET /ab-testing/campaigns': campaigns,
      'GET /content': { items: [], total: 0 },
      'POST /ab-testing/campaigns/1/variants': reply({ detail: 'A/B test campaign not found' }, 404),
    })
    render(<ABTestingTab />)
    await screen.findByText('Subject line test')

    fireEvent.change(screen.getByLabelText('Variant name'), { target: { value: 'Bold' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add variant' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('A/B test campaign not found')
  })
})
