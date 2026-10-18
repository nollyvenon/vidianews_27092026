import { fireEvent, screen, waitFor } from '@testing-library/react'
import ResearchPage from '@/app/dashboard/ai/research/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const answer = {
  id: 1,
  query: 'What happened to the harbour?',
  summary: 'The harbour closed at noon.',
  created_at: '2026-10-01T10:00:00Z',
}

function requestTo(fetchMock: jest.Mock, method: string, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
}

describe('/dashboard/ai/research page', () => {
  it('asks a question and shows the answer built from the documents', async () => {
    const fetchMock = mockFetch({ 'POST /ai/research': answer })
    renderWithQuery(<ResearchPage />)

    const ask = screen.getByRole('button', { name: 'Ask' })
    expect(ask).toBeDisabled()
    fireEvent.change(screen.getByPlaceholderText('What do your documents say about…'), {
      target: { value: 'What happened to the harbour?' },
    })
    fireEvent.click(ask)

    expect(await screen.findByText('The harbour closed at noon.')).toBeInTheDocument()
    expect(screen.getByText('Question: What happened to the harbour?')).toBeInTheDocument()
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ai/research')![1].body as string)).toEqual({
      query: 'What happened to the harbour?',
    })
  })

  it('shows the server reason when the question cannot be answered', async () => {
    mockFetch({
      'POST /ai/research': reply({ detail: 'AI features are not configured: set ANTHROPIC_API_KEY on the server' }, 503),
    })
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('What do your documents say about…'), { target: { value: 'Why?' } })
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('ANTHROPIC_API_KEY')
  })

  it('adds a document to the library and clears the form', async () => {
    const fetchMock = mockFetch({
      'POST /ai/documents': { id: 4, title: 'Harbour notes', document_type: 'pdf', is_indexed: true, created_at: '2026-10-01T10:00:00Z' },
    })
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Harbour notes' } })
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'pdf' } })
    fireEvent.change(screen.getByPlaceholderText('Document text'), { target: { value: 'The harbour closed at noon.' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add document' }))

    expect(await screen.findByText('Harbour notes')).toBeInTheDocument()
    expect(screen.getByText('pdf')).toBeInTheDocument()
    expect(JSON.parse(requestTo(fetchMock, 'POST', '/ai/documents')![1].body as string)).toEqual({
      title: 'Harbour notes',
      content: 'The harbour closed at noon.',
      document_type: 'pdf',
    })
    expect(screen.getByPlaceholderText('Title')).toHaveValue('')
    expect(screen.getByPlaceholderText('Document text')).toHaveValue('')
  })

  it('keeps a document the server rejects out of the library', async () => {
    mockFetch({ 'POST /ai/documents': reply({ detail: 'Document text is too large' }, 413) })
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Huge' } })
    fireEvent.change(screen.getByPlaceholderText('Document text'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add document' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Document text is too large')
    expect(screen.queryByText('Huge')).not.toBeInTheDocument()
  })

  it('searches the library and lists the matches', async () => {
    const fetchMock = mockFetch({
      'GET /ai/documents/search': [{ id: 5, title: 'Storm notes', document_type: 'text', is_indexed: true, created_at: '2026-10-01T10:00:00Z' }],
    })
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('Search documents'), { target: { value: 'storm report' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(await screen.findByText('Storm notes')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/ai/documents/search?query=storm%20report'))).toBe(true)
  })

  it('says when no documents match the search', async () => {
    mockFetch({ 'GET /ai/documents/search': [] })
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('Search documents'), { target: { value: 'nothing' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(await screen.findByText('No documents match.')).toBeInTheDocument()
  })

  it('shows the server reason when the search fails', async () => {
    mockFetch({ 'GET /ai/documents/search': reply({ detail: 'Search is unavailable' }, 500) })
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('Search documents'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Search is unavailable')
  })

  it('disables the submit buttons while a request is running', async () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<ResearchPage />)

    fireEvent.change(screen.getByPlaceholderText('What do your documents say about…'), { target: { value: 'Why?' } })
    fireEvent.click(screen.getByRole('button', { name: 'Ask' }))

    await waitFor(() => expect(screen.getByRole('button', { name: 'Ask' })).toBeDisabled())
    expect(screen.getByRole('button', { name: 'Add document' })).toBeDisabled()
  })
})
