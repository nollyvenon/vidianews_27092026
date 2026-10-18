import { render, screen } from '@testing-library/react'
import InvoicesPage from '@/app/dashboard/invoices/page'
import { mockFetch, reply } from '@/test-utils'

const invoices = [
  { id: 4, amount: 49, status: 'paid', due_date: '2026-10-01T00:00:00Z', paid_date: '2026-10-02T00:00:00Z', created_at: null },
]

describe('/dashboard/invoices page', () => {
  it('lists the invoices of the current subscription', async () => {
    mockFetch({
      'GET /monetization/subscriptions/current': { id: 2, status: 'active' },
      'GET /monetization/invoices': invoices,
    })
    render(<InvoicesPage />)

    expect(await screen.findByText('#4')).toBeInTheDocument()
    expect(screen.getByText('$49.00')).toBeInTheDocument()
    expect(screen.getByText('paid')).toBeInTheDocument()
  })

  it('says when there is no subscription and so no invoices', async () => {
    mockFetch({ 'GET /monetization/subscriptions/current': reply({ detail: 'No active subscription' }, 404) })
    render(<InvoicesPage />)

    expect(await screen.findByText('You have no active subscription, so there are no invoices.')).toBeInTheDocument()
  })

  it('says when the subscription has no invoices yet', async () => {
    mockFetch({
      'GET /monetization/subscriptions/current': { id: 2 },
      'GET /monetization/invoices': [],
    })
    render(<InvoicesPage />)

    expect(await screen.findByText('No invoices yet.')).toBeInTheDocument()
  })

  it('shows the server reason when invoices cannot be loaded', async () => {
    mockFetch({
      'GET /monetization/subscriptions/current': { id: 2 },
      'GET /monetization/invoices': reply({ detail: 'Billing is unavailable' }, 503),
    })
    render(<InvoicesPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Billing is unavailable')
  })
})
