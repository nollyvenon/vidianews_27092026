import { fireEvent, screen, waitFor } from '@testing-library/react'
import { useRouter } from 'next/navigation'
import DashboardLayout from '@/app/dashboard/layout'
import { buildAuth, renderWithAuth } from '@/test-utils'

describe('dashboard layout', () => {
  it('shows a loading state while the session is being restored', () => {
    renderWithAuth(
      <DashboardLayout>
        <p>secret page</p>
      </DashboardLayout>,
      buildAuth({ loading: true, token: null, user: null })
    )

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(screen.queryByText('secret page')).not.toBeInTheDocument()
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('sends signed-out visitors to /auth/login and renders nothing', async () => {
    const { container } = renderWithAuth(
      <DashboardLayout>
        <p>secret page</p>
      </DashboardLayout>,
      buildAuth({ token: null, user: null, loading: false })
    )

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/auth/login'))
    expect(container).toBeEmptyDOMElement()
  })

  it('renders the navigation bar and the page for signed-in users', () => {
    renderWithAuth(
      <DashboardLayout>
        <p>dashboard page</p>
      </DashboardLayout>
    )

    expect(screen.getByRole('navigation')).toBeInTheDocument()
    expect(screen.getByText('dashboard page')).toBeInTheDocument()
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('signs the user out from the navigation bar', () => {
    const auth = buildAuth({ logout: jest.fn() })
    renderWithAuth(
      <DashboardLayout>
        <p>dashboard page</p>
      </DashboardLayout>,
      auth
    )

    fireEvent.click(screen.getByRole('button', { name: 'Logout' }))

    expect(auth.logout).toHaveBeenCalledTimes(1)
  })
})
