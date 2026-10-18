import { render, screen } from '@testing-library/react'
import FollowersPage from '@/app/dashboard/followers/page'
import { useAuth } from '@/hooks/useAuth'
import { mockFetch, reply } from '@/test-utils'

jest.mock('@/hooks/useAuth', () => ({ useAuth: jest.fn() }))
const mockedUseAuth = useAuth as jest.Mock

const follows = [
  { id: 1, follower_id: 2, following_id: 4, created_at: '2026-10-01T10:00:00Z', follower_name: 'Sam Rivera' },
  { id: 2, follower_id: 7, following_id: 4, created_at: '2026-10-05T10:00:00Z', follower_name: null },
]

describe('/dashboard/followers page', () => {
  beforeEach(() => {
    mockedUseAuth.mockReturnValue({ user: { id: 4 } })
  })

  it('loads the followers of the signed-in user', async () => {
    const fetchMock = mockFetch({ 'GET /platform/followers/4': follows })
    render(<FollowersPage />)

    expect(await screen.findByText('Sam Rivera')).toBeInTheDocument()
    expect(screen.getByText('User #7')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/platform/followers/4'))).toBe(true)
  })

  it('waits for the signed-in user before loading anything', () => {
    mockedUseAuth.mockReturnValue({ user: null })
    const fetchMock = mockFetch({})
    render(<FollowersPage />)

    expect(screen.getByText('Loading followers…')).toBeInTheDocument()
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('says when the user has no followers yet', async () => {
    mockFetch({ 'GET /platform/followers/4': [] })
    render(<FollowersPage />)

    expect(await screen.findByText('You have no followers yet.')).toBeInTheDocument()
  })

  it('shows the server reason when followers cannot be loaded', async () => {
    mockFetch({ 'GET /platform/followers/4': reply({ detail: 'Profile not found' }, 404) })
    render(<FollowersPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Profile not found')
  })
})
