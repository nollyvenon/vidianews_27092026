import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import axios from 'axios'
import ActivityPage from '@/app/dashboard/activity/page'

jest.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

const activities = [
  {
    id: 1,
    action: 'login',
    entity_type: 'session',
    description: 'Signed in from Chrome',
    status: 'success',
    created_at: '2026-10-01T10:00:00Z',
  },
  { id: 2, action: 'delete', entity_type: 'content', description: null, status: 'failed', created_at: '2026-10-02T10:00:00Z' },
]
const summary = {
  total_activities: 2,
  period_days: 30,
  by_action: { login: 1, delete: 1 },
  by_entity: { session: 1, content: 1 },
}

describe('/dashboard/activity page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
    mockedAxios.get.mockImplementation(async (url: string) => {
      if (url.endsWith('/summary')) return { data: summary }
      return { data: activities }
    })
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('shows the activity summary and the activity list', async () => {
    render(<ActivityPage />)

    expect(await screen.findByRole('heading', { name: 'Activity Log' })).toBeInTheDocument()
    expect(screen.getByText('Total Activities')).toBeInTheDocument()
    expect(screen.getByText('30 days')).toBeInTheDocument()
    expect(screen.getByText('LOGIN - session')).toBeInTheDocument()
    expect(screen.getByText('Signed in from Chrome')).toBeInTheDocument()
    expect(screen.getByText('success')).toHaveClass('bg-green-100')
    expect(screen.getByText('failed')).toHaveClass('bg-red-100')
  })

  it('breaks the summary down by action and by entity', async () => {
    render(<ActivityPage />)

    expect(await screen.findByText('login: 1')).toBeInTheDocument()
    expect(screen.getByText('content: 1')).toBeInTheDocument()
    expect(screen.getByText('session: 1')).toBeInTheDocument()
  })

  it('filters the list by action as the user types', async () => {
    render(<ActivityPage />)
    await screen.findByRole('heading', { name: 'Activity Log' })

    fireEvent.change(screen.getByPlaceholderText('Filter by action...'), { target: { value: 'login' } })

    await waitFor(() =>
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/activity/me?action=login')
    )
  })

  it('shows the empty state when no activity matches', async () => {
    mockedAxios.get.mockImplementation(async (url: string) => (url.endsWith('/summary') ? { data: null } : { data: [] }))
    render(<ActivityPage />)

    expect(await screen.findByText('No activities found')).toBeInTheDocument()
  })

  it('logs failures to load the activity and the summary', async () => {
    mockedAxios.get.mockRejectedValue(new Error('down'))
    render(<ActivityPage />)

    expect(await screen.findByRole('heading', { name: 'Activity Log' })).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Error loading activities:', expect.any(Error))
    expect(consoleError).toHaveBeenCalledWith('Error loading summary:', expect.any(Error))
  })

  it('renders a summary that has no action or entity breakdown', async () => {
    mockedAxios.get.mockImplementation(async (url: string) =>
      url.endsWith('/summary') ? { data: { total_activities: 0, period_days: 7 } } : { data: [] }
    )
    render(<ActivityPage />)

    expect(await screen.findByText('7 days')).toBeInTheDocument()
    expect(screen.getByText('No activities found')).toBeInTheDocument()
  })
})
