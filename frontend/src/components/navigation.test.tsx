import { fireEvent, screen } from '@testing-library/react'
import { usePathname } from 'next/navigation'
import { Navigation } from '@/components/navigation'
import { buildAuth, renderWithAuth, testUser } from '@/test-utils'

describe('Navigation', () => {
  it('shows the brand, every section link, and the signed-in user name', () => {
    renderWithAuth(<Navigation />)

    expect(screen.getByRole('link', { name: 'VidiNews' })).toHaveAttribute('href', '/dashboard')
    expect(screen.getByRole('link', { name: /Content/ })).toHaveAttribute('href', '/dashboard/content')
    expect(screen.getByRole('link', { name: /Analytics/ })).toHaveAttribute('href', '/dashboard/analytics')
    expect(screen.getByRole('link', { name: /AI Features/ })).toHaveAttribute('href', '/dashboard/ai')
    expect(screen.getByRole('link', { name: /Organizations/ })).toHaveAttribute('href', '/dashboard/organizations')
    expect(screen.getByRole('link', { name: /Settings/ })).toHaveAttribute('href', '/dashboard/settings')
    expect(screen.getByText(testUser.name)).toBeInTheDocument()
  })

  it('highlights the link for the current page only', () => {
    (usePathname as jest.Mock).mockReturnValue('/dashboard/content')
    renderWithAuth(<Navigation />)

    expect(screen.getByRole('link', { name: /Content/ })).toHaveClass('bg-blue-100')
    expect(screen.getByRole('link', { name: /Analytics/ })).toHaveClass('text-gray-700')
  })

  it('omits the user name while the user is unknown', () => {
    renderWithAuth(<Navigation />, buildAuth({ user: null }))

    expect(screen.queryByText(testUser.name)).not.toBeInTheDocument()
  })

  it('logs out when the logout button is pressed', () => {
    const auth = buildAuth({ logout: jest.fn() })
    renderWithAuth(<Navigation />, auth)

    fireEvent.click(screen.getByRole('button', { name: 'Logout' }))

    expect(auth.logout).toHaveBeenCalledTimes(1)
  })
})
