import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import IntegrationsPage from '@/app/dashboard/integrations/page'
import { mockFetch, reply } from '@/test-utils'

const integrations = [
  { id: 1, integration_type: 'slack', name: 'Newsroom Slack', is_active: true, config: { webhook_url: 'https://hooks.example.com/x', api_token: '********' }, created_at: '2026-10-01T10:00:00Z' },
]

function bodyOf(fetchMock: jest.Mock, method: string, suffix: string) {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
  return JSON.parse(call![1].body as string)
}

describe('/dashboard/integrations page', () => {
  it('shows a loading message until the connected integrations arrive', () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    render(<IntegrationsPage />)

    expect(screen.getByText('Loading integrations…')).toBeInTheDocument()
  })

  it('lists the connected integrations with their type and masked configuration', async () => {
    mockFetch({ 'GET /system/integrations': integrations })
    render(<IntegrationsPage />)

    expect(await screen.findByText('✓ Newsroom Slack')).toBeInTheDocument()
    expect(screen.getAllByText(/Slack/).length).toBeGreaterThan(0)
    expect(screen.getByText(/"api_token": "\*\*\*\*\*\*\*\*"/)).toBeInTheDocument()
  })

  it('says when nothing is connected yet', async () => {
    mockFetch({ 'GET /system/integrations': [] })
    render(<IntegrationsPage />)

    expect(await screen.findByText('No integrations connected yet.')).toBeInTheDocument()
  })

  it('connects the chosen type with its name and JSON configuration', async () => {
    const fetchMock = mockFetch({
      'GET /system/integrations': [],
      'POST /system/integrations': { id: 2, integration_type: 'webhook', name: 'Hook' },
    })
    render(<IntegrationsPage />)
    await screen.findByText('No integrations connected yet.')

    fireEvent.click(screen.getByRole('button', { name: /Webhook/ }))
    fireEvent.change(screen.getByRole('textbox', { name: /Name/ }), { target: { value: ' Hook ' } })
    fireEvent.change(screen.getByRole('textbox', { name: /Configuration/ }), { target: { value: '{"url": "https://example.com/hook"}' } })
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Hook is connected.')
    expect(bodyOf(fetchMock, 'POST', '/system/integrations')).toEqual({
      integration_type: 'webhook',
      name: 'Hook',
      config: { url: 'https://example.com/hook' },
    })
  })

  it('refuses a configuration that is not valid JSON', async () => {
    const fetchMock = mockFetch({ 'GET /system/integrations': [] })
    render(<IntegrationsPage />)
    await screen.findByText('No integrations connected yet.')

    fireEvent.change(screen.getByRole('textbox', { name: /Name/ }), { target: { value: 'Broken' } })
    fireEvent.change(screen.getByRole('textbox', { name: /Configuration/ }), { target: { value: '{not json' } })
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('The configuration must be valid JSON.')
    expect(fetchMock.mock.calls.some(([, init]) => init?.method === 'POST')).toBe(false)
  })

  it('refuses a configuration that is a list rather than an object', async () => {
    mockFetch({ 'GET /system/integrations': [] })
    render(<IntegrationsPage />)
    await screen.findByText('No integrations connected yet.')

    fireEvent.change(screen.getByRole('textbox', { name: /Name/ }), { target: { value: 'List' } })
    fireEvent.change(screen.getByRole('textbox', { name: /Configuration/ }), { target: { value: '[1, 2]' } })
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('The configuration must be a JSON object.')
  })

  it('shows the server reason when the integration cannot be connected', async () => {
    mockFetch({
      'GET /system/integrations': [],
      'POST /system/integrations': reply({ detail: 'Your account has no organization yet.' }, 422),
    })
    render(<IntegrationsPage />)
    await screen.findByText('No integrations connected yet.')

    fireEvent.change(screen.getByRole('textbox', { name: /Name/ }), { target: { value: 'Stripe' } })
    fireEvent.click(screen.getByRole('button', { name: 'Connect' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Your account has no organization yet.')
    await waitFor(() => expect(screen.getByRole('button', { name: 'Connect' })).toBeEnabled())
  })
})
