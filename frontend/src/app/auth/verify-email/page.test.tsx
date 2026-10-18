import { render, screen, waitFor } from '@testing-library/react'
import { useSearchParams } from 'next/navigation'
import VerifyEmailPage from '@/app/auth/verify-email/page'
import { mockFetch, reply } from '@/test-utils'

const mockedUseSearchParams = useSearchParams as jest.Mock

function withToken(token: string | null) {
  mockedUseSearchParams.mockReturnValue(new URLSearchParams(token === null ? '' : `token=${token}`))
}

describe('/auth/verify-email page', () => {
  afterEach(() => {
    mockedUseSearchParams.mockReturnValue(new URLSearchParams())
  })

  it('explains that the link is incomplete when there is no token and makes no request', () => {
    withToken(null)
    const fetchMock = mockFetch({})
    render(<VerifyEmailPage />)

    expect(screen.getByRole('alert')).toHaveTextContent('This link is missing its confirmation token.')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('shows the confirming state while the token is checked', () => {
    withToken('abc')
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<VerifyEmailPage />)

    expect(screen.getByText('Confirming your address…')).toBeInTheDocument()
  })

  it('confirms the address with the token and links to sign-in', async () => {
    withToken('abc')
    const fetchMock = mockFetch({ 'POST /auth/verify-email': { message: 'verified' } })
    render(<VerifyEmailPage />)

    expect(await screen.findByText('Your email is confirmed. You can sign in now.')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login')
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/auth/verify-email') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({ token: 'abc' })
  })

  it('shows the server reason when the link has expired', async () => {
    withToken('old')
    mockFetch({ 'POST /auth/verify-email': reply({ detail: 'Verification link has expired' }, 400) })
    render(<VerifyEmailPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Verification link has expired')
    expect(screen.getByRole('link', { name: 'Create an account again' })).toHaveAttribute('href', '/auth/signup')
  })

  it('shows a generic message when the request cannot reach the server', async () => {
    withToken('abc')
    global.fetch = jest.fn().mockRejectedValue(new Error('Failed to fetch')) as unknown as typeof fetch
    render(<VerifyEmailPage />)

    await waitFor(() =>
      expect(screen.getByRole('alert')).toHaveTextContent('We could not confirm this address. The link may have expired.')
    )
  })
})
