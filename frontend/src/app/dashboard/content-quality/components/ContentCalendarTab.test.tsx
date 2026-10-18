import { screen } from '@testing-library/react'
import ContentCalendarTab, { confidenceClass } from '@/app/dashboard/content-quality/components/ContentCalendarTab'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

// Local-time construction keeps date-fns formatting deterministic across time zones.
const launch = new Date(2026, 9, 1, 10, 0).toISOString()
const recommended = new Date(2026, 9, 2, 14, 30).toISOString()

const events = [
  {
    id: 1,
    event_type: 'post',
    title: 'Launch video',
    scheduled_for: launch,
    ai_recommended_time: recommended,
    ai_confidence_score: 0.8,
    predicted_reach: 12000,
    predicted_engagement: 100,
  },
  {
    id: 2,
    event_type: 'newsletter',
    title: 'Weekly digest',
    scheduled_for: launch,
    ai_confidence_score: 0.6,
  },
]

describe('ContentCalendarTab', () => {
  it('shows a loading message while events are fetched', () => {
    mockFetch({ 'GET /calendar/events': { count: 0, events: [] } })
    renderWithQuery(<ContentCalendarTab />)

    expect(screen.getByText('Loading calendar events…')).toBeInTheDocument()
  })

  it('requests the next 30 days of events from the calendar endpoint', async () => {
    const fetchMock = mockFetch({ 'GET /calendar/events': { count: 2, events } })
    renderWithQuery(<ContentCalendarTab />)
    await screen.findByRole('heading', { name: 'Launch video' })

    const url = String(fetchMock.mock.calls[0][0])
    expect(url).toMatch(/\/api\/v1\/calendar\/events\?start_date=/)
    expect(url).toMatch(/end_date=/)
  })

  it('summarises the events with count, average confidence and predicted reach', async () => {
    mockFetch({ 'GET /calendar/events': { count: 2, events } })
    renderWithQuery(<ContentCalendarTab />)

    expect(await screen.findByRole('heading', { name: 'Launch video' })).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('70%')).toBeInTheDocument()
    expect(screen.getByText('12K')).toBeInTheDocument()
  })

  it('lists each event with its confidence badge, schedule and predicted reach', async () => {
    mockFetch({ 'GET /calendar/events': { count: 2, events } })
    renderWithQuery(<ContentCalendarTab />)

    expect(await screen.findByText('80% Confidence')).toHaveClass('bg-green-100')
    expect(screen.getByText('60% Confidence')).toHaveClass('bg-blue-100')
    expect(screen.getAllByText('Scheduled: Oct 1, 10:00')).toHaveLength(2)
    expect(screen.getByText('Recommended: Oct 2, 14:30')).toBeInTheDocument()
    expect(screen.getByText('Est. Reach: 12.0K')).toBeInTheDocument()
  })

  it('shows the empty state when nothing is scheduled', async () => {
    mockFetch({ 'GET /calendar/events': { count: 0, events: [] } })
    renderWithQuery(<ContentCalendarTab />)

    expect(await screen.findByText('No events scheduled in the next 30 days.')).toBeInTheDocument()
    expect(screen.getByText('0%')).toBeInTheDocument()
  })

  it('shows the server message when the calendar cannot be loaded', async () => {
    mockFetch({ 'GET /calendar/events': reply({ detail: 'Your account has no organization yet.' }, 422) })
    renderWithQuery(<ContentCalendarTab />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
  })

  it.each([
    [0.9, 'bg-green-100'],
    [0.6, 'bg-blue-100'],
    [0.45, 'bg-yellow-100'],
    [0.2, 'bg-gray-100'],
  ])('colours a %s confidence score', (confidence, colour) => {
    expect(confidenceClass(confidence)).toContain(colour)
  })
})
