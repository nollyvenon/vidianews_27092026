import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import ProductsPage from '@/app/dashboard/ecommerce/products/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const products = [
  {
    id: 1,
    sku: 'CAM-01',
    name: 'Pocket Camera',
    price: 199,
    category: 'electronics',
    status: 'active',
    stock_quantity: 4,
    average_rating: 4.6,
    review_count: 12,
  },
]

describe('/dashboard/ecommerce/products page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('lists products with SKU, price, rating and stock', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: products })
    render(<ProductsPage />)

    expect(await screen.findByText('Pocket Camera')).toBeInTheDocument()
    expect(screen.getByText('CAM-01')).toBeInTheDocument()
    expect(screen.getByText('$199')).toBeInTheDocument()
    expect(screen.getByText(/⭐ 4.6 \(12\)/)).toBeInTheDocument()
    expect(screen.getByText('Stock: 4')).toBeInTheDocument()
  })

  it('reloads the products for the selected category', async () => {
    mockedAxios.get.mockResolvedValue({ data: products })
    render(<ProductsPage />)
    await screen.findByText('Pocket Camera')

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'books' } })

    await waitFor(() =>
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/products', { params: { category: 'books' } })
    )
  })

  it('searches the catalogue by the entered query', async () => {
    mockedAxios.get.mockResolvedValue({ data: products })
    render(<ProductsPage />)
    await screen.findByText('Pocket Camera')

    fireEvent.change(screen.getByPlaceholderText('Search products...'), { target: { value: 'camera' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() =>
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/products/search', { params: { q: 'camera' } })
    )
  })

  it('reloads the full catalogue when the search is blank', async () => {
    mockedAxios.get.mockResolvedValue({ data: products })
    render(<ProductsPage />)
    await screen.findByText('Pocket Camera')
    const callsBefore = mockedAxios.get.mock.calls.length

    fireEvent.change(screen.getByPlaceholderText('Search products...'), { target: { value: '   ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() => expect(mockedAxios.get.mock.calls.length).toBeGreaterThan(callsBefore))
    expect(mockedAxios.get).not.toHaveBeenCalledWith('/api/v1/products/search', expect.anything())
  })

  it('adds a product to the cart and confirms it', async () => {
    mockedAxios.get.mockResolvedValue({ data: products })
    mockedAxios.post.mockResolvedValue({ data: {} })
    render(<ProductsPage />)
    await screen.findByText('Pocket Camera')

    fireEvent.click(screen.getByRole('button', { name: 'Add to Cart' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Pocket Camera added to your cart.')
    expect(mockedAxios.post).toHaveBeenCalledWith('/api/v1/cart/items', { product_id: 1, quantity: 1 })
  })

  it('reports when a product could not be added to the cart', async () => {
    mockedAxios.get.mockResolvedValue({ data: products })
    mockedAxios.post.mockRejectedValue(new Error('Out of stock'))
    render(<ProductsPage />)
    await screen.findByText('Pocket Camera')

    fireEvent.click(screen.getByRole('button', { name: 'Add to Cart' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Could not add Pocket Camera to your cart.')
    expect(consoleError).toHaveBeenCalledWith('Error adding to cart:', expect.any(Error))
  })

  it('logs a failed product load and leaves the grid empty', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('down'))
    render(<ProductsPage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Error fetching products:', expect.any(Error)))
    expect(screen.queryByText('Pocket Camera')).not.toBeInTheDocument()
  })

  it('logs a failed search', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: products })
    mockedAxios.get.mockRejectedValueOnce(new Error('search down'))
    render(<ProductsPage />)
    await screen.findByText('Pocket Camera')

    fireEvent.change(screen.getByPlaceholderText('Search products...'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Error searching products:', expect.any(Error)))
  })
})
