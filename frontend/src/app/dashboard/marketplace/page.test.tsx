import { fireEvent, render, screen } from '@testing-library/react'
import MarketplacePage from '@/app/dashboard/marketplace/page'
import { mockFetch, reply } from '@/test-utils'

const products = [
  { id: 1, name: 'Field notebook', price: 12.5, category: 'stationery', stock_quantity: 4, average_rating: 4.5, review_count: 2 },
  { id: 2, name: 'Desk lamp', price: 30, category: 'office', stock_quantity: 0, average_rating: 0, review_count: 0 },
]

describe('/dashboard/marketplace page', () => {
  it('lists the products with price, rating and stock', async () => {
    mockFetch({ 'GET /products': products })
    render(<MarketplacePage />)

    expect(await screen.findByText('Field notebook')).toBeInTheDocument()
    expect(screen.getByText('$12.50')).toBeInTheDocument()
    expect(screen.getByText('4.5 ★ (2 reviews) · 4 in stock')).toBeInTheDocument()
    expect(screen.getByText('0.0 ★ (0 reviews) · Out of stock')).toBeInTheDocument()
  })

  it('filters by category', async () => {
    const fetchMock = mockFetch({ 'GET /products': products })
    render(<MarketplacePage />)
    await screen.findByText('Field notebook')

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'office' } })

    expect(await screen.findByText('Desk lamp')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/products?category=office'))).toBe(true)
  })

  it('searches the catalogue by the words entered', async () => {
    const fetchMock = mockFetch({ 'GET /products': products, 'GET /products/search': [products[0]] })
    render(<MarketplacePage />)
    await screen.findByText('Field notebook')

    fireEvent.change(screen.getByPlaceholderText('Search products'), { target: { value: ' note book ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    expect(await screen.findByText('Field notebook')).toBeInTheDocument()
    expect(fetchMock.mock.calls.some(([url]) => String(url).includes('/products/search?q=note%20book'))).toBe(true)
  })

  it('says when no products match', async () => {
    mockFetch({ 'GET /products': [] })
    render(<MarketplacePage />)

    expect(await screen.findByText('No products match.')).toBeInTheDocument()
  })

  it('shows the server reason when products cannot be loaded', async () => {
    mockFetch({ 'GET /products': reply({ detail: 'Catalogue is offline' }, 503) })
    render(<MarketplacePage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Catalogue is offline')
  })
})
