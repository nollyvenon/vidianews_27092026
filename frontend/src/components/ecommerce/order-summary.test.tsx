import { render, screen } from '@testing-library/react'
import axios from 'axios'
import { OrderSummary, Order } from '@/components/ecommerce/order-summary'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const order: Order = {
  id: 5,
  order_number: 'ORD-0005',
  email: 'buyer@example.com',
  subtotal: '40.00',
  tax: '3.20',
  shipping: 5,
  discount: '4.00',
  total: '44.20',
  order_status: 'shipped',
  shipping_status: 'in_transit',
  shipping_method: 'standard',
  created_at: '2026-10-01T10:00:00Z',
  items: [
    { product_name: 'Field Notebook', product_sku: 'NB-1', quantity: 2, unit_price: '15.00', line_total: '30.00' },
    { product_name: 'Pen', product_sku: 'PN-9', quantity: 1, unit_price: 10, line_total: 10 },
  ],
}

describe('OrderSummary', () => {
  it('shows a loading state until the order arrives', () => {
    mockedAxios.get.mockReturnValue(new Promise(() => undefined))
    render(<OrderSummary orderId="5" />)

    expect(screen.getByText('Loading order…')).toBeInTheDocument()
  })

  it('loads the order by id and renders its status, items and totals', async () => {
    mockedAxios.get.mockResolvedValue({ data: order })
    render(<OrderSummary orderId="5" />)

    expect(await screen.findByRole('heading', { name: 'Order ORD-0005' })).toBeInTheDocument()
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/orders/5')
    expect(screen.getByText(/buyer@example.com/)).toBeInTheDocument()
    expect(screen.getByText('shipped')).toHaveClass('bg-purple-100')
    expect(screen.getByText('Shipping: in_transit')).toBeInTheDocument()
    expect(screen.getByText('Field Notebook')).toBeInTheDocument()
    expect(screen.getByText('SKU NB-1')).toBeInTheDocument()
    expect(screen.getByText('$30.00')).toBeInTheDocument()
    expect(screen.getByText('Shipping (standard)')).toBeInTheDocument()
    expect(screen.getByText('-$4.00')).toBeInTheDocument()
    expect(screen.getByText('$44.20')).toBeInTheDocument()
  })

  it('omits the discount row and shipping method when neither applies', async () => {
    mockedAxios.get.mockResolvedValue({
      data: { ...order, discount: 0, shipping_method: null, order_status: 'on_hold', items: [] },
    })
    render(<OrderSummary orderId="5" />)

    expect(await screen.findByText('on_hold')).toHaveClass('bg-gray-100')
    expect(screen.queryByText('Discount')).not.toBeInTheDocument()
    expect(screen.getByText('Shipping')).toBeInTheDocument()
  })

  it('styles every known order status', async () => {
    mockedAxios.get.mockResolvedValue({ data: { ...order, order_status: 'cancelled' } })
    render(<OrderSummary orderId="5" />)

    expect(await screen.findByText('cancelled')).toHaveClass('bg-red-100')
  })

  it('shows the server reason when the order cannot be loaded', async () => {
    mockedAxios.get.mockRejectedValue({ response: { data: { detail: 'Order not found' } } })
    render(<OrderSummary orderId="99" />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Order not found')
  })

  it('shows a generic message when the request fails without a server reason', async () => {
    mockedAxios.get.mockRejectedValue(new Error('Network Error'))
    render(<OrderSummary orderId="5" />)

    expect(await screen.findByRole('alert')).toHaveTextContent('This order could not be loaded.')
  })

  it('reports a missing order when the response has no body', async () => {
    mockedAxios.get.mockResolvedValue({ data: null })
    render(<OrderSummary orderId="5" />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Order not found.')
  })

  it('ignores a response that arrives after the component has unmounted', async () => {
    let resolve: (value: unknown) => void = () => undefined
    mockedAxios.get.mockReturnValue(new Promise((r) => (resolve = r)))
    const { unmount } = render(<OrderSummary orderId="5" />)
    unmount()

    resolve({ data: order })
    await Promise.resolve()

    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })
})
