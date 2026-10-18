import { render, screen } from '@testing-library/react'
import AIPage from '@/app/dashboard/ai/page'

describe('/dashboard/ai page', () => {
  it('lists the AI feature areas as links', () => {
    render(<AIPage />)

    expect(screen.getByRole('heading', { name: 'AI Features' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /AI Chat/ })).toHaveAttribute('href', '/dashboard/ai/chat')
    expect(screen.getByRole('link', { name: /Prompt Library/ })).toHaveAttribute('href', '/dashboard/ai/prompts')
    expect(screen.getByRole('link', { name: /AI Workflows/ })).toHaveAttribute('href', '/dashboard/ai/workflows')
    expect(screen.getByRole('link', { name: /AI Monitoring/ })).toHaveAttribute('href', '/dashboard/ai/monitoring')
  })

  it('describes each feature area', () => {
    render(<AIPage />)

    expect(screen.getByText('Multi-turn AI conversations with context memory')).toBeInTheDocument()
    expect(screen.getByText('Track usage, costs, and performance metrics')).toBeInTheDocument()
    expect(screen.getAllByRole('link')).toHaveLength(6)
  })
})
