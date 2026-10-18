import { fireEvent, screen, waitFor } from '@testing-library/react'
import PermissionsPage from '@/app/dashboard/permissions/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const permissions = [{ id: 1, name: 'content:read', resource: 'content', action: 'read', category: 'content' }]
const roles = [
  { id: 1, name: 'admin', description: 'Administrators', is_system: true },
  { id: 2, name: 'editor', description: null, is_system: false },
]

// Overrides come first and replace the defaults with the same key: mockFetch matches by suffix,
// so '/users/9/roles' would otherwise be answered by the default 'GET /roles'.
function base(extra: Record<string, unknown> = {}) {
  const defaults: Record<string, unknown> = { 'GET /permissions': permissions, 'GET /roles': roles }
  const merged: Record<string, unknown> = { ...extra }
  for (const [key, value] of Object.entries(defaults)) {
    if (!(key in merged)) merged[key] = value
  }
  return mockFetch(merged)
}

describe('/dashboard/permissions page', () => {
  it('lists the permissions and the roles', async () => {
    base()
    renderWithQuery(<PermissionsPage />)

    expect(await screen.findByText('content:read')).toBeInTheDocument()
    expect(screen.getByText('admin', { selector: 'span.font-medium' })).toBeInTheDocument()
    expect(screen.getByText('(system)')).toBeInTheDocument()
    expect(screen.getByText('Administrators')).toBeInTheDocument()
  })

  it('says when no roles or permissions are defined', async () => {
    base({ 'GET /permissions': [], 'GET /roles': [] })
    renderWithQuery(<PermissionsPage />)

    expect(await screen.findByText('No roles defined yet.')).toBeInTheDocument()
    expect(screen.getByText('No permissions defined yet.')).toBeInTheDocument()
  })

  it('creates a role with its name and description', async () => {
    const fetchMock = base({ 'POST /roles': { id: 3, name: 'reviewer' } })
    renderWithQuery(<PermissionsPage />)
    await screen.findByText('admin', { selector: 'span.font-medium' })

    fireEvent.change(screen.getByPlaceholderText('Role name'), { target: { value: ' reviewer ' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: 'Reviews drafts' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create role' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Role created.')
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/roles') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({ name: 'reviewer', description: 'Reviews drafts' })
  })

  it('shows the roles a user holds and assigns another', async () => {
    const fetchMock = base({
      'GET /users/5/roles': [roles[1]],
      'POST /users/5/roles/1': { assigned: true },
    })
    renderWithQuery(<PermissionsPage />)
    await screen.findByText('admin', { selector: 'span.font-medium' })

    fireEvent.change(screen.getAllByRole('spinbutton')[0], { target: { value: '5' } })
    fireEvent.click(screen.getByRole('button', { name: 'Show roles' }))
    // The role list shows the user's role, and the assignment select also offers "editor".
    await waitFor(() => expect(screen.getAllByText('editor').length).toBeGreaterThanOrEqual(2))

    fireEvent.change(screen.getByLabelText('Role to assign'), { target: { value: '1' } })
    fireEvent.click(screen.getByRole('button', { name: 'Assign role' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Role assigned.')
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/users/5/roles/1') && init?.method === 'POST')).toBe(true)
  })

  it('shows the server reason when a user has no roles to show', async () => {
    base({ 'GET /users/9/roles': reply({ detail: 'User not found' }, 404) })
    renderWithQuery(<PermissionsPage />)
    await screen.findByText('admin', { selector: 'span.font-medium' })

    fireEvent.change(screen.getAllByRole('spinbutton')[0], { target: { value: '9' } })
    fireEvent.click(screen.getByRole('button', { name: 'Show roles' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('User not found')
    await waitFor(() => expect(screen.queryByRole('status')).not.toBeInTheDocument())
  })
})
