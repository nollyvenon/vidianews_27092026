import { fireEvent, screen, waitFor } from '@testing-library/react'
import SettingsPage from '@/app/dashboard/settings/page'
import { buildAuth, mockFetch, reply, renderWithAuth, testUser } from '@/test-utils'

const settings = {
  notifications: {
    email_on_activity: true, email_on_mention: false, email_on_message: true, email_digest: 'daily',
    push_enabled: false, push_on_activity: false, push_on_message: true,
    inapp_enabled: true, inapp_sound: false, dnd_enabled: false, dnd_start_time: null, dnd_end_time: null,
  },
  privacy: {
    profile_visibility: 'public', show_email: false, show_phone: false, show_activity: true, show_last_seen: true,
    allow_messages: 'friends_only', allow_search: true, allow_analytics: true, allow_marketing_emails: false, allow_third_party_sharing: false,
  },
  display: {
    theme: 'light', language: 'en', timezone: 'UTC', date_format: 'YYYY-MM-DD', time_format: '24h',
    sidebar_collapsed: false, compact_mode: false, animations_enabled: true, font_size: 'medium',
  },
}
const profile = { bio: 'Hello', title: 'Editor', location: 'Paris', timezone: 'UTC', is_public: true }

function loadRoutes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /settings/me': settings,
    'GET /profiles/me': profile,
    ...extra,
  })
}

function bodyOf(fetchMock: jest.Mock, method: string, suffix: string) {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
  return JSON.parse(call![1].body as string)
}

async function ready() {
  await screen.findByRole('heading', { name: 'Settings' })
}

describe('/dashboard/settings page', () => {
  it('shows a loading state, then every notification preference', async () => {
    loadRoutes()
    renderWithAuth(<SettingsPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    await ready()
    expect(screen.getByRole('checkbox', { name: /Activity email notifications/ })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: /Mention email notifications/ })).not.toBeChecked()
    expect(screen.getByRole('checkbox', { name: /Push notifications/ })).not.toBeChecked()
    expect(screen.getByRole('checkbox', { name: /In-app notifications/ })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: /Do not disturb/ })).not.toBeChecked()
    expect(screen.getByDisplayValue('Daily')).toBeInTheDocument()
  })

  it('saves every notification preference and reloads the saved values', async () => {
    const fetchMock = loadRoutes({ 'PUT /settings/me/notifications': { push_enabled: true } })
    renderWithAuth(<SettingsPage />)
    await ready()

    fireEvent.click(screen.getByRole('checkbox', { name: /Push notifications/ }))
    fireEvent.change(screen.getByDisplayValue('Daily'), { target: { value: 'weekly' } })
    fireEvent.change(screen.getByLabelText('Do not disturb from'), { target: { value: '22:00' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save notifications' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Settings saved')
    expect(bodyOf(fetchMock, 'PUT', '/settings/me/notifications')).toEqual({
      email_on_activity: true, email_on_mention: false, email_on_message: true, email_digest: 'weekly',
      push_enabled: true, push_on_activity: false, push_on_message: true,
      inapp_enabled: true, inapp_sound: false, dnd_enabled: false, dnd_start_time: '22:00', dnd_end_time: null,
    })
    expect(fetchMock.mock.calls.filter(([url, init]) => String(url).endsWith('/settings/me') && init?.method === 'GET').length).toBeGreaterThanOrEqual(2)
  })

  it('switches to the privacy tab and saves every privacy choice', async () => {
    const fetchMock = loadRoutes({ 'PUT /settings/me/privacy': { profile_visibility: 'private' } })
    renderWithAuth(<SettingsPage />)
    await ready()

    fireEvent.click(screen.getByRole('button', { name: 'privacy' }))
    fireEvent.change(screen.getByDisplayValue('Public'), { target: { value: 'private' } })
    fireEvent.change(screen.getByDisplayValue('Friends only'), { target: { value: 'nobody' } })
    fireEvent.click(screen.getByRole('checkbox', { name: /Show email on profile/ }))
    fireEvent.click(screen.getByRole('button', { name: 'Save privacy' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Settings saved')
    expect(bodyOf(fetchMock, 'PUT', '/settings/me/privacy')).toEqual({
      profile_visibility: 'private', show_email: true, show_phone: false, show_activity: true, show_last_seen: true,
      allow_messages: 'nobody', allow_search: true, allow_analytics: true, allow_marketing_emails: false, allow_third_party_sharing: false,
    })
  })

  it('changes the display preferences and saves them', async () => {
    const fetchMock = loadRoutes({ 'PUT /settings/me/display': { theme: 'dark' } })
    renderWithAuth(<SettingsPage />)
    await ready()

    fireEvent.click(screen.getByRole('button', { name: 'display' }))
    fireEvent.change(screen.getByDisplayValue('Light'), { target: { value: 'dark' } })
    fireEvent.change(screen.getByDisplayValue('English'), { target: { value: 'fr' } })
    fireEvent.change(screen.getByDisplayValue('24-hour'), { target: { value: '12h' } })
    fireEvent.change(screen.getByDisplayValue('Medium'), { target: { value: 'large' } })
    fireEvent.change(screen.getByDisplayValue('UTC'), { target: { value: 'Europe/Paris' } })
    fireEvent.click(screen.getByRole('checkbox', { name: /Compact layout/ }))
    fireEvent.click(screen.getByRole('button', { name: 'Save display' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Settings saved')
    expect(bodyOf(fetchMock, 'PUT', '/settings/me/display')).toEqual({
      theme: 'dark', language: 'fr', timezone: 'Europe/Paris', date_format: 'YYYY-MM-DD', time_format: '12h',
      sidebar_collapsed: false, compact_mode: true, animations_enabled: true, font_size: 'large',
    })
  })

  it('shows the server reason when a section cannot be saved', async () => {
    loadRoutes({ 'PUT /settings/me/privacy': reply({ detail: 'allow_messages is not allowed' }, 422) })
    renderWithAuth(<SettingsPage />)
    await ready()

    fireEvent.click(screen.getByRole('button', { name: 'privacy' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save privacy' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('allow_messages is not allowed')
  })

  it('shows a fallback error when a section save fails without a message', async () => {
    loadRoutes()
    renderWithAuth(<SettingsPage />)
    await ready()
    global.fetch = jest.fn().mockRejectedValue('offline') as unknown as typeof fetch

    fireEvent.click(screen.getByRole('button', { name: 'Save notifications' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Settings could not be saved.')
  })

  it('edits and saves the public profile', async () => {
    const fetchMock = loadRoutes({ 'PUT /profiles/me': { ...profile, title: 'Chief Editor' } })
    renderWithAuth(<SettingsPage />)
    await ready()

    fireEvent.click(screen.getByRole('button', { name: 'profile' }))
    expect(screen.getByText(testUser.name)).toBeInTheDocument()
    expect(screen.getByText(testUser.email)).toBeInTheDocument()

    fireEvent.change(screen.getByDisplayValue('Editor'), { target: { value: 'Chief Editor' } })
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByRole('button', { name: 'Save profile' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Profile saved')
    expect(bodyOf(fetchMock, 'PUT', '/profiles/me')).toMatchObject({ title: 'Chief Editor', is_public: false })
  })

  it('shows the server error when a profile save is rejected', async () => {
    loadRoutes({ 'PUT /profiles/me': reply({ detail: 'Bio too long' }, 422) })
    renderWithAuth(<SettingsPage />)
    await ready()

    fireEvent.click(screen.getByRole('button', { name: 'profile' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save profile' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Bio too long')
  })

  it('shows a fallback error when a profile save fails without a message', async () => {
    loadRoutes()
    renderWithAuth(<SettingsPage />)
    await ready()
    fireEvent.click(screen.getByRole('button', { name: 'profile' }))
    global.fetch = jest.fn().mockRejectedValue('offline') as unknown as typeof fetch

    fireEvent.click(screen.getByRole('button', { name: 'Save profile' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Your profile could not be saved.')
  })

  it('reports that the settings could not be loaded, with the server reason', async () => {
    mockFetch({
      'GET /settings/me': reply({ detail: 'Service unavailable' }, 503),
      'GET /profiles/me': profile,
    })
    renderWithAuth(<SettingsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Service unavailable')
    expect(screen.queryByRole('button', { name: 'Save notifications' })).not.toBeInTheDocument()
  })

  it('uses a generic message when the settings request fails without one', async () => {
    global.fetch = jest.fn().mockRejectedValue('down') as unknown as typeof fetch
    renderWithAuth(<SettingsPage />)

    expect(await screen.findByText('Settings could not be loaded.')).toBeInTheDocument()
  })

  it('keeps the settings usable when only the profile cannot be loaded', async () => {
    mockFetch({
      'GET /settings/me': settings,
      'GET /profiles/me': reply({ detail: 'Profile missing' }, 404),
    })
    renderWithAuth(<SettingsPage />)
    await ready()

    expect(screen.getByRole('button', { name: 'Save notifications' })).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'profile' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Profile missing')
  })

  it('explains that account deletion is unavailable', async () => {
    loadRoutes()
    renderWithAuth(<SettingsPage />)
    await ready()

    expect(screen.getByRole('button', { name: 'Delete Account' })).toBeDisabled()
    expect(screen.getByText(/Account deletion is not yet available/)).toBeInTheDocument()
  })

  it('falls back to placeholders for a profile and user with missing fields', async () => {
    mockFetch({
      'GET /settings/me': settings,
      'GET /profiles/me': { bio: null, title: null, location: null, timezone: 'UTC', is_public: false },
    })
    renderWithAuth(<SettingsPage />, buildAuth({ user: null }))
    await ready()

    fireEvent.click(screen.getByRole('button', { name: 'profile' }))

    await waitFor(() => expect(screen.getAllByText('—')).toHaveLength(2))
    expect(screen.getByRole('checkbox')).not.toBeChecked()
  })
})
