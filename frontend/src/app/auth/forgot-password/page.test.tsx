import { fireEvent, screen } from '@testing-library/react'
import ForgotPasswordPage from '@/app/auth/forgot-password/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

describe('/auth/forgot-password page', () => {
  it('asks for the account email and shows the server confirmation', async () => {
    const fetchMock = mockFetch({
      'POST /auth/forgot-password': { message: 'If email exists, password reset link has been sent' },
    })
    renderWithQuery(<ForgotPasswordPage />)

    fireEvent.change(screen.getByLabelText('Email address'), { target: { value: ' editor@example.com ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send reset link' }))

    expect(await screen.findByRole('status')).toHaveTextContent('If email exists, password reset link has been sent')
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/auth/forgot-password') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({ email: 'editor@example.com' })
  })

  it('shows the server reason when the request fails', async () => {
    mockFetch({ 'POST /auth/forgot-password': reply({ detail: 'Too many requests' }, 429) })
    renderWithQuery(<ForgotPasswordPage />)

    fireEvent.change(screen.getByLabelText('Email address'), { target: { value: 'editor@example.com' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send reset link' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Too many requests')
  })

  it('links back to sign-in', () => {
    renderWithQuery(<ForgotPasswordPage />)

    expect(screen.getByRole('link', { name: 'Back to sign in' })).toHaveAttribute('href', '/auth/login')
  })
})
