import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import AlertsPage from '@/app/dashboard/alerts/page'
import { mockFetch, reply } from '@/test-utils'

const notifications = [
  { id: 1, title: 'New follower', message: 'Sarah followed you', is_read: false, created_at: '2026-10-17T10:00:00Z' },
  { id: 2, title: 'Mention', message: 'You were mentioned', is_read: true, created_at: '2026-10-16T10:00:00Z' },
]

describe('/dashboard/alerts page', () => {
  it('shows a loading message until the alerts arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<AlertsPage />)

    expect(screen.getByText('Loading alerts…')).toBeInTheDocument()
  })

  it('lists the signed-in user notifications and marks which are unread', async () => {
    mockFetch({ 'GET /notifications/me': notifications })
    render(<AlertsPage />)

    expect(await screen.findByText('New follower')).toBeInTheDocument()
    expect(screen.getByText('Sarah followed you')).toBeInTheDocument()
    expect(screen.getByText('You were mentioned')).toBeInTheDocument()
    expect(screen.getAllByRole('button', { name: 'Mark as read' })).toHaveLength(1)
    expect(screen.getByText('Read')).toBeInTheDocument()
  })

  it('says so when there are no alerts', async () => {
    mockFetch({ 'GET /notifications/me': [] })
    render(<AlertsPage />)

    expect(await screen.findByText('No alerts yet.')).toBeInTheDocument()
  })

  it('treats a response that is not a list as no alerts', async () => {
    mockFetch({ 'GET /notifications/me': { detail: 'unexpected' } })
    render(<AlertsPage />)

    expect(await screen.findByText('No alerts yet.')).toBeInTheDocument()
  })

  it('marks an alert as read on the server and updates it in place', async () => {
    const fetchMock = mockFetch({
      'GET /notifications/me': notifications,
      'POST /notifications/me/1/read': { ...notifications[0], is_read: true },
    })
    render(<AlertsPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Mark as read' }))

    await waitFor(() => expect(screen.queryByRole('button', { name: 'Mark as read' })).not.toBeInTheDocument())
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/notifications/me/1/read') && init?.method === 'POST')).toBe(true)
  })

  it('shows the server reason when an alert cannot be marked as read', async () => {
    mockFetch({
      'GET /notifications/me': notifications,
      'POST /notifications/me/1/read': reply({ detail: 'Notification not found' }, 404),
    })
    render(<AlertsPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Mark as read' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Notification not found')
  })

  it('shows the server reason when the alerts cannot be loaded', async () => {
    mockFetch({ 'GET /notifications/me': reply({ detail: 'Session expired' }, 401) })
    render(<AlertsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Session expired')
  })
})
