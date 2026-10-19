import { fireEvent, render, screen, waitFor } from '@testing-library/react'
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

const paused = { ...endpoint, id: 8, url: 'https://hooks.example.com/paused', is_active: false }

function routeGet(list: unknown[], deliveries: unknown[] = []) {
  get.mockImplementation((path: string) => {
    if (path === '/outbound-webhooks') return Promise.resolve(list)
    if (path === '/outbound-webhooks/events') return Promise.resolve(eventTypes)
    if (path.startsWith('/outbound-webhooks/')) return Promise.resolve(deliveries)
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('/dashboard/webhooks page fallbacks', () => {
  beforeEach(() => jest.clearAllMocks())

  it('updates only the endpoint that was paused when several are listed', async () => {
    routeGet([endpoint, paused])
    patch.mockResolvedValueOnce({ ...endpoint, is_active: false })
    render(<WebhooksPage />)

    await screen.findByText('https://hooks.example.com/paused')
    fireEvent.click(screen.getAllByRole('button', { name: 'Pause' })[0])

    expect(await screen.findByText('Endpoint paused.')).toBeInTheDocument()
    expect(screen.getByText('https://hooks.example.com/paused')).toBeInTheDocument()
  })

  it('resumes a paused endpoint and says so', async () => {
    routeGet([paused])
    patch.mockResolvedValueOnce({ ...paused, is_active: true })
    render(<WebhooksPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Resume' }))

    expect(await screen.findByText('Endpoint resumed.')).toBeInTheDocument()
    expect(patch).toHaveBeenCalledWith('/outbound-webhooks/8', { is_active: true })
  })

  it('uses a generic message when a test delivery is refused without a reason', async () => {
    routeGet([endpoint])
    post.mockResolvedValueOnce({ id: 3, webhook_id: 7, event: 'webhook.test', status: 'failed', response_status: null, error: null, created_at: null })
    render(<WebhooksPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Send test' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('The test event was not accepted.')
  })

  it('keeps the endpoint when deletion is declined', async () => {
    routeGet([endpoint])
    const confirm = jest.spyOn(window, 'confirm').mockReturnValue(false)
    render(<WebhooksPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Delete' }))

    expect(del).not.toHaveBeenCalled()
    expect(screen.getByText('https://hooks.example.com/receive')).toBeInTheDocument()
    confirm.mockRestore()
  })

  it('shows a dash for a delivery with neither a status code nor an error, and an empty history message', async () => {
    routeGet([endpoint], [
      { id: 1, webhook_id: 7, event: 'content.published', status: 'delivered', response_status: null, error: null, created_at: null },
    ])
    render(<WebhooksPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Deliveries' }))

    expect(await screen.findByText('Delivered')).toBeInTheDocument()
    expect(screen.getAllByText('—').length).toBeGreaterThan(0)
  })

  it('says when an endpoint has no deliveries yet', async () => {
    routeGet([endpoint], [])
    render(<WebhooksPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Deliveries' }))

    expect(await screen.findByText('No deliveries yet.')).toBeInTheDocument()
  })

  it('reports a failure to load the delivery history', async () => {
    get.mockImplementation((path: string) => {
      if (path === '/outbound-webhooks') return Promise.resolve([endpoint])
      if (path === '/outbound-webhooks/events') return Promise.resolve(eventTypes)
      return Promise.reject(new ApiError('History unavailable'))
    })
    render(<WebhooksPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Deliveries' }))

    expect(await screen.findByText('History unavailable')).toBeInTheDocument()
  })

  it('ticks an event and then unticks it again', async () => {
    routeGet([endpoint])
    render(<WebhooksPage />)

    await screen.findByText('https://hooks.example.com/receive')
    const first = (await screen.findAllByRole('checkbox'))[0]
    fireEvent.click(first)
    expect(first).toBeChecked()
    fireEvent.click(first)
    await waitFor(() => expect(first).not.toBeChecked())
  })
})
