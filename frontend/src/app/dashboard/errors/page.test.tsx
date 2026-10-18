import { render, screen } from '@testing-library/react'
import ErrorsPage from '@/app/dashboard/errors/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/errors page', () => {
  it('lists unresolved errors with their occurrences, most frequent first', async () => {
    mockFetch({
      'GET /errors/unresolved': [
        { id: 1, error_type: 'TimeoutError', message: 'Upstream timed out', severity: 'high', occurrence_count: 2, first_seen: null, last_seen: '2026-10-18T09:00:00Z' },
        { id: 2, error_type: 'ValueError', message: 'Bad input', severity: null, occurrence_count: 9, first_seen: null, last_seen: null },
      ],
    })
    const { container } = render(<ErrorsPage />)

    expect(await screen.findByText('ValueError')).toBeInTheDocument()
    expect(screen.getByText('9 occurrences')).toBeInTheDocument()
    expect(screen.getByText('2 occurrences · high')).toBeInTheDocument()
    const types = Array.from(container.querySelectorAll('li .font-medium')).map((node) => node.textContent)
    expect(types).toEqual(['ValueError', 'TimeoutError'])
  })

  it('says when no errors are unresolved', async () => {
    mockFetch({ 'GET /errors/unresolved': [] })
    render(<ErrorsPage />)

    expect(await screen.findByText('No unresolved errors.')).toBeInTheDocument()
  })

  it('shows the server reason when errors cannot be loaded', async () => {
    mockFetch({ 'GET /errors/unresolved': reply({ detail: 'Admin access required' }, 403) })
    render(<ErrorsPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Admin access required')
  })
})
