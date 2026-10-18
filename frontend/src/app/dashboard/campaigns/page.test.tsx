import { fireEvent, screen, waitFor } from '@testing-library/react'
import CampaignsPage from '@/app/dashboard/campaigns/page'
import { mockFetch, reply, renderWithQuery } from '@/test-utils'

const campaigns = [{ id: 3, name: 'Spring launch', subject: 'New season', body: 'Hello', status: 'draft' }]

function bodyOf(fetchMock: jest.Mock, method: string, suffix: string) {
  const call = fetchMock.mock.calls.find(([url, init]) => String(url).endsWith(suffix) && init?.method === method)
  return JSON.parse(call![1].body as string)
}

describe('/dashboard/campaigns page', () => {
  it('lists the campaigns with their subject and status', async () => {
    mockFetch({ 'GET /monetization/campaigns': campaigns })
    renderWithQuery(<CampaignsPage />)

    expect(await screen.findByText('Spring launch')).toBeInTheDocument()
    expect(screen.getByText('Subject: New season')).toBeInTheDocument()
    expect(screen.getByText('Status: draft')).toBeInTheDocument()
  })

  it('says when there are no campaigns', async () => {
    mockFetch({ 'GET /monetization/campaigns': [] })
    renderWithQuery(<CampaignsPage />)

    expect(await screen.findByText('No campaigns yet.')).toBeInTheDocument()
  })

  it('creates a campaign with its name, subject and body', async () => {
    const fetchMock = mockFetch({
      'GET /monetization/campaigns': [],
      'POST /monetization/campaigns': { id: 4 },
    })
    renderWithQuery(<CampaignsPage />)
    await screen.findByText('No campaigns yet.')

    fireEvent.change(screen.getByPlaceholderText('Campaign name'), { target: { value: ' Autumn ' } })
    fireEvent.change(screen.getByPlaceholderText('Subject line'), { target: { value: 'Fall news' } })
    fireEvent.change(screen.getByPlaceholderText('Message body'), { target: { value: 'Read more' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create campaign' }))

    expect(await screen.findByRole('status')).toHaveTextContent('Campaign created.')
    expect(bodyOf(fetchMock, 'POST', '/monetization/campaigns')).toEqual({ name: 'Autumn', subject: 'Fall news', body: 'Read more' })
  })

  it('sends a campaign and reports it', async () => {
    const fetchMock = mockFetch({
      'GET /monetization/campaigns': campaigns,
      'POST /monetization/campaigns/3/send': { status: 'sent' },
    })
    renderWithQuery(<CampaignsPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Send' }))

    expect(await screen.findByRole('status')).toHaveTextContent('"Spring launch" was sent.')
    await waitFor(() =>
      expect(fetchMock.mock.calls.some(([url, init]) => String(url).endsWith('/monetization/campaigns/3/send') && init?.method === 'POST')).toBe(true),
    )
  })

  it('shows the server reason when a campaign cannot be sent', async () => {
    mockFetch({
      'GET /monetization/campaigns': campaigns,
      'POST /monetization/campaigns/3/send': reply({ detail: 'Campaign has no recipients' }, 422),
    })
    renderWithQuery(<CampaignsPage />)

    fireEvent.click(await screen.findByRole('button', { name: 'Send' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Campaign has no recipients')
  })
})
