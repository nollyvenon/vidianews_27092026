import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import SearchPage from '@/app/dashboard/search/page'
import { mockFetch, reply } from '@/test-utils'

function search(query: string) {
  fireEvent.change(screen.getByPlaceholderText('Search content, videos, articles...'), {
    target: { value: query },
  })
  fireEvent.click(screen.getByRole('button', { name: 'Search' }))
}

describe('/dashboard/search page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('invites a search before any query is entered', () => {
    render(<SearchPage />)

    expect(screen.getByText('Search to discover content')).toBeInTheDocument()
  })

  it('shows matching results with a snippet, type and view action', async () => {
    const fetchMock = mockFetch({
      'GET /system/search': [
        { id: 1, title: 'Climate explainer', content: 'A'.repeat(150), resource_type: 'video' },
      ],
    })
    render(<SearchPage />)

    search('climate news')

    expect(await screen.findByRole('heading', { name: 'Climate explainer' })).toBeInTheDocument()
    expect(screen.getByText(`${'A'.repeat(100)}...`)).toBeInTheDocument()
    expect(screen.getByText('video')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'View' })).toBeInTheDocument()
    expect(String(fetchMock.mock.calls[0][0])).toMatch(/system\/search\?q=climate%20news$/)
  })

  it('reports when a search has no matches', async () => {
    mockFetch({ 'GET /system/search': [] })
    render(<SearchPage />)

    search('nothing here')

    expect(await screen.findByText('No results found')).toBeInTheDocument()
  })

  it('does not search for a blank query', () => {
    const fetchMock = mockFetch({})
    render(<SearchPage />)

    search('   ')

    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('shows a searching state while the request is pending', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<SearchPage />)

    search('pending')

    expect(screen.getByRole('button', { name: 'Searching...' })).toBeDisabled()
  })

  it('logs a failed search and returns to the idle state', async () => {
    mockFetch({ 'GET /system/search': reply({ detail: 'down' }, 500) })
    render(<SearchPage />)

    search('broken')

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Search failed', expect.any(Error)))
    expect(screen.getByRole('button', { name: 'Search' })).toBeEnabled()
  })
})
