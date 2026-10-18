import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import { useParams } from 'next/navigation'
import MembersPage from '@/app/dashboard/tenants/[id]/members/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const members = [
  { id: 1, user_id: 10, role: 'owner', status: 'active', is_owner: true, joined_at: '2026-01-05' },
  { id: 2, user_id: 11, role: 'editor', status: 'invited', is_owner: false, joined_at: '2026-02-05' },
]

function failure(detail: string) {
  return { response: { data: { detail } } }
}

describe('/dashboard/tenants/[id]/members page', () => {
  beforeEach(() => {
    (useParams as jest.Mock).mockReturnValue({ id: '3' })
    mockedAxios.get.mockResolvedValue({ data: members })
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  it('lists the members with their role and status, marking the owner', async () => {
    render(<MembersPage />)

    expect(await screen.findByRole('heading', { name: 'Team Members' })).toBeInTheDocument()
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/tenants/3/members')
    expect(screen.getByText('User #10')).toBeInTheDocument()
    expect(screen.getByText('OWNER')).toBeInTheDocument()
    expect(screen.getByText('editor')).toBeInTheDocument()
    expect(screen.getByText('invited')).toHaveClass('bg-gray-100')
    expect(screen.getByRole('link', { name: '← Back to Tenant' })).toHaveAttribute('href', '/dashboard/tenants/3')
  })

  it('only offers removal for members who are not the owner', async () => {
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    expect(screen.getAllByRole('button', { name: 'Remove' })).toHaveLength(1)
  })

  it('invites a member and refreshes the list', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: { ok: true } })
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: '+ Invite Member' }))
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'new@example.com' } })
    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'admin' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send Invitation' }))

    await waitFor(() => expect(screen.queryByRole('heading', { name: 'Invite Member' })).not.toBeInTheDocument())
    expect(mockedAxios.post).toHaveBeenCalledWith('/api/v1/tenants/3/invite', { email: 'new@example.com', role: 'admin' })
    expect(mockedAxios.get).toHaveBeenCalledTimes(2)
  })

  it('shows the server error when an invitation is rejected', async () => {
    mockedAxios.post.mockRejectedValueOnce(failure('Seat limit reached'))
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: '+ Invite Member' }))
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'x@example.com' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send Invitation' }))

    expect(await screen.findByText('Seat limit reached')).toBeInTheDocument()
  })

  it('uses a generic message when an invitation fails without a server detail', async () => {
    mockedAxios.post.mockRejectedValueOnce({})
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: '+ Invite Member' }))
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'x@example.com' } })
    fireEvent.click(screen.getByRole('button', { name: 'Send Invitation' }))

    expect(await screen.findByText('Failed to send invitation')).toBeInTheDocument()
  })

  it('cancels the invite form without sending anything', async () => {
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: '+ Invite Member' }))
    fireEvent.click(screen.getByRole('button', { name: 'Cancel' }))

    expect(screen.queryByPlaceholderText('Email')).not.toBeInTheDocument()
    expect(mockedAxios.post).not.toHaveBeenCalled()
  })

  it('removes a member after confirmation and refreshes the list', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true)
    mockedAxios.delete.mockResolvedValueOnce({ data: {} })
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: 'Remove' }))

    await waitFor(() => expect(mockedAxios.delete).toHaveBeenCalledWith('/api/v1/tenants/3/members/11'))
    await waitFor(() => expect(mockedAxios.get).toHaveBeenCalledTimes(2))
  })

  it('keeps the member when removal is not confirmed', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(false)
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: 'Remove' }))

    expect(mockedAxios.delete).not.toHaveBeenCalled()
  })

  it('shows the server error when removal is rejected', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true)
    mockedAxios.delete.mockRejectedValueOnce(failure('Cannot remove the last admin'))
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: 'Remove' }))

    expect(await screen.findByText('Cannot remove the last admin')).toBeInTheDocument()
  })

  it('shows the server error when the members cannot be loaded', async () => {
    mockedAxios.get.mockRejectedValueOnce(failure('Forbidden'))
    render(<MembersPage />)

    expect(await screen.findByText('Forbidden')).toBeInTheDocument()
  })

  it('shows a generic message when the members cannot be requested', async () => {
    mockedAxios.get.mockRejectedValueOnce({})
    render(<MembersPage />)

    expect(await screen.findByText('Failed to load members')).toBeInTheDocument()
  })

  it('shows a generic message when removal fails without a server detail', async () => {
    jest.spyOn(window, 'confirm').mockReturnValue(true)
    mockedAxios.delete.mockRejectedValueOnce({})
    render(<MembersPage />)
    await screen.findByRole('heading', { name: 'Team Members' })

    fireEvent.click(screen.getByRole('button', { name: 'Remove' }))

    expect(await screen.findByText('Failed to remove member')).toBeInTheDocument()
  })
})
