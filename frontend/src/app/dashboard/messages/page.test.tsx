import { fireEvent, screen, waitFor } from '@testing-library/react'
import MessagesPage from '@/app/dashboard/messages/page'
import { mockFetch, reply, renderWithAuth, testUser } from '@/test-utils'

const thread = [
  { id: 1, sender_id: 7, content: 'Can you review the draft?', is_read: false },
  { id: 2, sender_id: testUser.id, content: 'Sure, tomorrow.', is_read: true },
]

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({ 'GET /messages/unread/count': { unread_count: 3 }, ...extra })
}

describe('/dashboard/messages page', () => {
  it('shows the number of unread messages', async () => {
    base()
    renderWithAuth(<MessagesPage />)

    expect(await screen.findByText('Unread messages: 3')).toBeInTheDocument()
  })

  it('opens a conversation with a member and lists it', async () => {
    const fetchMock = base({ 'GET /messages/7': thread })
    renderWithAuth(<MessagesPage />)

    fireEvent.change(screen.getByLabelText('Member user ID'), { target: { value: '7' } })
    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }))

    expect(await screen.findByText('Can you review the draft?')).toBeInTheDocument()
    expect(screen.getByText('Sure, tomorrow.')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/messages/7'))).toBe(true)
  })

  it('says when there are no messages with the member yet', async () => {
    base({ 'GET /messages/9': [] })
    renderWithAuth(<MessagesPage />)

    fireEvent.change(screen.getByLabelText('Member user ID'), { target: { value: '9' } })
    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }))

    expect(await screen.findByText('No messages with this member yet.')).toBeInTheDocument()
  })

  it('sends a message to the member and reloads the conversation', async () => {
    const fetchMock = base({ 'GET /messages/7': thread, 'POST /messages/send': { id: 3, sent_at: '2026-10-18T10:00:00Z' } })
    renderWithAuth(<MessagesPage />)

    fireEvent.change(screen.getByLabelText('Member user ID'), { target: { value: '7' } })
    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }))
    await screen.findByText('Can you review the draft?')
    fireEvent.change(screen.getByPlaceholderText('Write a message'), { target: { value: ' Thanks ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/messages/send?recipient_id=7&content=Thanks'))).toBe(true),
    )
  })

  it('marks an unread message from the member as read', async () => {
    const fetchMock = base({ 'GET /messages/7': thread, 'PUT /messages/1/read': { read: true } })
    renderWithAuth(<MessagesPage />)

    fireEvent.change(screen.getByLabelText('Member user ID'), { target: { value: '7' } })
    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }))
    fireEvent.click(await screen.findByRole('button', { name: 'Mark read' }))

    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/messages/1/read') && init?.method === 'PUT')).toBe(true))
    expect(await screen.findByText('Unread messages: 2')).toBeInTheDocument()
  })

  it('shows the server reason when the conversation cannot be loaded', async () => {
    base({ 'GET /messages/7': reply({ detail: 'You cannot message this member' }, 403) })
    renderWithAuth(<MessagesPage />)

    fireEvent.change(screen.getByLabelText('Member user ID'), { target: { value: '7' } })
    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('You cannot message this member')
  })
})
