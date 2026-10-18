import { render, screen } from '@testing-library/react'
import { useParams } from 'next/navigation'
import axios from 'axios'
import OrderDetailPage from '@/app/dashboard/ecommerce/orders/[id]/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

describe('/dashboard/ecommerce/orders/[id] page', () => {
  it('links back to the orders list and loads the order named in the route', async () => {
    ;(useParams as jest.Mock).mockReturnValue({ id: '5' })
    mockedAxios.get.mockResolvedValue({
      data: {
        id: 5,
        order_number: 'ORD-0005',
        email: 'buyer@example.com',
        subtotal: 10,
        tax: 0,
        shipping: 0,
        discount: 0,
        total: 10,
        order_status: 'pending',
        shipping_status: 'pending',
        shipping_method: null,
        created_at: '2026-10-01T10:00:00Z',
        items: [],
      },
    })
    render(<OrderDetailPage />)

    expect(screen.getByRole('link', { name: '← Back to orders' })).toHaveAttribute('href', '/dashboard/ecommerce/orders')
    expect(await screen.findByRole('heading', { name: 'Order ORD-0005' })).toBeInTheDocument()
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/orders/5')
  })
})
