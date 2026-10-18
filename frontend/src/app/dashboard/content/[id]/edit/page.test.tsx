import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useParams, useRouter } from 'next/navigation'
import EditContentPage from '@/app/dashboard/content/[id]/edit/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const item = {
  id: 1,
  title: 'Storm report',
  slug: 'storm-report',
  description: null,
  body: 'The storm arrived early.',
  content_type: 'article',
  status: 'draft',
  access_level: 'public',
  thumbnail_url: null,
}

describe('/dashboard/content/[id]/edit page', () => {
  beforeEach(() => {
    ;(useParams as jest.Mock).mockReturnValue({ id: '1' })
  })

  it('shows a loading message until the item is loaded', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<EditContentPage />)

    expect(screen.getByText('Loading content…')).toBeInTheDocument()
  })

  it('pre-fills the form with the stored values', async () => {
    mockFetch({ 'GET /content/1': item })
    renderWithQuery(<EditContentPage />)

    expect(await screen.findByDisplayValue('Storm report')).toBeInTheDocument()
    expect(screen.getByLabelText('Slug')).toHaveValue('storm-report')
    expect(screen.getByLabelText('Body')).toHaveValue('The storm arrived early.')
    expect(screen.getByRole('button', { name: 'Save changes' })).toBeEnabled()
  })

  it('saves the changes and returns to the item', async () => {
    const fetchMock = mockFetch({ 'GET /content/1': item, 'PUT /content/1': { ...item, title: 'Storm report revised' } })
    renderWithQuery(<EditContentPage />)

    fireEvent.change(await screen.findByLabelText('Title'), { target: { value: 'Storm report revised' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save changes' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/content/1'))
    const put = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/content/1') && init?.method === 'PUT')
    expect(JSON.parse(put![1].body as string)).toEqual({
      title: 'Storm report revised',
      slug: 'storm-report',
      description: null,
      body: 'The storm arrived early.',
      content_type: 'article',
      status: 'draft',
      access_level: 'public',
      thumbnail_url: null,
    })
  })

  it('keeps the form open and shows the server reason when saving is refused', async () => {
    mockFetch({
      'GET /content/1': item,
      'PUT /content/1': reply({ detail: 'Slug already used by another item' }, 409),
    })
    renderWithQuery(<EditContentPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Save changes' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Slug already used by another item')
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('shows the server reason when the item cannot be loaded', async () => {
    mockFetch({ 'GET /content/1': reply({ detail: 'Content not found' }, 404) })
    renderWithQuery(<EditContentPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Content not found')
  })

  it('links back to the item', async () => {
    mockFetch({ 'GET /content/1': item })
    renderWithQuery(<EditContentPage />)

    expect(await screen.findByRole('link', { name: 'Back to content' })).toHaveAttribute('href', '/dashboard/content/1')
  })
})
