import { fireEvent, screen } from '@testing-library/react'
import PremiumPage from '@/app/dashboard/premium/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

describe('/dashboard/premium page', () => {
  it('shows a free account and offers premium access', async () => {
    mockFetch({ 'GET /premium/status': { is_premium: false } })
    renderWithQuery(<PremiumPage />)

    expect(await screen.findByText('Free')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Turn on premium access' })).toBeInTheDocument()
  })

  it('lists the features of a premium account and offers no subscription', async () => {
    mockFetch({ 'GET /premium/status': { is_premium: true, features: ['hd_streaming', 'ad_free'] } })
    renderWithQuery(<PremiumPage />)

    expect(await screen.findByText('Premium')).toBeInTheDocument()
    expect(await screen.findByText('hd streaming')).toBeInTheDocument()
    expect(screen.getByText('ad free')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Turn on premium access' })).not.toBeInTheDocument()
  })

  it('turns premium on and reports it', async () => {
    mockFetch({
      'GET /premium/status': { is_premium: false },
      'POST /premium/subscribe': { id: 1, is_active: true },
    })
    renderWithQuery(<PremiumPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Turn on premium access' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Premium access is on.')
  })

  it('shows the server reason when premium cannot be turned on', async () => {
    mockFetch({
      'GET /premium/status': { is_premium: false },
      'POST /premium/subscribe': reply({ detail: 'Payment method required' }, 402),
    })
    renderWithQuery(<PremiumPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Turn on premium access' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Payment method required')
  })

  it('shows the server reason when the status cannot be loaded', async () => {
    mockFetch({ 'GET /premium/status': reply({ detail: 'Premium is unavailable' }, 503) })
    renderWithQuery(<PremiumPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Premium is unavailable')
  })
})
