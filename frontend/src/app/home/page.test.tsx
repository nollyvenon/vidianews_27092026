import { render, screen } from '@testing-library/react'
import Home from '@/app/home/page'

describe('/home page', () => {
  it('renders the platform introduction', () => {
    render(<Home />)

    expect(screen.getByRole('heading', { name: 'AetherCMS AI' })).toBeInTheDocument()
    expect(screen.getByText('Enterprise AI Publishing Platform')).toBeInTheDocument()
  })

  it('links visitors to sign in and to create an account', () => {
    render(<Home />)

    expect(screen.getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login')
    expect(screen.getByRole('link', { name: 'Create account' })).toHaveAttribute('href', '/auth/signup')
  })

  it('does not show internal build status', () => {
    render(<Home />)

    expect(screen.queryByText(/Foundation Complete/)).not.toBeInTheDocument()
  })
})
