import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import ModerationPage from '@/app/dashboard/moderation/page'
import { mockFetch, reply } from '@/test-utils'

const queue = [
  { id: 1, content_id: 40, content_type: 'video', status: 'pending', reason: 'Offensive language', confidence_score: 0.92, created_at: '2026-10-17T10:00:00Z' },
  { id: 2, content_id: 41, content_type: 'comment', status: 'pending', reason: 'Promotional link', confidence_score: 0.6, created_at: '2026-10-17T09:00:00Z' },
]

function requestTo(fetchMock: jest.Mock, suffix: string) {
  return fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === 'POST')
}

describe('/dashboard/moderation page', () => {
  it('lists the pending queue with the reason and confidence for each item', async () => {
    mockFetch({ 'GET /moderation/queue/pending': queue })
    render(<ModerationPage />)

    expect(await screen.findByText('video #40')).toBeInTheDocument()
    expect(screen.getByText('Reason: Offensive language')).toBeInTheDocument()
    expect(screen.getByText('Confidence: 92%')).toBeInTheDocument()
    expect(screen.getByText('comment #41')).toBeInTheDocument()
    expect(screen.getByText('Confidence: 60%')).toBeInTheDocument()
  })

  it('requires a decision note before a review can be recorded', async () => {
    mockFetch({ 'GET /moderation/queue/pending': queue })
    render(<ModerationPage />)
    await screen.findByText('video #40')

    expect(screen.getAllByRole('button', { name: 'Approve' })[0]).toBeDisabled()
    expect(screen.getAllByRole('button', { name: 'Reject' })[0]).toBeDisabled()
  })

  it('approves an item with the note and reloads the queue', async () => {
    const fetchMock = mockFetch({
      'GET /moderation/queue/pending': queue,
      'POST /moderation/queue/1/review': { reviewed: true, status: 'approved' },
    })
    render(<ModerationPage />)
    await screen.findByText('video #40')

    fireEvent.change(screen.getByPlaceholderText('Why you approved or rejected this content'), { target: { value: ' Within policy ' } })
    fireEvent.click(screen.getAllByRole('button', { name: 'Approve' })[0])

    await waitFor(() => expect(requestTo(fetchMock, '/moderation/queue/1/review')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, '/moderation/queue/1/review')![1].body as string)).toEqual({
      status: 'approved',
      decision: 'Within policy',
    })
  })

  it('rejects an item with the note', async () => {
    const fetchMock = mockFetch({
      'GET /moderation/queue/pending': queue,
      'POST /moderation/queue/2/review': { reviewed: true, status: 'rejected' },
    })
    render(<ModerationPage />)
    await screen.findByText('comment #41')

    fireEvent.change(screen.getByPlaceholderText('Why you approved or rejected this content'), { target: { value: 'Spam' } })
    fireEvent.click(screen.getAllByRole('button', { name: 'Reject' })[1])

    await waitFor(() => expect(requestTo(fetchMock, '/moderation/queue/2/review')).toBeDefined())
    expect(JSON.parse(requestTo(fetchMock, '/moderation/queue/2/review')![1].body as string)).toEqual({
      status: 'rejected',
      decision: 'Spam',
    })
  })

  it('shows the server reason when a review cannot be saved', async () => {
    mockFetch({
      'GET /moderation/queue/pending': queue,
      'POST /moderation/queue/1/review': reply({ detail: 'Item was already reviewed' }, 409),
    })
    render(<ModerationPage />)
    await screen.findByText('video #40')

    fireEvent.change(screen.getByPlaceholderText('Why you approved or rejected this content'), { target: { value: 'Checked' } })
    fireEvent.click(screen.getAllByRole('button', { name: 'Approve' })[0])

    expect(await screen.findByRole('alert')).toHaveTextContent('Item was already reviewed')
  })

  it('says when nothing is waiting for review', async () => {
    mockFetch({ 'GET /moderation/queue/pending': [] })
    render(<ModerationPage />)

    expect(await screen.findByText('No content is waiting for review.')).toBeInTheDocument()
  })

  it('shows the server reason when the queue cannot be loaded', async () => {
    mockFetch({ 'GET /moderation/queue/pending': reply({ detail: 'Moderator role required' }, 403) })
    render(<ModerationPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Moderator role required')
  })
})
