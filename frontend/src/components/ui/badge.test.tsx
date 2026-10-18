import { render, screen } from '@testing-library/react'
import { Badge } from '@/components/ui/badge'

describe('Badge', () => {
  it('renders its label with the default variant', () => {
    render(<Badge>Live</Badge>)

    expect(screen.getByText('Live')).toHaveClass('bg-blue-600')
  })

  it.each([
    ['secondary', 'bg-gray-200'],
    ['destructive', 'bg-red-600'],
    ['outline', 'border-gray-300'],
  ])('applies the %s variant styles', (variant, expectedClass) => {
    render(<Badge variant={variant as 'secondary' | 'destructive' | 'outline'}>Tag</Badge>)

    expect(screen.getByText('Tag')).toHaveClass(expectedClass)
  })

  it('merges a custom className and passes through other props', () => {
    render(
      <Badge className="ml-2" data-testid="badge">
        New
      </Badge>
    )

    expect(screen.getByTestId('badge')).toHaveClass('ml-2', 'rounded-full')
  })
})
