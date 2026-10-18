import { render, screen, within } from '@testing-library/react'
import EcommerceHubPage from '@/app/dashboard/ecommerce/page'

describe('/dashboard/ecommerce hub page', () => {
  it('links shopping pages to customers', () => {
    render(<EcommerceHubPage />)
    const shopping = screen.getByRole('region', { name: 'Shopping' })
    expect(within(shopping).getByRole('link', { name: /Wishlists/ })).toHaveAttribute('href', '/dashboard/ecommerce/wishlists')
    expect(within(shopping).getByRole('link', { name: /Addresses/ })).toHaveAttribute('href', '/dashboard/ecommerce/addresses')
    expect(within(shopping).getByRole('link', { name: /Orders/ })).toHaveAttribute('href', '/dashboard/ecommerce/orders')
  })

  it('keeps fulfilment and discount codes in the administration section', () => {
    render(<EcommerceHubPage />)
    const administration = screen.getByRole('region', { name: 'Administration' })
    expect(within(administration).getByRole('link', { name: /Fulfilment/ })).toHaveAttribute('href', '/dashboard/ecommerce/fulfilment')
    expect(within(administration).getByRole('link', { name: /Discount codes/ })).toHaveAttribute('href', '/dashboard/ecommerce/coupons')
  })
})
