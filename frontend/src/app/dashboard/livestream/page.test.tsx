import { fireEvent, screen, waitFor } from '@testing-library/react'
import LivestreamPage from '@/app/dashboard/livestream/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({ 'GET /livestream/active': [{ id: 1, title: 'Morning briefing', viewers: 42 }], ...extra })
}

describe('/dashboard/livestream page', () => {
  it('lists the streams that are live now with their viewers', async () => {
    base()
    renderWithQuery(<LivestreamPage />)

    expect(await screen.findByText('Morning briefing')).toBeInTheDocument()
    expect(screen.getByText('42 viewers')).toBeInTheDocument()
  })

  it('says when nobody is live', async () => {
    base({ 'GET /livestream/active': [] })
    renderWithQuery(<LivestreamPage />)

    expect(await screen.findByText('Nobody is live right now.')).toBeInTheDocument()
  })

  it('creates a stream and shows its key', async () => {
    const fetchMock = base({ 'POST /livestream': { id: 8, stream_key: 'sk_live_123', status: 'scheduled' } })
    renderWithQuery(<LivestreamPage />)
    await screen.findByText('Morning briefing')

    fireEvent.change(screen.getByPlaceholderText('Stream title'), { target: { value: 'Evening news' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: 'Top stories' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create stream' }))

    expect(await screen.findByText('sk_live_123')).toBeInTheDocument()
    expect(screen.getByText('Stream #8 is scheduled.')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/livestream?title=Evening+news&description=Top+stories'))).toBe(true)
  })

  it('starts a stream by its id and reloads the live list', async () => {
    const fetchMock = base({ 'PUT /livestream/8/start': { started: true } })
    renderWithQuery(<LivestreamPage />)
    await screen.findByText('Morning briefing')

    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '8' } })
    fireEvent.click(screen.getByRole('button', { name: 'Start' }))

    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/livestream/8/start') && init?.method === 'PUT')).toBe(true))
  })

  it('shows the server reason when a stream cannot be ended', async () => {
    base({ 'PUT /livestream/8/end': reply({ detail: 'Stream is not live' }, 409) })
    renderWithQuery(<LivestreamPage />)
    await screen.findByText('Morning briefing')

    fireEvent.change(screen.getByRole('spinbutton'), { target: { value: '8' } })
    fireEvent.click(screen.getByRole('button', { name: 'End' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Stream is not live')
  })
})
