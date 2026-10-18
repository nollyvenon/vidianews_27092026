import { render, screen } from '@testing-library/react'
import { useParams } from 'next/navigation'
import axios from 'axios'
import OrderConfirmationPage from '@/app/dashboard/ecommerce/order-confirmation/[id]/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

describe('/dashboard/ecommerce/order-confirmation/[id] page', () => {
  beforeEach(() => {
    ;(useParams as jest.Mock).mockReturnValue({ id: '12' })
    mockedAxios.get.mockReturnValue(new Promise(() => undefined))
  })

  it('confirms the payment and offers the order and shopping links', () => {
    render(<OrderConfirmationPage />)

    expect(screen.getByRole('heading', { name: 'Thank you — your payment was received' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'View order' })).toHaveAttribute('href', '/dashboard/ecommerce/orders/12')
    expect(screen.getByRole('link', { name: 'Continue shopping' })).toHaveAttribute('href', '/dashboard/ecommerce/products')
  })

  it('shows the order summary for the paid order', () => {
    render(<OrderConfirmationPage />)

    expect(screen.getByText('Loading order…')).toBeInTheDocument()
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/orders/12')
  })
})
