import { render, screen, waitFor } from '@testing-library/react'
import BadgesPage from '@/app/dashboard/badges/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/badges page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows the earned badges and the top of the leaderboard', async () => {
    mockFetch({
      'GET /badges/user': [{ id: 1, name: 'First Upload' }],
      'GET /leaderboard': [{ id: 7, name: 'Ada', rank: 1, points: 980, views: 5400 }],
    })
    render(<BadgesPage />)

    expect(screen.getByRole('heading', { name: 'Badges & Gamification' })).toBeInTheDocument()
    expect(await screen.findByText('First Upload')).toBeInTheDocument()
    expect(await screen.findByText('#1')).toBeInTheDocument()
    expect(screen.getByText('980 points')).toBeInTheDocument()
    expect(screen.getByText('5400 views')).toBeInTheDocument()
  })

  it('keeps the sections empty when the server responds with an error', async () => {
    mockFetch({
      'GET /badges/user': reply({ detail: 'nope' }, 500),
      'GET /leaderboard': reply({ detail: 'nope' }, 500),
    })
    render(<BadgesPage />)

    expect(screen.getByRole('heading', { name: 'Your Badges' })).toBeInTheDocument()
    await screen.findByRole('heading', { name: 'Top Leaderboard' })
    expect(screen.queryByText(/points/)).not.toBeInTheDocument()
    expect(consoleError).not.toHaveBeenCalled()
  })

  it('logs the failure when the requests cannot be made', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<BadgesPage />)

    await waitFor(() =>
      expect(consoleError).toHaveBeenCalledWith('Failed to fetch leaderboard:', expect.any(Error))
    )
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch badges:', expect.any(Error))
  })
})
