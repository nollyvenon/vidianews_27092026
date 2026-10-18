import { screen, waitFor } from '@testing-library/react'
import DashboardPage from '@/app/dashboard/page'
import { ApiClient } from '@/lib/api-client'
import { ApiError } from '@/lib/api-error'
import { buildAuth, renderWithAuth, testUser } from '@/test-utils'

jest.mock('@/lib/api-client', () => ({
  ApiClient: { get: jest.fn() },
}))

const get = ApiClient.get as jest.Mock

const zeros = { videos: 0, articles: 0, chats: 0, monthly_spend: 0 }

function routeGet(summary: unknown = zeros, activity: unknown = []) {
  get.mockImplementation((path: string) => {
    if (path === '/dashboard/summary') return summary instanceof Error ? Promise.reject(summary) : Promise.resolve(summary)
    if (path === '/activity/me?limit=5') return Promise.resolve(activity)
    return Promise.reject(new Error(`unexpected GET ${path}`))
  })
}

describe('/dashboard page', () => {
  beforeEach(() => jest.clearAllMocks())

  it('greets the signed-in user by name', async () => {
    routeGet()
    renderWithAuth(<DashboardPage />)

    expect(screen.getByRole('heading', { name: `Welcome, ${testUser.name}!` })).toBeInTheDocument()
    await waitFor(() => expect(get).toHaveBeenCalledWith('/dashboard/summary'))
  })

  it('shows the user own totals, with spend to the cent', async () => {
    routeGet({ videos: 3, articles: 2, chats: 7, monthly_spend: 15.5 })
    renderWithAuth(<DashboardPage />)

    expect(await screen.findByText('$15.50')).toBeInTheDocument()
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('7')).toBeInTheDocument()
  })

  it('lists recent activity, and says so when there is none', async () => {
    routeGet(zeros, [{ id: 1, action: 'create', entity_type: 'content', description: 'Published a video', created_at: '2026-10-10T10:00:00Z' }])
    renderWithAuth(<DashboardPage />)

    expect(await screen.findByText('Published a video')).toBeInTheDocument()
  })

  it('says when there is no recent activity', async () => {
    routeGet(zeros, [])
    renderWithAuth(<DashboardPage />)

    expect(await screen.findByText('No recent activity yet.')).toBeInTheDocument()
  })

  it('reports a failure to load the totals with the server message', async () => {
    routeGet(new ApiError('Sign in again'), [])
    renderWithAuth(<DashboardPage />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Sign in again')
    expect(screen.queryByText('No recent activity yet.')).toBeInTheDocument()
  })

  it('links to the main feature areas', async () => {
    routeGet()
    renderWithAuth(<DashboardPage />)

    expect(screen.getByRole('link', { name: /Manage Content/ })).toHaveAttribute('href', '/dashboard/content')
    expect(screen.getByRole('link', { name: /AI Features/ })).toHaveAttribute('href', '/dashboard/ai')
    expect(screen.getByRole('link', { name: /View Analytics/ })).toHaveAttribute('href', '/dashboard/analytics')
    expect(screen.getByRole('link', { name: /Ecommerce/ })).toHaveAttribute('href', '/dashboard/ecommerce')
    await screen.findByText('No recent activity yet.')
  })

  it('renders without a user while the profile is unavailable', async () => {
    routeGet()
    renderWithAuth(<DashboardPage />, buildAuth({ user: null }))

    expect(screen.getByRole('heading', { name: 'Welcome, !' })).toBeInTheDocument()
    await screen.findByText('No recent activity yet.')
  })
})
