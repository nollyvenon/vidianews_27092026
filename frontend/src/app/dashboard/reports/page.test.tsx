import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import ReportsPage from '@/app/dashboard/reports/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/reports page', () => {
  let consoleError: jest.SpyInstance
  let consoleLog: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
    consoleLog = jest.spyOn(console, 'log').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
    consoleLog.mockRestore()
  })

  it('lists previously generated reports with their type and date', async () => {
    mockFetch({ 'GET /reports': [{ id: 1, type: 'Revenue', generated: '2026-10-01T00:00:00Z' }] })
    render(<ReportsPage />)

    expect(await screen.findByRole('heading', { name: 'Revenue Report' })).toBeInTheDocument()
    expect(screen.getByText(/Generated:/)).toBeInTheDocument()
  })

  it('generates a report of the selected type and refreshes the list', async () => {
    const fetchMock = mockFetch({ 'GET /reports': [], 'POST /reports': { id: 2 } })
    render(<ReportsPage />)
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))

    fireEvent.change(screen.getByRole('combobox'), { target: { value: 'growth' } })
    fireEvent.click(screen.getByRole('button', { name: 'Generate Report' }))

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3))
    const postCall = fetchMock.mock.calls.find(([, init]) => init?.method === 'POST')
    expect(JSON.parse(postCall![1].body as string)).toEqual({ report_type: 'growth' })
  })

  it('shows progress while a report is being generated', async () => {
    global.fetch = jest.fn(async (_url: RequestInfo | URL, init?: RequestInit) =>
      init?.method === 'POST' ? new Promise(() => undefined) : ({ ok: true, json: async () => [] } as Response)
    ) as unknown as typeof fetch
    render(<ReportsPage />)

    fireEvent.click(screen.getByRole('button', { name: 'Generate Report' }))

    expect(await screen.findByRole('button', { name: 'Generating...' })).toBeDisabled()
  })

  it('does not refresh the list when report generation is rejected', async () => {
    const fetchMock = mockFetch({
      'GET /reports': [],
      'POST /reports': reply({ detail: 'Quota exceeded' }, 429),
    })
    render(<ReportsPage />)
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))

    fireEvent.click(screen.getByRole('button', { name: 'Generate Report' }))

    await waitFor(() => expect(screen.getByRole('button', { name: 'Generate Report' })).toBeEnabled())
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })

  it('requests a CSV data export and logs the export id', async () => {
    const fetchMock = mockFetch({ 'GET /reports': [], 'POST /data-export': { id: 'exp-9' } })
    render(<ReportsPage />)

    fireEvent.click(screen.getByRole('button', { name: 'Export Data' }))

    await waitFor(() => expect(consoleLog).toHaveBeenCalledWith('Export requested:', 'exp-9'))
    const exportCall = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/data-export'))
    expect(JSON.parse(exportCall![1].body as string)).toEqual({ export_type: 'csv' })
  })

  it('logs failures from loading, generating and exporting', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<ReportsPage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to fetch reports:', expect.any(Error)))

    fireEvent.click(screen.getByRole('button', { name: 'Generate Report' }))
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to generate report:', expect.any(Error)))

    fireEvent.click(screen.getByRole('button', { name: 'Export Data' }))
    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to request export:', expect.any(Error)))
  })
})
