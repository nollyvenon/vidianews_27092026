import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import ShippingAddressesPage from '@/app/dashboard/ecommerce/addresses/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock

const home = {
  id: 1, first_name: 'Ada', last_name: 'Lovelace', street_address: '1 Main St', city: 'London',
  state: null, postal_code: 'W1', country: 'UK', phone: null, is_default: true,
}

function fillRequired() {
  fireEvent.change(screen.getByLabelText('First name'), { target: { value: 'Grace' } })
  fireEvent.change(screen.getByLabelText('Last name'), { target: { value: 'Hopper' } })
  fireEvent.change(screen.getByLabelText('Street address'), { target: { value: '2 Harbor Rd' } })
  fireEvent.change(screen.getByLabelText('City'), { target: { value: 'Arlington' } })
  fireEvent.change(screen.getByLabelText('Postal code'), { target: { value: '22201' } })
  fireEvent.change(screen.getByLabelText('Country'), { target: { value: 'US' } })
}

describe('/dashboard/ecommerce/addresses page', () => {
  beforeEach(() => jest.clearAllMocks())

  it('lists saved addresses and marks the default', async () => {
    get.mockResolvedValue([home])
    render(<ShippingAddressesPage />)
    expect(await screen.findByText('Default')).toBeInTheDocument()
    expect(screen.getByText(/1 Main St, London/)).toBeInTheDocument()
  })

  it('shows an empty state', async () => {
    get.mockResolvedValue([])
    render(<ShippingAddressesPage />)
    expect(await screen.findByText('You have no saved addresses.')).toBeInTheDocument()
  })

  it('reports load failures with the server message', async () => {
    get.mockRejectedValue(new ApiError('Session expired'))
    render(<ShippingAddressesPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Session expired')
  })

  it('saves a new address and reloads the list', async () => {
    get.mockResolvedValue([])
    post.mockResolvedValue({ id: 2 })
    render(<ShippingAddressesPage />)
    await screen.findByText('You have no saved addresses.')

    fillRequired()
    fireEvent.click(screen.getByRole('button', { name: 'Save address' }))

    await waitFor(() =>
      expect(post).toHaveBeenCalledWith('/shipping-addresses', expect.objectContaining({
        first_name: 'Grace', city: 'Arlington', state: null, phone: null, is_default: false,
      })),
    )
    expect(await screen.findByText('Address saved.')).toBeInTheDocument()
  })

  it('shows the server message when saving fails', async () => {
    get.mockResolvedValue([])
    post.mockRejectedValue(new ApiError('Postal code is invalid'))
    render(<ShippingAddressesPage />)
    await screen.findByText('You have no saved addresses.')

    fillRequired()
    fireEvent.click(screen.getByRole('button', { name: 'Save address' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Postal code is invalid')
  })
})
