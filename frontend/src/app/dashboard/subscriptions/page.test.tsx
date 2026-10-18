import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import SubscriptionsPage from '@/app/dashboard/subscriptions/page'
import { mockFetch, reply } from '@/test-utils'

const tiers = [
  { id: 1, name: 'Silver', tier: 'basic', description: 'Starter', price: 4.99, billing_cycle: 'monthly', is_active: true, subscriber_count: 12 },
  { id: 2, name: 'Platinum', tier: 'enterprise', description: null, price: 19.99, billing_cycle: 'annual', is_active: false, subscriber_count: 1 },
]

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
}

describe('/dashboard/subscriptions page', () => {
  it('shows a loading message until the tiers arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<SubscriptionsPage />)

    expect(screen.getByText('Loading tiers…')).toBeInTheDocument()
  })

  it('lists each tier with its price, level and status', async () => {
    mockFetch({ 'GET /membership-types': tiers })
    render(<SubscriptionsPage />)

    expect(await screen.findByText('Silver')).toBeInTheDocument()
    expect(screen.getByText('$4.99/monthly')).toBeInTheDocument()
    expect(screen.getByText('Starter')).toBeInTheDocument()
    expect(screen.getByText('Level: basic')).toBeInTheDocument()
    expect(screen.getByText('$19.99/annual')).toBeInTheDocument()
    expect(screen.getByText('Inactive')).toBeInTheDocument()
    expect(screen.getByText('12 active subscribers')).toBeInTheDocument()
    expect(screen.getByText('1 active subscriber')).toBeInTheDocument()
  })

  it('says when there are no tiers yet', async () => {
    mockFetch({ 'GET /membership-types': [] })
    render(<SubscriptionsPage />)

    expect(await screen.findByText('No subscription tiers yet.')).toBeInTheDocument()
  })

  it('creates a tier from the form and reloads the list', async () => {
    const fetchMock = mockFetch({ 'GET /membership-types': tiers, 'POST /membership-types': { id: 3 } })
    render(<SubscriptionsPage />)
    await screen.findByText('Silver')

    fireEvent.click(screen.getByRole('button', { name: '+ New Tier' }))
    const create = screen.getByRole('button', { name: 'Create tier' })
    expect(create).toBeDisabled()
    fireEvent.change(screen.getByPlaceholderText('Tier name'), { target: { value: ' Gold ' } })
    fireEvent.change(screen.getByLabelText('Level'), { target: { value: 'premium' } })
    fireEvent.change(screen.getByLabelText('Price (USD)'), { target: { value: '9.99' } })
    fireEvent.change(screen.getByLabelText('Billing'), { target: { value: 'quarterly' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: 'Most popular' } })
    fireEvent.click(create)

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/membership-types')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/membership-types')![1].body as string)).toEqual({
      name: 'Gold',
      tier: 'premium',
      description: 'Most popular',
      price: 9.99,
      billing_cycle: 'quarterly',
    })
    await waitFor(() => expect(screen.queryByRole('button', { name: 'Create tier' })).not.toBeInTheDocument())
  })

  it('shows the server reason when a tier cannot be created', async () => {
    mockFetch({
      'GET /membership-types': tiers,
      'POST /membership-types': reply({ detail: 'Tier name already in use' }, 409),
    })
    render(<SubscriptionsPage />)
    await screen.findByText('Silver')

    fireEvent.click(screen.getByRole('button', { name: '+ New Tier' }))
    fireEvent.change(screen.getByPlaceholderText('Tier name'), { target: { value: 'Silver' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create tier' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Tier name already in use')
  })

  it('shows the server reason when tiers cannot be loaded', async () => {
    mockFetch({ 'GET /membership-types': reply({ detail: 'Your account has no workspace yet.' }, 422) })
    render(<SubscriptionsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no workspace yet.')
  })
})
