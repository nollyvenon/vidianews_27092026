import { fireEvent, screen, waitFor } from '@testing-library/react'
import SecurityPage from '@/app/dashboard/security/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const auditLogs = [
  { id: 1, user_id: 4, action: 'login', resource_type: 'session', status: 'success', ip_address: '10.0.0.2', severity: 'info', created_at: '2026-10-17T10:00:00Z' },
  { id: 2, user_id: 9, action: 'password_reset', resource_type: null, status: null, ip_address: null, severity: 'warning', created_at: '2026-10-16T10:00:00Z' },
]
const limits = [{ id: 1, endpoint: '/api/v1/content', requests_per_minute: 60, requests_per_hour: 1000, requests_per_day: 10000, burst_limit: 100 }]
const providers = [
  { provider: 'google', display_name: 'Google', enabled: false, client_id: null, client_secret_set: false, redirect_uri: null },
]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /security/audit-logs': auditLogs,
    'GET /rate-limits/configs': limits,
    'GET /admin/social-providers': providers,
    'GET /auth/mfa': { enabled: false },
    ...extra,
  })
}

function bodyOf(fetchMock: jest.Mock, method: string, suffix: string) {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
  return JSON.parse(call![1].body as string)
}

describe('/dashboard/security page', () => {
  it('lists the security events with their user, status, severity and address', async () => {
    base()
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('login (session)')).toBeInTheDocument()
    expect(screen.getByText('success')).toBeInTheDocument()
    expect(screen.getByText('10.0.0.2')).toBeInTheDocument()
    expect(screen.getByText('password_reset')).toBeInTheDocument()
    expect(screen.getByText('#9')).toBeInTheDocument()
  })

  it('says when no security events have been recorded', async () => {
    base({ 'GET /security/audit-logs': [] })
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('No security events recorded yet.')).toBeInTheDocument()
  })

  it('shows the server reason when the audit log cannot be loaded', async () => {
    base({ 'GET /security/audit-logs': reply({ detail: 'Admin access required' }, 403) })
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('Admin access required')).toBeInTheDocument()
  })

  it('lists the configured rate limits and saves a new one for an endpoint', async () => {
    const fetchMock = base({ 'POST /rate-limits/config': { id: 2 } })
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('/api/v1/content')).toBeInTheDocument()
    expect(screen.getByText(/60\/min/)).toBeInTheDocument()
    fireEvent.change(screen.getByLabelText('Endpoint'), { target: { value: '/api/v1/orders' } })
    fireEvent.change(screen.getByLabelText('Requests per minute'), { target: { value: '120' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save limit' }))

    await waitFor(() => expect(bodyOf(fetchMock, 'POST', '/rate-limits/config')).toEqual({ endpoint: '/api/v1/orders', requests_per_minute: 120 }))
  })

  it('explains that rate limits are for administrators only', async () => {
    base({ 'GET /rate-limits/configs': reply({ detail: 'Admin access required' }, 403) })
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('Admin access required')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Save limit' })).not.toBeInTheDocument()
  })

  it('turns a sign-in provider on and shows the server reason when it is not configured', async () => {
    const fetchMock = base({
      'PUT /admin/social-providers/google': reply({ detail: 'Enabling a provider requires client_id, client_secret and redirect_uri' }, 422),
    })
    renderWithQuery(<SecurityPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Disabled — enable' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Enabling a provider requires client_id, client_secret and redirect_uri')
    expect(bodyOf(fetchMock, 'PUT', '/admin/social-providers/google')).toEqual({ enabled: true })
  })

  it('shows the two-factor status and the setup secret, then turns the factor on with a code', async () => {
    const fetchMock = base({
      'POST /auth/mfa/setup': { secret: 'JBSWY3DPEHPK3PXP', otpauth_uri: 'otpauth://totp/AetherCMS%20AI:x?secret=JBSWY3DPEHPK3PXP' },
      'POST /auth/mfa/enable': { enabled: true },
    })
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('Disabled')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Set up 2FA' }))
    expect(await screen.findByTestId('mfa-secret')).toHaveTextContent('JBSWY3DPEHPK3PXP')
    fireEvent.change(screen.getByLabelText('Authentication code'), { target: { value: '123456' } })
    fireEvent.click(screen.getByRole('button', { name: 'Turn on 2FA' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Two-factor authentication is on.')
    expect(bodyOf(fetchMock, 'POST', '/auth/mfa/enable')).toEqual({ code: '123456' })
  })

  it('turns the factor off with a current code when it is on', async () => {
    const fetchMock = base({
      'GET /auth/mfa': { enabled: true },
      'POST /auth/mfa/disable': { enabled: false },
    })
    renderWithQuery(<SecurityPage />)

    expect(await screen.findByText('Enabled')).toBeInTheDocument()
    fireEvent.change(screen.getByLabelText('Authentication code'), { target: { value: '654321' } })
    fireEvent.click(screen.getByRole('button', { name: 'Disable 2FA' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Two-factor authentication is off.')
    expect(bodyOf(fetchMock, 'POST', '/auth/mfa/disable')).toEqual({ code: '654321' })
  })

  it('shows the server reason when the authenticator code is rejected', async () => {
    base({
      'POST /auth/mfa/setup': { secret: 'JBSWY3DPEHPK3PXP', otpauth_uri: 'otpauth://totp/x' },
      'POST /auth/mfa/enable': reply({ detail: 'Invalid authentication code' }, 422),
    })
    renderWithQuery(<SecurityPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Set up 2FA' }))
    await screen.findByTestId('mfa-secret')
    fireEvent.change(screen.getByLabelText('Authentication code'), { target: { value: '000000' } })
    fireEvent.click(screen.getByRole('button', { name: 'Turn on 2FA' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid authentication code')
  })
})
