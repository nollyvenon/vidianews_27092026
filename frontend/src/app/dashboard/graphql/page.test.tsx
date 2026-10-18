import { fireEvent, render, screen } from '@testing-library/react'
import GraphQLPage from '@/app/dashboard/graphql/page'
import { mockFetch, reply } from '@/test-utils'

const saved = [
  { id: 1, name: 'LatestContent', query_string: '{ contents { id } }', execution_count: 12540, avg_execution_time_ms: 25.3 },
  { id: 2, name: 'SingleItem', query_string: '{ content(id: 1) { title } }', execution_count: 0, avg_execution_time_ms: 0 },
]

const schema = {
  types: [
    { name: 'Content', fields: [{ name: 'id', type: 'Int!' }, { name: 'title', type: 'String!' }] },
    { name: 'Query', fields: [{ name: 'contents', type: '[Content!]!' }] },
  ],
}

function bodyOf(fetchMock: jest.Mock, method: string, path: string): Record<string, unknown> {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).includes(path) && (init?.method ?? 'GET') === method)
  if (!call) throw new Error(`No ${method} call to ${path}`)
  return JSON.parse(String(call[1]?.body))
}

describe('/dashboard/graphql page', () => {
  it('lists saved queries with their execution counts and average response times', async () => {
    mockFetch({ 'GET /graphql/queries': saved })
    render(<GraphQLPage />)

    expect(await screen.findByText('LatestContent')).toBeInTheDocument()
    expect(screen.getByText('12,540 executions')).toBeInTheDocument()
    expect(screen.getByText('Avg Response: 25.3ms')).toBeInTheDocument()
  })

  it('says when no queries have been saved', async () => {
    mockFetch({ 'GET /graphql/queries': [] })
    render(<GraphQLPage />)

    expect(await screen.findByText('No saved queries yet.')).toBeInTheDocument()
  })

  it('runs the typed query and shows the data and the time it took', async () => {
    const fetchMock = mockFetch({
      'GET /graphql/queries': [],
      'POST /graphql/run': { elapsed_ms: 3.5, response: { data: { contents: [{ id: 1 }] } } },
    })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.change(screen.getByLabelText('Query'), { target: { value: '{ contents { id } }' } })
    fireEvent.click(screen.getByRole('button', { name: 'Execute' }))

    expect(await screen.findByText('Ran in 3.50 ms')).toBeInTheDocument()
    expect(screen.getByText(/"contents"/)).toBeInTheDocument()
    expect(bodyOf(fetchMock, 'POST', '/graphql/run')).toEqual({ query: '{ contents { id } }' })
  })

  it('lists the errors the query produced', async () => {
    mockFetch({
      'GET /graphql/queries': [],
      'POST /graphql/run': { elapsed_ms: 1, response: { data: null, errors: [{ message: 'Syntax Error: Expected Name' }] } },
    })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.change(screen.getByLabelText('Query'), { target: { value: '{' } })
    fireEvent.click(screen.getByRole('button', { name: 'Execute' }))

    expect(await screen.findByText('Syntax Error: Expected Name')).toBeInTheDocument()
  })

  it('shows the server reason when the query cannot be run', async () => {
    mockFetch({ 'GET /graphql/queries': [], 'POST /graphql/run': reply({ detail: 'Query is too long' }, 422) })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.change(screen.getByLabelText('Query'), { target: { value: '{ contents { id } }' } })
    fireEvent.click(screen.getByRole('button', { name: 'Execute' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Query is too long')
  })

  it('saves the typed query under the name entered and reloads the list', async () => {
    const fetchMock = mockFetch({
      'GET /graphql/queries': [],
      'POST /graphql/query': reply({ id: 3, name: 'Latest' }, 201),
    })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.change(screen.getByLabelText('Query'), { target: { value: '{ contents { id } }' } })
    fireEvent.change(screen.getByLabelText('Query name'), { target: { value: ' Latest ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save Query' }))

    expect(await screen.findByText('Saved "Latest".')).toBeInTheDocument()
    expect(bodyOf(fetchMock, 'POST', '/graphql/query')).toEqual({ name: 'Latest', query_string: '{ contents { id } }' })
  })

  it('keeps Save disabled until both a query and a name are present', async () => {
    mockFetch({ 'GET /graphql/queries': [] })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    const save = screen.getByRole('button', { name: 'Save Query' })
    expect(save).toBeDisabled()
    fireEvent.change(screen.getByLabelText('Query'), { target: { value: '{ contents { id } }' } })
    expect(save).toBeDisabled()
    fireEvent.change(screen.getByLabelText('Query name'), { target: { value: 'Named' } })
    expect(save).toBeEnabled()
  })

  it('shows the server reason when a query cannot be saved', async () => {
    mockFetch({ 'GET /graphql/queries': [], 'POST /graphql/query': reply({ detail: 'Name already used' }, 422) })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.change(screen.getByLabelText('Query'), { target: { value: '{ contents { id } }' } })
    fireEvent.change(screen.getByLabelText('Query name'), { target: { value: 'Dup' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save Query' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Name already used')
  })

  it('runs a saved query by its id and shows the recorded result', async () => {
    const fetchMock = mockFetch({
      'GET /graphql/queries': saved,
      'POST /graphql/execute': { query_id: 1, elapsed_ms: 2, response: { data: { contents: [] } } },
    })
    render(<GraphQLPage />)
    await screen.findByText('LatestContent')

    fireEvent.click(screen.getByRole('button', { name: 'Run LatestContent' }))

    expect(await screen.findByText('Ran in 2.00 ms')).toBeInTheDocument()
    expect(bodyOf(fetchMock, 'POST', '/graphql/execute')).toEqual({ query_id: 1 })
  })

  it('shows the server reason when a saved query cannot be run', async () => {
    mockFetch({
      'GET /graphql/queries': saved,
      'POST /graphql/execute': reply({ detail: 'GraphQL query 1 not found' }, 404),
    })
    render(<GraphQLPage />)
    await screen.findByText('LatestContent')

    fireEvent.click(screen.getByRole('button', { name: 'Run LatestContent' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('GraphQL query 1 not found')
  })

  it('shows the live schema on request and hides it again', async () => {
    mockFetch({ 'GET /graphql/queries': [], 'GET /graphql/schema': schema })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.click(screen.getByRole('button', { name: 'View Full Schema' }))

    expect(await screen.findByText('type Content')).toBeInTheDocument()
    expect(screen.getByText('title: String!')).toBeInTheDocument()
    expect(screen.getByText('contents: [Content!]!')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Hide Schema' }))
    expect(screen.queryByText('type Content')).not.toBeInTheDocument()
  })

  it('reports a failure to load the schema', async () => {
    mockFetch({ 'GET /graphql/queries': [], 'GET /graphql/schema': reply({ detail: 'Schema offline' }, 500) })
    render(<GraphQLPage />)
    await screen.findByText('No saved queries yet.')

    fireEvent.click(screen.getByRole('button', { name: 'View Full Schema' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Schema offline')
  })

  it('uses generic messages when requests fail without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<GraphQLPage />)

    expect(await screen.findByText('Saved queries could not be loaded.')).toBeInTheDocument()
  })

  it('shows loading placeholders while the saved queries are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<GraphQLPage />)

    expect(screen.getByText('Loading saved queries…')).toBeInTheDocument()
  })
})
