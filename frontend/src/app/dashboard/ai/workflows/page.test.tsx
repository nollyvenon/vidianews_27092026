import { render, screen } from '@testing-library/react'
import WorkflowsPage from '@/app/dashboard/ai/workflows/page'
import { mockFetch, reply } from '@/test-utils'

describe('/dashboard/ai/workflows page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('lists workflows with their description and status', async () => {
    mockFetch({
      'GET /ai/workflows': [
        { id: 1, name: 'Auto-tag videos', description: 'Tags new uploads', status: 'active', created_at: '2026-10-01' },
        { id: 2, name: 'Weekly digest', status: 'draft', created_at: '2026-10-01' },
      ],
    })
    render(<WorkflowsPage />)

    expect(await screen.findByRole('heading', { name: 'Auto-tag videos' })).toBeInTheDocument()
    expect(screen.getByText('Tags new uploads')).toBeInTheDocument()
    expect(screen.getByText('active')).toHaveClass('bg-green-100')
    expect(screen.getByText('draft')).toHaveClass('bg-gray-100')
    expect(screen.getAllByRole('button', { name: 'Edit' })).toHaveLength(2)
  })

  it('offers the create action', async () => {
    mockFetch({ 'GET /ai/workflows': [] })
    render(<WorkflowsPage />)

    expect(await screen.findByText(/No workflows yet/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Create Workflow' })).toBeInTheDocument()
  })

  it('logs the failure and shows the empty state when workflows cannot be loaded', async () => {
    mockFetch({ 'GET /ai/workflows': reply({ detail: 'down' }, 500) })
    render(<WorkflowsPage />)

    expect(await screen.findByText(/No workflows yet/)).toBeInTheDocument()
    expect(consoleError).toHaveBeenCalledWith('Failed to fetch workflows', expect.any(Error))
  })
})
