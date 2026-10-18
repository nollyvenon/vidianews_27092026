import { fireEvent, screen, waitFor } from '@testing-library/react'
import CreatorPage from '@/app/dashboard/creator/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const directory = [{ id: 1, user_id: 7, bio: 'Investigations', followers: 120, is_verified: true }]

describe('/dashboard/creator page', () => {
  it('shows the signed-in creator profile and the directory', async () => {
    mockFetch({
      'GET /monetization/creator-profile': { id: 2, user_id: 1, bio: 'Local reporter', followers: 5, is_verified: false },
      'GET /monetization/creators': directory,
    })
    renderWithQuery(<CreatorPage />)

    expect(await screen.findByText('Local reporter')).toBeInTheDocument()
    expect(screen.getByText('5 followers · Not verified')).toBeInTheDocument()
    expect(await screen.findByText('Creator #7')).toBeInTheDocument()
    expect(screen.getByText('Verified')).toBeInTheDocument()
  })

  it('offers to create a profile when the member has none, and creates it with a bio', async () => {
    const fetchMock = mockFetch({
      'GET /monetization/creator-profile': reply({ detail: 'Creator profile not found' }, 404),
      'GET /monetization/creators': [],
      'POST /monetization/creator-profile': { id: 3 },
    })
    renderWithQuery(<CreatorPage />)

    expect(await screen.findByText('You have no creator profile yet.')).toBeInTheDocument()
    fireEvent.change(screen.getByPlaceholderText('Tell viewers about your work'), { target: { value: 'Food stories' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create creator profile' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/monetization/creator-profile?bio=Food%20stories'))).toBe(true),
    )
  })

  it('shows the server reason when the profile cannot be loaded for another reason', async () => {
    mockFetch({
      'GET /monetization/creator-profile': reply({ detail: 'Creator service is down' }, 503),
      'GET /monetization/creators': [],
    })
    renderWithQuery(<CreatorPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Creator service is down')
  })

  it('filters the directory to verified creators', async () => {
    const fetchMock = mockFetch({
      'GET /monetization/creator-profile': { id: 2, user_id: 1, bio: null, followers: 0, is_verified: false },
      'GET /monetization/creators': directory,
    })
    renderWithQuery(<CreatorPage />)
    await screen.findByText('Creator #7')

    fireEvent.click(screen.getByRole('checkbox'))

    await waitFor(() => expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/monetization/creators?verified_only=true'))).toBe(true))
  })

  it('says when there are no creators to show', async () => {
    mockFetch({
      'GET /monetization/creator-profile': { id: 2, user_id: 1, bio: null, followers: 0, is_verified: false },
      'GET /monetization/creators': [],
    })
    renderWithQuery(<CreatorPage />)

    expect(await screen.findByText('No creators to show.')).toBeInTheDocument()
  })
})
