import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import DocsPage from '@/app/dashboard/docs/page'
import { mockFetch, reply } from '@/test-utils'

const docs = [
  { id: 1, title: 'API Reference', slug: 'api-reference', doc_type: 'reference', views: 3420, version: '1.0.0' },
  { id: 2, title: 'Getting Started', slug: 'getting-started', doc_type: 'guide', views: 1250, version: '1.0.0' },
]

const apiDocs = [
  { id: 1, endpoint: '/api/v1/content', method: 'GET' },
  { id: 2, endpoint: '/api/v1/content', method: 'POST' },
]

function bodyOf(fetchMock: jest.Mock, method: string, path: string): Record<string, unknown> {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).includes(path) && (init?.method ?? 'GET') === method)
  if (!call) throw new Error(`No ${method} call to ${path}`)
  return JSON.parse(String(call[1]?.body))
}

describe('/dashboard/docs page', () => {
  it('lists published documents with their type and real view counts', async () => {
    mockFetch({ 'GET /docs': docs, 'GET /docs/api/all': apiDocs })
    render(<DocsPage />)

    expect(await screen.findByText('API Reference')).toBeInTheDocument()
    expect(screen.getByText('Type: reference')).toBeInTheDocument()
    expect(screen.getByText('3,420 views')).toBeInTheDocument()
    expect(screen.getByText('Getting Started')).toBeInTheDocument()
  })

  it('derives the stats from the documents and endpoints returned', async () => {
    mockFetch({ 'GET /docs': docs, 'GET /docs/api/all': apiDocs })
    render(<DocsPage />)

    expect(await screen.findByText('4,670')).toBeInTheDocument()
    expect(screen.getByText('Total Docs').previousElementSibling).toHaveTextContent('2')
    expect(screen.getByText('Total Views').previousElementSibling).toHaveTextContent('4,670')
    expect(screen.getByText('API Endpoints').previousElementSibling).toHaveTextContent('2')
  })

  it('says when nothing has been published yet', async () => {
    mockFetch({ 'GET /docs': [], 'GET /docs/api/all': [] })
    render(<DocsPage />)

    expect(await screen.findByText('No published documents yet.')).toBeInTheDocument()
  })

  it('lists the documented API endpoints when asked', async () => {
    mockFetch({ 'GET /docs': docs, 'GET /docs/api/all': apiDocs })
    render(<DocsPage />)
    await screen.findByText('API Reference')

    fireEvent.click(screen.getByRole('button', { name: 'View All API Docs' }))

    expect(await screen.findByText('GET')).toBeInTheDocument()
    expect(screen.getByText('POST')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Hide API docs' })).toBeInTheDocument()
  })

  it('says when no API endpoints are documented', async () => {
    mockFetch({ 'GET /docs': docs, 'GET /docs/api/all': [] })
    render(<DocsPage />)
    await screen.findByText('API Reference')

    fireEvent.click(screen.getByRole('button', { name: 'View All API Docs' }))

    expect(await screen.findByText('No API endpoints are documented yet.')).toBeInTheDocument()
  })

  it('publishes a new document: creates it, publishes it and reloads the list', async () => {
    const fetchMock = mockFetch({
      'GET /docs': docs,
      'GET /docs/api/all': apiDocs,
      'POST /docs': reply({ id: 9, title: 'Authentication', slug: 'authentication', published: false }, 201),
      'PUT /docs/9/publish': { published: true },
    })
    render(<DocsPage />)
    await screen.findByText('API Reference')

    fireEvent.click(screen.getByRole('button', { name: '+ New Doc' }))
    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Authentication' } })
    fireEvent.change(screen.getByPlaceholderText('URL slug, e.g. getting-started'), { target: { value: 'authentication' } })
    fireEvent.change(screen.getByLabelText('Type'), { target: { value: 'tutorial' } })
    fireEvent.change(screen.getByPlaceholderText('Content'), { target: { value: 'Sign in with a token.' } })
    fireEvent.click(screen.getByRole('button', { name: 'Publish document' }))

    expect(await screen.findByText('Published "Authentication".')).toBeInTheDocument()
    expect(bodyOf(fetchMock, 'POST', '/docs')).toEqual({
      title: 'Authentication',
      slug: 'authentication',
      content: 'Sign in with a token.',
      doc_type: 'tutorial',
    })
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).includes('/docs/9/publish') && init?.method === 'PUT')).toBe(true)
    await waitFor(() => expect(screen.queryByPlaceholderText('Title')).not.toBeInTheDocument())
  })

  it('shows the server reason when a document cannot be created', async () => {
    mockFetch({
      'GET /docs': docs,
      'GET /docs/api/all': apiDocs,
      'POST /docs': reply({ detail: 'A document with this slug already exists' }, 409),
    })
    render(<DocsPage />)
    await screen.findByText('API Reference')

    fireEvent.click(screen.getByRole('button', { name: '+ New Doc' }))
    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Dup' } })
    fireEvent.change(screen.getByPlaceholderText('URL slug, e.g. getting-started'), { target: { value: 'api-reference' } })
    fireEvent.change(screen.getByPlaceholderText('Content'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Publish document' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('A document with this slug already exists')
  })

  it('shows a generic message when publishing fails without an API error', async () => {
    const routes = { 'GET /docs': docs, 'GET /docs/api/all': apiDocs }
    mockFetch(routes)
    render(<DocsPage />)
    await screen.findByText('API Reference')

    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    fireEvent.click(screen.getByRole('button', { name: '+ New Doc' }))
    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Offline' } })
    fireEvent.change(screen.getByPlaceholderText('URL slug, e.g. getting-started'), { target: { value: 'offline' } })
    fireEvent.change(screen.getByPlaceholderText('Content'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Publish document' }))

    expect(await screen.findByText('The document could not be published.')).toBeInTheDocument()
  })

  it('shows the server reason when documents cannot be loaded', async () => {
    mockFetch({ 'GET /docs': reply({ detail: 'Docs offline' }, 503), 'GET /docs/api/all': apiDocs })
    render(<DocsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Docs offline')
  })

  it('reports a failure to load the API endpoint list', async () => {
    mockFetch({ 'GET /docs': docs, 'GET /docs/api/all': reply({ detail: 'API docs offline' }, 500) })
    render(<DocsPage />)

    expect(await screen.findByText('API docs offline')).toBeInTheDocument()
  })

  it('uses generic messages when loading fails without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<DocsPage />)

    expect(await screen.findByText('Documentation could not be loaded.')).toBeInTheDocument()
    expect(await screen.findByText('API documentation could not be loaded.')).toBeInTheDocument()
  })

  it('shows loading placeholders while the requests are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<DocsPage />)

    expect(screen.getByText('Loading documents…')).toBeInTheDocument()
  })
})
