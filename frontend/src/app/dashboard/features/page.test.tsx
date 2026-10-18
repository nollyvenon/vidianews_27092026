import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import FeaturesPage from '@/app/dashboard/features/page'
import { mockFetch, reply } from '@/test-utils'

const flags = [
  { id: 1, name: 'dark_mode', description: 'Dark theme', enabled: true, rollout_percentage: 100, target_segments: [], created_at: '2026-10-01T10:00:00Z' },
  { id: 2, name: 'new_ui', description: null, enabled: false, rollout_percentage: 50, target_segments: [], created_at: '2026-10-02T10:00:00Z' },
  { id: 3, name: 'beta_search', description: null, enabled: false, rollout_percentage: 0, target_segments: [], created_at: '2026-10-03T10:00:00Z' },
]
const tests = [
  { id: 4, name: 'Headline test', status: 'running', metric_a: 3.2, metric_b: 4.1, confidence: 95.5, winner: null },
  { id: 5, name: 'CTA test', status: 'draft', metric_a: 0, metric_b: 0, confidence: 0, winner: null },
]

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
}

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({ 'GET /feature-flags': flags, 'GET /ab-tests': tests, ...extra })
}

describe('/dashboard/features page', () => {
  it('lists feature flags with their status and description', async () => {
    base()
    render(<FeaturesPage />)

    expect(await screen.findByText('dark_mode')).toBeInTheDocument()
    expect(screen.getByText('Dark theme')).toBeInTheDocument()
    expect(screen.getByText('enabled')).toHaveClass('bg-green-100')
    expect(screen.getByText('rollout')).toHaveClass('bg-blue-100')
    expect(screen.getByText('disabled')).toHaveClass('bg-gray-100')
  })

  it('shows the rollout percentage only for flags that are rolled out', async () => {
    base()
    render(<FeaturesPage />)

    expect(await screen.findByText('Rollout: 100%')).toBeInTheDocument()
    expect(screen.getByText('Rollout: 50%')).toBeInTheDocument()
    expect(screen.queryByText('Rollout: 0%')).not.toBeInTheDocument()
  })

  it('turns a flag off with the full flag body and shows the saved state', async () => {
    const fetchMock = base({ 'PATCH /feature-flags/1': { ...flags[0], enabled: false } })
    render(<FeaturesPage />)

    fireEvent.click((await screen.findAllByRole('button', { name: 'Disable' }))[0])

    await waitFor(() => expect(requestTo(fetchMock, 'PATCH', '/feature-flags/1')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'PATCH', '/feature-flags/1')![1].body as string)).toEqual({
      name: 'dark_mode',
      description: 'Dark theme',
      enabled: false,
      rollout_percentage: 100,
      target_segments: [],
    })
    await waitFor(() => expect(screen.getAllByRole('button', { name: 'Enable' })).toHaveLength(3))
  })

  it('shows the server reason when a flag cannot be changed', async () => {
    base({ 'PATCH /feature-flags/2': reply({ detail: 'Flag is locked by a release' }, 409) })
    render(<FeaturesPage />)

    // Flag 1 is enabled and shows "Disable", so the first "Enable" button belongs to flag 2.
    fireEvent.click((await screen.findAllByRole('button', { name: 'Enable' }))[0])

    expect(await screen.findByRole('alert')).toHaveTextContent('Flag is locked by a release')
  })

  it('creates a flag from the form and reloads the list', async () => {
    const fetchMock = base({ 'POST /feature-flags': { id: 4 } })
    render(<FeaturesPage />)
    await screen.findByText('dark_mode')

    fireEvent.click(screen.getByRole('button', { name: '+ New Flag' }))
    const create = screen.getByRole('button', { name: 'Create flag' })
    expect(create).toBeDisabled()
    fireEvent.change(screen.getByPlaceholderText('Flag name (for example new_checkout)'), { target: { value: ' new_checkout ' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: 'Checkout redesign' } })
    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '25' } })
    fireEvent.click(create)

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/feature-flags')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/feature-flags')![1].body as string)).toEqual({
      name: 'new_checkout',
      description: 'Checkout redesign',
      enabled: false,
      rollout_percentage: 25,
      target_segments: [],
    })
    await waitFor(() => expect(screen.queryByRole('button', { name: 'Create flag' })).not.toBeInTheDocument())
  })

  it('shows the server reason when a flag cannot be created', async () => {
    base({ 'POST /feature-flags': reply({ detail: 'A flag with this name already exists' }, 409) })
    render(<FeaturesPage />)
    await screen.findByText('dark_mode')

    fireEvent.click(screen.getByRole('button', { name: '+ New Flag' }))
    fireEvent.change(screen.getByPlaceholderText('Flag name (for example new_checkout)'), { target: { value: 'dark_mode' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create flag' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('A flag with this name already exists')
  })

  it('says when there are no flags yet and shows the server reason when flags cannot be loaded', async () => {
    mockFetch({ 'GET /feature-flags': [], 'GET /ab-tests': [] })
    const { unmount } = render(<FeaturesPage />)
    expect(await screen.findByText('No feature flags yet.')).toBeInTheDocument()
    unmount()

    mockFetch({ 'GET /feature-flags': reply({ detail: 'Flags unavailable' }, 500), 'GET /ab-tests': [] })
    render(<FeaturesPage />)
    expect(await screen.findByText('Flags unavailable')).toBeInTheDocument()
  })

  it('lists the A/B tests with their results and status', async () => {
    base()
    render(<FeaturesPage />)

    expect(await screen.findByText('Headline test')).toBeInTheDocument()
    expect(screen.getByText(/Variant A 3\.20 · Variant B 4\.10 · Confidence 95\.5%/)).toBeInTheDocument()
    expect(screen.getByText('CTA test')).toBeInTheDocument()
  })

  it('starts a draft test and ends a running one', async () => {
    const fetchMock = base({
      'POST /ab-tests/5/start': { id: 5, status: 'running' },
      'POST /ab-tests/4/end': { id: 4, status: 'completed' },
    })
    render(<FeaturesPage />)
    await screen.findByText('Headline test')

    fireEvent.click(screen.getByRole('button', { name: 'Start' }))
    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ab-tests/5/start')).toBeDefined())
    fireEvent.click(screen.getByRole('button', { name: 'End' }))
    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ab-tests/4/end')).toBeDefined())
  })

  it('creates an A/B test with its hypothesis and metric', async () => {
    const fetchMock = base({ 'POST /ab-tests': { id: 6 } })
    render(<FeaturesPage />)
    await screen.findByText('Headline test')

    fireEvent.change(screen.getByPlaceholderText('Test name'), { target: { value: 'Pricing test' } })
    fireEvent.change(screen.getByPlaceholderText('Hypothesis'), { target: { value: 'Lower price converts' } })
    fireEvent.change(screen.getByPlaceholderText('Metric to optimize'), { target: { value: 'conversion' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create A/B test' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ab-tests')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ab-tests')![1].body as string)).toEqual({
      name: 'Pricing test',
      hypothesis: 'Lower price converts',
      metric_to_optimize: 'conversion',
    })
  })

  it('shows the server reason when A/B tests cannot be loaded', async () => {
    mockFetch({ 'GET /feature-flags': flags, 'GET /ab-tests': reply({ detail: 'Experiments are unavailable' }, 503) })
    render(<FeaturesPage />)

    expect(await screen.findByText('Experiments are unavailable')).toBeInTheDocument()
  })
})
