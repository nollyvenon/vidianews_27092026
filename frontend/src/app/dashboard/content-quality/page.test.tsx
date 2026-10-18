import { fireEvent, screen } from '@testing-library/react'
import ContentQualityPage from '@/app/dashboard/content-quality/page'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

const overview = {
  proofreading: { checks: 3, average_score: 87.5 },
  readability: { checks: 2, average_grade: 8.4 },
  brand_voice: { checks: 1, average_compliance: 92 },
  plagiarism: { checks: 0, average_similarity: null },
}

function base(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /calendar/events': { count: 4, events: [] },
    'GET /content': { items: [], total: 0 },
    'GET /brand-voice/guide': [],
    'GET /content-quality/overview': overview,
    ...extra,
  })
}

describe('/dashboard/content-quality page', () => {
  it('shows the number of events scheduled in the next 30 days', async () => {
    base()
    renderWithQuery(<ContentQualityPage />)

    expect(screen.getByRole('heading', { name: 'Content Quality' })).toBeInTheDocument()
    expect(await screen.findByText('4')).toBeInTheDocument()
    expect(screen.getByText('Scheduled in the next 30 days')).toBeInTheDocument()
  })

  it('shows the averages of the quality checks that have been run and says when none have', async () => {
    base()
    renderWithQuery(<ContentQualityPage />)

    expect(await screen.findByText('87.5')).toBeInTheDocument()
    expect(screen.getByText('3 checks run')).toBeInTheDocument()
    expect(screen.getByText('Grade 8.4')).toBeInTheDocument()
    expect(screen.getByText('92%')).toBeInTheDocument()
    expect(screen.getByText('No checks yet')).toBeInTheDocument()
  })

  it('asks the calendar API, not the content API, for the events in the next 30 days', async () => {
    const fetchMock = base({ 'GET /calendar/events': { count: 1, events: [] } })
    renderWithQuery(<ContentQualityPage />)

    expect(await screen.findByText('1')).toBeInTheDocument()
    const calendarUrl = String(fetchMock.mock.calls.find(([url]) => String(url).includes('/calendar/events'))![0])
    expect(calendarUrl).toMatch(/\/api\/v1\/calendar\/events\?start_date=/)
    expect(calendarUrl).not.toContain('/content/calendar')
  })

  it('shows unavailable when the calendar count cannot be loaded', async () => {
    base({ 'GET /calendar/events': reply({ detail: 'down' }, 500) })
    renderWithQuery(<ContentQualityPage />)

    expect(await screen.findByText('Unavailable')).toBeInTheDocument()
  })

  it('shows the server reason when the quality figures cannot be loaded', async () => {
    base({ 'GET /content-quality/overview': reply({ detail: 'Your account has no organization yet.' }, 422) })
    renderWithQuery(<ContentQualityPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
  })

  it('opens on the calendar tool and switches between the analysis tools', async () => {
    base()
    renderWithQuery(<ContentQualityPage />)

    expect(screen.getByRole('tab', { name: 'Calendar' })).toHaveAttribute('aria-selected', 'true')
    expect(await screen.findByText('No events scheduled in the next 30 days.')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Proofreading' }))
    expect(screen.getByRole('button', { name: 'Check Proofreading' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Plagiarism' }))
    expect(screen.getByRole('button', { name: 'Check Plagiarism' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Readability' }))
    expect(screen.getByRole('button', { name: 'Check Readability' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Brand Voice' }))
    expect(await screen.findByRole('heading', { name: 'Brand Guide' })).toBeInTheDocument()
  })
})
