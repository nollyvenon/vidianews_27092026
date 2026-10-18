import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import { useParams } from 'next/navigation'
import TenantSettingsPage from '@/app/dashboard/tenants/[id]/settings/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

function failure(detail: string) {
  return { response: { data: { detail } } }
}

describe('/dashboard/tenants/[id]/settings page', () => {
  beforeEach(() => {
    (useParams as jest.Mock).mockReturnValue({ id: '3' })
    mockedAxios.get.mockImplementation(async (url: string) => {
      if (url.endsWith('/settings/timezone')) return { data: { key: 'timezone', value: { value: 'Europe/London' } } }
      throw failure('Setting not found')
    })
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('lists the common settings with their saved values or "Not set"', async () => {
    render(<TenantSettingsPage />)

    expect(await screen.findByText('Europe/London')).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'Tenant Settings' })).toBeInTheDocument()
    expect(screen.getByText('webhook url')).toBeInTheDocument()
    expect(screen.getAllByText('Not set')).toHaveLength(4)
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/tenants/3/settings/webhook_url')
  })

  it('edits a setting and saves it when the field loses focus', async () => {
    mockedAxios.put.mockResolvedValueOnce({ data: { key: 'timezone', value: { value: 'UTC' } } })
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getAllByRole('button', { name: 'Edit' })[4])
    const field = screen.getByDisplayValue('Europe/London')
    fireEvent.change(field, { target: { value: 'UTC' } })
    fireEvent.blur(field)

    await waitFor(() => expect(screen.getByText('UTC')).toBeInTheDocument())
    expect(mockedAxios.put).toHaveBeenCalledWith('/api/v1/tenants/3/settings/timezone', {
      key: 'timezone',
      value: { value: 'UTC' },
    })
  })

  it('saves an edited setting when Enter is pressed', async () => {
    mockedAxios.put.mockResolvedValueOnce({ data: { key: 'timezone', value: { value: 'PST' } } })
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getAllByRole('button', { name: 'Edit' })[4])
    const field = screen.getByDisplayValue('Europe/London')
    fireEvent.change(field, { target: { value: 'PST' } })
    fireEvent.keyDown(field, { key: 'Enter' })

    await waitFor(() => expect(mockedAxios.put).toHaveBeenCalled())
  })

  it('shows the server error when a setting cannot be saved', async () => {
    mockedAxios.put.mockRejectedValueOnce(failure('Invalid timezone'))
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getAllByRole('button', { name: 'Edit' })[4])
    const field = screen.getByDisplayValue('Europe/London')
    fireEvent.change(field, { target: { value: 'Mars/Base' } })
    fireEvent.blur(field)

    expect(await screen.findByText('Invalid timezone')).toBeInTheDocument()
  })

  it('does not save an emptied value', async () => {
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getAllByRole('button', { name: 'Edit' })[4])
    const field = screen.getByDisplayValue('Europe/London')
    fireEvent.change(field, { target: { value: '' } })
    fireEvent.blur(field)

    expect(mockedAxios.put).not.toHaveBeenCalled()
  })

  it('adds a custom setting through the add form', async () => {
    mockedAxios.put.mockResolvedValueOnce({ data: { key: 'brand_color', value: { value: 'red' } } })
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getByRole('button', { name: '+ Add Setting' }))
    fireEvent.change(screen.getByPlaceholderText('Setting Key'), { target: { value: 'brand_color' } })
    fireEvent.change(screen.getByPlaceholderText('Value'), { target: { value: 'red' } })
    fireEvent.click(screen.getByRole('button', { name: 'Save' }))

    await waitFor(() => expect(screen.queryByPlaceholderText('Setting Key')).not.toBeInTheDocument())
    expect(mockedAxios.put).toHaveBeenCalledWith('/api/v1/tenants/3/settings/brand_color', {
      key: 'brand_color',
      value: { value: 'red' },
    })
  })

  it('closes the add form without saving', async () => {
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getByRole('button', { name: '+ Add Setting' }))
    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))

    expect(screen.queryByPlaceholderText('Setting Key')).not.toBeInTheDocument()
    expect(mockedAxios.put).not.toHaveBeenCalled()
  })

  it('shows the empty-state prompt when the add form is closed and nothing is saved', async () => {
    mockedAxios.get.mockRejectedValue(failure('Setting not found'))
    render(<TenantSettingsPage />)

    expect(await screen.findByText(/No settings configured/)).toBeInTheDocument()
  })

  it('shows a generic message when a setting cannot be saved without a server detail', async () => {
    mockedAxios.put.mockRejectedValueOnce({})
    render(<TenantSettingsPage />)
    await screen.findByText('Europe/London')

    fireEvent.click(screen.getAllByRole('button', { name: 'Edit' })[4])
    const field = screen.getByDisplayValue('Europe/London')
    fireEvent.change(field, { target: { value: 'UTC' } })
    fireEvent.blur(field)

    expect(await screen.findByText('Failed to save setting')).toBeInTheDocument()
  })
})
