import { render, screen, waitFor } from '@testing-library/react'
import SocialLoginCallbackPage from '@/app/auth/social/[provider]/callback/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({ ApiClient: { post: jest.fn() } }))
jest.mock('next/navigation', () => ({
  useParams: () => ({ provider: 'google' }),
  useRouter: () => ({ push: jest.fn(), replace: jest.fn() }),
}))
const mockedPost = ApiClient.post as jest.Mock

describe('/auth/social/[provider]/callback page', () => {
  const replace = jest.fn()
  const originalLocation = window.location

  beforeAll(() => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { ...originalLocation, search: '', replace },
    })
  })

  afterAll(() => {
    Object.defineProperty(window, 'location', { configurable: true, value: originalLocation })
  })

  beforeEach(() => {
    jest.clearAllMocks()
    localStorage.clear()
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { ...originalLocation, search: '?code=abc&state=xyz', replace },
    })
  })

  it('exchanges the code, stores the session tokens and enters the dashboard', async () => {
    mockedPost.mockResolvedValueOnce({ access_token: 'access-1', refresh_token: 'refresh-1', token_type: 'bearer' })
    render(<SocialLoginCallbackPage />)

    expect(screen.getByRole('status')).toHaveTextContent('Completing sign-in...')
    await waitFor(() => expect(replace).toHaveBeenCalledWith('/dashboard'))
    expect(mockedPost).toHaveBeenCalledWith('/auth/social/google/exchange', { code: 'abc', state: 'xyz' })
    expect(localStorage.getItem('token')).toBe('access-1')
    expect(localStorage.getItem('refresh_token')).toBe('refresh-1')
  })

  it('shows the provider error when the user cancels consent', async () => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { ...window.location, search: '?error=access_denied&error_description=User+cancelled', replace },
    })
    render(<SocialLoginCallbackPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Sign-in was cancelled: User cancelled')
    expect(mockedPost).not.toHaveBeenCalled()
  })

  it('asks the user to retry when the response is missing code or state', async () => {
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { ...window.location, search: '?code=abc', replace },
    })
    render(<SocialLoginCallbackPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('The sign-in response is incomplete')
    expect(mockedPost).not.toHaveBeenCalled()
  })

  it('confirms a mobile sign-in without storing tokens in the browser', async () => {
    mockedPost.mockResolvedValueOnce({ handoff: true })
    render(<SocialLoginCallbackPage />)

    expect(await screen.findByText('You are signed in')).toBeInTheDocument()
    expect(replace).not.toHaveBeenCalled()
    expect(localStorage.getItem('token')).toBeNull()
  })

  it('treats a response with no tokens and no handoff as a failed sign-in', async () => {
    mockedPost.mockResolvedValueOnce({})
    render(<SocialLoginCallbackPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('The sign-in response was incomplete')
    expect(replace).not.toHaveBeenCalled()
  })

  it('shows the server message and stores nothing when the exchange is rejected', async () => {
    mockedPost.mockRejectedValueOnce(new ApiError('Login state does not match this provider'))
    render(<SocialLoginCallbackPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Login state does not match this provider')
    expect(replace).not.toHaveBeenCalled()
    expect(localStorage.getItem('token')).toBeNull()
  })
})
