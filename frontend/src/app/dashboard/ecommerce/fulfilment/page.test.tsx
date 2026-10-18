import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import FulfilmentPage from '@/app/dashboard/ecommerce/fulfilment/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock

const pendingReturn = {
  id: 4, order_id: 9, rma_number: 'RMA-1', reason: 'defective', status: 'initiated',
  quantity_requested: 1, quantity_received: null, refund_amount: null,
}
const lowStock = { id: 2, product_id: 42, quantity_on_hand: 3, quantity_available: 3, reorder_level: 10, status: 'low_stock' }
const outOfStock = { id: 3, product_id: 43, quantity_on_hand: 0, quantity_available: 0, reorder_level: 10, status: 'out_of_stock' }

function routeGet(returns: unknown[] = [pendingReturn], low: unknown[] = [lowStock], out: unknown[] = [outOfStock]) {
  get.mockImplementation((path: string) => {
    if (path === '/returns/pending') return Promise.resolve(returns)
    if (path === '/inventory/low-stock') return Promise.resolve(low)
    if (path === '/inventory/out-of-stock') return Promise.resolve(out)
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('/dashboard/ecommerce/fulfilment page', () => {
  beforeEach(() => jest.clearAllMocks())

  it('shows stock alerts and pending returns', async () => {
    routeGet()
    render(<FulfilmentPage />)
    expect(await screen.findByText('Product #43 is out of stock (on hand 0)')).toBeInTheDocument()
    expect(screen.getByText('Product #42 is low on stock (on hand 3, reorder at 10)')).toBeInTheDocument()
    expect(screen.getByText('RMA-1')).toBeInTheDocument()
  })

  it('says when nothing needs attention', async () => {
    routeGet([], [], [])
    render(<FulfilmentPage />)
    expect(await screen.findByText('Every product is above its reorder level.')).toBeInTheDocument()
    expect(screen.getByText('No returns are waiting for a decision.')).toBeInTheDocument()
  })

  it('reports a load failure', async () => {
    get.mockRejectedValue(new ApiError('Not allowed'))
    render(<FulfilmentPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Not allowed')
  })

  it('creates a shipment for an order', async () => {
    routeGet([], [], [])
    post.mockResolvedValue({ id: 77 })
    render(<FulfilmentPage />)
    await screen.findByText('No returns are waiting for a decision.')

    fireEvent.change(screen.getByLabelText('Order number'), { target: { value: '9' } })
    fireEvent.change(screen.getByLabelText('Carrier'), { target: { value: 'dhl' } })
    fireEvent.change(screen.getByLabelText('Tracking number'), { target: { value: 'DHL-9' } })
    fireEvent.change(screen.getByLabelText('Base rate'), { target: { value: '4.5' } })
    fireEvent.change(screen.getByLabelText('Total cost'), { target: { value: '6' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create shipment' }))

    await waitFor(() =>
      expect(post).toHaveBeenCalledWith('/orders/9/shipment', {
        carrier: 'dhl', tracking_number: 'DHL-9', base_rate: 4.5, total_cost: 6,
      }),
    )
    expect(await screen.findByText('Shipment 77 created for order 9.')).toBeInTheDocument()
  })

  it('refuses a shipment without a valid order number', async () => {
    routeGet([], [], [])
    render(<FulfilmentPage />)
    await screen.findByText('No returns are waiting for a decision.')

    fireEvent.change(screen.getByLabelText('Order number'), { target: { value: 'x' } })
    fireEvent.change(screen.getByLabelText('Tracking number'), { target: { value: 'T-1' } })
    fireEvent.change(screen.getByLabelText('Base rate'), { target: { value: '1' } })
    fireEvent.change(screen.getByLabelText('Total cost'), { target: { value: '2' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create shipment' }))

    expect(await screen.findByText('Enter a valid order number.')).toBeInTheDocument()
    expect(post).not.toHaveBeenCalled()
  })

  it('adds a tracking update to a shipment', async () => {
    routeGet([], [], [])
    post.mockResolvedValue({})
    render(<FulfilmentPage />)
    await screen.findByText('No returns are waiting for a decision.')

    fireEvent.change(screen.getByLabelText('Shipment number'), { target: { value: '77' } })
    fireEvent.change(screen.getByLabelText('Status'), { target: { value: 'delivered' } })
    fireEvent.change(screen.getByLabelText('Location'), { target: { value: 'Dock 2' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add update' }))

    await waitFor(() =>
      expect(post).toHaveBeenCalledWith('/shipments/77/tracking', {
        status: 'delivered', location: 'Dock 2', description: null,
      }),
    )
  })

  it('approves a return with the approved refund amount', async () => {
    routeGet()
    post.mockResolvedValue({ status: 'approved' })
    render(<FulfilmentPage />)
    await screen.findByText('RMA-1')

    fireEvent.change(screen.getByLabelText('Approved refund for return 4'), { target: { value: '19.99' } })
    fireEvent.click(screen.getByRole('button', { name: 'Approve' }))

    await waitFor(() => expect(post).toHaveBeenCalledWith('/returns/4/approve?refund_amount=19.99', {}))
    expect(await screen.findByText('Return approved.')).toBeInTheDocument()
  })

  it('rejects a return', async () => {
    routeGet()
    post.mockResolvedValue({ status: 'rejected' })
    render(<FulfilmentPage />)
    await screen.findByText('RMA-1')

    fireEvent.click(screen.getByRole('button', { name: 'Reject' }))

    await waitFor(() => expect(post).toHaveBeenCalledWith('/returns/4/reject', {}))
  })

  it('shows the server message when a return action fails', async () => {
    routeGet()
    post.mockRejectedValue(new ApiError('Return cannot move from initiated to refunded'))
    render(<FulfilmentPage />)
    await screen.findByText('RMA-1')

    fireEvent.click(screen.getByRole('button', { name: 'Reject' }))

    expect(await screen.findByText('Return cannot move from initiated to refunded')).toBeInTheDocument()
  })

  it('moves a received return through to refund', async () => {
    routeGet([{ ...pendingReturn, status: 'received', quantity_received: 1 }])
    post.mockResolvedValue({ status: 'refunded' })
    render(<FulfilmentPage />)
    await screen.findByText('RMA-1')

    fireEvent.click(screen.getByRole('button', { name: 'Refund' }))

    await waitFor(() => expect(post).toHaveBeenCalledWith('/returns/4/refund', {}))
    expect(await screen.findByText('Refund processed.')).toBeInTheDocument()
  })

  it('records the items received for an approved return', async () => {
    routeGet([{ ...pendingReturn, status: 'approved' }])
    post.mockResolvedValue({ status: 'received' })
    render(<FulfilmentPage />)
    await screen.findByText('RMA-1')

    fireEvent.change(screen.getByLabelText('Items received for return 4'), { target: { value: '1' } })
    fireEvent.click(screen.getByRole('button', { name: 'Mark received' }))

    await waitFor(() => expect(post).toHaveBeenCalledWith('/returns/4/receive?quantity_received=1', {}))
  })
})
