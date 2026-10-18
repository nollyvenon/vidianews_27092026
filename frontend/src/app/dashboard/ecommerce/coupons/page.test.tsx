import { fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import CouponsPage from '@/app/dashboard/ecommerce/coupons/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn(), patch: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock
const patch = ApiClient.patch as jest.Mock

const spring = {
  id: 1, code: 'SPRING10', discount_type: 'percent', discount_value: 10, min_subtotal: 0,
  max_redemptions: 50, redemption_count: 3, valid_from: null, valid_until: null, is_active: true,
}

describe('/dashboard/ecommerce/coupons page', () => {
  beforeEach(() => jest.clearAllMocks())

  it('lists codes with their use and status', async () => {
    get.mockResolvedValue([spring])
    render(<CouponsPage />)
    const row = (await screen.findByText('SPRING10')).closest('tr') as HTMLElement
    expect(within(row).getByText('10%')).toBeInTheDocument()
    expect(within(row).getByText('3 / 50')).toBeInTheDocument()
    expect(within(row).getByText('Active')).toBeInTheDocument()
  })

  it('shows an empty state', async () => {
    get.mockResolvedValue([])
    render(<CouponsPage />)
    expect(await screen.findByText('No discount codes yet.')).toBeInTheDocument()
  })

  it('reports a load failure with the server message', async () => {
    get.mockRejectedValue(new ApiError('Administrator access required'))
    render(<CouponsPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Administrator access required')
  })

  it('creates a percentage code with a usage limit', async () => {
    get.mockResolvedValue([])
    post.mockResolvedValue({ ...spring, code: 'WELCOME5', discount_value: 5 })
    render(<CouponsPage />)
    await screen.findByText('No discount codes yet.')

    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'welcome5' } })
    fireEvent.change(screen.getByLabelText('Discount value'), { target: { value: '5' } })
    fireEvent.change(screen.getByLabelText('Maximum uses (blank for unlimited)'), { target: { value: '100' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create code' }))

    await waitFor(() =>
      expect(post).toHaveBeenCalledWith('/coupons', {
        code: 'welcome5', discount_type: 'percent', discount_value: 5, min_subtotal: 0,
        max_redemptions: 100, valid_until: null,
      }),
    )
    expect(await screen.findByText('Coupon WELCOME5 created.')).toBeInTheDocument()
  })

  it('refuses a discount that is not above zero', async () => {
    get.mockResolvedValue([])
    render(<CouponsPage />)
    await screen.findByText('No discount codes yet.')

    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'FREE' } })
    fireEvent.change(screen.getByLabelText('Discount value'), { target: { value: '0' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create code' }))

    expect(await screen.findByText('The discount must be greater than zero.')).toBeInTheDocument()
    expect(post).not.toHaveBeenCalled()
  })

  it('shows the server message when a code is rejected', async () => {
    get.mockResolvedValue([])
    post.mockRejectedValue(new ApiError('A coupon with this code already exists'))
    render(<CouponsPage />)
    await screen.findByText('No discount codes yet.')

    fireEvent.change(screen.getByLabelText('Code'), { target: { value: 'SPRING10' } })
    fireEvent.change(screen.getByLabelText('Discount value'), { target: { value: '10' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create code' }))

    expect(await screen.findByText('A coupon with this code already exists')).toBeInTheDocument()
  })

  it('disables an active code', async () => {
    get.mockResolvedValue([spring])
    patch.mockResolvedValue({ ...spring, is_active: false })
    render(<CouponsPage />)
    await screen.findByText('SPRING10')

    fireEvent.click(screen.getByRole('button', { name: 'Disable' }))

    await waitFor(() => expect(patch).toHaveBeenCalledWith('/coupons/1', { is_active: false }))
    expect(await screen.findByText('SPRING10 disabled.')).toBeInTheDocument()
  })
})
