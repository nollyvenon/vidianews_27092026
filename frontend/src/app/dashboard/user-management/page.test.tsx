import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import UserManagementPage from '@/app/dashboard/user-management/page'
import { mockFetch, reply } from '@/test-utils'

const overview = {
  total_subscribers: 24500,
  new_subscribers_this_month: 2300,
  average_engagement: 68.5,
  average_churn_risk: 0.123,
  tiers: [
    { tier: 'enterprise', count: 1800 },
    { tier: 'free', count: 15200 },
    { tier: 'premium', count: 7500 },
  ],
  engagement_levels: [
    { level: 'highly_engaged', count: 8200 },
    { level: 'engaged', count: 10500 },
    { level: 'low_engagement', count: 4300 },
    { level: 'inactive', count: 1500 },
  ],
  churn_risk_levels: [
    { level: 'high', count: 450 },
    { level: 'medium', count: 1200 },
    { level: 'low', count: 3500 },
  ],
  campaigns_sent: 156,
  campaigns_sent_last_7_days: 8,
  active_segments: 12,
  dynamic_segments: 8,
}

const campaigns = [
  { id: 1, name: 'Weekly Tech Digest', status: 'sent', sent_count: 8500, open_count: 5610, click_count: 787, ctr: 9.3, sent_at: '2026-10-10T08:00:00Z' },
  { id: 2, name: 'New Feature Announcement', status: 'sent', sent_count: 12300, open_count: 8610, click_count: 1353, ctr: 11, sent_at: null },
]

const apiKeys = [
  { id: 7, name: 'Analytics export', permissions: ['read', 'write'], is_active: true, key_suffix: 'Ab9x' },
  { id: 8, name: 'Old importer', permissions: [], is_active: false, key_suffix: 'Qz11' },
]

/** Routes for a fully working dashboard. Individual tests override the entries they need. */
function workingRoutes(extra: Record<string, unknown> = {}) {
  return {
    'GET /subscribers/overview': overview,
    'GET /emails/campaigns': campaigns,
    'GET /api-keys/': apiKeys,
    ...extra,
  }
}

function bodyOf(fetchMock: jest.Mock, method: string, path: string): Record<string, unknown> {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).includes(path) && (init?.method ?? 'GET') === method)
  if (!call) throw new Error(`No ${method} call to ${path}`)
  return JSON.parse(String(call[1]?.body))
}

describe('/dashboard/user-management page', () => {
  describe('subscriber overview', () => {
    it('shows the overview figures from the subscriber overview API', async () => {
      mockFetch(workingRoutes())
      render(<UserManagementPage />)

      expect(await screen.findByText('24,500')).toBeInTheDocument()
      expect(screen.getByText('Total Subscribers')).toBeInTheDocument()
      expect(screen.getByText('+2,300 this month')).toBeInTheDocument()
      expect(screen.getByText('156')).toBeInTheDocument()
      expect(screen.getByText('8 in last 7 days')).toBeInTheDocument()
      expect(screen.getByText('68.5%')).toBeInTheDocument()
      expect(screen.getByText('12.3%')).toBeInTheDocument()
      expect(screen.getByText('12')).toBeInTheDocument()
      expect(screen.getByText('8 rule-based segments')).toBeInTheDocument()
    })

    it('breaks subscribers down by tier with each tier share of the total', async () => {
      mockFetch(workingRoutes())
      render(<UserManagementPage />)

      expect(screen.getByText('Subscriber Distribution')).toBeInTheDocument()
      expect(await screen.findByText('Free')).toBeInTheDocument()
      expect(screen.getByText('15,200')).toBeInTheDocument()
      expect(screen.getByText('Premium')).toBeInTheDocument()
      expect(screen.getByText('Enterprise')).toBeInTheDocument()
    })

    it('lists engagement levels in order, with a fallback label for an unknown level', async () => {
      mockFetch(
        workingRoutes({
          'GET /subscribers/overview': {
            ...overview,
            engagement_levels: [...overview.engagement_levels, { level: 'dormant', count: 3 }],
          },
        })
      )
      render(<UserManagementPage />)

      expect(await screen.findByText('Highly Engaged')).toBeInTheDocument()
      expect(screen.getByText('Inactive')).toBeInTheDocument()
      expect(screen.getByText('dormant')).toBeInTheDocument()
    })

    it('shows the at-risk groups with the action for each', async () => {
      mockFetch(
        workingRoutes({
          'GET /subscribers/overview': {
            ...overview,
            churn_risk_levels: [...overview.churn_risk_levels, { level: 'unknown', count: 1 }],
          },
        })
      )
      render(<UserManagementPage />)

      expect(await screen.findByText('High Risk (>80%)')).toBeInTheDocument()
      expect(screen.getByText('450 subscribers')).toBeInTheDocument()
      expect(screen.getByText('Urgent outreach')).toBeInTheDocument()
      expect(screen.getByText('Engagement campaign')).toBeInTheDocument()
      expect(screen.getByText('Monitor')).toBeInTheDocument()
      expect(screen.getByText('unknown')).toBeInTheDocument()
      expect(screen.getByText('Review')).toBeInTheDocument()
    })

    it('says when there are no subscribers yet', async () => {
      mockFetch(workingRoutes({ 'GET /subscribers/overview': { ...overview, total_subscribers: 0, tiers: [] } }))
      render(<UserManagementPage />)

      expect(await screen.findByText('No subscribers yet.')).toBeInTheDocument()
    })

    it('shows the server reason when the overview cannot be loaded', async () => {
      mockFetch(workingRoutes({ 'GET /subscribers/overview': reply({ detail: 'Admin access required' }, 403) }))
      render(<UserManagementPage />)

      expect(await screen.findByRole('alert')).toHaveTextContent('Admin access required')
    })

    it('falls back to a generic message when the request fails without an API error', async () => {
      global.fetch = jest.fn(() => Promise.reject(new TypeError('network down'))) as unknown as typeof fetch
      render(<UserManagementPage />)

      expect(await screen.findByText('Subscriber figures could not be loaded.')).toBeInTheDocument()
      expect(await screen.findByText('Campaign performance could not be loaded.')).toBeInTheDocument()
      expect(await screen.findByText('API keys could not be loaded.')).toBeInTheDocument()
    })
  })

  describe('recent campaigns', () => {
    it('lists campaigns with recipients, click-through rate, opens and clicks', async () => {
      mockFetch(workingRoutes())
      render(<UserManagementPage />)

      expect(await screen.findByText('Weekly Tech Digest')).toBeInTheDocument()
      expect(screen.getByText('Sent to 8,500')).toBeInTheDocument()
      expect(screen.getByText('9.3% CTR')).toBeInTheDocument()
      expect(screen.getByText('Opens: 5,610')).toBeInTheDocument()
      expect(screen.getByText('Clicks: 787')).toBeInTheDocument()
      expect(screen.getByText('11% CTR')).toBeInTheDocument()
    })

    it('says when no campaign has been created', async () => {
      mockFetch(workingRoutes({ 'GET /emails/campaigns': [] }))
      render(<UserManagementPage />)

      expect(await screen.findByText('No campaigns sent yet.')).toBeInTheDocument()
    })

    it('reports a failure to load campaigns without hiding the other sections', async () => {
      mockFetch(workingRoutes({ 'GET /emails/campaigns': reply({ detail: 'Campaigns offline' }, 503) }))
      render(<UserManagementPage />)

      expect(await screen.findByText('Campaigns offline')).toBeInTheDocument()
      expect(screen.getByText('24,500')).toBeInTheDocument()
    })

    it('shows loading placeholders before the figures arrive', () => {
      global.fetch = jest.fn(() => new Promise<Response>(() => undefined)) as unknown as typeof fetch
      render(<UserManagementPage />)

      expect(screen.getByText('Loading campaigns…')).toBeInTheDocument()
      expect(screen.getAllByText('Loading…').length).toBeGreaterThan(0)
      expect(screen.getByText('Loading keys…')).toBeInTheDocument()
    })
  })

  describe('API keys', () => {
    it('lists keys with their suffix, permissions and revoked state', async () => {
      mockFetch(workingRoutes())
      render(<UserManagementPage />)

      expect(await screen.findByText('Analytics export')).toBeInTheDocument()
      expect(screen.getByText(/ends …Ab9x · read, write/)).toBeInTheDocument()
      expect(screen.getByText('(revoked)')).toBeInTheDocument()
      expect(screen.getAllByRole('button', { name: 'Revoke' })).toHaveLength(1)
    })

    it('says when there are no keys', async () => {
      mockFetch(workingRoutes({ 'GET /api-keys/': [] }))
      render(<UserManagementPage />)

      expect(await screen.findByText('No API keys yet.')).toBeInTheDocument()
    })

    it('reports a key list that cannot be loaded', async () => {
      mockFetch(workingRoutes({ 'GET /api-keys/': reply({ detail: 'Keys offline' }, 500) }))
      render(<UserManagementPage />)

      expect(await screen.findByRole('alert')).toHaveTextContent('Keys offline')
    })

    it('creates a key with its permissions and shows the secret once', async () => {
      const fetchMock = mockFetch(workingRoutes({ 'POST /api-keys/': reply({ key: 'sk_live_123' }, 201) }))
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByPlaceholderText('Key name'), { target: { value: ' CRM sync ' } })
      fireEvent.change(screen.getByPlaceholderText('Permissions (comma separated)'), { target: { value: 'read, write ,' } })
      fireEvent.click(screen.getByRole('button', { name: 'Create API key' }))

      expect(await screen.findByText('sk_live_123')).toBeInTheDocument()
      expect(bodyOf(fetchMock, 'POST', '/api-keys/')).toEqual({ name: 'CRM sync', permissions: ['read', 'write'] })
    })

    it('keeps the create button disabled until a name is entered', async () => {
      mockFetch(workingRoutes())
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      expect(screen.getByRole('button', { name: 'Create API key' })).toBeDisabled()
    })

    it('shows the server reason when a key cannot be created', async () => {
      mockFetch(workingRoutes({ 'POST /api-keys/': reply({ detail: 'Key limit reached' }, 409) }))
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByPlaceholderText('Key name'), { target: { value: 'Extra' } })
      fireEvent.click(screen.getByRole('button', { name: 'Create API key' }))

      expect(await screen.findByRole('alert')).toHaveTextContent('Key limit reached')
    })

    it('revokes an active key and reloads the list', async () => {
      const fetchMock = mockFetch(
        workingRoutes({ 'DELETE /api-keys/7': { message: 'revoked' } })
      )
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.click(screen.getByRole('button', { name: 'Revoke' }))

      expect(await screen.findByText('"Analytics export" was revoked.')).toBeInTheDocument()
      await waitFor(() => {
        expect(fetchMock.mock.calls.some(([url, init]) => String(url).includes('/api-keys/7') && init?.method === 'DELETE')).toBe(true)
      })
    })

    it('shows the server reason when a key cannot be revoked', async () => {
      mockFetch(workingRoutes({ 'DELETE /api-keys/7': reply({ detail: 'API key not found' }, 404) }))
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.click(screen.getByRole('button', { name: 'Revoke' }))

      expect(await screen.findByRole('alert')).toHaveTextContent('API key not found')
    })
  })

  describe('webhooks', () => {
    it('registers an endpoint and shows its signing secret once', async () => {
      const fetchMock = mockFetch(
        workingRoutes({
          'POST /webhooks/endpoints': reply({ id: 4, name: 'Hook', url: 'https://example.com/h', events: ['content.published'], secret_key: 'whsec_abc' }, 201),
        })
      )
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByPlaceholderText('Endpoint name'), { target: { value: 'Hook' } })
      fireEvent.change(screen.getByPlaceholderText('https://example.com/hook'), { target: { value: 'https://example.com/h' } })
      fireEvent.change(screen.getByPlaceholderText('Events (comma separated)'), { target: { value: 'content.published, comment.created' } })
      fireEvent.click(screen.getByRole('button', { name: 'Register endpoint' }))

      expect(await screen.findByText('whsec_abc')).toBeInTheDocument()
      expect(screen.getByText(/Endpoint 4 is registered/)).toBeInTheDocument()
      expect(bodyOf(fetchMock, 'POST', '/webhooks/endpoints')).toEqual({
        name: 'Hook',
        url: 'https://example.com/h',
        events: ['content.published', 'comment.created'],
      })
      expect(screen.getByPlaceholderText('Endpoint name')).toHaveValue('')
    })

    it('shows the server reason when an endpoint cannot be registered', async () => {
      mockFetch(workingRoutes({ 'POST /webhooks/endpoints': reply({ detail: 'URL must use https' }, 422) }))
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByPlaceholderText('Endpoint name'), { target: { value: 'Hook' } })
      fireEvent.change(screen.getByPlaceholderText('https://example.com/hook'), { target: { value: 'http://example.com' } })
      fireEvent.click(screen.getByRole('button', { name: 'Register endpoint' }))

      expect(await screen.findByRole('alert')).toHaveTextContent('URL must use https')
    })

    it('reports a successful signed delivery', async () => {
      const fetchMock = mockFetch(
        workingRoutes({
          'POST /webhooks/3/trigger': { log_id: 9, webhook_id: 3, event_type: 'content.published', delivered: true, status_code: 200, error: null },
        })
      )
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByLabelText('Endpoint ID'), { target: { value: '3' } })
      fireEvent.click(screen.getByRole('button', { name: 'Send test event' }))

      expect(await screen.findByText('Delivered to webhook 3 (HTTP 200).')).toBeInTheDocument()
      expect(bodyOf(fetchMock, 'POST', '/webhooks/3/trigger')).toEqual({ event_type: 'content.published', payload: {} })
    })

    it('reports an endpoint that answers with a failure status', async () => {
      mockFetch(
        workingRoutes({
          'POST /webhooks/3/trigger': { log_id: 9, webhook_id: 3, event_type: 'content.published', delivered: false, status_code: 500, error: null },
        })
      )
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByLabelText('Endpoint ID'), { target: { value: '3' } })
      fireEvent.click(screen.getByRole('button', { name: 'Send test event' }))

      expect(await screen.findByText('Webhook 3 responded with HTTP 500; it is not marked delivered.')).toBeInTheDocument()
    })

    it('reports an endpoint that cannot be reached, with the network error', async () => {
      mockFetch(
        workingRoutes({
          'POST /webhooks/3/trigger': { log_id: 9, webhook_id: 3, event_type: 'content.published', delivered: false, status_code: null, error: 'ConnectError: refused' },
        })
      )
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByLabelText('Endpoint ID'), { target: { value: '3' } })
      fireEvent.click(screen.getByRole('button', { name: 'Send test event' }))

      expect(await screen.findByText('Webhook 3 could not be reached: ConnectError: refused.')).toBeInTheDocument()
    })

    it('says the reason is unknown when an unreachable endpoint gives no error', async () => {
      mockFetch(
        workingRoutes({
          'POST /webhooks/3/trigger': { log_id: 9, webhook_id: 3, event_type: 'content.published', delivered: false, status_code: null, error: null },
        })
      )
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByLabelText('Endpoint ID'), { target: { value: '3' } })
      fireEvent.click(screen.getByRole('button', { name: 'Send test event' }))

      expect(await screen.findByText('Webhook 3 could not be reached: unknown error.')).toBeInTheDocument()
    })

    it('shows the server reason when the event cannot be sent', async () => {
      mockFetch(workingRoutes({ 'POST /webhooks/99/trigger': reply({ detail: 'Webhook 99 not found' }, 404) }))
      render(<UserManagementPage />)
      await screen.findByText('Analytics export')

      fireEvent.change(screen.getByLabelText('Endpoint ID'), { target: { value: '99' } })
      fireEvent.click(screen.getByRole('button', { name: 'Send test event' }))

      expect(await screen.findByRole('alert')).toHaveTextContent('Webhook 99 not found')
    })

    it('keeps the API key and webhook sections usable when the overview fails', async () => {
      mockFetch(workingRoutes({ 'GET /subscribers/overview': reply({ detail: 'Admin access required' }, 403) }))
      render(<UserManagementPage />)

      expect(await screen.findByText('Analytics export')).toBeInTheDocument()
      expect(screen.getByText('Webhook endpoints')).toBeInTheDocument()
      expect(screen.getByRole('button', { name: 'Register endpoint' })).toBeInTheDocument()
    })
  })
})
