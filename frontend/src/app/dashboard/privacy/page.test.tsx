import { fireEvent, screen, waitFor } from '@testing-library/react'
import PrivacyPage from '@/app/dashboard/privacy/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const settings = { profile_visibility: 'public', content_visibility: 'public', allow_analytics: true, allow_marketing: false }
const consents = [{ id: 1, consent_type: 'analytics', granted: true, version: null }]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /privacy/settings': settings,
    'GET /privacy/consents': consents,
    ...extra,
  })
}

describe('/dashboard/privacy page', () => {
  it('shows the saved privacy preferences and the consent history', async () => {
    base()
    renderWithQuery(<PrivacyPage />)

    expect(await screen.findAllByDisplayValue('Public')).toHaveLength(2)
    expect(screen.getByLabelText('Allow analytics tracking')).toBeChecked()
    expect(screen.getByLabelText('Allow marketing emails')).not.toBeChecked()
    expect(await screen.findByText('analytics')).toBeInTheDocument()
    expect(screen.getByText(/granted/)).toBeInTheDocument()
  })

  it('saves the preferences and records the consent decisions', async () => {
    const fetchMock = base({
      'PUT /privacy/settings': { ...settings, profile_visibility: 'private' },
      'POST /privacy/consent-log': { id: 2, consent_type: 'analytics', granted: true },
    })
    renderWithQuery(<PrivacyPage />)
    await screen.findAllByDisplayValue('Public')

    fireEvent.change(screen.getAllByRole('combobox')[0], { target: { value: 'private' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save Changes' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Privacy preferences saved.')
    const put = fetchMock.mock.calls.find(([url, init]) => String(url).includes('/privacy/settings?') && init?.method === 'PUT')
    expect(String(put![0])).toContain('profile_visibility=private')
    expect(String(put![0])).toContain('allow_analytics=true')
    expect(String(put![0])).toContain('allow_marketing=false')
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('consent_type=analytics&granted=true'))).toBe(true)
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('consent_type=marketing&granted=false'))).toBe(true)
  })

  it('downloads a copy of the personal data', async () => {
    base({ 'GET /privacy/export': { account: { email: 'editor@example.com' } } })
    const createObjectURL = jest.fn(() => 'blob:export')
    const revokeObjectURL = jest.fn()
    global.URL.createObjectURL = createObjectURL as unknown as typeof URL.createObjectURL
    global.URL.revokeObjectURL = revokeObjectURL
    renderWithQuery(<PrivacyPage />)
    await screen.findAllByDisplayValue('Public')

    fireEvent.click(screen.getByRole('button', { name: 'Export Data' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Your data export has been downloaded.')
    expect(createObjectURL).toHaveBeenCalled()
    expect(revokeObjectURL).toHaveBeenCalledWith('blob:export')
  })

  it('records a deletion request and shows when it is scheduled', async () => {
    base({ 'POST /privacy/request-deletion': { id: 3, status: 'pending', scheduled_for: '2026-11-16T00:00:00Z' } })
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(true)
    renderWithQuery(<PrivacyPage />)
    await screen.findAllByDisplayValue('Public')

    fireEvent.click(screen.getByRole('button', { name: 'Request Account Deletion' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Deletion scheduled for')
    confirm.mockRestore()
  })

  it('does nothing when the deletion is not confirmed', async () => {
    const fetchMock = base()
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(false)
    renderWithQuery(<PrivacyPage />)
    await screen.findAllByDisplayValue('Public')

    fireEvent.click(screen.getByRole('button', { name: 'Request Account Deletion' }))

    await waitFor(() => expect(confirm).toHaveBeenCalled())
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/privacy/request-deletion'))).toBe(false)
    confirm.mockRestore()
  })

  it('shows the server reason when the settings cannot be loaded', async () => {
    base({ 'GET /privacy/settings': reply({ detail: 'Privacy is unavailable' }, 503) })
    renderWithQuery(<PrivacyPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Privacy is unavailable')
  })

  it('says when no consent decisions are recorded', async () => {
    base({ 'GET /privacy/consents': [] })
    renderWithQuery(<PrivacyPage />)

    expect(await screen.findByText('No consent decisions recorded yet.')).toBeInTheDocument()
  })
})
