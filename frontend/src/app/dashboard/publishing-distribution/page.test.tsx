import { fireEvent, screen } from '@testing-library/react'
import PublishingDistributionPage from '@/app/dashboard/publishing-distribution/page'
import { mockFetch, renderWithQuery, reply } from '@/test-utils'

const overview = {
  pending_publications: 2,
  average_engagement: 61.4,
  distribution_reach: 12500,
  click_through_rate: 4.2,
  running_ab_tests: 1,
}

function baseRoutes(extra: Record<string, unknown> = {}) {
  return mockFetch({
    'GET /publishing/overview': overview,
    'GET /publishing/jobs/pending': [{ id: 1, title: 'Launch', status: 'scheduled', scheduled_publish_time: '2026-10-20T10:00:00Z', distribution_channels: [] }],
    'GET /content': { items: [], total: 0 },
    'GET /distribution/channels': [],
    'GET /distribution/syndication-profiles': [],
    'GET /ab-testing/campaigns': [],
    'GET /content-recommendations/engines': [],
    ...extra,
  })
}

describe('/dashboard/publishing-distribution page', () => {
  it('shows the publishing figures recorded for the organization', async () => {
    baseRoutes()
    renderWithQuery(<PublishingDistributionPage />)

    expect(screen.getByRole('heading', { name: 'Publishing & Distribution' })).toBeInTheDocument()
    expect(await screen.findByText('61.4')).toBeInTheDocument()
    expect(screen.getByText('12,500')).toBeInTheDocument()
    expect(screen.getByText('4.20%')).toBeInTheDocument()
    expect(screen.getByText('Scheduled and not yet published')).toBeInTheDocument()
  })

  it('says when no engagement, reach or click figures have been recorded yet', async () => {
    baseRoutes({
      'GET /publishing/overview': { pending_publications: 0, average_engagement: null, distribution_reach: null, click_through_rate: null, running_ab_tests: 0 },
    })
    renderWithQuery(<PublishingDistributionPage />)

    expect((await screen.findAllByText('No data yet')).length).toBe(3)
  })

  it('shows the server reason when the publishing figures cannot be loaded', async () => {
    baseRoutes({ 'GET /publishing/overview': reply({ detail: 'Your account has no organization yet.' }, 422) })
    renderWithQuery(<PublishingDistributionPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
  })

  it('opens on publishing and switches to each management tool', async () => {
    baseRoutes()
    renderWithQuery(<PublishingDistributionPage />)

    expect(screen.getByRole('tab', { name: 'Publishing' })).toHaveAttribute('aria-selected', 'true')
    expect(screen.getByRole('button', { name: 'Schedule Publication' })).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Distribution' }))
    expect(await screen.findByText('Distribution Channels')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Analytics' }))
    expect(await screen.findByText('Content Engagement')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'A/B Testing' }))
    expect(await screen.findByText('New A/B Test')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('tab', { name: 'Recommendations' }))
    expect(await screen.findByText('Recommendation Engines')).toBeInTheDocument()
  })
})
