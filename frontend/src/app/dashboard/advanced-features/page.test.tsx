import { fireEvent, render, screen } from '@testing-library/react'
import AdvancedFeaturesPage from '@/app/dashboard/advanced-features/page'
import { mockFetch, reply } from '@/test-utils'

const summary = {
  recommendations: {
    total: 2847,
    click_through_rate: 28.4,
    conversion_rate: 12.7,
    by_type: [
      { type: 'collaborative', count: 850, click_through_rate: 32.1, conversion_rate: 14.2 },
      { type: 'content_based', count: 920, click_through_rate: 26.3, conversion_rate: 11.5 },
    ],
  },
  retention: { subscribers: 1000, at_risk: 120, average_churn_risk: 0.68 },
  personalization: { profiles: 8234, average_score: 0.72 },
  predictions: { deployed_models: 4, average_accuracy: 0.894, predictions_this_month: 24300 },
  performance: { measured_endpoints: 2, total_calls: 66666, average_response_time_ms: 28.5 },
}

const tests = [
  { id: 1, name: 'Headline test', status: 'running', confidence: 0.4, winner: null },
  { id: 2, name: 'Layout test', status: 'completed', confidence: 0.97, winner: 'B' },
  { id: 3, name: 'Price test', status: 'completed', confidence: 0.6, winner: null },
]

const insights = [
  { id: 1, type: 'anomaly', title: 'Spike in 404 errors', confidence_level: 0.94 },
]

const cohorts = [
  { id: 1, name: 'High-Value Users', user_count: 1247 },
]

function workingRoutes(extra: Record<string, unknown> = {}) {
  return {
    'GET /advanced/summary': summary,
    'GET /ab-tests': tests,
    'GET /insights': insights,
    'GET /cohorts': cohorts,
    ...extra,
  }
}

describe('/dashboard/advanced-features page', () => {
  it('shows the recommendation totals and the performance of each type', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    expect(screen.getByRole('heading', { name: 'Advanced Features' })).toBeInTheDocument()
    expect(await screen.findByText('2,847')).toBeInTheDocument()
    expect(screen.getByText('28.4%')).toBeInTheDocument()
    expect(screen.getByText('12.7%')).toBeInTheDocument()
    expect(screen.getByText('collaborative')).toBeInTheDocument()
    expect(screen.getByText('32.1% CTR')).toBeInTheDocument()
    expect(screen.getByText('11.5% conversion')).toBeInTheDocument()
  })

  it('says when no recommendations have been made', async () => {
    mockFetch(workingRoutes({
      'GET /advanced/summary': { ...summary, recommendations: { ...summary.recommendations, total: 0, by_type: [] } },
    }))
    render(<AdvancedFeaturesPage />)

    expect(await screen.findByText('No recommendations have been made yet.')).toBeInTheDocument()
  })

  it('shows retention figures from the subscriber churn data', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Retention' }))

    expect(await screen.findByText('120')).toBeInTheDocument()
    expect(screen.getByText('12.0% of subscribers')).toBeInTheDocument()
    expect(screen.getByText('0.68')).toBeInTheDocument()
    expect(screen.getByText('68% estimated churn risk')).toBeInTheDocument()
  })

  it('lists the A/B tests and the share of completed tests that found a winner', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'A/B Tests' }))

    expect(await screen.findByText('Headline test')).toBeInTheDocument()
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('50.0%')).toBeInTheDocument()
    expect(screen.getByText('completed · winner: B')).toBeInTheDocument()
    expect(screen.getByText('completed · no winner yet')).toBeInTheDocument()
  })

  it('shows zero success when no test has completed, and says when there are no tests', async () => {
    mockFetch(workingRoutes({ 'GET /ab-tests': [] }))
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'A/B Tests' }))

    expect(await screen.findByText('0.0%')).toBeInTheDocument()
    expect(screen.queryByText('Headline test')).not.toBeInTheDocument()
  })

  it('lists insights with their confidence as a percentage', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Insights' }))

    expect(await screen.findByText('Spike in 404 errors')).toBeInTheDocument()
    expect(screen.getByText('Confidence: 94%')).toBeInTheDocument()
    expect(screen.getByText('anomaly')).toBeInTheDocument()
  })

  it('says when there are no insights yet', async () => {
    mockFetch(workingRoutes({ 'GET /insights': [] }))
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Insights' }))

    expect(await screen.findByText('No insights have been generated yet.')).toBeInTheDocument()
  })

  it('lists user cohorts with their sizes', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Cohorts' }))

    expect(await screen.findByText('High-Value Users')).toBeInTheDocument()
    expect(screen.getByText('1,247 users')).toBeInTheDocument()
  })

  it('says when there are no cohorts yet', async () => {
    mockFetch(workingRoutes({ 'GET /cohorts': [] }))
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Cohorts' }))

    expect(await screen.findByText('No cohorts have been defined yet.')).toBeInTheDocument()
  })

  it('shows the personalization score and profile count', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Personalization' }))

    expect(await screen.findByText('0.72')).toBeInTheDocument()
    expect(screen.getByText('8,234')).toBeInTheDocument()
  })

  it('shows the deployed models, their accuracy and this month’s predictions', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Predictions' }))

    expect(await screen.findByText('0.894')).toBeInTheDocument()
    expect(screen.getByText('24,300')).toBeInTheDocument()
    expect(screen.getByText('4')).toBeInTheDocument()
  })

  it('shows the measured API performance', async () => {
    mockFetch(workingRoutes())
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Performance' }))

    expect(await screen.findByText('66,666')).toBeInTheDocument()
    expect(screen.getByText('28.5ms')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
  })

  it('shows the server reason when the platform figures cannot be loaded', async () => {
    mockFetch(workingRoutes({ 'GET /advanced/summary': reply({ detail: 'Figures offline' }, 503) }))
    render(<AdvancedFeaturesPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Figures offline')
  })

  it('reports each list that cannot be loaded on its own tab', async () => {
    mockFetch(workingRoutes({
      'GET /ab-tests': reply({ detail: 'Tests offline' }, 500),
      'GET /insights': reply({ detail: 'Insights offline' }, 500),
      'GET /cohorts': reply({ detail: 'Cohorts offline' }, 500),
    }))
    render(<AdvancedFeaturesPage />)

    fireEvent.click(screen.getByRole('tab', { name: 'A/B Tests' }))
    expect(await screen.findByText('Tests offline')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Insights' }))
    expect(await screen.findByText('Insights offline')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Cohorts' }))
    expect(await screen.findByText('Cohorts offline')).toBeInTheDocument()
  })

  it('uses generic messages when the requests fail without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<AdvancedFeaturesPage />)

    expect(await screen.findByText('Platform figures could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'A/B Tests' }))
    expect(await screen.findByText('A/B tests could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Insights' }))
    expect(await screen.findByText('Insights could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Cohorts' }))
    expect(await screen.findByText('Cohorts could not be loaded.')).toBeInTheDocument()
  })

  it('shows loading placeholders while the figures are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<AdvancedFeaturesPage />)

    expect(screen.getAllByText('—').length).toBeGreaterThan(0)
  })
})
