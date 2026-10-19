import { fireEvent, screen } from '@testing-library/react'
import ProfilePage from '@/app/dashboard/profile/page'
import { mockFetch, renderWithAuth, testUser } from '@/test-utils'

const skills = [{ id: 5, name: 'Writing', category: null, proficiency: 'expert', years_experience: 6, endorsed_count: 2 }]

describe('/dashboard/profile page fallbacks', () => {
  it('shows a dash for each profile field the user has left empty', async () => {
    mockFetch({
      'GET /profiles/me': { title: null, location: '', bio: undefined, timezone: 'UTC', is_public: false },
      [`GET /profiles/${testUser.id}/skills`]: skills,
      [`GET /profiles/${testUser.id}/experiences`]: [],
      [`GET /profiles/${testUser.id}/educations`]: [],
    })
    renderWithAuth(<ProfilePage />)

    expect(await screen.findAllByText('-')).toHaveLength(3)
  })

  it('opens the editor with empty text boxes for fields the profile does not have', async () => {
    mockFetch({
      'GET /profiles/me': { timezone: 'UTC', is_public: true },
      [`GET /profiles/${testUser.id}/skills`]: skills,
      [`GET /profiles/${testUser.id}/experiences`]: [],
      [`GET /profiles/${testUser.id}/educations`]: [],
    })
    renderWithAuth(<ProfilePage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Edit Profile' }))

    expect(screen.getByPlaceholderText('Title')).toHaveValue('')
    expect(screen.getByPlaceholderText('Location')).toHaveValue('')
  })

  it('treats a list that is not an array as an empty list instead of failing', async () => {
    mockFetch({
      'GET /profiles/me': { title: 'Editor', location: 'Paris', bio: 'Hello', timezone: 'UTC', is_public: true },
      [`GET /profiles/${testUser.id}/skills`]: { unexpected: true },
      [`GET /profiles/${testUser.id}/experiences`]: null,
      [`GET /profiles/${testUser.id}/educations`]: 'not a list',
    })
    renderWithAuth(<ProfilePage />)

    expect(await screen.findByText('Editor')).toBeInTheDocument()
    expect(screen.queryByText('Writing')).not.toBeInTheDocument()
  })
})
