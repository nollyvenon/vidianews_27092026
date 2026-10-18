import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { OrderShippingReturns } from '@/components/ecommerce/order-shipping-returns'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock

const shipment = {
  id: 5, order_id: 9, carrier: 'ups', tracking_number: '1Z-1', status: 'in_transit',
  shipped_at: null, delivered_at: null,
}
const event = {
  id: 1, shipment_id: 5, status: 'picked_up', description: 'Left the warehouse', location: 'Dallas',
  timestamp: '2026-10-10T10:00:00Z',
}
const refund = {
  id: 7, rma_number: 'RMA-ABCD1234', reason: 'defective', status: 'refunded',
  quantity_requested: 1, quantity_received: 1, refund_amount: 20, refund_method: 'stripe',
}

function routeGet(shipments: unknown[] = [shipment], returns: unknown[] = []) {
  get.mockImplementation((path: string) => {
    if (path === '/orders/9/shipments') return Promise.resolve(shipments)
    if (path === '/orders/9/returns') return Promise.resolve(returns)
    if (path === '/shipments/5/tracking') return Promise.resolve([event])
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('OrderShippingReturns', () => {
  beforeEach(() => jest.clearAllMocks())

  it('shows the shipment with its tracking history', async () => {
    routeGet()
    render(<OrderShippingReturns orderId="9" />)
    expect(await screen.findByText('UPS 1Z-1')).toBeInTheDocument()
    expect(screen.getByText('picked_up')).toBeInTheDocument()
    expect(screen.getByText(/Left the warehouse/)).toBeInTheDocument()
  })

  it('says when an order has not shipped', async () => {
    routeGet([], [])
    render(<OrderShippingReturns orderId="9" />)
    expect(await screen.findByText('This order has not shipped yet.')).toBeInTheDocument()
  })

  it('lists existing returns with their refund', async () => {
    routeGet([], [refund])
    render(<OrderShippingReturns orderId="9" />)
    expect(await screen.findByText('RMA-ABCD1234')).toBeInTheDocument()
    expect(screen.getByText(/refund 20 \(stripe\)/)).toBeInTheDocument()
  })

  it('submits a return request for the chosen reason and quantity', async () => {
    routeGet([], [])
    post.mockResolvedValue({ id: 8 })
    render(<OrderShippingReturns orderId="9" />)
    await screen.findByText('No return requests for this order.')

    fireEvent.change(screen.getByLabelText('Reason'), { target: { value: 'wrong_item' } })
    fireEvent.change(screen.getByLabelText('Items to return'), { target: { value: '2' } })
    fireEvent.click(screen.getByRole('button', { name: 'Request a return' }))

    await waitFor(() =>
      expect(post).toHaveBeenCalledWith('/orders/9/return', {
        reason: 'wrong_item', quantity_requested: 2, reason_details: null,
      }),
    )
    expect(await screen.findByText('Your return request has been submitted.')).toBeInTheDocument()
  })

  it('refuses a return quantity below one', async () => {
    routeGet([], [])
    render(<OrderShippingReturns orderId="9" />)
    await screen.findByText('No return requests for this order.')

    fireEvent.change(screen.getByLabelText('Items to return'), { target: { value: '0' } })
    fireEvent.click(screen.getByRole('button', { name: 'Request a return' }))

    expect(await screen.findByText('Enter how many items you are returning.')).toBeInTheDocument()
    expect(post).not.toHaveBeenCalled()
  })

  it('shows the server message when a return cannot be requested', async () => {
    routeGet([], [])
    post.mockRejectedValue(new ApiError('This order is not eligible for returns'))
    render(<OrderShippingReturns orderId="9" />)
    await screen.findByText('No return requests for this order.')

    fireEvent.click(screen.getByRole('button', { name: 'Request a return' }))

    expect(await screen.findByText('This order is not eligible for returns')).toBeInTheDocument()
  })
})
