import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import WebhooksPage from '@/app/dashboard/webhooks/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn(), patch: jest.fn(), delete: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock
const patch = ApiClient.patch as jest.Mock
const del = ApiClient.delete as jest.Mock

const eventTypes = [
  { event: 'content.published', description: 'A content item was published' },
  { event: 'user.created', description: 'A user account was created' },
]

const endpoint = {
  id: 7,
  url: 'https://hooks.example.com/receive',
  description: 'Main receiver',
  events: ['content.published'],
  is_active: true,
  created_at: '2026-10-01T10:00:00Z',
  updated_at: '2026-10-01T10:00:00Z',
}

function routeGet(list = [endpoint]) {
  get.mockImplementation((path: string) => {
    if (path === '/outbound-webhooks') return Promise.resolve(list)
    if (path === '/outbound-webhooks/events') return Promise.resolve(eventTypes)
    if (path.startsWith('/outbound-webhooks/7/deliveries')) return Promise.resolve([])
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('/dashboard/webhooks page', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    routeGet()
  })

  it('lists the endpoints with their events and status', async () => {
    render(<WebhooksPage />)
    expect(await screen.findByText('https://hooks.example.com/receive')).toBeInTheDocument()
    expect(screen.getByText('Main receiver')).toBeInTheDocument()
    expect(screen.getByText('Active')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Pause' })).toBeInTheDocument()
  })

  it('shows the empty state when no endpoint exists', async () => {
    routeGet([])
    render(<WebhooksPage />)
    expect(await screen.findByText(/No endpoints yet/)).toBeInTheDocument()
  })

  it('shows a load error instead of a fabricated list', async () => {
    get.mockRejectedValue(new ApiError('Service unavailable'))
    render(<WebhooksPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Service unavailable')
    expect(screen.queryByText('https://example.com/hook')).not.toBeInTheDocument()
  })

  it('refuses a non-HTTPS endpoint without calling the API', async () => {
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.change(screen.getByLabelText('Endpoint URL'), { target: { value: 'http://insecure.example.com' } })
    fireEvent.click(screen.getByLabelText(/content.published/))
    fireEvent.click(screen.getByRole('button', { name: 'Add endpoint' }))

    expect(await screen.findByText(/must be an https:\/\/ address/)).toBeInTheDocument()
    expect(post).not.toHaveBeenCalled()
  })

  it('requires at least one event', async () => {
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.change(screen.getByLabelText('Endpoint URL'), { target: { value: 'https://new.example.com/hook' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add endpoint' }))

    expect(await screen.findByText('Select at least one event.')).toBeInTheDocument()
    expect(post).not.toHaveBeenCalled()
  })

  it('creates an endpoint, shows its secret once and keeps the secret out of the list', async () => {
    const created = { ...endpoint, id: 9, url: 'https://new.example.com/hook', events: ['user.created'], secret: 'whsec_abc' }
    post.mockResolvedValueOnce(created)
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')

    fireEvent.change(screen.getByLabelText('Endpoint URL'), { target: { value: 'https://new.example.com/hook' } })
    fireEvent.click(screen.getByLabelText(/user.created/))
    fireEvent.click(screen.getByRole('button', { name: 'Add endpoint' }))

    expect(await screen.findByText('whsec_abc')).toBeInTheDocument()
    expect(post).toHaveBeenCalledWith('/outbound-webhooks', {
      url: 'https://new.example.com/hook',
      description: null,
      events: ['user.created'],
    })
    const list = screen.getByRole('list')
    expect(within(list).getByText('https://new.example.com/hook')).toBeInTheDocument()
    expect(within(list).queryByText('whsec_abc')).not.toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'I have saved it' }))
    expect(screen.queryByText('whsec_abc')).not.toBeInTheDocument()
  })

  it('shows the server reason when creation is refused', async () => {
    post.mockRejectedValueOnce(new ApiError('Endpoint URL must not point to a private or reserved address'))
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.change(screen.getByLabelText('Endpoint URL'), { target: { value: 'https://10.0.0.5/hook' } })
    fireEvent.click(screen.getByLabelText(/content.published/))
    fireEvent.click(screen.getByRole('button', { name: 'Add endpoint' }))

    expect(await screen.findByText(/private or reserved address/)).toBeInTheDocument()
  })

  it('sends a test event and reports that it was delivered', async () => {
    post.mockResolvedValueOnce({ id: 1, webhook_id: 7, event: 'webhook.test', status: 'delivered', response_status: 204, error: null, created_at: null })
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Send test' }))

    expect(await screen.findByText('Test event delivered.')).toBeInTheDocument()
    expect(post).toHaveBeenCalledWith('/outbound-webhooks/7/test', {})
  })

  it('reports a failed test delivery with the recorded reason', async () => {
    post.mockResolvedValueOnce({ id: 2, webhook_id: 7, event: 'webhook.test', status: 'failed', response_status: 500, error: 'Endpoint answered HTTP 500', created_at: null })
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Send test' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Endpoint answered HTTP 500')
  })

  it('pauses and resumes an endpoint', async () => {
    patch.mockResolvedValueOnce({ ...endpoint, is_active: false })
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Pause' }))

    expect(await screen.findByText('Endpoint paused.')).toBeInTheDocument()
    expect(patch).toHaveBeenCalledWith('/outbound-webhooks/7', { is_active: false })
    expect(screen.getByRole('button', { name: 'Resume' })).toBeInTheDocument()
  })

  it('rotates the secret after confirmation and shows the new one once', async () => {
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(true)
    post.mockResolvedValueOnce({ secret: 'whsec_rotated' })
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Rotate secret' }))

    expect(await screen.findByText('whsec_rotated')).toBeInTheDocument()
    expect(post).toHaveBeenCalledWith('/outbound-webhooks/7/rotate-secret', {})
    confirm.mockRestore()
  })

  it('does not rotate the secret when the administrator declines', async () => {
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(false)
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Rotate secret' }))

    expect(post).not.toHaveBeenCalled()
    confirm.mockRestore()
  })

  it('deletes an endpoint after confirmation', async () => {
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(true)
    del.mockResolvedValueOnce(null)
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    expect(await screen.findByText('Endpoint deleted.')).toBeInTheDocument()
    expect(del).toHaveBeenCalledWith('/outbound-webhooks/7')
    expect(screen.queryByText('https://hooks.example.com/receive')).not.toBeInTheDocument()
    confirm.mockRestore()
  })

  it('shows the delivery history for an endpoint', async () => {
    get.mockImplementation((path: string) => {
      if (path === '/outbound-webhooks') return Promise.resolve([endpoint])
      if (path === '/outbound-webhooks/events') return Promise.resolve(eventTypes)
      if (path.startsWith('/outbound-webhooks/7/deliveries')) {
        return Promise.resolve([
          { id: 1, webhook_id: 7, event: 'content.published', status: 'failed', response_status: 503, error: 'Endpoint answered HTTP 503', created_at: '2026-10-02T09:00:00Z' },
        ])
      }
      return Promise.reject(new Error(`unexpected GET ${path}`))
    })
    render(<WebhooksPage />)
    await screen.findByText('https://hooks.example.com/receive')
    fireEvent.click(screen.getByRole('button', { name: 'Deliveries' }))

    expect(await screen.findByText('Endpoint answered HTTP 503')).toBeInTheDocument()
    expect(screen.getByText('Failed')).toBeInTheDocument()
    await waitFor(() => expect(get).toHaveBeenCalledWith('/outbound-webhooks/7/deliveries?limit=20'))
  })
})
