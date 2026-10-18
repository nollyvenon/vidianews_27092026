import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import NotificationsCenterPage from '@/app/dashboard/notifications-center/page'
import { mockFetch, reply } from '@/test-utils'

const items = [
  {
    id: 1,
    title: 'Upload complete',
    message: 'Tutorial.mp4 is ready',
    is_read: false,
    notification_type: 'system',
    created_at: '2026-10-01T10:00:00Z',
  },
  {
    id: 2,
    title: 'Welcome',
    message: 'Thanks for joining',
    is_read: true,
    notification_type: 'info',
    created_at: '2026-09-30T10:00:00Z',
  },
]

describe('/dashboard/notifications-center page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state, then the notifications with their type', async () => {
    mockFetch({ 'GET /system/notifications': items })
    render(<NotificationsCenterPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByText('Upload complete')).toBeInTheDocument()
    expect(screen.getByText('system')).toBeInTheDocument()
    expect(screen.getByText('Thanks for joining')).toBeInTheDocument()
  })

  it('marks an unread notification as read when it is clicked', async () => {
    const fetchMock = mockFetch({
      'GET /system/notifications': items,
      'POST /system/notifications/1/read': { ok: true },
    })
    render(<NotificationsCenterPage />)

    const unread = (await screen.findByText('Upload complete')).closest('div.p-4') as HTMLElement
    expect(unread).toHaveClass('bg-blue-50')
    fireEvent.click(unread)

    await waitFor(() => expect(unread).toHaveClass('bg-white'))
    expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/system/notifications/1/read') && init?.method === 'POST')).toBe(true)
  })

  it('does not call the API when an already-read notification is clicked', async () => {
    const fetchMock = mockFetch({ 'GET /system/notifications': items })
    render(<NotificationsCenterPage />)

    fireEvent.click((await screen.findByText('Welcome')).closest('div.p-4') as HTMLElement)

    expect(fetchMock.mock.calls.filter(([, init]) => init?.method === 'POST')).toHaveLength(0)
  })

  it('shows the empty state when there are no notifications', async () => {
    mockFetch({ 'GET /system/notifications': [] })
    render(<NotificationsCenterPage />)

    expect(await screen.findByText('No notifications')).toBeInTheDocument()
  })

  it('logs a failed load and still leaves the loading state', async () => {
    mockFetch({ 'GET /system/notifications': reply({ detail: 'down' }, 500) })
    render(<NotificationsCenterPage />)

    expect(await screen.findByText('No notifications')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch notifications', expect.any(Error))
  })

  it('logs a failed mark-as-read and keeps the notification unread', async () => {
    mockFetch({
      'GET /system/notifications': items,
      'POST /system/notifications/1/read': reply({ detail: 'nope' }, 500),
    })
    render(<NotificationsCenterPage />)

    const unread = (await screen.findByText('Upload complete')).closest('div.p-4') as HTMLElement
    fireEvent.click(unread)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to mark as read', expect.any(Error)))
    expect(unread).toHaveClass('bg-blue-50')
  })
})
