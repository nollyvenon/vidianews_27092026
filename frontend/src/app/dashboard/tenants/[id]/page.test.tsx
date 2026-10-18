import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import { useParams, useRouter } from 'next/navigation'
import TenantDetailPage from '@/app/dashboard/tenants/[id]/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const tenant = {
  id: 3,
  name: 'Night Desk',
  slug: 'night',
  description: 'Late shift',
  logo_url: '',
  website: '',
  plan: 'pro',
  status: 'active',
  max_users: 25,
  created_at: '2026-02-01',
}

function failure(detail: string) {
  return { response: { data: { detail } } }
}

describe('/dashboard/tenants/[id] page', () => {
  beforeEach(() => {
    (useParams as jest.Mock).mockReturnValue({ id: '3' })
    mockedAxios.get.mockResolvedValue({ data: tenant })
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('shows the tenant details and links to its members and settings', async () => {
    render(<TenantDetailPage />)

    expect(await screen.findByRole('heading', { name: 'Night Desk' })).toBeInTheDocument()
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/tenants/3')
    expect(screen.getByText('night')).toBeInTheDocument()
    expect(screen.getByText('Late shift')).toBeInTheDocument()
    expect(screen.getByText('25')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: 'Members' }))
    expect(screen.getByRole('link', { name: 'Manage members →' })).toHaveAttribute('href', '/dashboard/tenants/3/members')
    fireEvent.click(screen.getByRole('button', { name: 'Settings' }))
    expect(screen.getByRole('link', { name: 'Manage settings →' })).toHaveAttribute('href', '/dashboard/tenants/3/settings')
  })

  it('shows a dash for a missing description', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { ...tenant, description: '' } })
    render(<TenantDetailPage />)

    expect(await screen.findByText('-')).toBeInTheDocument()
  })

  it('edits the tenant and shows the saved values', async () => {
    mockedAxios.put.mockResolvedValueOnce({ data: { ...tenant, name: 'Night Desk Live' } })
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Edit' }))
    fireEvent.change(screen.getByPlaceholderText('Name'), { target: { value: 'Night Desk Live' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByRole('heading', { name: 'Night Desk Live' })).toBeInTheDocument()
    expect(mockedAxios.put).toHaveBeenCalledWith('/api/v1/tenants/3', expect.objectContaining({ name: 'Night Desk Live' }))
  })

  it('discards edits when cancelled', async () => {
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Edit' }))
    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))

    expect(screen.getByRole('button', { name: 'Edit' })).toBeInTheDocument()
    expect(mockedAxios.put).not.toHaveBeenCalled()
  })

  it('shows the server error when an update is rejected and stays in edit mode', async () => {
    mockedAxios.put.mockRejectedValueOnce(failure('Slug taken'))
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Edit' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByText('Slug taken')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument()
  })

  it('uses a generic message when an update fails without a server detail', async () => {
    mockedAxios.put.mockRejectedValueOnce({})
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Edit' }))
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    expect(await screen.findByText('Failed to update tenant')).toBeInTheDocument()
  })

  it('deletes the tenant after confirmation and returns to the list', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true)
    mockedAxios.delete.mockResolvedValueOnce({ data: {} })
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    await waitFor(() => expect(useRouter().push).toHaveBeenCalledWith('/dashboard/tenants'))
    expect(mockedAxios.delete).toHaveBeenCalledWith('/api/v1/tenants/3')
  })

  it('does nothing when the deletion is not confirmed', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(false)
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    expect(mockedAxios.delete).not.toHaveBeenCalled()
    expect(useRouter().push).not.toHaveBeenCalled()
  })

  it('shows the server error when deletion is rejected', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true)
    mockedAxios.delete.mockRejectedValueOnce(failure('Tenant has active subscriptions'))
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Delete' }))

    expect(await screen.findByText('Tenant has active subscriptions')).toBeInTheDocument()
  })

  it('reports that the tenant is not found when it cannot be loaded', async () => {
    mockedAxios.get.mockRejectedValueOnce(failure('Tenant not found'))
    render(<TenantDetailPage />)

    expect(await screen.findByText('Tenant not found')).toBeInTheDocument()
  })

  it('opens the edit form for a tenant whose optional fields are empty', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { ...tenant, slug: null, description: null } })
    render(<TenantDetailPage />)
    await screen.findByRole('heading', { name: 'Night Desk' })

    fireEvent.click(screen.getByRole('button', { name: 'Edit' }))

    expect(screen.getByPlaceholderText('Slug')).toHaveValue('')
    expect(screen.getByPlaceholderText('Description')).toHaveValue('')
  })
})
