import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import OrganizationsPage from '@/app/dashboard/organizations/page'
import { mockFetch, reply } from '@/test-utils'

const orgs = [
  { id: 1, tenant_id: 5, name: 'Newsroom', slug: 'newsroom', org_type: 'department', status: 'active', created_at: '2026-01-01' },
  { id: 2, tenant_id: 5, name: 'Video Desk', slug: 'video-desk', org_type: 'team', status: 'inactive', created_at: '2026-01-02' },
]

async function enterTenant(id: string) {
  fireEvent.change(screen.getByLabelText('Tenant ID'), { target: { value: id } })
}

describe('/dashboard/organizations page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('asks for a tenant before showing anything', () => {
    mockFetch({})
    render(<OrganizationsPage />)

    expect(screen.getByText('Enter a tenant ID to view its organizations.')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: '+ Create Organization' })).not.toBeInTheDocument()
  })

  it('loads and lists the organizations of the entered tenant', async () => {
    const fetchMock = mockFetch({ 'GET /organizations': { data: orgs } })
    render(<OrganizationsPage />)

    await enterTenant('5')

    expect(await screen.findByRole('heading', { name: 'Newsroom' })).toBeInTheDocument()
    expect(screen.getByText('video-desk')).toBeInTheDocument()
    expect(screen.getByText('team')).toBeInTheDocument()
    expect(screen.getByText('inactive')).toBeInTheDocument()
    expect(String(fetchMock.mock.calls[0][0])).toMatch(/\/organizations\?tenant_id=5$/)
  })

  it('shows a loading state while the organizations are fetched', async () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<OrganizationsPage />)

    await enterTenant('5')

    expect(await screen.findByText('Loading...')).toBeInTheDocument()
  })

  it('shows the empty state for a tenant with no organizations', async () => {
    mockFetch({ 'GET /organizations': { data: [] } })
    render(<OrganizationsPage />)

    await enterTenant('9')

    expect(await screen.findByText('No organizations yet. Create one to get started!')).toBeInTheDocument()
  })

  it('shows the server error when the tenant cannot be loaded', async () => {
    mockFetch({ 'GET /organizations': reply({ detail: 'Tenant not found' }, 404) })
    render(<OrganizationsPage />)

    await enterTenant('404')

    expect(await screen.findByRole('alert')).toHaveTextContent('Tenant not found')
  })

  it('uses a generic message when loading fails without an error object', async () => {
    global.fetch = jest.fn().mockRejectedValue('offline') as unknown as typeof fetch
    render(<OrganizationsPage />)

    await enterTenant('5')

    expect(await screen.findByRole('alert')).toHaveTextContent('Failed to load organizations')
  })

  it('clears the list when the tenant is removed', async () => {
    mockFetch({ 'GET /organizations': { data: orgs } })
    render(<OrganizationsPage />)
    await enterTenant('5')
    await screen.findByRole('heading', { name: 'Newsroom' })

    await enterTenant('')

    expect(screen.getByText('Enter a tenant ID to view its organizations.')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Newsroom' })).not.toBeInTheDocument()
  })

  it('creates an organization for the tenant and adds it to the list', async () => {
    const created = { id: 3, tenant_id: 5, name: 'Sports', slug: 'sports', org_type: 'project', status: 'active', created_at: '2026-02-01' }
    const fetchMock = mockFetch({
      'GET /organizations': { data: orgs },
      'POST /organizations': created,
    })
    render(<OrganizationsPage />)
    await enterTenant('5')
    await screen.findByRole('heading', { name: 'Newsroom' })

    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Sports' } })
    fireEvent.change(screen.getByPlaceholderText('Slug'), { target: { value: 'sports' } })
    fireEvent.change(screen.getByRole('combobox', { name: 'Organization type' }), { target: { value: 'project' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    expect(await screen.findByRole('heading', { name: 'Sports' })).toBeInTheDocument()
    expect(screen.queryByPlaceholderText('Name')).not.toBeInTheDocument()
    const postCall = fetchMock.mock.calls.find(([, init]) => init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({
      tenant_id: 5,
      name: 'Sports',
      slug: 'sports',
      org_type: 'project',
    })
  })

  it('shows progress while the organization is being created', async () => {
    global.fetch = jest.fn(async (_url: RequestInfo | URL, init?: RequestInit) =>
      init?.method === 'POST' ? new Promise(() => undefined) : ({ ok: true, json: async () => ({ data: [] }) } as Response)
    ) as unknown as typeof fetch
    render(<OrganizationsPage />)
    await enterTenant('5')
    await screen.findByText(/No organizations yet/)

    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'X' } })
    fireEvent.change(screen.getByPlaceholderText('Slug'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    expect(await screen.findByRole('button', { name: 'Creating...' })).toBeDisabled()
  })

  it('keeps the form open with the server error when creation is rejected', async () => {
    mockFetch({
      'GET /organizations': { data: [] },
      'POST /organizations': reply({ detail: 'Slug already exists' }, 409),
    })
    render(<OrganizationsPage />)
    await enterTenant('5')
    await screen.findByText(/No organizations yet/)

    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Dup' } })
    fireEvent.change(screen.getByPlaceholderText('Slug'), { target: { value: 'dup' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Slug already exists')
    expect(screen.getByPlaceholderText('Name')).toHaveValue('Dup')
  })

  it('uses a generic message when creation fails without an error object', async () => {
    mockFetch({ 'GET /organizations': { data: [] } })
    render(<OrganizationsPage />)
    await enterTenant('5')
    await screen.findByText(/No organizations yet/)
    global.fetch = jest.fn().mockRejectedValue('offline') as unknown as typeof fetch

    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Y' } })
    fireEvent.change(screen.getByPlaceholderText('Slug'), { target: { value: 'y' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Failed to create organization')
  })

  it('toggles and cancels the create form', async () => {
    mockFetch({ 'GET /organizations': { data: [] } })
    render(<OrganizationsPage />)
    await enterTenant('5')
    await screen.findByText(/No organizations yet/)

    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    expect(screen.getByPlaceholderText('Name')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))
    expect(screen.queryByPlaceholderText('Name')).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    fireEvent.click(screen.getByRole('button', { name: '+ Create Organization' }))
    await waitFor(() => expect(screen.queryByPlaceholderText('Name')).not.toBeInTheDocument())
  })
})
