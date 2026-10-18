import { render, screen } from '@testing-library/react'
import TestingPage from '@/app/dashboard/testing/page'
import { mockFetch, reply } from '@/test-utils'

const suites = [
  { id: 1, name: 'Unit Tests', test_count: 250, passed: 245, failed: 5, skipped: 0, coverage_percentage: 94.5, last_run_at: '2026-10-18T06:00:00Z' },
  { id: 2, name: 'Integration Tests', test_count: 85, passed: 83, failed: 2, skipped: 0, coverage_percentage: 89.5, last_run_at: null },
]

describe('/dashboard/testing page', () => {
  it('shows the totals across the suites and each suite result', async () => {
    mockFetch({ 'GET /testing/suites': suites })
    render(<TestingPage />)

    expect(await screen.findByText('Unit Tests')).toBeInTheDocument()
    expect(screen.getByText('335')).toBeInTheDocument()
    expect(screen.getByText('97.9%')).toBeInTheDocument()
    expect(screen.getByText('92.0%')).toBeInTheDocument()
    expect(screen.getByText('250 tests')).toBeInTheDocument()
    expect(screen.getByText('✓ 245 passed')).toBeInTheDocument()
    expect(screen.getByText('✗ 2 failed')).toBeInTheDocument()
    expect(screen.getByText('Coverage: 89.5%')).toBeInTheDocument()
    expect(screen.getByText('Not run yet')).toBeInTheDocument()
    expect(screen.getByText(/Last run/)).toBeInTheDocument()
  })

  it('reports zero totals when no suite has been recorded', async () => {
    mockFetch({ 'GET /testing/suites': [] })
    render(<TestingPage />)

    expect(await screen.findByText('No test suites have been recorded yet.')).toBeInTheDocument()
    expect(screen.getAllByText('0.0%')).toHaveLength(2)
  })

  it('states that runs cannot be started from the page and disables the run controls', async () => {
    mockFetch({ 'GET /testing/suites': [] })
    render(<TestingPage />)
    await screen.findByText('No test suites have been recorded yet.')

    expect(screen.getByText(/Starting a test run from here is not available/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Run All Tests' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Coverage Report' })).toBeDisabled()
  })

  it('shows the server reason when results cannot be loaded', async () => {
    mockFetch({ 'GET /testing/suites': reply({ detail: 'Testing API offline' }, 503) })
    render(<TestingPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Testing API offline')
  })

  it('uses a generic message when the request fails without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<TestingPage />)

    expect(await screen.findByText('Test results could not be loaded.')).toBeInTheDocument()
  })

  it('shows a loading placeholder while the suites are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<TestingPage />)

    expect(screen.getByText('Loading test suites…')).toBeInTheDocument()
  })
})
