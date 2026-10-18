import { render, screen } from '@testing-library/react'
import QuotaPage from '@/app/dashboard/quota/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/quota page', () => {
  it('shows the usage recorded for the signed-in user', async () => {
    mockFetch({ 'GET /quota/usage': { api_calls: 8500, storage_gb: 4.5, bandwidth_gb: 2.8 } })
    render(<QuotaPage />)

    expect(await screen.findByText('8,500')).toBeInTheDocument()
    expect(screen.getByText('4.50 GB')).toBeInTheDocument()
    expect(screen.getByText('2.80 GB')).toBeInTheDocument()
    expect(screen.getByText(/Plan limits are not set on this server/)).toBeInTheDocument()
  })

  it('shows a loading message until the usage arrives', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<QuotaPage />)

    expect(screen.getByText('Loading usage…')).toBeInTheDocument()
  })

  it('shows the server reason when usage cannot be loaded', async () => {
    mockFetch({ 'GET /quota/usage': reply({ detail: 'Usage is unavailable' }, 503) })
    render(<QuotaPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Usage is unavailable')
  })
})
