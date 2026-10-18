import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import NotificationsPage from '@/app/dashboard/notifications/page'
import { mockFetch, reply } from '@/test-utils'

const unread = {
  id: 1,
  title: 'New follower',
  message: 'Sarah followed you',
  is_read: false,
  created_at: '2026-10-01T10:00:00Z',
}
const read = {
  id: 2,
  title: 'Comment',
  message: 'Great video',
  is_read: true,
  created_at: '2026-09-30T10:00:00Z',
}

function mockNotifications(items = [unread, read], count = 1) {
  return mockFetch({
    'GET /notifications/me/unread-count': { unread_count: count },
    'GET /notifications/me': items,
    'POST /notifications/me/read-all': { ok: true },
    'POST /notifications/me/1/read': { ok: true },
    'POST /notifications/me/1/archive': { ok: true },
    'DELETE /notifications/me/1': { ok: true },
  })
}

describe('/dashboard/notifications page', () => {
  it('shows a loading state and then the notification list with the unread count', async () => {
    mockNotifications()
    render(<NotificationsPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'New follower' })).toBeInTheDocument()
    expect(screen.getByText('1 unread')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Comment' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Mark all as read' })).toBeInTheDocument()
  })

  it('offers a per-notification read action only for unread notifications', async () => {
    mockNotifications()
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })

    expect(screen.getAllByRole('button', { name: 'Mark read' })).toHaveLength(1)
    expect(screen.getAllByRole('button', { name: 'Archive' })).toHaveLength(2)
    expect(screen.getAllByRole('button', { name: 'Delete' })).toHaveLength(2)
  })

  it('marks every notification read and refreshes the list', async () => {
    const fetchMock = mockNotifications()
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })

    fireEvent.click(screen.getByRole('button', { name: 'Mark all as read' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/notifications/me/read-all'))).toBe(true)
    )
    // The list request carries a query string (?limit=50), so match on the path prefix.
    await waitFor(() =>
      expect(fetchMock.mock.calls.filter(([url]) => String(url).includes('/notifications/me?limit=')).length).toBeGreaterThan(1)
    )
  })

  it('marks a single notification read', async () => {
    const fetchMock = mockNotifications()
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })

    fireEvent.click(screen.getByRole('button', { name: 'Mark read' }))

    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/notifications/me/1/read'))).toBe(true)
    )
  })

  it('archives and deletes a notification', async () => {
    const fetchMock = mockNotifications()
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })

    fireEvent.click(screen.getAllByRole('button', { name: 'Archive' })[0])
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url]) => String(url).endsWith('/notifications/me/1/archive'))).toBe(true)
    )

    fireEvent.click(screen.getAllByRole('button', { name: 'Delete' })[0])
    await waitFor(() =>
      expect(
        fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/notifications/me/1') && init?.method === 'DELETE')
      ).toBe(true)
    )
  })

  it('shows the error returned by a failed action', async () => {
    mockFetch({
      'GET /notifications/me/unread-count': { unread_count: 0 },
      'GET /notifications/me': [unread],
      'DELETE /notifications/me/1': reply({ detail: 'Cannot delete' }, 409),
    })
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Cannot delete')
  })

  it('reports an empty inbox and hides the unread badge', async () => {
    mockNotifications([], 0)
    render(<NotificationsPage />)

    expect(await screen.findByText('No notifications')).toBeInTheDocument()
    expect(screen.queryByText(/unread/)).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Mark all as read' })).not.toBeInTheDocument()
  })

  it('shows a generic message when a failure has no message', async () => {
    mockFetch({})
    global.fetch = jest.fn().mockRejectedValue('boom') as unknown as typeof fetch
    render(<NotificationsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Failed to load notifications')
  })

  it('explains that push devices are not available and links to settings', async () => {
    mockNotifications()
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })

    expect(screen.getByRole('link', { name: 'Settings' })).toHaveAttribute('href', '/dashboard/settings')
    expect(screen.getByText(/Registered push devices are not yet available/)).toBeInTheDocument()
  })

  it('reports a non-Error action failure with the generic message', async () => {
    mockNotifications()
    render(<NotificationsPage />)
    await screen.findByRole('heading', { name: 'New follower' })
    global.fetch = jest.fn().mockRejectedValue('offline') as unknown as typeof fetch

    fireEvent.click(screen.getByRole('button', { name: 'Mark read' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Action failed')
  })
})
