import { render, screen } from '@testing-library/react'
import axios from 'axios'
import OrdersPage from '@/app/dashboard/ecommerce/orders/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

describe('/dashboard/ecommerce/orders page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('lists each order with its number, total and both statuses', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: [
        {
          id: 5,
          order_number: 'ORD-1005',
          total: 88.5,
          order_status: 'confirmed',
          shipping_status: 'shipped',
          created_at: '2026-10-01T10:00:00Z',
        },
        {
          id: 6,
          order_number: 'ORD-1006',
          total: 12,
          order_status: 'cancelled',
          shipping_status: 'pending',
          created_at: '2026-10-02T10:00:00Z',
        },
      ],
    })
    render(<OrdersPage />)

    expect(await screen.findByText('ORD-1005')).toBeInTheDocument()
    expect(screen.getByText('$88.5')).toBeInTheDocument()
    expect(screen.getByText('shipped')).toHaveClass('bg-purple-100')
    expect(screen.getByText('cancelled')).toHaveClass('bg-red-100')
    expect(screen.getAllByRole('link', { name: 'View' })[0]).toHaveAttribute('href', '/dashboard/ecommerce/orders/5')
  })

  it('uses a neutral badge for a status it does not recognise', async () => {
    mockedAxios.get.mockResolvedValueOnce({
      data: [
        { id: 7, order_number: 'ORD-7', total: 1, order_status: 'on_hold', shipping_status: 'pending', created_at: '2026-10-01' },
      ],
    })
    render(<OrdersPage />)

    expect(await screen.findByText('on_hold')).toHaveClass('bg-gray-100')
  })

  it('shows the empty state with a link to start shopping', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: [] })
    render(<OrdersPage />)

    expect(await screen.findByText('No orders yet')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Start Shopping' })).toHaveAttribute('href', '/dashboard/ecommerce/products')
  })

  it('logs the failure and shows the empty state when orders cannot be loaded', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('down'))
    render(<OrdersPage />)

    expect(await screen.findByText('No orders yet')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Error fetching orders:', expect.any(Error))
  })
})
