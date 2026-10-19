import { fireEvent, render, screen, within } from '@testing-library/react'
import CouponsPage from '@/app/dashboard/ecommerce/coupons/page'
import { ApiClient } from '@/lib/api-client'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn(), post: jest.fn(), patch: jest.fn() },
}))

const get = ApiClient.get as jest.Mock
const post = ApiClient.post as jest.Mock
const patch = ApiClient.patch as jest.Mock

const fixedWithMinimum = {
  id: 2, code: 'SAVE5', discount_type: 'fixed', discount_value: 5, min_subtotal: 25,
  max_redemptions: null, redemption_count: 0, valid_from: null,
  valid_until: '2030-01-01T00:00:00Z', is_active: false,
}

describe('/dashboard/ecommerce/coupons page fallbacks', () => {
  beforeEach(() => jest.clearAllMocks())

  it('describes a fixed discount with a minimum, an end date and no use limit', async () => {
    get.mockResolvedValue([fixedWithMinimum])
    render(<CouponsPage />)

    const row = (await screen.findByText('SAVE5')).closest('tr') as HTMLElement
    expect(within(row).getByText(/5 off/)).toBeInTheDocument()
    expect(within(row).getByText(/\(min 25\)/)).toBeInTheDocument()
    expect(within(row).getByText('Disabled')).toBeInTheDocument()
    expect(within(row).getByRole('button', { name: 'Enable' })).toBeInTheDocument()
    expect(within(row).queryByText('No end date')).not.toBeInTheDocument()
  })

  it('enables a disabled code and confirms it', async () => {
    get.mockResolvedValue([fixedWithMinimum])
    patch.mockResolvedValue({ ...fixedWithMinimum, is_active: true })
    render(<CouponsPage />)

    const row = (await screen.findByText('SAVE5')).closest('tr') as HTMLElement
    fireEvent.click(within(row).getByRole('button', { name: 'Enable' }))

    expect(await screen.findByText('SAVE5 enabled.')).toBeInTheDocument()
  })

  it('creates a code without a minimum or end date by sending null and zero', async () => {
    get.mockResolvedValue([])
    post.mockResolvedValue({ ...fixedWithMinimum, id: 3, code: 'OPEN' })
    render(<CouponsPage />)

    fireEvent.change(await screen.findByLabelText('Code'), { target: { value: 'OPEN' } })
    fireEvent.change(screen.getByLabelText('Discount value'), { target: { value: '10' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create code' }))

    await screen.findByText('Coupon OPEN created.')
    const payload = post.mock.calls[0][1]
    expect(payload.min_subtotal).toBe(0)
    expect(payload.valid_until).toBeNull()
  })

  it('sends the end date as an ISO timestamp when one is entered', async () => {
    get.mockResolvedValue([])
    post.mockResolvedValue({ ...fixedWithMinimum, id: 4, code: 'DATED' })
    render(<CouponsPage />)

    fireEvent.change(await screen.findByLabelText('Code'), { target: { value: 'DATED' } })
    fireEvent.change(screen.getByLabelText('Discount value'), { target: { value: '10' } })
    fireEvent.change(screen.getByLabelText('Valid until (optional)'), { target: { value: '2031-06-15T09:30' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create code' }))

    await screen.findByText('Coupon DATED created.')
    expect(post.mock.calls[0][1].valid_until).toBe(new Date('2031-06-15T09:30').toISOString())
  })
})
