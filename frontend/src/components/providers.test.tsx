import { act, render, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import { Providers } from '@/components/providers'
import { useAuth } from '@/hooks/useAuth'
import { ApiClient } from '@/lib/api-client'
import { mockFetch, reply, testUser } from '@/test-utils'

// Reads the session from the real provider so each test can assert on what users see.
function SessionProbe() {
  const auth = useAuth()
  return (
    <div>
      <span data-testid="token">{auth.token ?? 'none'}</span>
      <span data-testid="loading">{String(auth.loading)}</span>
      <span data-testid="user">{auth.user?.email ?? 'anonymous'}</span>
      <button onClick={() => auth.logout()}>logout</button>
      <button onClick={() => auth.login('editor@example.com', 'secret123').catch(() => undefined)}>
        login
      </button>
      <button
        onClick={() =>
          auth.signup({
            email: 'new@example.com',
            password: 'secret123',
            first_name: 'New',
            last_name: 'User',
          }).catch(() => undefined)
        }
      >
        signup
      </button>
    </div>
  )
}

const tokens = { access_token: 'access-1', refresh_token: 'refresh-1', token_type: 'bearer' }

function renderProviders() {
  return render(
    <Providers>
      <SessionProbe />
    </Providers>
  )
}

describe('Providers (auth session)', () => {
  beforeEach(() => {
    ApiClient.setToken(null)
  })

  it('starts signed out and does not call the API when nothing is stored', async () => {
    const fetchMock = mockFetch({})
    renderProviders()

    await waitFor(() => expect(screen.getByTestId('loading')).toHaveTextContent('false'))
    expect(screen.getByTestId('token')).toHaveTextContent('none')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('restores a stored session through /auth/me', async () => {
    localStorage.setItem('token', 'stored-token')
    const fetchMock = mockFetch({ 'GET /auth/me': testUser })
    renderProviders()

    await waitFor(() => expect(screen.getByTestId('user')).toHaveTextContent(testUser.email))
    expect(screen.getByTestId('token')).toHaveTextContent('stored-token')

    const [url, init] = fetchMock.mock.calls[0]
    expect(String(url)).toMatch(/\/api\/v1\/auth\/me$/)
    expect(init.headers).toMatchObject({ Authorization: 'Bearer stored-token' })
  })

  it('signs out and clears the stored token when /auth/me rejects it', async () => {
    localStorage.setItem('token', 'expired-token')
    mockFetch({ 'GET /auth/me': reply({ detail: 'Token expired' }, 401) })
    renderProviders()

    await waitFor(() => expect(screen.getByTestId('loading')).toHaveTextContent('false'))
    expect(screen.getByTestId('token')).toHaveTextContent('none')
    expect(localStorage.getItem('token')).toBeNull()
  })

  it('stores both tokens, loads the user, and opens the dashboard on login', async () => {
    const fetchMock = mockFetch({
      'POST /auth/login': tokens,
      'GET /auth/me': testUser,
    })
    renderProviders()
    await waitFor(() => expect(screen.getByTestId('loading')).toHaveTextContent('false'))

    act(() => screen.getByRole('button', { name: 'login' }).click())

    await waitFor(() => expect(screen.getByTestId('user')).toHaveTextContent(testUser.email))
    expect(localStorage.getItem('token')).toBe('access-1')
    expect(localStorage.getItem('refresh_token')).toBe('refresh-1')
    expect(useRouter().push).toHaveBeenCalledWith('/dashboard')

    const loginCall = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/auth/login'))
    expect(JSON.parse(loginCall![1].body as string)).toEqual({
      email: 'editor@example.com',
      password: 'secret123',
    })
  })

  it('stays signed out when login is rejected', async () => {
    mockFetch({ 'POST /auth/login': reply({ detail: 'Invalid credentials' }, 401) })
    renderProviders()
    await waitFor(() => expect(screen.getByTestId('loading')).toHaveTextContent('false'))

    act(() => screen.getByRole('button', { name: 'login' }).click())

    await waitFor(() => expect(localStorage.getItem('token')).toBeNull())
    expect(screen.getByTestId('token')).toHaveTextContent('none')
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('sends the full registration payload on signup, including password confirmation', async () => {
    const fetchMock = mockFetch({
      'POST /auth/register': tokens,
      'GET /auth/me': testUser,
    })
    renderProviders()
    await waitFor(() => expect(screen.getByTestId('loading')).toHaveTextContent('false'))

    act(() => screen.getByRole('button', { name: 'signup' }).click())

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard'))
    const registerCall = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/auth/register'))
    expect(JSON.parse(registerCall![1].body as string)).toEqual({
      email: 'new@example.com',
      password: 'secret123',
      password_confirm: 'secret123',
      first_name: 'New',
      last_name: 'User',
    })
    expect(localStorage.getItem('token')).toBe('access-1')
  })

  it('clears every stored credential and returns to the login page on logout', async () => {
    localStorage.setItem('token', 'stored-token')
    localStorage.setItem('refresh_token', 'refresh-1')
    localStorage.setItem('tenant_id', '20')
    mockFetch({ 'GET /auth/me': testUser })
    renderProviders()
    await waitFor(() => expect(screen.getByTestId('user')).toHaveTextContent(testUser.email))

    act(() => screen.getByRole('button', { name: 'logout' }).click())

    expect(screen.getByTestId('token')).toHaveTextContent('none')
    expect(localStorage.getItem('token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
    expect(localStorage.getItem('tenant_id')).toBeNull()
    expect(useRouter().push).toHaveBeenCalledWith('/auth/login')
  })
})
