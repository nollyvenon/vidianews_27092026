import { fireEvent, screen, waitFor } from '@testing-library/react'
import AgentsPage from '@/app/dashboard/ai/agents/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const agents = [
  { id: 1, name: 'Story Bot', slug: 'story-bot', description: 'Drafts intros', status: 'draft', execution_count: 3, success_rate: 50, created_at: '2026-10-01T10:00:00Z' },
  { id: 2, name: 'Fact Checker', slug: 'fact-checker', description: null, status: 'active', execution_count: 10, success_rate: 90, created_at: '2026-10-02T10:00:00Z' },
]

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
}

describe('/dashboard/ai/agents page', () => {
  it('lists the agents with their status and run statistics', async () => {
    mockFetch({ 'GET /ai/agents': agents })
    renderWithQuery(<AgentsPage />)

    expect(await screen.findByRole('heading', { name: 'Story Bot' })).toBeInTheDocument()
    expect(screen.getByText('Drafts intros')).toBeInTheDocument()
    expect(screen.getByText('3 runs · 50% success')).toBeInTheDocument()
    expect(screen.getByText('active')).toHaveClass('bg-green-100')
    expect(screen.getByRole('button', { name: 'Activate' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Pause' })).toBeInTheDocument()
  })

  it('explains that there are no agents yet', async () => {
    mockFetch({ 'GET /ai/agents': [] })
    renderWithQuery(<AgentsPage />)

    expect(await screen.findByText('No agents yet. Create one above.')).toBeInTheDocument()
  })

  it('treats a response that is not a list as no agents', async () => {
    mockFetch({ 'GET /ai/agents': { detail: 'unexpected' } })
    renderWithQuery(<AgentsPage />)

    expect(await screen.findByText('No agents yet. Create one above.')).toBeInTheDocument()
  })

  it('shows a loading message until the agents arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<AgentsPage />)

    expect(screen.getByText('Loading agents…')).toBeInTheDocument()
  })

  it('derives the slug from the name until the slug is edited', async () => {
    mockFetch({ 'GET /ai/agents': [] })
    renderWithQuery(<AgentsPage />)
    await screen.findByText('No agents yet. Create one above.')

    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Caption Writer' } })
    expect(screen.getByPlaceholderText('Slug')).toHaveValue('caption-writer')

    fireEvent.change(screen.getByPlaceholderText('Slug'), { target: { value: 'captions' } })
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Caption Pro' } })
    expect(screen.getByPlaceholderText('Slug')).toHaveValue('captions')
  })

  it('creates an agent, clears the form and reloads the list', async () => {
    const fetchMock = mockFetch({ 'GET /ai/agents': [], 'POST /ai/agents': { id: 3 } })
    renderWithQuery(<AgentsPage />)
    await screen.findByText('No agents yet. Create one above.')

    const create = screen.getByRole('button', { name: 'Create agent' })
    expect(create).toBeDisabled()

    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: '  Caption Writer ' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: 'Writes captions' } })
    fireEvent.change(screen.getByPlaceholderText('System prompt'), { target: { value: 'Be brief' } })
    expect(create).toBeEnabled()
    fireEvent.click(create)

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ai/agents')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ai/agents')![1].body as string)).toEqual({
      name: 'Caption Writer',
      slug: 'caption-writer',
      description: 'Writes captions',
      system_prompt: 'Be brief',
    })
    await waitFor(() => expect(screen.getByPlaceholderText('Name')).toHaveValue(''))
    expect(screen.getByPlaceholderText('Slug')).toHaveValue('')
    // One load on mount and one reload after the create.
    expect(fetchMock.mock.calls.filter(([url, init]) => String(url).endsWith('/ai/agents') && init?.method === 'GET')).toHaveLength(2)
  })

  it('sends null for blank optional fields', async () => {
    const fetchMock = mockFetch({ 'GET /ai/agents': [], 'POST /ai/agents': { id: 4 } })
    renderWithQuery(<AgentsPage />)
    await screen.findByText('No agents yet. Create one above.')

    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Quiet' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: '   ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create agent' }))

    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ai/agents')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ai/agents')![1].body as string)).toEqual({
      name: 'Quiet',
      slug: 'quiet',
      description: null,
      system_prompt: null,
    })
  })

  it('shows the server reason when an agent cannot be created', async () => {
    mockFetch({
      'GET /ai/agents': [],
      'POST /ai/agents': reply({ detail: 'An agent with this slug already exists' }, 409),
    })
    renderWithQuery(<AgentsPage />)
    await screen.findByText('No agents yet. Create one above.')

    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Story Bot' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create agent' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('An agent with this slug already exists')
  })

  it('activates a draft agent and pauses an active one', async () => {
    const fetchMock = mockFetch({
      'GET /ai/agents': agents,
      'POST /ai/agents/1/activate': {},
      'POST /ai/agents/2/pause': {},
    })
    renderWithQuery(<AgentsPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Activate' }))
    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ai/agents/1/activate')).toBeDefined())

    fireEvent.click(screen.getByRole('button', { name: 'Pause' }))
    await waitFor(() => expect(requestTo(fetchMock, 'POST', '/ai/agents/2/pause')).toBeDefined())
  })

  it('shows the server reason when the status cannot be changed', async () => {
    mockFetch({
      'GET /ai/agents': agents,
      'POST /ai/agents/1/activate': reply({ detail: 'Agent has no system prompt' }, 422),
    })
    renderWithQuery(<AgentsPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Activate' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Agent has no system prompt')
  })

  it('shows the server reason when agents cannot be loaded', async () => {
    mockFetch({ 'GET /ai/agents': reply({ detail: 'Your account has no workspace yet.' }, 500) })
    renderWithQuery(<AgentsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no workspace yet.')
  })
})
