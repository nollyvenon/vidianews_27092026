import { fireEvent, screen, waitFor } from '@testing-library/react'
import ProfilePage from '@/app/dashboard/profile/page'
import { mockFetch, reply, renderWithAuth, testUser } from '@/test-utils'

const profile = { title: 'Editor', location: 'Paris', bio: 'Hello', timezone: 'UTC', is_public: true }
const skills = [{ id: 5, name: 'Writing', category: null, proficiency: 'expert', years_experience: 6, endorsed_count: 2 }]
const experiences = [
  { id: 7, company: 'Daily News', title: 'Reporter', start_date: '2020-01-01T00:00:00Z', end_date: null, current: true, description: null },
]
const educations = [{ id: 9, school: 'State University', degree: 'BA', field: 'Journalism', start_date: '2014-09-01T00:00:00Z', end_date: '2018-06-01T00:00:00Z' }]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /profiles/me': profile,
    [`GET /profiles/${testUser.id}/skills`]: skills,
    [`GET /profiles/${testUser.id}/experiences`]: experiences,
    [`GET /profiles/${testUser.id}/educations`]: educations,
    ...extra,
  })
}

function bodyOf(fetchMock: jest.Mock, method: string, suffix: string) {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
  return JSON.parse(call![1].body as string)
}

describe('/dashboard/profile page', () => {
  it('shows a loading message until the profile arrives', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithAuth(<ProfilePage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('shows the profile and saves an edit to it', async () => {
    const fetchMock = base({ 'PUT /profiles/me': { ...profile, title: 'Chief Editor' } })
    renderWithAuth(<ProfilePage />)

    expect(await screen.findByText('Editor')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'Edit Profile' }))
    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Chief Editor' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByText('Chief Editor')).toBeInTheDocument()
    expect(bodyOf(fetchMock, 'PUT', '/profiles/me')).toMatchObject({ title: 'Chief Editor', location: 'Paris' })
  })

  it('discards an edit when cancelled', async () => {
    base()
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'Edit Profile' }))
    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Something else' } })
    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))

    expect(screen.getByText('Editor')).toBeInTheDocument()
    expect(screen.queryByText('Something else')).not.toBeInTheDocument()
  })

  it('shows the server reason when the profile cannot be saved', async () => {
    base({ 'PUT /profiles/me': reply({ detail: 'Bio too long' }, 422) })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'Edit Profile' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Bio too long')
  })

  it('shows the server reason when the profile cannot be loaded', async () => {
    base({ 'GET /profiles/me': reply({ detail: 'Profile not found' }, 404) })
    renderWithAuth(<ProfilePage />)

    expect(await screen.findByText('Profile not found')).toBeInTheDocument()
  })

  it('lists the skills and adds one with its level and years', async () => {
    const fetchMock = base({ 'POST /profiles/me/skills': { id: 6 } })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'skills' }))
    expect(await screen.findByText('Writing')).toBeInTheDocument()
    fireEvent.change(screen.getByPlaceholderText('Skill'), { target: { value: ' Photography ' } })
    fireEvent.change(screen.getByLabelText('Proficiency'), { target: { value: 'advanced' } })
    fireEvent.change(screen.getByLabelText('Years'), { target: { value: '3' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add skill' }))

    await waitFor(() => expect(bodyOf(fetchMock, 'POST', '/profiles/me/skills')).toEqual({ name: 'Photography', proficiency: 'advanced', years_experience: 3 }))
  })

  it('removes a skill', async () => {
    const fetchMock = base({ 'DELETE /profiles/skills/5': null })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'skills' }))
    fireEvent.click(await screen.findByRole('button', { name: 'Remove' }))

    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/profiles/skills/5') && init?.method === 'DELETE')).toBe(true))
  })

  it('lists the experience and adds a position, with its dates', async () => {
    const fetchMock = base({ 'POST /profiles/me/experiences': { id: 8 } })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'experience' }))
    expect(await screen.findByText('Reporter')).toBeInTheDocument()
    expect(screen.getByText(/Present/)).toBeInTheDocument()
    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Columnist' } })
    fireEvent.change(screen.getByPlaceholderText('Company'), { target: { value: 'Weekly Review' } })
    fireEvent.change(screen.getAllByLabelText(/Start date/)[0], { target: { value: '2024-02-01' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add experience' }))

    await waitFor(() =>
      expect(bodyOf(fetchMock, 'POST', '/profiles/me/experiences')).toEqual({
        company: 'Weekly Review',
        title: 'Columnist',
        start_date: '2024-02-01T00:00:00Z',
        end_date: null,
        current: false,
        description: null,
      }),
    )
  })

  it('lists the education and adds an entry', async () => {
    const fetchMock = base({ 'POST /profiles/me/educations': { id: 10 } })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'education' }))
    expect(await screen.findByText('State University')).toBeInTheDocument()
    expect(screen.getByText(/BA in Journalism/)).toBeInTheDocument()
    fireEvent.change(screen.getByPlaceholderText('School'), { target: { value: 'City College' } })
    fireEvent.change(screen.getAllByLabelText(/Start date/)[0], { target: { value: '2020-09-01' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add education' }))

    await waitFor(() =>
      expect(bodyOf(fetchMock, 'POST', '/profiles/me/educations')).toEqual({
        school: 'City College',
        degree: null,
        field: null,
        start_date: '2020-09-01T00:00:00Z',
        end_date: null,
      }),
    )
  })

  it('shows the server reason when a section entry cannot be added', async () => {
    base({ 'POST /profiles/me/skills': reply({ detail: 'Skill already listed' }, 409) })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'skills' }))
    fireEvent.change(screen.getByPlaceholderText('Skill'), { target: { value: 'Writing' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add skill' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Skill already listed')
  })

  it('says when a section has no entries yet', async () => {
    base({
      [`GET /profiles/${testUser.id}/skills`]: [],
      [`GET /profiles/${testUser.id}/experiences`]: [],
      [`GET /profiles/${testUser.id}/educations`]: [],
    })
    renderWithAuth(<ProfilePage />)
    await screen.findByText('Editor')

    fireEvent.click(screen.getByRole('button', { name: 'skills' }))
    expect(await screen.findByText('No skills added yet.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'experience' }))
    expect(await screen.findByText('No experience added yet.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('button', { name: 'education' }))
    expect(await screen.findByText('No education added yet.')).toBeInTheDocument()
  })
})
