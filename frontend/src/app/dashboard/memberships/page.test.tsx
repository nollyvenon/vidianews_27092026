import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import MembershipsPage from '@/app/dashboard/memberships/page'
import { mockFetch, reply } from '@/test-utils'

const basic = {
  id: 1,
  name: 'Basic',
  tier: 'basic',
  price: 9,
  billing_cycle: 'month',
  max_courses: 3,
  features: { ads: false, downloads: true },
  is_active: true,
}
const pro = {
  id: 2,
  name: 'Pro',
  tier: 'pro',
  price: 29.5,
  billing_cycle: 'year',
  max_courses: -1,
  features: { ads: false, downloads: true, offline: true },
  is_active: true,
}
const activeSubscription = {
  id: 50,
  status: 'active',
  start_date: '2026-09-01',
  renewal_date: '2026-11-01',
  membership_type: basic,
}

describe('/dashboard/memberships page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state, then the plans with prices, features and course limits', async () => {
    mockFetch({
      'GET /membership-types': [basic, pro],
      'GET /subscriptions/me/active': reply({ detail: 'No active subscription' }, 404),
    })
    render(<MembershipsPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Membership Plans' })).toBeInTheDocument()
    expect(screen.getByText('$9.00')).toBeInTheDocument()
    expect(screen.getByText('$29.50')).toBeInTheDocument()
    expect(screen.getByText('per year')).toBeInTheDocument()
    // Both plans include the downloads feature.
    expect(screen.getAllByText('downloads: ✓')[0]).toHaveClass('text-green-600')
    expect(screen.getAllByText('downloads: ✓')).toHaveLength(2)
    expect(screen.getAllByText('ads: ✗')[0]).toHaveClass('text-gray-400')
    expect(screen.getByText('Max Courses: 3')).toBeInTheDocument()
    expect(screen.getByText('Max Courses: Unlimited')).toBeInTheDocument()
  })

  it('renders the plans without an active subscription panel when the user has none', async () => {
    mockFetch({
      'GET /membership-types': [basic],
      'GET /subscriptions/me/active': reply({ detail: 'No active subscription' }, 404),
    })
    render(<MembershipsPage />)

    expect(await screen.findByRole('heading', { name: 'Basic' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Active Subscription' })).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Subscribe' })).toBeEnabled()
  })

  it('shows the active subscription and disables the plan the user already has', async () => {
    mockFetch({
      'GET /membership-types': [basic, pro],
      'GET /subscriptions/me/active': activeSubscription,
    })
    render(<MembershipsPage />)

    expect(await screen.findByRole('heading', { name: 'Active Subscription' })).toBeInTheDocument()
    expect(screen.getByText('Plan: Basic')).toBeInTheDocument()
    expect(screen.getByText('Status: active')).toBeInTheDocument()
    expect(screen.getByText(/Renewal Date:/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Current Plan' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Subscribe' })).toBeEnabled()
  })

  it('subscribes to a plan and shows it as the active subscription', async () => {
    const fetchMock = mockFetch({
      'GET /membership-types': [basic, pro],
      'GET /subscriptions/me/active': reply({ detail: 'none' }, 404),
      'POST /subscriptions': { ...activeSubscription, id: 51, membership_type: pro },
    })
    render(<MembershipsPage />)
    await screen.findByRole('heading', { name: 'Pro' })

    fireEvent.click(screen.getAllByRole('button', { name: 'Subscribe' })[1])

    expect(await screen.findByText('Plan: Pro')).toBeInTheDocument()
    const postCall = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/subscriptions') && init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({ membership_type_id: 2 })
  })

  it('keeps the current subscription when a new subscription is rejected', async () => {
    mockFetch({
      'GET /membership-types': [basic, pro],
      'GET /subscriptions/me/active': activeSubscription,
      'POST /subscriptions': reply({ detail: 'Payment required' }, 402),
    })
    render(<MembershipsPage />)
    await screen.findByText('Plan: Basic')

    fireEvent.click(screen.getByRole('button', { name: 'Subscribe' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Subscription failed:', 402))
    expect(screen.getByText('Plan: Basic')).toBeInTheDocument()
  })

  it('logs a subscription that cannot be sent at all', async () => {
    mockFetch({
      'GET /membership-types': [basic],
      'GET /subscriptions/me/active': reply({ detail: 'none' }, 404),
    })
    render(<MembershipsPage />)
    await screen.findByRole('heading', { name: 'Basic' })
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch

    fireEvent.click(screen.getByRole('button', { name: 'Subscribe' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Subscription failed:', expect.any(Error)))
  })

  it('cancels the active subscription and removes the panel', async () => {
    const fetchMock = mockFetch({
      'GET /membership-types': [basic],
      'GET /subscriptions/me/active': activeSubscription,
      'POST /subscriptions/50/cancel': { ok: true },
    })
    render(<MembershipsPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Cancel Subscription' }))

    await waitFor(() => expect(screen.queryByRole('heading', { name: 'Active Subscription' })).not.toBeInTheDocument())
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/subscriptions/50/cancel') && init?.method === 'POST')).toBe(true)
  })

  it('logs a failed cancellation and keeps the subscription visible', async () => {
    global.fetch = jest.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input)
      if (url.endsWith('/membership-types')) return { ok: true, json: async () => [basic] } as Response
      if (url.endsWith('/subscriptions/me/active')) return { ok: true, json: async () => activeSubscription } as Response
      if (init?.method === 'POST') throw new Error('network down')
      return { ok: false, status: 404, json: async () => ({}) } as Response
    }) as unknown as typeof fetch
    render(<MembershipsPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Cancel Subscription' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Cancellation failed:', expect.any(Error)))
    expect(screen.getByRole('heading', { name: 'Active Subscription' })).toBeInTheDocument()
  })

  it('still shows the page when the plans cannot be loaded', async () => {
    mockFetch({
      'GET /membership-types': reply({ detail: 'down' }, 500),
      'GET /subscriptions/me/active': reply({ detail: 'none' }, 404),
    })
    render(<MembershipsPage />)

    expect(await screen.findByRole('heading', { name: 'Membership Plans' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Subscribe' })).not.toBeInTheDocument()
  })

  it('logs the failure when the membership data cannot be requested', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<MembershipsPage />)

    expect(await screen.findByRole('heading', { name: 'Membership Plans' })).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to load memberships:', expect.any(Error))
  })

  it('treats a plan response that is not a list as having no plans', async () => {
    mockFetch({
      'GET /membership-types': { detail: 'unexpected' },
      'GET /subscriptions/me/active': reply({ detail: 'none' }, 404),
    })
    render(<MembershipsPage />)

    expect(await screen.findByRole('heading', { name: 'Membership Plans' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Subscribe' })).not.toBeInTheDocument()
  })
})
