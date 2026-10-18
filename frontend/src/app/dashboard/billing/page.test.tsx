import { render, screen } from '@testing-library/react'
import BillingPage from '@/app/dashboard/billing/page'
import { mockFetch, reply } from '@/test-utils'

const invoices = [
  { id: 1, created_at: '2026-09-01T00:00:00Z', amount: 29, status: 'completed' },
  { id: 2, created_at: '2026-10-01T00:00:00Z', amount: 29, status: 'pending' },
]

describe('/dashboard/billing page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows the current plan and the invoice history', async () => {
    mockFetch({
      'GET /monetization/subscriptions/current': { tier: 'Pro', amount: 49 },
      'GET /monetization/invoices': invoices,
    })
    render(<BillingPage />)

    expect(await screen.findByText('Pro')).toBeInTheDocument()
    expect(screen.getByText('$49/month')).toBeInTheDocument()
    expect(screen.getAllByText('$29')).toHaveLength(2)
    expect(screen.getByText('completed')).toHaveClass('bg-green-100')
    expect(screen.getByText('pending')).not.toHaveClass('bg-green-100')
  })

  it('falls back to the free plan when there is no active subscription', async () => {
    mockFetch({
      'GET /monetization/subscriptions/current': null,
      'GET /monetization/invoices': [],
    })
    render(<BillingPage />)

    expect(await screen.findByText('Free')).toBeInTheDocument()
    expect(screen.getByText('$0/month')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Upgrade' })).toBeInTheDocument()
  })

  it('logs the failure and leaves the default plan when billing cannot be loaded', async () => {
    mockFetch({ 'GET /monetization/subscriptions/current': reply({ detail: 'down' }, 500) })
    render(<BillingPage />)

    expect(await screen.findByText('Free')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch billing', expect.any(Error))
  })
})
