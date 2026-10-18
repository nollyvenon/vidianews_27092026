import { screen } from '@testing-library/react'
import DashboardPage from '@/app/dashboard/page'
import { buildAuth, renderWithAuth, testUser } from '@/test-utils'

describe('/dashboard page', () => {
  it('greets the signed-in user by name', () => {
    renderWithAuth(<DashboardPage />)

    expect(screen.getByRole('heading', { name: `Welcome, ${testUser.name}!` })).toBeInTheDocument()
  })

  it('shows the headline counters at zero for a new account', () => {
    renderWithAuth(<DashboardPage />)

    expect(screen.getByText('Videos')).toBeInTheDocument()
    expect(screen.getByText('Articles')).toBeInTheDocument()
    expect(screen.getByText('Chats')).toBeInTheDocument()
    expect(screen.getByText('$0')).toBeInTheDocument()
  })

  it('links to the main feature areas', () => {
    renderWithAuth(<DashboardPage />)

    expect(screen.getByRole('link', { name: /Manage Content/ })).toHaveAttribute('href', '/dashboard/content')
    expect(screen.getByRole('link', { name: /AI Features/ })).toHaveAttribute('href', '/dashboard/ai')
    expect(screen.getByRole('link', { name: /View Analytics/ })).toHaveAttribute('href', '/dashboard/analytics')
    expect(screen.getByText('No recent activity yet.')).toBeInTheDocument()
  })

  it('renders without a user while the profile is unavailable', () => {
    renderWithAuth(<DashboardPage />, buildAuth({ user: null }))

    expect(screen.getByRole('heading', { name: 'Welcome, !' })).toBeInTheDocument()
  })
})
