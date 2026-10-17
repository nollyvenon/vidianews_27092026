import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import BillingAdminPage from '@/app/dashboard/admin/billing/page'
import { ApiClient } from '@/lib/api-client'

jest.mock('@/lib/api-client', () => ({ ApiClient: { get: jest.fn(), patch: jest.fn(), post: jest.fn() } }))
const mockedGet = ApiClient.get as jest.Mock
const mockedPatch = ApiClient.patch as jest.Mock
const mockedPost = ApiClient.post as jest.Mock

const subscription = {
  id: 7, user_id: 3, user_email: 'subscriber@example.com', organization_id: 1, tier: 'pro', billing_cycle: 'monthly',
  amount: 49, is_active: true, started_at: '2026-09-01T00:00:00Z', renews_at: '2026-11-01T00:00:00Z', canceled_at: null,
}

const transactions = [
  {
    source: 'checkout', id: 2, user_id: null, user_email: 'buyer@example.com', amount: 20, currency: 'USD',
    status: 'failed', payment_method: 'credit_card', reference: 'txn-9', created_at: '2026-10-02T10:00:00Z',
  },
  {
    source: 'subscription', id: 1, user_id: 3, user_email: 'payer@example.com', amount: 49, currency: 'USD',
    status: 'completed', payment_method: 'card', reference: 'pay_1', created_at: '2026-10-01T10:00:00Z',
  },
]

function mockLists(subs = [subscription], txs = transactions) {
  mockedGet.mockImplementation((endpoint: string) => {
    if (endpoint.startsWith('/admin/subscriptions')) {
      return Promise.resolve({ items: subs, total: subs.length, skip: 0, limit: 20 })
    }
    return Promise.resolve({ items: txs, total: txs.length, skip: 0, limit: 20 })
  })
}

describe('/dashboard/admin/billing page', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    mockLists()
  })

  it('lists subscriptions with the customer email and current tier', async () => {
    render(<BillingAdminPage />)
    expect(await screen.findByText('subscriber@example.com')).toBeInTheDocument()
    expect(screen.getByLabelText('Tier for subscription 7')).toHaveValue('pro')
    expect(mockedGet).toHaveBeenCalledWith('/admin/subscriptions?skip=0&limit=20')
  })

  it('lists transactions from both sources with their statuses and references', async () => {
    render(<BillingAdminPage />)
    expect(await screen.findByText('buyer@example.com')).toBeInTheDocument()
    expect(screen.getByText('txn-9')).toBeInTheDocument()
    expect(screen.getByText('pay_1')).toBeInTheDocument()
    expect(screen.getByText('failed')).toBeInTheDocument()
  })

  it('changes a subscription tier through the admin API', async () => {
    mockedPatch.mockResolvedValueOnce({ ...subscription, tier: 'enterprise' })
    render(<BillingAdminPage />)
    await screen.findByText('subscriber@example.com')

    fireEvent.change(screen.getByLabelText('Tier for subscription 7'), { target: { value: 'enterprise' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save tier' }))

    await waitFor(() => expect(mockedPatch).toHaveBeenCalledWith('/admin/subscriptions/7', { tier: 'enterprise' }))
    expect(await screen.findByLabelText('Tier for subscription 7')).toHaveValue('enterprise')
  })

  it('cancels a subscription only after confirmation', async () => {
    mockedPost.mockResolvedValueOnce({ ...subscription, is_active: false, canceled_at: '2026-10-17T00:00:00Z' })
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(true)
    render(<BillingAdminPage />)
    await screen.findByText('subscriber@example.com')

    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))

    await waitFor(() => expect(mockedPost).toHaveBeenCalledWith('/admin/subscriptions/7/cancel', {}))
    expect(confirm).toHaveBeenCalled()
    await waitFor(() => expect(screen.queryByRole('button', { name: 'Cancel' })).not.toBeInTheDocument())
    confirm.mockRestore()
  })

  it('does not cancel when the administrator declines the confirmation', async () => {
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(false)
    render(<BillingAdminPage />)
    await screen.findByText('subscriber@example.com')

    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))

    expect(mockedPost).not.toHaveBeenCalled()
    confirm.mockRestore()
  })

  it('filters transactions by source and refetches', async () => {
    render(<BillingAdminPage />)
    await screen.findByText('buyer@example.com')

    fireEvent.change(screen.getByLabelText('Source'), { target: { value: 'checkout' } })

    await waitFor(() =>
      expect(mockedGet).toHaveBeenCalledWith('/admin/transactions?source=checkout&skip=0&limit=20'),
    )
  })

  it('shows an error when the subscriptions cannot be loaded', async () => {
    mockedGet.mockRejectedValueOnce(new Error('Admin access required'))
    render(<BillingAdminPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Admin access required')
  })
})
