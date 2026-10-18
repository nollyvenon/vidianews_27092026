import { render, screen, waitFor } from '@testing-library/react'
import CompliancePage from '@/app/dashboard/compliance/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/compliance page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows GDPR and CCPA status and an overall good rating when fully compliant', async () => {
    mockFetch({
      'GET /compliance/status': { gdpr: true, ccpa: true, compliant: true },
      'GET /audit/logs': [],
    })
    render(<CompliancePage />)

    expect(await screen.findByText('Good')).toBeInTheDocument()
    expect(screen.getAllByText('✓ Compliant')).toHaveLength(2)
    expect(screen.getByText('Good')).toHaveClass('text-green-600')
  })

  it('flags non-compliant frameworks and asks for a review', async () => {
    mockFetch({
      'GET /compliance/status': { gdpr: false, ccpa: true, compliant: false },
      'GET /audit/logs': [],
    })
    render(<CompliancePage />)

    // Wait for the response: before it arrives both frameworks show as non-compliant.
    await waitFor(() => expect(screen.getAllByText('✗ Non-compliant')).toHaveLength(1))
    expect(screen.getByText('Review Required')).toBeInTheDocument()
    expect(screen.getByText('✗ Non-compliant')).toHaveClass('text-red-600')
    expect(screen.getByText('✓ Compliant')).toBeInTheDocument()
  })

  it('lists the audit trail entries with their resource and time', async () => {
    mockFetch({
      'GET /compliance/status': { gdpr: true, ccpa: true, compliant: true },
      'GET /audit/logs': [{ id: 1, action: 'EXPORT_DATA', resource: 'user:7', created_at: '2026-10-01T10:00:00Z' }],
    })
    render(<CompliancePage />)

    expect(await screen.findByText('EXPORT_DATA')).toBeInTheDocument()
    expect(screen.getByText(/user:7 •/)).toBeInTheDocument()
  })

  it('keeps the unknown state when the compliance service is unavailable', async () => {
    mockFetch({
      'GET /compliance/status': reply({ detail: 'down' }, 503),
      'GET /audit/logs': reply({ detail: 'down' }, 503),
    })
    render(<CompliancePage />)

    expect(await screen.findByText('Review Required')).toBeInTheDocument()
    expect(screen.getAllByText('✗ Non-compliant')).toHaveLength(2)
    expect(consoleError).not.toHaveBeenCalled()
  })

  it('logs both failures when the requests cannot be made', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<CompliancePage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to fetch compliance:', expect.any(Error)))
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch audit logs:', expect.any(Error))
  })
})
