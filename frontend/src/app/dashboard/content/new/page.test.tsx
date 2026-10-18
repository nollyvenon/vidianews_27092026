import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import NewContentPage from '@/app/dashboard/content/new/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

describe('/dashboard/content/new page', () => {
  it('creates the item from the form and opens its detail page', async () => {
    const fetchMock = mockFetch({ 'POST /content': { id: 9, title: 'Storm report' } })
    renderWithQuery(<NewContentPage />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Storm report' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create content' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/content/9'))
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/content') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      title: 'Storm report',
      slug: 'storm-report',
      description: null,
      body: null,
      content_type: 'article',
      status: 'draft',
      access_level: 'public',
      thumbnail_url: null,
    })
  })

  it('keeps the author on the form and shows the server reason when creation is refused', async () => {
    mockFetch({ 'POST /content': reply({ detail: 'A content item with this slug already exists' }, 409) })
    renderWithQuery(<NewContentPage />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Storm report' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create content' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('A content item with this slug already exists')
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('links back to the content list', () => {
    renderWithQuery(<NewContentPage />)

    expect(screen.getByRole('link', { name: 'Back to content' })).toHaveAttribute('href', '/dashboard/content')
  })
})
