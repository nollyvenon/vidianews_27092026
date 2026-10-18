import { fireEvent, screen } from '@testing-library/react'
import PartnershipsPage from '@/app/dashboard/partnerships/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

describe('/dashboard/partnerships page', () => {
  it('lists the partnerships with their type and status', async () => {
    mockFetch({ 'GET /partnerships': [{ id: 1, type: 'revenue_share', status: 'active' }] })
    renderWithQuery(<PartnershipsPage />)

    // The type select also offers 'revenue share', so wait for the list item itself.
    expect(await screen.findByRole('listitem')).toHaveTextContent('revenue share')
    expect(screen.getByText('active')).toBeInTheDocument()
  })

  it('says when there are no partnerships yet', async () => {
    mockFetch({ 'GET /partnerships': [] })
    renderWithQuery(<PartnershipsPage />)

    expect(await screen.findByText('No partnerships yet.')).toBeInTheDocument()
  })

  it('proposes a partnership with the partner and type chosen', async () => {
    const fetchMock = mockFetch({
      'GET /partnerships': [],
      'POST /partnerships': { id: 2, type: 'sponsorship', status: 'proposed' },
    })
    renderWithQuery(<PartnershipsPage />)
    await screen.findByText('No partnerships yet.')

    fireEvent.change(screen.getByLabelText('Partner user ID'), { target: { value: '12' } })
    fireEvent.change(screen.getByLabelText('Partnership type'), { target: { value: 'sponsorship' } })
    fireEvent.click(screen.getByRole('button', { name: 'Propose partnership' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Partnership proposed.')
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/partnerships?partner_id=12&partnership_type=sponsorship'))).toBe(true)
  })

  it('shows the server reason when the partnership cannot be proposed', async () => {
    mockFetch({
      'GET /partnerships': [],
      'POST /partnerships': reply({ detail: 'Partner not found' }, 404),
    })
    renderWithQuery(<PartnershipsPage />)
    await screen.findByText('No partnerships yet.')

    fireEvent.change(screen.getByLabelText('Partner user ID'), { target: { value: '99' } })
    fireEvent.click(screen.getByRole('button', { name: 'Propose partnership' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Partner not found')
  })
})
