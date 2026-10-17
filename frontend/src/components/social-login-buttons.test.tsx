import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { SocialLoginButtons } from '@/components/social-login-buttons'
import { ApiClient } from '@/lib/api-client'

jest.mock('@/lib/api-client', () => ({ ApiClient: { get: jest.fn() } }))
const mockedGet = ApiClient.get as jest.Mock

describe('SocialLoginButtons', () => {
  const assign = jest.fn()
  const originalLocation = window.location

  beforeAll(() => {
    Object.defineProperty(window, 'location', { configurable: true, value: { ...originalLocation, assign } })
  })

  afterAll(() => {
    Object.defineProperty(window, 'location', { configurable: true, value: originalLocation })
  })

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders nothing when no provider is enabled', async () => {
    mockedGet.mockResolvedValueOnce([])
    const { container } = render(<SocialLoginButtons />)
    await waitFor(() => expect(mockedGet).toHaveBeenCalledWith('/auth/social/providers'))
    expect(container).toBeEmptyDOMElement()
  })

  it('renders a button for each enabled provider', async () => {
    mockedGet.mockResolvedValueOnce([
      { provider: 'google', display_name: 'Google' },
      { provider: 'github', display_name: 'GitHub' },
    ])
    render(<SocialLoginButtons />)
    expect(await screen.findByRole('button', { name: 'Continue with Google' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Continue with GitHub' })).toBeInTheDocument()
  })

  it('redirects the browser to the provider consent URL', async () => {
    mockedGet
      .mockResolvedValueOnce([{ provider: 'google', display_name: 'Google' }])
      .mockResolvedValueOnce({ authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?state=x' })
    render(<SocialLoginButtons />)
    fireEvent.click(await screen.findByRole('button', { name: 'Continue with Google' }))
    await waitFor(() =>
      expect(assign).toHaveBeenCalledWith('https://accounts.google.com/o/oauth2/v2/auth?state=x'),
    )
    expect(mockedGet).toHaveBeenLastCalledWith('/auth/social/google/authorize')
  })

  it('shows an error and re-enables the buttons when the consent URL cannot be created', async () => {
    mockedGet
      .mockResolvedValueOnce([{ provider: 'github', display_name: 'GitHub' }])
      .mockRejectedValueOnce(new Error('GitHub login is not enabled'))
    render(<SocialLoginButtons />)
    fireEvent.click(await screen.findByRole('button', { name: 'Continue with GitHub' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('GitHub login is not enabled')
    expect(screen.getByRole('button', { name: 'Continue with GitHub' })).toBeEnabled()
    expect(assign).not.toHaveBeenCalled()
  })

  it('hides itself when the provider list cannot be loaded', async () => {
    mockedGet.mockRejectedValueOnce(new Error('network down'))
    const { container } = render(<SocialLoginButtons />)
    await waitFor(() => expect(mockedGet).toHaveBeenCalled())
    await waitFor(() => expect(container).toBeEmptyDOMElement())
  })
})
