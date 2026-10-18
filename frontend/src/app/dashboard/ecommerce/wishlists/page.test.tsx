import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import WishlistsPage from '@/app/dashboard/ecommerce/wishlists/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn(), delete: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock
const del = ApiClient.delete as jest.Mock

const gifts = { id: 3, name: 'Gifts', description: 'For friends', is_public: true, share_token: 'tok-abc' }
const item = { id: 11, wishlist_id: 3, product_id: 42, priority: 0, notes: null, added_at: null }

function routeGet(wishlists: unknown[] = [gifts], items: unknown[] = [item]) {
  get.mockImplementation((path: string) => {
    if (path === '/wishlists') return Promise.resolve(wishlists)
    if (path === '/wishlists/3/items') return Promise.resolve(items)
    if (path === '/products/42') return Promise.resolve({ id: 42, name: 'Desk Lamp' })
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('/dashboard/ecommerce/wishlists page', () => {
  beforeEach(() => jest.clearAllMocks())

  it('shows the first wishlist, its share token and its products', async () => {
    routeGet()
    render(<WishlistsPage />)

    expect(await screen.findByRole('heading', { name: 'Gifts' })).toBeInTheDocument()
    expect(screen.getByText('tok-abc')).toBeInTheDocument()
    expect(await screen.findByText('Desk Lamp')).toBeInTheDocument()
  })

  it('falls back to the product number when the product cannot be loaded', async () => {
    get.mockImplementation((path: string) => {
      if (path === '/wishlists') return Promise.resolve([gifts])
      if (path === '/wishlists/3/items') return Promise.resolve([item])
      return Promise.reject(new Error('gone'))
    })
    render(<WishlistsPage />)
    expect(await screen.findByText('Product #42')).toBeInTheDocument()
  })

  it('shows a message when there are no wishlists', async () => {
    routeGet([], [])
    render(<WishlistsPage />)
    expect(await screen.findByText('You have no wishlists yet.')).toBeInTheDocument()
  })

  it('reports a load failure with the server message', async () => {
    get.mockRejectedValue(new ApiError('Sign in again'))
    render(<WishlistsPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Sign in again')
  })

  it('creates a wishlist with its visibility', async () => {
    routeGet([])
    post.mockResolvedValue({ id: 4, name: 'Later', description: null, is_public: false, share_token: 't2' })
    render(<WishlistsPage />)
    await screen.findByText('You have no wishlists yet.')

    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Later' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create wishlist' }))

    await waitFor(() =>
      expect(post).toHaveBeenCalledWith('/wishlists', { name: 'Later', description: null, is_public: false }),
    )
    expect(await screen.findByText('Wishlist "Later" created.')).toBeInTheDocument()
  })

  it('adds a product by number', async () => {
    routeGet()
    post.mockResolvedValue({})
    render(<WishlistsPage />)
    await screen.findByText('Desk Lamp')

    fireEvent.change(screen.getByLabelText('Product number'), { target: { value: '99' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add product' }))

    await waitFor(() => expect(post).toHaveBeenCalledWith('/wishlists/3/items/99', {}))
  })

  it('refuses a product number that is not a positive whole number', async () => {
    routeGet()
    render(<WishlistsPage />)
    await screen.findByText('Desk Lamp')

    fireEvent.change(screen.getByLabelText('Product number'), { target: { value: 'abc' } })
    fireEvent.click(screen.getByRole('button', { name: 'Add product' }))

    expect(await screen.findByText('Enter a valid product number.')).toBeInTheDocument()
    expect(post).not.toHaveBeenCalled()
  })

  it('removes an item', async () => {
    routeGet()
    del.mockResolvedValue({})
    render(<WishlistsPage />)
    await screen.findByText('Desk Lamp')

    fireEvent.click(screen.getByRole('button', { name: 'Remove Desk Lamp' }))

    await waitFor(() => expect(del).toHaveBeenCalledWith('/wishlist-items/11'))
    await waitFor(() => expect(screen.queryByText('Desk Lamp')).not.toBeInTheDocument())
  })
})
