import { fireEvent, screen, waitFor } from '@testing-library/react'
import { ContentPicker } from '@/components/content/content-picker'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

const items = [
  { id: 7, title: 'Storm report', status: 'published', content_type: 'article' },
  { id: 8, title: 'Launch notes', status: 'draft', content_type: 'newsletter' },
]

describe('ContentPicker', () => {
  it('lists the signed-in user content and reports when there is none', async () => {
    mockFetch({ 'GET /content': { items: [], total: 0 } })
    renderWithQuery(<ContentPicker value={null} onChange={jest.fn()} />)

    expect(await screen.findByText(/You have no content yet/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Create a content item' })).toHaveAttribute('href', '/dashboard/content/new')
  })

  it('offers each item with its status and a custom label', async () => {
    mockFetch({ 'GET /content': { items, total: 2 } })
    renderWithQuery(<ContentPicker value={null} onChange={jest.fn()} label="Article" />)

    expect(await screen.findByText('Article')).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Storm report (published)' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'Launch notes (draft)' })).toBeInTheDocument()
  })

  it('treats a list response without items as empty', async () => {
    mockFetch({ 'GET /content': { total: 0 } })
    renderWithQuery(<ContentPicker value={null} onChange={jest.fn()} />)

    expect(await screen.findByText(/You have no content yet/)).toBeInTheDocument()
  })

  it('loads the full item body after a selection and reports it upward', async () => {
    const onChange = jest.fn()
    const fetchMock = mockFetch({
      'GET /content': { items, total: 2 },
      'GET /content/7': { id: 7, title: 'Storm report', body: 'The storm arrived early.' },
    })
    renderWithQuery(<ContentPicker value={null} onChange={onChange} />)

    fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })

    await waitFor(() =>
      expect(onChange).toHaveBeenCalledWith({ ...items[0], body: 'The storm arrived early.' })
    )
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/content/7'))).toBe(true)
  })

  it('reports an item without a body as empty text', async () => {
    const onChange = jest.fn()
    mockFetch({
      'GET /content': { items, total: 2 },
      'GET /content/8': { id: 8, title: 'Launch notes', body: null },
    })
    renderWithQuery(<ContentPicker value={null} onChange={onChange} />)

    fireEvent.change(await screen.findByRole('combobox'), { target: { value: '8' } })

    await waitFor(() => expect(onChange).toHaveBeenCalledWith({ ...items[1], body: '' }))
  })

  it('clears the choice when the placeholder is selected again', async () => {
    const onChange = jest.fn()
    mockFetch({
      'GET /content': { items, total: 2 },
      'GET /content/7': { id: 7, title: 'Storm report', body: 'Text' },
    })
    renderWithQuery(<ContentPicker value={7} onChange={onChange} />)

    fireEvent.change(await screen.findByRole('combobox'), { target: { value: '' } })

    expect(onChange).toHaveBeenCalledWith(null)
  })

  it('shows the server reason when the chosen item cannot be opened', async () => {
    mockFetch({
      'GET /content': { items, total: 2 },
      'GET /content/7': reply({ detail: 'Content is locked' }, 403),
    })
    renderWithQuery(<ContentPicker value={null} onChange={jest.fn()} />)

    fireEvent.change(await screen.findByRole('combobox'), { target: { value: '7' } })

    expect(await screen.findByRole('alert')).toHaveTextContent('Content is locked')
  })

  it('shows the server reason when the list cannot be loaded', async () => {
    mockFetch({ 'GET /content': reply({ detail: 'Your account has no workspace yet.' }, 500) })
    renderWithQuery(<ContentPicker value={null} onChange={jest.fn()} />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no workspace yet.')
  })

  it('shows a loading message until the list arrives', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<ContentPicker value={null} onChange={jest.fn()} />)

    expect(screen.getByText('Loading your content…')).toBeInTheDocument()
  })
})
