import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import CartPage from '@/app/dashboard/ecommerce/cart/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const cart = {
  id: 1,
  subtotal: 40,
  tax: 3.2,
  shipping: 5,
  discount: 0,
  total: 48.2,
  item_count: 2,
  items: [
    { id: 11, product_id: 101, quantity: 2, unit_price: 15, line_total: 30 },
    { id: 12, product_id: 102, quantity: 1, unit_price: 10, line_total: 10 },
  ],
}

describe('/dashboard/ecommerce/cart page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state, then the cart items and totals', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: cart })
    render(<CartPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByText('Product 101')).toBeInTheDocument()
    expect(screen.getByText('Product 102')).toBeInTheDocument()
    expect(screen.getByText('$48.2')).toBeInTheDocument()
    expect(screen.getByText('$40')).toBeInTheDocument()
    expect(screen.queryByText(/Discount/)).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Proceed to Checkout' })).toHaveAttribute(
      'href',
      '/dashboard/ecommerce/checkout'
    )
  })

  it('shows the discount line only when a discount applies', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { ...cart, discount: 5 } })
    render(<CartPage />)

    expect(await screen.findByText('Discount')).toBeInTheDocument()
    expect(screen.getByText('-$5')).toHaveClass('text-green-600')
  })

  it('shows the empty cart state when there are no items', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { ...cart, item_count: 0, items: [] } })
    render(<CartPage />)

    expect(await screen.findByText('Your cart is empty')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Continue Shopping' })).toHaveAttribute(
      'href',
      '/dashboard/ecommerce/products'
    )
  })

  it('updates an item quantity and reloads the cart', async () => {
    mockedAxios.get.mockResolvedValue({ data: cart })
    mockedAxios.put.mockResolvedValue({ data: {} })
    render(<CartPage />)
    await screen.findByText('Product 101')

    fireEvent.change(screen.getAllByRole('spinbutton')[0], { target: { value: '3' } })

    await waitFor(() => expect(mockedAxios.put).toHaveBeenCalledWith('/api/v1/cart/items/11', { quantity: 3 }))
    await waitFor(() => expect(mockedAxios.get).toHaveBeenCalledTimes(2))
  })

  it('removes an item from the cart', async () => {
    mockedAxios.get.mockResolvedValue({ data: cart })
    mockedAxios.delete.mockResolvedValue({ data: {} })
    render(<CartPage />)
    await screen.findByText('Product 102')

    fireEvent.click(screen.getAllByRole('button', { name: 'Remove' })[1])

    await waitFor(() => expect(mockedAxios.delete).toHaveBeenCalledWith('/api/v1/cart/items/12'))
  })

  it('clears the whole cart and shows the empty state', async () => {
    mockedAxios.get.mockResolvedValue({ data: cart })
    mockedAxios.delete.mockResolvedValue({ data: {} })
    render(<CartPage />)
    await screen.findByText('Product 101')

    fireEvent.click(screen.getByRole('button', { name: 'Clear Cart' }))

    expect(await screen.findByText('Your cart is empty')).toBeInTheDocument()
    expect(mockedAxios.delete).toHaveBeenCalledWith('/api/v1/cart')
  })

  it('logs failures to load, update, remove and clear', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('offline'))
    render(<CartPage />)

    expect(await screen.findByText('Your cart is empty')).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Error fetching cart:', expect.any(Error))
  })

  it('logs failed quantity, removal and clear actions', async () => {
    mockedAxios.get.mockResolvedValue({ data: cart })
    const failure = new Error('rejected')
    mockedAxios.put.mockRejectedValue(failure)
    mockedAxios.delete.mockRejectedValue(failure)
    render(<CartPage />)
    await screen.findByText('Product 101')

    fireEvent.change(screen.getAllByRole('spinbutton')[0], { target: { value: '4' } })
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Error updating quantity:', failure))

    fireEvent.click(screen.getAllByRole('button', { name: 'Remove' })[0])
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Error removing item:', failure))

    fireEvent.click(screen.getByRole('button', { name: 'Clear Cart' }))
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Error clearing cart:', failure))
  })
})
