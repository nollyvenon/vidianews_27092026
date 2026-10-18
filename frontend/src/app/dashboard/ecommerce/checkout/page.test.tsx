import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import { useRouter } from 'next/navigation'
import { useElements, useStripe } from '@stripe/react-stripe-js'
import CheckoutPage from '@/app/dashboard/ecommerce/checkout/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

// Stripe.js itself talks to the network; the page only needs the hooks and the loader.
jest.mock('@stripe/stripe-js', () => ({ loadStripe: jest.fn(() => Promise.resolve(null)) }))
jest.mock('@stripe/react-stripe-js', () => ({
  Elements: ({ children }: { children: unknown }) => children,
  CardElement: () => null,
  useStripe: jest.fn(),
  useElements: jest.fn(),
}))

const ORIGINAL_KEY = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY

function fillForm() {
  fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'buyer@example.com' } })
  const fill = (placeholder: string, values: string[]) =>
    screen.getAllByPlaceholderText(placeholder).forEach((input, index) =>
      fireEvent.change(input, { target: { value: values[index] } })
    )
  fill('Street', ['1 Main St', '9 Dock Rd'])
  fill('City', ['Springfield', 'Shelbyville'])
  fill('State', ['IL', 'IL'])
  fill('ZIP Code', ['62701', '62702'])
  fill('Country', ['US', 'US'])
}

function submit() {
  fireEvent.submit(document.querySelector('form') as HTMLFormElement)
}

function stripeReady(createPaymentMethod = jest.fn().mockResolvedValue({ paymentMethod: { id: 'pm_123' } })) {
  ;(useStripe as jest.Mock).mockReturnValue({ createPaymentMethod })
  ;(useElements as jest.Mock).mockReturnValue({ getElement: () => ({}) })
  return createPaymentMethod
}

describe('/dashboard/ecommerce/checkout page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
    process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = 'pk_test_123'
  })

  afterEach(() => {
    consoleError.mockRestore()
    if (ORIGINAL_KEY === undefined) delete process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
    else process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = ORIGINAL_KEY
  })

  it('collects contact, billing, shipping and shipping-method details', () => {
    stripeReady()
    render(<CheckoutPage />)

    expect(screen.getByRole('heading', { name: 'Checkout' })).toBeInTheDocument()
    expect(screen.getAllByPlaceholderText('Street')).toHaveLength(2)
    expect(screen.getByLabelText(/Standard \(5-7 days\)/)).toBeChecked()
    fireEvent.click(screen.getByLabelText(/Express/))
    expect(screen.getByLabelText(/Express/)).toBeChecked()
  })

  it('tells the user that card payments are not configured and blocks purchase', () => {
    delete process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
    stripeReady()
    render(<CheckoutPage />)

    expect(screen.getByRole('alert')).toHaveTextContent('NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY')
    expect(screen.getByRole('button', { name: 'Complete Purchase' })).toBeDisabled()
  })

  it('creates the checkout, tokenises the card with Stripe, charges it and opens the order', async () => {
    const createPaymentMethod = stripeReady()
    mockedAxios.post
      .mockResolvedValueOnce({ data: { id: 42, total: 659.76 } })
      .mockResolvedValueOnce({ data: { payment_id: 5, status: 'completed', order_id: 9, order_number: 'ORD-9' } })
    render(<CheckoutPage />)
    fillForm()
    fireEvent.click(screen.getByLabelText(/Overnight/))

    submit()

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/ecommerce/order-confirmation/9'))
    expect(createPaymentMethod).toHaveBeenCalledWith(
      expect.objectContaining({
        type: 'card',
        billing_details: expect.objectContaining({ email: 'buyer@example.com' }),
      })
    )
    const [checkoutUrl, checkoutBody] = mockedAxios.post.mock.calls[0]
    expect(checkoutUrl).toBe('/api/v1/checkout')
    expect(checkoutBody).toMatchObject({
      email: 'buyer@example.com',
      shipping_method: 'overnight',
      billing_address: { street: '1 Main St', city: 'Springfield', state: 'IL', zip: '62701', country: 'US' },
      shipping_address: { street: '9 Dock Rd', city: 'Shelbyville', state: 'IL', zip: '62702', country: 'US' },
    })
    expect(mockedAxios.post.mock.calls[1]).toEqual([
      '/api/v1/checkout/42/payment',
      { payment_method: 'stripe', amount: 659.76, card_token: 'pm_123' },
    ])
  })

  it('shows the card error reported by Stripe and does not charge', async () => {
    stripeReady(jest.fn().mockResolvedValue({ error: { message: 'Your card was declined.' } }))
    mockedAxios.post.mockResolvedValueOnce({ data: { id: 42, total: 10 } })
    render(<CheckoutPage />)
    fillForm()

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Your card was declined.')
    expect(mockedAxios.post).toHaveBeenCalledTimes(1)
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('asks for card details when the card field is empty', async () => {
    ;(useStripe as jest.Mock).mockReturnValue({ createPaymentMethod: jest.fn() })
    ;(useElements as jest.Mock).mockReturnValue({ getElement: () => null })
    mockedAxios.post.mockResolvedValueOnce({ data: { id: 42, total: 10 } })
    render(<CheckoutPage />)
    fillForm()

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Enter your card details to continue.')
  })

  it('reports that payments are not ready while Stripe is still loading', async () => {
    ;(useStripe as jest.Mock).mockReturnValue(null)
    ;(useElements as jest.Mock).mockReturnValue(null)
    render(<CheckoutPage />)
    fillForm()

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Card payments are not ready yet.')
    expect(mockedAxios.post).not.toHaveBeenCalled()
  })

  it('shows the server reason when the payment is declined by the backend', async () => {
    stripeReady()
    mockedAxios.post
      .mockResolvedValueOnce({ data: { id: 42, total: 10 } })
      .mockRejectedValueOnce({ response: { data: { detail: 'Card declined by the bank' } } })
    render(<CheckoutPage />)
    fillForm()

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Card declined by the bank')
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('uses a generic message when checkout fails without a server reason', async () => {
    stripeReady()
    mockedAxios.post.mockRejectedValueOnce({})
    render(<CheckoutPage />)
    fillForm()

    submit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Checkout could not be completed.')
  })

  it('shows progress while the order is being processed', async () => {
    stripeReady()
    mockedAxios.post.mockReturnValue(new Promise(() => undefined))
    render(<CheckoutPage />)
    fillForm()

    submit()

    expect(await screen.findByRole('button', { name: 'Processing...' })).toBeDisabled()
  })
})
