import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import { useRouter } from 'next/navigation'
import TenantsPage from '@/app/dashboard/tenants/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const tenants = [
  { id: 1, name: 'Acme News', slug: 'acme', description: 'Daily news', plan: 'pro', status: 'active', max_users: 25, created_at: '2026-01-01' },
  { id: 2, name: 'Solo Studio', slug: 'solo', description: '', plan: 'free', status: 'active', max_users: 3, created_at: '2026-01-02' },
]

function failure(detail: string) {
  return { response: { data: { detail } } }
}

describe('/dashboard/tenants page', () => {
  beforeEach(() => {
    mockedAxios.get.mockResolvedValue({ data: { data: tenants } })
  })

  it('shows a loading state, then each tenant with its plan and seat count', async () => {
    render(<TenantsPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Acme News' })).toBeInTheDocument()
    expect(screen.getByText('Daily news')).toBeInTheDocument()
    expect(screen.getByText('pro')).toHaveClass('bg-blue-100')
    expect(screen.getByText('free')).toHaveClass('bg-gray-100')
    expect(screen.getByText('25 users')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Solo Studio/ })).toHaveAttribute('href', '/dashboard/tenants/2')
  })

  it('shows the empty state when the user has no tenants', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { data: [] } })
    render(<TenantsPage />)

    expect(await screen.findByText(/No tenants yet/)).toBeInTheDocument()
  })

  it('shows the server error when tenants cannot be loaded', async () => {
    mockedAxios.get.mockRejectedValueOnce(failure('Forbidden'))
    render(<TenantsPage />)

    expect(await screen.findByText('Forbidden')).toBeInTheDocument()
  })

  it('uses a generic message when loading fails without a server detail', async () => {
    mockedAxios.get.mockRejectedValueOnce({})
    render(<TenantsPage />)

    expect(await screen.findByText('Failed to load tenants')).toBeInTheDocument()
  })

  it('opens the create form and closes it again with cancel', async () => {
    render(<TenantsPage />)
    await screen.findByRole('heading', { name: 'Acme News' })

    fireEvent.click(screen.getByRole('button', { name: '+ Create Tenant' }))
    expect(screen.getByRole('heading', { name: 'Create New Tenant' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))
    expect(screen.queryByRole('heading', { name: 'Create New Tenant' })).not.toBeInTheDocument()
  })

  it('creates a tenant, lists it, and opens its page', async () => {
    mockedAxios.post.mockResolvedValueOnce({
      data: { id: 3, name: 'Night Desk', slug: 'night', description: 'Late shift', plan: 'enterprise', status: 'active', max_users: 100, created_at: '2026-02-01' },
    })
    render(<TenantsPage />)
    await screen.findByRole('heading', { name: 'Acme News' })

    fireEvent.click(screen.getByRole('button', { name: '+ Create Tenant' }))
    fireEvent.change(screen.getByPlaceholderText('Tenant Name'), { target: { value: 'Night Desk' } })
    fireEvent.change(screen.getByPlaceholderText('Slug (url-friendly)'), { target: { value: 'night' } })
    fireEvent.change(screen.getByPlaceholderText('Description'), { target: { value: 'Late shift' } })
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'enterprise' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    expect(await screen.findByRole('heading', { name: 'Night Desk' })).toBeInTheDocument()
    expect(mockedAxios.post).toHaveBeenCalledWith('/api/v1/tenants', {
      name: 'Night Desk',
      slug: 'night',
      description: 'Late shift',
      plan: 'enterprise',
    })
    expect(useRouter().push).toHaveBeenCalledWith('/dashboard/tenants/3')
  })

  it('keeps the form open and shows the error when creation is rejected', async () => {
    mockedAxios.post.mockRejectedValueOnce(failure('Slug already in use'))
    render(<TenantsPage />)
    await screen.findByRole('heading', { name: 'Acme News' })

    fireEvent.click(screen.getByRole('button', { name: '+ Create Tenant' }))
    fireEvent.change(screen.getByPlaceholderText('Tenant Name'), { target: { value: 'Dup' } })
    fireEvent.change(screen.getByPlaceholderText('Slug (url-friendly)'), { target: { value: 'acme' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    expect(await screen.findByText('Slug already in use')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Tenant Name')).toHaveValue('Dup')
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('uses a generic message when creation fails without a server detail', async () => {
    mockedAxios.post.mockRejectedValueOnce({})
    render(<TenantsPage />)
    await screen.findByRole('heading', { name: 'Acme News' })

    fireEvent.click(screen.getByRole('button', { name: '+ Create Tenant' }))
    fireEvent.change(screen.getByPlaceholderText('Tenant Name'), { target: { value: 'X' } })
    fireEvent.change(screen.getByPlaceholderText('Slug (url-friendly)'), { target: { value: 'x' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create' }))

    await waitFor(() => expect(screen.getByText('Failed to create tenant')).toBeInTheDocument())
  })
})
