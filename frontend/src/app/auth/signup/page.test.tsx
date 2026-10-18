import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import SignupPage from '@/app/auth/signup/page'
import { buildAuth, mockFetch, renderWithAuth } from '@/test-utils'

interface SignupValues {
  first?: string
  last?: string
  email?: string
  password?: string
  confirm?: string
}

function fillForm({ first = 'Jane', last = 'Public', email = 'jane@example.com', password = 'secret123', confirm }: SignupValues = {}) {
  fireEvent.change(screen.getByLabelText('First name'), { target: { value: first } })
  fireEvent.change(screen.getByLabelText('Last name'), { target: { value: last } })
  fireEvent.change(screen.getByLabelText('Email address'), { target: { value: email } })
  fireEvent.change(screen.getByLabelText('Password (min 8 characters)'), { target: { value: password } })
  fireEvent.change(screen.getByLabelText('Confirm password'), { target: { value: confirm ?? password } })
}

const submit = () => fireEvent.click(screen.getByRole('button', { name: 'Create account' }))

describe('/auth/signup page', () => {
  beforeEach(() => {
    mockFetch({ 'GET /auth/social/providers': [] })
  })

  it('renders every account field, the sign-in link and no social buttons when none are enabled', async () => {
    renderWithAuth(<SignupPage />)

    expect(screen.getByRole('heading', { name: 'Create Account' })).toBeInTheDocument()
    expect(screen.getByLabelText('First name')).toBeRequired()
    expect(screen.getByLabelText('Last name')).toBeRequired()
    expect(screen.getByLabelText('Confirm password')).toBeRequired()
    expect(screen.getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login')
    await waitFor(() => expect(screen.queryByRole('button', { name: /Continue with/ })).not.toBeInTheDocument())
  })

  it('offers each enabled social provider as a sign-in option', async () => {
    mockFetch({ 'GET /auth/social/providers': [{ provider: 'google', display_name: 'Google' }] })
    renderWithAuth(<SignupPage />)

    expect(await screen.findByRole('button', { name: /Google/ })).toBeInTheDocument()
  })

  it('creates the account with the names and email entered', async () => {
    const auth = buildAuth({ signup: jest.fn().mockResolvedValue({}) })
    renderWithAuth(<SignupPage />, auth)

    fillForm({ first: 'Jane', last: 'Q Public' })
    submit()

    // Opening the session (and the dashboard) is the auth context's job; this page only sends the account.
    await waitFor(() => expect(auth.signup).toHaveBeenCalledWith({
      email: 'jane@example.com',
      password: 'secret123',
      first_name: 'Jane',
      last_name: 'Q Public',
    }))
  })

  it('rejects a password shorter than 8 characters before any request is made', () => {
    const auth = buildAuth({ signup: jest.fn() })
    renderWithAuth(<SignupPage />, auth)

    fillForm({ password: 'short' })
    submit()

    expect(screen.getByRole('alert')).toHaveTextContent('Password must be at least 8 characters')
    expect(auth.signup).not.toHaveBeenCalled()
  })

  it('rejects a confirmation that does not match before any request is made', () => {
    const auth = buildAuth({ signup: jest.fn() })
    renderWithAuth(<SignupPage />, auth)

    fillForm({ confirm: 'secret999' })
    submit()

    expect(screen.getByRole('alert')).toHaveTextContent('Passwords do not match')
    expect(auth.signup).not.toHaveBeenCalled()
  })

  it('shows the confirmation message when the account needs its email confirmed', async () => {
    const auth = buildAuth({ signup: jest.fn().mockResolvedValue({ requires_verification: true }) })
    renderWithAuth(<SignupPage />, auth)

    fillForm({ email: 'new@example.com' })
    submit()

    expect(await screen.findByRole('heading', { name: 'Check your email' })).toBeInTheDocument()
    expect(screen.getByText('new@example.com')).toBeInTheDocument()
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('shows the error returned by the server and does not navigate', async () => {
    const auth = buildAuth({ signup: jest.fn().mockRejectedValue(new Error('Email already registered')) })
    renderWithAuth(<SignupPage />, auth)

    fillForm({ email: 'taken@example.com' })
    submit()

    expect(await screen.findByText('Email already registered')).toBeInTheDocument()
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('falls back to a generic message when the failure has no message', async () => {
    const auth = buildAuth({ signup: jest.fn().mockRejectedValue({}) })
    renderWithAuth(<SignupPage />, auth)

    fillForm()
    submit()

    expect(await screen.findByText('Registration failed')).toBeInTheDocument()
  })

  it('disables the button while the account is being created', () => {
    const auth = buildAuth({ signup: jest.fn(() => new Promise(() => undefined)) })
    renderWithAuth(<SignupPage />, auth)

    fillForm()
    submit()

    expect(screen.getByRole('button', { name: 'Creating account...' })).toBeDisabled()
  })
})
