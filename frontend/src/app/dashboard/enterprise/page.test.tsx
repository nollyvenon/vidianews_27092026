import { fireEvent, render, screen } from '@testing-library/react'
import EnterprisePage from '@/app/dashboard/enterprise/page'
import { mockFetch, reply } from '@/test-utils'

const auditLogs = [
  { id: 1, user_id: 1, action: 'login', severity: 'info', created_at: '2026-10-18T10:30:00Z' },
  { id: 2, user_id: 9, action: 'user_delete', severity: 'high', created_at: '2026-10-18T10:25:00Z' },
  { id: 3, user_id: 3, action: 'content_edit', severity: 'medium', created_at: '2026-10-18T10:20:00Z' },
]

const moderation = [
  { id: 1, content_id: 123, content_type: 'article', status: 'pending', confidence_score: 0.92, created_at: '2026-10-18T10:00:00Z' },
  { id: 2, content_id: 456, content_type: 'comment', status: 'flagged', confidence_score: 0.78, created_at: '2026-10-18T10:00:00Z' },
  { id: 3, content_id: 789, content_type: 'video', status: 'appealed', confidence_score: 0.65, created_at: '2026-10-18T10:00:00Z' },
]

const alerts = [
  { id: 1, notification_type: 'alert', title: 'High CPU Usage', message: 'Server load exceeded 80%', read: false },
  { id: 2, notification_type: 'warning', title: 'Rate Limit Warning', message: 'API rate limit at 95%', read: false },
  { id: 3, notification_type: 'info', title: 'Backup Complete', message: 'Daily backup finished successfully', read: true },
]

const reports = [
  { id: 1, name: 'Monthly Analytics', report_type: 'analytics', status: 'completed', generated_at: '2026-01-15T00:00:00Z', created_at: '2026-01-15T00:00:00Z' },
  { id: 2, name: 'Compliance Report', report_type: 'compliance', status: 'processing', generated_at: null, created_at: '2026-01-15T00:00:00Z' },
  { id: 3, name: 'Performance Report', report_type: 'performance', status: 'pending', generated_at: null, created_at: '2026-01-14T00:00:00Z' },
]

const limits = [
  { id: 1, endpoint: '/api/v1/content', requests_per_minute: 60, requests_per_hour: 1000, requests_per_day: 10000, burst_limit: 100 },
]

function workingRoutes(extra: Record<string, unknown> = {}) {
  return {
    'GET /subscribers/overview': { total_subscribers: 2543 },
    'GET /security/audit-logs': auditLogs,
    'GET /moderation/queue/pending': moderation,
    'GET /enterprise/notifications/': alerts,
    'GET /reports/': reports,
    'GET /rate-limits/configs': limits,
    ...extra,
  };
}

describe('/dashboard/enterprise page', () => {
  it('shows the headline statistics from the live sources', async () => {
    mockFetch(workingRoutes())
    render(<EnterprisePage />)

    expect(screen.getByRole('heading', { name: 'Enterprise Dashboard' })).toBeInTheDocument()
    expect(screen.getByText('Subscribers')).toBeInTheDocument()
    expect(await screen.findByText('2,543')).toBeInTheDocument()
    expect(screen.getByText('Security Events')).toBeInTheDocument()
    // Pending moderation and security events both hold three records in this fixture.
    expect(await screen.findAllByText('3', { selector: 'p.text-2xl' })).toHaveLength(3);
  });

  it('shows dashes for statistics whose source is refused, without hiding the page', async () => {
    mockFetch(workingRoutes({
      'GET /subscribers/overview': reply({ detail: 'Admin access required' }, 403),
      'GET /moderation/queue/pending': reply({ detail: 'Admin access required' }, 403),
    }))
    render(<EnterprisePage />)

    expect(await screen.findByText('Security Audit Logs')).toBeInTheDocument()
    expect(screen.getAllByText('—').length).toBeGreaterThanOrEqual(2)
  });

  it('opens on the security tab with the audit log and colours each severity', async () => {
    mockFetch(workingRoutes())
    render(<EnterprisePage />)

    expect(screen.getByRole('tab', { name: 'Security' })).toHaveAttribute('aria-selected', 'true')
    expect(await screen.findByText('Security Audit Logs')).toBeInTheDocument()
    expect(await screen.findByText('User: 9')).toBeInTheDocument()
    expect(screen.getByText('user_delete')).toBeInTheDocument()
    expect(screen.getByText('high')).toHaveClass('bg-red-100')
    expect(screen.getByText('medium')).toHaveClass('bg-yellow-100')
    expect(screen.getByText('info')).toHaveClass('bg-green-100')
  });

  it('says when there are no security events in the period', async () => {
    mockFetch(workingRoutes({ 'GET /security/audit-logs': [] }))
    render(<EnterprisePage />)

    expect(await screen.findByText('No security events in the last 30 days.')).toBeInTheDocument()
  });

  it('shows an unrated severity when the event carries none', async () => {
    mockFetch(workingRoutes({ 'GET /security/audit-logs': [{ id: 4, user_id: 1, action: 'view', severity: null, created_at: '2026-10-18T10:00:00Z' }] }))
    render(<EnterprisePage />)

    expect(await screen.findByText('unrated')).toHaveClass('bg-gray-100')
  });

  it('shows the moderation queue with the confidence of each decision', async () => {
    mockFetch(workingRoutes())
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Moderation' }))

    expect(screen.getByText('Content Moderation Queue')).toBeInTheDocument()
    expect(await screen.findByText('article #123')).toBeInTheDocument()
    expect(screen.getByText('92%')).toBeInTheDocument()
    expect(screen.getByText('65%')).toBeInTheDocument()
    expect(screen.getByText('flagged')).toHaveClass('bg-red-100')
    expect(screen.getByText('appealed')).toHaveClass('bg-orange-100')
  });

  it('says when the moderation queue is empty', async () => {
    mockFetch(workingRoutes({ 'GET /moderation/queue/pending': [] }))
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Moderation' }))

    expect(await screen.findByText('The moderation queue is empty.')).toBeInTheDocument()
  });

  it('lists system alerts, marking unread ones', async () => {
    mockFetch(workingRoutes())
    const { container } = render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Alerts' }))

    expect(await screen.findByText('High CPU Usage')).toBeInTheDocument()
    expect(screen.getByText('Server load exceeded 80%')).toBeInTheDocument()
    expect(screen.getByText('Daily backup finished successfully')).toBeInTheDocument()
    // Only the two unread alerts carry the unread dot.
    expect(container.querySelectorAll('.bg-blue-600.rounded-full.w-2')).toHaveLength(2)
  });

  it('says when there are no alerts', async () => {
    mockFetch(workingRoutes({ 'GET /enterprise/notifications/': [] }))
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Alerts' }))

    expect(await screen.findByText('No alerts.')).toBeInTheDocument()
  });

  it('lists generated reports with their status and date', async () => {
    mockFetch(workingRoutes())
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Reports' }))

    expect(await screen.findByText('Monthly Analytics')).toBeInTheDocument()
    expect(screen.getByText('completed')).toHaveClass('bg-green-100')
    expect(screen.getByText('processing')).toHaveClass('bg-blue-100')
    expect(screen.getByText('pending')).toHaveClass('bg-gray-100')
  });

  it('says when no reports have been generated', async () => {
    mockFetch(workingRoutes({ 'GET /reports/': [] }))
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Reports' }))

    expect(await screen.findByText('You have not generated any reports.')).toBeInTheDocument()
  });

  it('shows the configured limits for each endpoint, noting that live usage is not recorded', async () => {
    mockFetch(workingRoutes())
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Limits' }))

    expect(await screen.findByText('/api/v1/content')).toBeInTheDocument()
    expect(screen.getByText('60 per minute · 1,000 per hour · 10,000 per day · burst 100')).toBeInTheDocument()
    expect(screen.getByText(/Live usage is not recorded yet/)).toBeInTheDocument()
  });

  it('says when no rate limits are configured', async () => {
    mockFetch(workingRoutes({ 'GET /rate-limits/configs': [] }))
    render(<EnterprisePage />)

    fireEvent.click(screen.getByRole('tab', { name: 'Limits' }))

    expect(await screen.findByText('No rate limits are configured.')).toBeInTheDocument()
  });

  it('shows the server reason when a section is refused to the caller', async () => {
    mockFetch(workingRoutes({ 'GET /security/audit-logs': reply({ detail: 'Admin access required' }, 403) }))
    render(<EnterprisePage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Admin access required')
  });

  it('uses each section’s generic message when its request fails without an API error', async () => {
    global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
    render(<EnterprisePage />)

    expect(await screen.findByText('Audit logs could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Moderation' }))
    expect(await screen.findByText('The moderation queue could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Alerts' }))
    expect(await screen.findByText('Alerts could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Reports' }))
    expect(await screen.findByText('Reports could not be loaded.')).toBeInTheDocument()
    fireEvent.click(screen.getByRole('tab', { name: 'Limits' }))
    expect(await screen.findByText('Rate limits could not be loaded.')).toBeInTheDocument()
  });

  it('shows loading placeholders while the sections are in flight', () => {
    global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
    render(<EnterprisePage />)

    expect(screen.getByText('Loading audit logs…')).toBeInTheDocument()
  });
})
