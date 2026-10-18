import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useSearchParams } from 'next/navigation'
import ResetPasswordPage from '@/app/auth/reset-password/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const mockedUseSearchParams = useSearchParams as jest.Mock

function withToken(token: string | null) {
  mockedUseSearchParams.mockReturnValue(new URLSearchParams(token === null ? '' : `token=${token}`))
}

function fill(password: string, confirm: string) {
  fireEvent.change(screen.getByLabelText('New password (min 8 characters)'), { target: { value: password } })
  fireEvent.change(screen.getByLabelText('Confirm new password'), { target: { value: confirm } })
  fireEvent.click(screen.getByRole('button', { name: 'Set new password' }))
}

describe('/auth/reset-password page', () => {
  afterEach(() => {
    mockedUseSearchParams.mockReturnValue(new URLSearchParams())
  })

  it('explains that the link needs its token when none is given', () => {
    withToken(null)
    renderWithQuery(<ResetPasswordPage />)

    expect(screen.getByRole('alert')).toHaveTextContent('This link is missing its reset token.')
  })

  it('sets the new password with the token from the link', async () => {
    withToken('reset-token')
    const fetchMock = mockFetch({ 'POST /auth/reset-password': { message: 'Password reset successfully' } })
    renderWithQuery(<ResetPasswordPage />)

    fill('secret123', 'secret123')

    expect(await screen.findByRole('status')).toHaveTextContent('Your password has been reset. You can sign in now.')
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/auth/reset-password') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      token: 'reset-token',
      new_password: 'secret123',
      password_confirm: 'secret123',
    })
  })

  it('refuses a short or mismatched password before sending anything', () => {
    withToken('reset-token')
    const fetchMock = mockFetch({})
    renderWithQuery(<ResetPasswordPage />)

    fill('short', 'short')
    expect(screen.getByRole('alert')).toHaveTextContent('Password must be at least 8 characters')

    fill('secret123', 'secret999')
    expect(screen.getByRole('alert')).toHaveTextContent('Passwords do not match')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('shows the server reason when the link has expired', async () => {
    withToken('old-token')
    mockFetch({ 'POST /auth/reset-password': reply({ detail: 'Reset token expired' }, 401) })
    renderWithQuery(<ResetPasswordPage />)

    fill('secret123', 'secret123')

    expect(await screen.findByRole('alert')).toHaveTextContent('Reset token expired')
  })

  it('falls back to a generic message when the failure has no reason', async () => {
    withToken('reset-token')
    global.fetch = jest.fn().mockRejectedValue(new Error('Failed to fetch')) as unknown as typeof fetch
    renderWithQuery(<ResetPasswordPage />)

    fill('secret123', 'secret123')

    await waitFor(() =>
      expect(screen.getByRole('alert')).toHaveTextContent('The password could not be reset. The link may have expired.')
    )
  })
})
