import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import TestingPage from '@/app/dashboard/testing/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'

jest.mock('@/lib/api-client', () => ({ ApiClient: { get: jest.fn() } }))
const get = ApiClient.get as jest.Mock

const suites = [
  { id: 1, name: 'Unit Tests', test_count: 4, passed: 2, failed: 1, skipped: 1, pass_rate: 66.7, coverage_percentage: 94.5, last_run_at: '2026-10-17T10:00:00Z' },
  { id: 2, name: 'E2E Tests', test_count: 2, passed: 2, failed: 0, skipped: 0, pass_rate: 100, coverage_percentage: 70, last_run_at: '2026-10-17T11:00:00Z' },
]

const failure = {
  id: 10, test_name: 'test_refund', status: 'failed', duration_ms: 40,
  error_message: 'expected 200, got 500', run_at: '2026-10-17T10:00:00Z',
}
const pass = { id: 11, test_name: 'test_login', status: 'passed', duration_ms: 12, error_message: null, run_at: '2026-10-17T10:00:00Z' }

function routes(options: { suiteList?: unknown[]; detailFailures?: unknown[]; detailAll?: unknown[] } = {}) {
  get.mockImplementation((path: string) => {
    if (path === '/test-reports/suites') return Promise.resolve(options.suiteList ?? suites)
    if (path.startsWith('/test-reports/suites/1?status=failed')) return Promise.resolve({ suite: suites[0], results: options.detailFailures ?? [failure] })
    if (path.startsWith('/test-reports/suites/1?limit=100')) return Promise.resolve({ suite: suites[0], results: options.detailAll ?? [failure, pass] })
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('/dashboard/testing page', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    routes()
  })

  it('shows totals computed from the recorded suites', async () => {
    render(<TestingPage />)
    expect(await screen.findByText('Unit Tests')).toBeInTheDocument()
    expect(screen.getByText('6')).toBeInTheDocument() // total tests: 4 + 2
    expect(screen.getByText('80.0%')).toBeInTheDocument() // pass rate: 4 passed of 5 executed
    expect(screen.getByText('82.3%')).toBeInTheDocument() // average coverage of 94.5 and 70
  })

  it('does not show invented figures when no run has been recorded', async () => {
    routes({ suiteList: [] })
    render(<TestingPage />)
    expect(await screen.findByText(/No test runs have been recorded yet/)).toBeInTheDocument()
    expect(screen.getByText(/POST \/api\/v1\/test-reports\/runs/)).toBeInTheDocument()
    expect(screen.queryByText('250')).not.toBeInTheDocument()
  })

  it('shows a load error without any placeholder data', async () => {
    get.mockRejectedValue(new ApiError('You do not have permission to do this.'))
    render(<TestingPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent('You do not have permission to do this.')
    expect(screen.queryByText('Unit Tests')).not.toBeInTheDocument()
  })

  it('shows the failures and their messages for a suite', async () => {
    render(<TestingPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'View results' }))[0])

    expect(await screen.findByText('test_refund')).toBeInTheDocument()
    expect(screen.getByText('expected 200, got 500')).toBeInTheDocument()
    expect(screen.queryByText('test_login')).not.toBeInTheDocument()
    expect(get).toHaveBeenCalledWith('/test-reports/suites/1?status=failed&limit=100')
  })

  it('switches to all results', async () => {
    render(<TestingPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'View results' }))[0])
    await screen.findByText('test_refund')

    fireEvent.click(screen.getByRole('button', { name: 'All results' }))

    expect(await screen.findByText('test_login')).toBeInTheDocument()
    await waitFor(() => expect(get).toHaveBeenCalledWith('/test-reports/suites/1?limit=100'))
  })

  it('says when a suite has no failures', async () => {
    routes({ detailFailures: [] })
    render(<TestingPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'View results' }))[0])

    expect(await screen.findByText('No failures in the latest runs.')).toBeInTheDocument()
  })

  it('shows an error when a suite’s results cannot be loaded', async () => {
    get.mockImplementation((path: string) => {
      if (path === '/test-reports/suites') return Promise.resolve(suites)
      return Promise.reject(new ApiError('Test suite not found'))
    })
    render(<TestingPage />)
    fireEvent.click((await screen.findAllByRole('button', { name: 'View results' }))[0])

    expect(await screen.findByRole('alert')).toHaveTextContent('Test suite not found')
  })
})
