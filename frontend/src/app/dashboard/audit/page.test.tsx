import { render, screen } from '@testing-library/react'
import AuditPage from '@/app/dashboard/audit/page'
import { mockFetch, reply } from '@/test-utils'

const logs = [
  { id: 1, action: 'LOGIN', resource_type: 'session', user_id: 7, created_at: '2026-10-01T10:00:00Z' },
  { id: 2, action: 'DELETE', resource_type: 'content', user_id: 9, created_at: '2026-10-02T11:30:00Z' },
]

describe('/dashboard/audit page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows a loading state before the audit logs arrive', () => {
    mockFetch({ 'GET /system/audit/logs': logs })
    render(<AuditPage />)

    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('renders one table row per audit entry', async () => {
    mockFetch({ 'GET /system/audit/logs': logs })
    render(<AuditPage />)

    expect(await screen.findByText('LOGIN')).toBeInTheDocument()
    expect(screen.getByText('DELETE')).toBeInTheDocument()
    expect(screen.getByText('session')).toBeInTheDocument()
    expect(screen.getByText('content')).toBeInTheDocument()
    expect(screen.getAllByRole('row')).toHaveLength(3)
  })

  it('logs the failure and shows an empty table when the logs cannot be loaded', async () => {
    mockFetch({ 'GET /system/audit/logs': reply({ detail: 'forbidden' }, 403) })
    render(<AuditPage />)

    expect(await screen.findByRole('table')).toBeInTheDocument()
    expect(screen.getAllByRole('row')).toHaveLength(1)
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch logs', expect.any(Error))
  })
})
