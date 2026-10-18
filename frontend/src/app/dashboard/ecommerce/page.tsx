import Link from 'next/link'

const SHOPPING = [
  { href: '/dashboard/ecommerce/products', label: 'Products', description: 'Browse the catalogue' },
  { href: '/dashboard/ecommerce/cart', label: 'Cart', description: 'Review items before checkout' },
  { href: '/dashboard/ecommerce/orders', label: 'Orders', description: 'Track orders, shipments and returns' },
  { href: '/dashboard/ecommerce/wishlists', label: 'Wishlists', description: 'Save products for later' },
  { href: '/dashboard/ecommerce/addresses', label: 'Addresses', description: 'Manage shipping addresses' },
]

const ADMINISTRATION = [
  { href: '/dashboard/ecommerce/fulfilment', label: 'Fulfilment', description: 'Shipments, stock alerts and return decisions' },
  { href: '/dashboard/ecommerce/coupons', label: 'Discount codes', description: 'Create and enable or disable codes' },
]

export default function EcommerceHubPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">Ecommerce</h1>

      <section aria-label="Shopping" className="space-y-3">
        <h2 className="text-xl font-semibold text-gray-900">Shopping</h2>
        <ul className="grid gap-3 md:grid-cols-2">
          {SHOPPING.map((item) => (
            <li key={item.href}>
              <Link href={item.href} className="block rounded-lg bg-white p-4 shadow hover:bg-gray-50">
                <span className="font-medium text-gray-900">{item.label}</span>
                <span className="block text-sm text-gray-600">{item.description}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section aria-label="Administration" className="space-y-3">
        <h2 className="text-xl font-semibold text-gray-900">Administration</h2>
        <ul className="grid gap-3 md:grid-cols-2">
          {ADMINISTRATION.map((item) => (
            <li key={item.href}>
              <Link href={item.href} className="block rounded-lg bg-white p-4 shadow hover:bg-gray-50">
                <span className="font-medium text-gray-900">{item.label}</span>
                <span className="block text-sm text-gray-600">{item.description}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
