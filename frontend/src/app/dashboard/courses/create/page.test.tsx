import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import CreateCoursePage from '@/app/dashboard/courses/create/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

describe('/dashboard/courses/create page', () => {
  it('sends the course with trimmed text and one entry per line for the lists', async () => {
    const fetchMock = mockFetch({ 'POST /courses': { id: 12, title: 'Storytelling' } })
    renderWithQuery(<CreateCoursePage />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: '  Storytelling  ' } })
    fireEvent.change(screen.getByLabelText('Price (USD)'), { target: { value: '49.5' } })
    fireEvent.change(screen.getByLabelText('Level'), { target: { value: 'advanced' } })
    fireEvent.change(screen.getByLabelText('Learning objectives (one per line)'), {
      target: { value: 'Hook viewers\n\n  Pace scenes  ' },
    })
    fireEvent.change(screen.getByLabelText('Prerequisites (one per line)'), { target: { value: 'Writing 101' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create course' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/courses/12'))
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/courses') && init?.method === 'POST')
    expect(JSON.parse(post![1].body as string)).toEqual({
      title: 'Storytelling',
      description: null,
      category: 'general',
      price: 49.5,
      difficulty_level: 'advanced',
      language: 'en',
      prerequisites: ['Writing 101'],
      learning_objectives: ['Hook viewers', 'Pace scenes'],
    })
  })

  it('sends a zero price when the price is not a number', async () => {
    const fetchMock = mockFetch({ 'POST /courses': { id: 13 } })
    renderWithQuery(<CreateCoursePage />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Free intro' } })
    fireEvent.change(screen.getByLabelText('Price (USD)'), { target: { value: '' } })
    fireEvent.change(screen.getByLabelText('Category'), { target: { value: '  Writing  ' } })
    fireEvent.change(screen.getByLabelText('Description'), { target: { value: 'Short' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create course' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/courses/13'))
    const post = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith('/courses') && init?.method === 'POST')
    const body = JSON.parse(post![1].body as string)
    expect(body.price).toBe(0)
    expect(body.category).toBe('Writing')
    expect(body.description).toBe('Short')
  })

  it('shows the server reason and stays on the form when creation is refused', async () => {
    mockFetch({ 'POST /courses': reply({ detail: 'Your account has no tenant for courses yet.' }, 422) })
    renderWithQuery(<CreateCoursePage />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Storytelling' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create course' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no tenant for courses yet.')
    expect(useRouter().push).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Create course' })).toBeEnabled()
  })

  it('shows the saving state while the request runs', async () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    renderWithQuery(<CreateCoursePage />)

    fireEvent.change(screen.getByLabelText('Title'), { target: { value: 'Storytelling' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create course' }))

    expect(await screen.findByRole('button', { name: 'Creating…' })).toBeDisabled()
  })

  it('links back to the course list', () => {
    renderWithQuery(<CreateCoursePage />)

    expect(screen.getByRole('link', { name: 'Back to courses' })).toHaveAttribute('href', '/dashboard/courses')
  })
})
