import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import RealtimePage from '@/app/dashboard/realtime/page'
import { mockFetch, reply } from '@/test-utils'

const events = [
  { id: 2, event_type: 'message', event_source: 'live-feed', payload: { message: 'Second post' }, created_at: '2026-10-18T09:00:00Z' },
  { id: 1, event_type: 'upload', event_source: 'studio', payload: { title: 'New clip' }, created_at: null },
]

function bodyOf(fetchMock: jest.Mock, method: string, path: string): Record<string, unknown> {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).includes(path) && (init?.method ?? 'GET') === method)
  if (!call) throw new Error(`No ${method} call to ${path}`)
  return JSON.parse(String(call[1]?.body))
}

describe('/dashboard/realtime page', () => {
  afterEach(() => {
    jest.useRealTimers();
  });

  it('lists the recent events and the number of users online and idle', async () => {
    mockFetch({ 'GET /websocket/events': events, 'GET /websocket/presence': { online: 45, idle: 12 } })
    render(<RealtimePage />)

    expect(await screen.findByText('Second post')).toBeInTheDocument()
    expect(screen.getByText('studio')).toBeInTheDocument()
    expect(screen.getByText('{"title":"New clip"}')).toBeInTheDocument()
    expect(screen.getByText('45 users online')).toBeInTheDocument()
    expect(screen.getByText('12 users idle')).toBeInTheDocument()
  });

  it('says when there are no events yet', async () => {
    mockFetch({ 'GET /websocket/events': [], 'GET /websocket/presence': { online: 0, idle: 0 } })
    render(<RealtimePage />)

    expect(await screen.findByText('No events yet.')).toBeInTheDocument()
    expect(screen.getByText('0 users online')).toBeInTheDocument()
  });

  it('shows loading placeholders while the feed is in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<RealtimePage />)

    expect(screen.getByText('Loading events…')).toBeInTheDocument()
    expect(screen.getAllByText('Loading…')).toHaveLength(2)
  });

  it('broadcasts the message typed and refreshes the feed', async () => {
    const fetchMock = mockFetch({
      'GET /websocket/events': events,
      'GET /websocket/presence': { online: 1, idle: 0 },
      'POST /websocket/broadcast': reply({ id: 3, event_type: 'message', status: 'pending', created_at: '2026-10-18T09:05:00Z' }, 200),
    })
    render(<RealtimePage />)
    await screen.findByText('Second post');

    fireEvent.change(screen.getByLabelText('Message'), { target: { value: '  Hello everyone  ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    await waitFor(() => expect(screen.getByLabelText('Message')).toHaveValue(''));
    expect(bodyOf(fetchMock, 'POST', '/websocket/broadcast')).toEqual({
      event_type: 'message',
      event_source: 'live-feed',
      user_ids: [],
      payload: { message: 'Hello everyone' },
      priority: 0,
    });
  });

  it('keeps Send disabled while the message is blank', async () => {
    mockFetch({ 'GET /websocket/events': events, 'GET /websocket/presence': { online: 1, idle: 0 } })
    render(<RealtimePage />)
    await screen.findByText('Second post');

    fireEvent.change(screen.getByLabelText('Message'), { target: { value: '   ' } })

    expect(screen.getByRole('button', { name: 'Send' })).toBeDisabled()
  });

  it('shows the server reason when a message cannot be sent', async () => {
    mockFetch({
      'GET /websocket/events': events,
      'GET /websocket/presence': { online: 1, idle: 0 },
      'POST /websocket/broadcast': reply({ detail: 'Event rejected' }, 422),
    })
    render(<RealtimePage />)
    await screen.findByText('Second post');

    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Hi' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Event rejected')
  });

  it('shows the server reason when the feed cannot be loaded', async () => {
    mockFetch({ 'GET /websocket/events': reply({ detail: 'Feed offline' }, 503), 'GET /websocket/presence': { online: 0, idle: 0 } })
    render(<RealtimePage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Feed offline')
  });

  it('uses generic messages when the requests fail without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<RealtimePage />)

    expect(await screen.findByText('The live feed could not be loaded.')).toBeInTheDocument()
  });

  it('refreshes the feed on an interval and stops when the page is left', async () => {
    jest.useFakeTimers()
    const fetchMock = mockFetch({ 'GET /websocket/events': events, 'GET /websocket/presence': { online: 1, idle: 0 } })
    const { unmount } = render(<RealtimePage />)
    await act(async () => {
      await Promise.resolve()
    })
    const countBefore = fetchMock.mock.calls.length

    await act(async () => {
      jest.advanceTimersByTime(15_000)
      await Promise.resolve()
    })
    expect(fetchMock.mock.calls.length).toBeGreaterThan(countBefore)

    unmount()
    const countAfterUnmount = fetchMock.mock.calls.length
    await act(async () => {
      jest.advanceTimersByTime(60_000)
    })
    expect(fetchMock.mock.calls.length).toBe(countAfterUnmount)
  });
})
