import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import LoginPage from '@/app/auth/login/page'
import { buildAuth, renderWithAuth } from '@/test-utils'

function fillCredentials(email: string, password: string) {
  fireEvent.change(screen.getByPlaceholderText('your@email.com'), { target: { value: email } })
  fireEvent.change(screen.getByPlaceholderText('••••••••'), { target: { value: password } })
}

describe('/auth/login page', () => {
  it('renders the sign-in form and its navigation links', () => {
    renderWithAuth(<LoginPage />)

    expect(screen.getByRole('heading', { name: 'VidiNews' })).toBeInTheDocument()
    expect(screen.getByPlaceholderText('your@email.com')).toHaveAttribute('type', 'email')
    expect(screen.getByPlaceholderText('••••••••')).toHaveAttribute('type', 'password')
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeEnabled()
    expect(screen.getByRole('link', { name: 'Sign up' })).toHaveAttribute('href', '/auth/signup')
    expect(screen.getByRole('link', { name: 'Forgot password?' })).toHaveAttribute(
      'href',
      '/auth/forgot-password'
    )
  })

  it('signs in with the entered credentials and opens the dashboard', async () => {
    const auth = buildAuth({ login: jest.fn().mockResolvedValue({}) })
    renderWithAuth(<LoginPage />, auth)

    fillCredentials('editor@example.com', 'secret123')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard'))
    expect(auth.login).toHaveBeenCalledWith('editor@example.com', 'secret123', undefined)
  })

  it('shows the server error message and stays on the page when sign-in fails', async () => {
    const auth = buildAuth({ login: jest.fn().mockRejectedValue(new Error('Invalid credentials')) })
    renderWithAuth(<LoginPage />, auth)

    fillCredentials('editor@example.com', 'wrong-password')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByText('Invalid credentials')).toBeInTheDocument()
    expect(useRouter().push).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeEnabled()
  })

  it('falls back to a generic message when the failure has no message', async () => {
    const auth = buildAuth({ login: jest.fn().mockRejectedValue({}) })
    renderWithAuth(<LoginPage />, auth)

    fillCredentials('editor@example.com', 'secret123')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByText('Login failed')).toBeInTheDocument()
  })

  it('disables the submit button while the request is in flight', () => {
    const auth = buildAuth({ login: jest.fn(() => new Promise(() => undefined)) })
    renderWithAuth(<LoginPage />, auth)

    fillCredentials('editor@example.com', 'secret123')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    const pending = screen.getByRole('button', { name: 'Signing in...' })
    expect(pending).toBeDisabled()
  })

  it('asks for the authenticator code when the account requires it, then signs in with that code', async () => {
    const login = jest.fn().mockRejectedValueOnce(new Error('MFA code required')).mockResolvedValueOnce({})
    renderWithAuth(<LoginPage />, buildAuth({ login }))

    fillCredentials('editor@example.com', 'secret123')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByText('Enter the 6-digit code from your authenticator app.')).toBeInTheDocument()
    fireEvent.change(screen.getByLabelText('Authentication code'), { target: { value: '12a3456' } })
    expect(screen.getByLabelText('Authentication code')).toHaveValue('123456')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard'))
    expect(login).toHaveBeenLastCalledWith('editor@example.com', 'secret123', '123456')
  })

  it('shows the server reason when the authenticator code is wrong', async () => {
    const login = jest
      .fn()
      .mockRejectedValueOnce(new Error('MFA code required'))
      .mockRejectedValueOnce(new Error('Invalid authentication code'))
    renderWithAuth(<LoginPage />, buildAuth({ login }))

    fillCredentials('editor@example.com', 'secret123')
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    await screen.findByLabelText('Authentication code')
    fireEvent.change(screen.getByLabelText('Authentication code'), { target: { value: '000000' } })
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid authentication code')
    expect(useRouter().push).not.toHaveBeenCalled()
  })
})
