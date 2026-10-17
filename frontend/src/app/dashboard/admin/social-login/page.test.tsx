import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import SocialLoginAdminPage from '@/app/dashboard/admin/social-login/page'
import { ApiClient } from '@/lib/api-client'

jest.mock('@/lib/api-client', () => ({ ApiClient: { get: jest.fn(), put: jest.fn() } }))
const mockedGet = ApiClient.get as jest.Mock
const mockedPut = ApiClient.put as jest.Mock

const providers = [
  {
    provider: 'google', display_name: 'Google', enabled: true, client_id: 'g-id', client_secret_set: true,
    redirect_uri: 'https://app.test/auth/social/google/callback', scopes: 'openid email profile', updated_at: null,
  },
  {
    provider: 'github', display_name: 'GitHub', enabled: false, client_id: null, client_secret_set: false,
    redirect_uri: null, scopes: 'read:user user:email', updated_at: null,
  },
]

describe('/dashboard/admin/social-login page', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    mockedGet.mockResolvedValue(providers)
  })

  it('lists each provider with its configuration and never shows a stored secret', async () => {
    render(<SocialLoginAdminPage />)
    expect(await screen.findByRole('heading', { name: 'Google' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'GitHub' })).toBeInTheDocument()
    expect(screen.getByDisplayValue('g-id')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Stored. Type a new value to replace it.')).toHaveValue('')
    expect(screen.getByText('Enabled: shown on the sign-in page')).toBeInTheDocument()
    expect(screen.getByText('Disabled: hidden from the sign-in page')).toBeInTheDocument()
  })

  it('saves credentials and omits the secret when none was typed', async () => {
    mockedPut.mockResolvedValueOnce({ ...providers[0], scopes: 'openid' })
    render(<SocialLoginAdminPage />)
    await screen.findByRole('heading', { name: 'Google' })

    fireEvent.change(screen.getAllByRole('textbox')[0], { target: { value: 'g-id-2' } })
    fireEvent.click(screen.getAllByRole('button', { name: 'Save' })[0])

    await waitFor(() => expect(mockedPut).toHaveBeenCalledTimes(1))
    const [endpoint, body] = mockedPut.mock.calls[0]
    expect(endpoint).toBe('/admin/social-providers/google')
    expect(body).toEqual({
      enabled: true,
      client_id: 'g-id-2',
      redirect_uri: 'https://app.test/auth/social/google/callback',
      scopes: 'openid email profile',
    })
    expect(body).not.toHaveProperty('client_secret')
    expect(await screen.findByText('Saved.')).toBeInTheDocument()
  })

  it('sends a new secret only when the administrator typed one', async () => {
    mockedPut.mockResolvedValueOnce({ ...providers[1], enabled: true, client_id: 'gh', client_secret_set: true })
    render(<SocialLoginAdminPage />)
    await screen.findByRole('heading', { name: 'GitHub' })

    fireEvent.click(screen.getByRole('checkbox', { name: /Enable GitHub/ }))
    fireEvent.change(screen.getByLabelText('Client secret', { selector: '#github-client-secret' }), {
      target: { value: 'new-secret' },
    })
    fireEvent.change(screen.getByLabelText('Client ID', { selector: '#github-client-id' }), { target: { value: 'gh' } })
    fireEvent.click(screen.getAllByRole('button', { name: 'Save' })[1])

    await waitFor(() => expect(mockedPut).toHaveBeenCalled())
    expect(mockedPut.mock.calls[0][1]).toMatchObject({ enabled: true, client_secret: 'new-secret', client_id: 'gh' })
    await waitFor(() => expect(screen.getByLabelText('Client secret', { selector: '#github-client-secret' })).toHaveValue(''))
  })

  it('shows the server validation message when enabling without credentials is refused', async () => {
    mockedPut.mockRejectedValueOnce(new Error('Cannot enable GitHub: missing client_id, client_secret, redirect_uri'))
    render(<SocialLoginAdminPage />)
    await screen.findByRole('heading', { name: 'GitHub' })

    fireEvent.click(screen.getByRole('checkbox', { name: /Enable GitHub/ }))
    fireEvent.click(screen.getAllByRole('button', { name: 'Save' })[1])

    expect(await screen.findByRole('alert')).toHaveTextContent('Cannot enable GitHub: missing client_id')
  })

  it('shows a load error when the providers cannot be fetched', async () => {
    mockedGet.mockRejectedValueOnce(new Error('Admin access required'))
    render(<SocialLoginAdminPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Admin access required')
  })
})
