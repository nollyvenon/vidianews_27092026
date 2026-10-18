import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import ChatPage from '@/app/dashboard/ai/chat/page'
import { mockFetch, reply } from '@/test-utils'

const chats = [
  { id: 1, title: 'Launch plan', created_at: '2026-10-01T10:00:00Z' },
  { id: 2, title: 'Headline ideas', created_at: '2026-10-02T10:00:00Z' },
]
const firstChatMessages = [
  { id: 10, role: 'user', content: 'Plan the launch', tokens: 4, created_at: '2026-10-01T10:00:00Z' },
]

describe('/dashboard/ai/chat page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('opens the most recent chat and shows its messages', async () => {
    mockFetch({
      'GET /ai/chats': chats,
      'GET /ai/chats/1': { ...chats[0], messages: firstChatMessages },
    })
    render(<ChatPage />)

    expect(await screen.findByText('Plan the launch')).toBeInTheDocument()
    expect(screen.getByText('Launch plan')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Launch plan/ })).toHaveClass('bg-blue-100')
  })

  it('switches to another chat and loads its messages', async () => {
    mockFetch({
      'GET /ai/chats': chats,
      'GET /ai/chats/1': { ...chats[0], messages: firstChatMessages },
      'GET /ai/chats/2': { ...chats[1], messages: [{ id: 20, role: 'assistant', content: 'Here are ideas', tokens: 3, created_at: '2026-10-02T10:00:00Z' }] },
    })
    render(<ChatPage />)
    await screen.findByText('Plan the launch')

    fireEvent.click(screen.getByRole('button', { name: /Headline ideas/ }))

    expect(await screen.findByText('Here are ideas')).toBeInTheDocument()
    expect(screen.queryByText('Plan the launch')).not.toBeInTheDocument()
  })

  it('prompts the user to create a chat when none exist', async () => {
    mockFetch({ 'GET /ai/chats': [] })
    render(<ChatPage />)

    expect(await screen.findByText('Create a new chat to get started')).toBeInTheDocument()
  })

  it('creates a new chat and selects it', async () => {
    mockFetch({
      'GET /ai/chats': [],
      'POST /ai/chats': { id: 3, title: 'New Chat', created_at: '2026-10-03T10:00:00Z' },
    })
    render(<ChatPage />)
    await screen.findByText('Create a new chat to get started')

    fireEvent.click(screen.getByRole('button', { name: '+ New Chat' }))

    expect(await screen.findByText('Start a conversation...')).toBeInTheDocument()
    // Anchored so it matches the chat list item, not the "+ New Chat" action button.
    expect(screen.getByRole('button', { name: /^New Chat/ })).toHaveClass('bg-blue-100')
  })

  it('sends a message to the selected chat and shows it', async () => {
    const fetchMock = mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
      'POST /ai/chats/1/messages': { id: 30, role: 'user', content: 'Draft the intro', tokens: 4, created_at: '2026-10-03T10:00:00Z' },
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: 'Draft the intro' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    expect(await screen.findByText('Draft the intro')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Ask anything...')).toHaveValue('')
    const postCall = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/ai/chats/1/messages') && init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({
      role: 'user',
      content: 'Draft the intro',
      tokens: Math.ceil('Draft the intro'.length / 4),
    })
  })

  it('stores the message and shows the assistant reply the server generates', async () => {
    const fetchMock = mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
      'POST /ai/chats/1/messages': { id: 31, role: 'user', content: 'Hi', tokens: 1, created_at: '2026-10-03T10:00:00Z' },
      'POST /ai/chats/1/reply': { id: 32, role: 'assistant', content: 'Hello, how can I help?', tokens: 9, created_at: '2026-10-03T10:00:01Z' },
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: 'Hi' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    expect(await screen.findByText('Hello, how can I help?')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/ai/chats/1/reply'))).toBe(true)
  })

  it('shows the server reason when the assistant cannot reply', async () => {
    mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
      'POST /ai/chats/1/messages': { id: 31, role: 'user', content: 'Hi', tokens: 1, created_at: '2026-10-03T10:00:00Z' },
      'POST /ai/chats/1/reply': reply({ detail: 'AI features are not configured: set ANTHROPIC_API_KEY on the server' }, 503),
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: 'Hi' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('ANTHROPIC_API_KEY')
    expect(screen.getByText('Hi')).toBeInTheDocument()
  })

  it('does not send a blank message', async () => {
    const fetchMock = mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: '   ' } })

    expect(screen.getByRole('button', { name: 'Send' })).toBeDisabled()
    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === 'POST')).toHaveLength(0)
  })

  it('shows the server reason and restores the typed text when the message is not stored', async () => {
    mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
      'POST /ai/chats/1/messages': reply({ detail: 'Rate limited' }, 429),
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: 'Retry me' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Rate limited')
    expect(screen.getByPlaceholderText('Ask anything...')).toHaveValue('Retry me')
    expect(screen.getByPlaceholderText('Ask anything...')).toBeEnabled()
  })

  it('keeps the stored message and does not restore the text when only the reply fails', async () => {
    mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
      'POST /ai/chats/1/messages': { id: 33, role: 'user', content: 'Keep me', tokens: 2, created_at: '2026-10-03T10:00:00Z' },
      'POST /ai/chats/1/reply': reply({ detail: 'AI features are not configured: set ANTHROPIC_API_KEY on the server' }, 503),
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: 'Keep me' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('ANTHROPIC_API_KEY')
    expect(screen.getByText('Keep me')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Ask anything...')).toHaveValue('')
  })

  it('logs failures to load and create chats', async () => {
    mockFetch({
      'GET /ai/chats': reply({ detail: 'down' }, 500),
      'POST /ai/chats': reply({ detail: 'quota' }, 403),
    })
    render(<ChatPage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to fetch chats', expect.any(Error)))
    fireEvent.click(screen.getByRole('button', { name: '+ New Chat' }))
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to create chat', expect.any(Error)))
  })

  it('logs a failure to load the messages of a chat', async () => {
    mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': reply({ detail: 'missing' }, 404),
    })
    render(<ChatPage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to load chat', expect.any(Error)))
  })

  it('treats a chat without a message list as an empty conversation', async () => {
    mockFetch({ 'GET /ai/chats': [chats[0]], 'GET /ai/chats/1': { ...chats[0] } })
    render(<ChatPage />)

    expect(await screen.findByText('Start a conversation...')).toBeInTheDocument()
  })

  it('does not send a message when the form is submitted with only whitespace', async () => {
    const fetchMock = mockFetch({
      'GET /ai/chats': [chats[0]],
      'GET /ai/chats/1': { ...chats[0], messages: [] },
    })
    render(<ChatPage />)
    await screen.findByText('Start a conversation...')

    fireEvent.change(screen.getByPlaceholderText('Ask anything...'), { target: { value: '   ' } })
    fireEvent.submit(screen.getByPlaceholderText('Ask anything...').closest('form') as HTMLFormElement)

    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === 'POST')).toHaveLength(0)
  })
})
