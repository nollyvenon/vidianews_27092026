import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import CommunityPage from '@/app/dashboard/community/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/community page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('lists forum threads and their reply counts, defaulting to zero replies', async () => {
    mockFetch({
      'GET /forum/threads': [
        { id: 1, title: 'Welcome aboard', replies: 4 },
        { id: 2, title: 'Feature ideas' },
      ],
    })
    render(<CommunityPage />)

    expect(await screen.findByRole('heading', { name: 'Welcome aboard' })).toBeInTheDocument()
    expect(screen.getByText('Replies: 4')).toBeInTheDocument()
    expect(screen.getByText('Replies: 0')).toBeInTheDocument()
  })

  it('creates a thread in the chosen category, then clears the form and reloads threads', async () => {
    const fetchMock = mockFetch({
      'GET /forum/threads': [],
      'POST /forum/thread': { id: 3 },
    })
    render(<CommunityPage />)
    await screen.findByRole('heading', { name: 'Threads' })

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'support' } })
    fireEvent.change(screen.getByPlaceholderText('Thread title'), { target: { value: 'Upload fails' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create Thread' }))

    await waitFor(() => expect(screen.getByPlaceholderText('Thread title')).toHaveValue(''))
    const postCall = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/forum/thread') && init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({ category: 'support', title: 'Upload fails' })
    expect(fetchMock.mock.calls.filter(([url]) => String(url).endsWith('/forum/threads'))).toHaveLength(2)
  })

  it('keeps the typed title when the server rejects the thread', async () => {
    mockFetch({
      'GET /forum/threads': [],
      'POST /forum/thread': reply({ detail: 'Rejected' }, 422),
    })
    render(<CommunityPage />)
    await screen.findByRole('heading', { name: 'Threads' })

    fireEvent.change(screen.getByPlaceholderText('Thread title'), { target: { value: 'Keep me' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create Thread' }))

    await waitFor(() => expect(screen.getByPlaceholderText('Thread title')).toHaveValue('Keep me'))
  })

  it('logs failures to load and create threads', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<CommunityPage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to fetch threads:', expect.any(Error)))

    fireEvent.change(screen.getByPlaceholderText('Thread title'), { target: { value: 'Offline post' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create Thread' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to create thread:', expect.any(Error)))
  })
})
