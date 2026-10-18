import { createRef } from 'react'
import { render, screen } from '@testing-library/react'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'

describe('Card components', () => {
  it('composes a full card with the expected semantic parts', () => {
    render(
      <Card data-testid="card">
        <CardHeader>
          <CardTitle>Channel stats</CardTitle>
          <CardDescription>Last 30 days</CardDescription>
        </CardHeader>
        <CardContent>1,200 views</CardContent>
        <CardFooter>Updated today</CardFooter>
      </Card>
    )

    expect(screen.getByTestId('card')).toHaveClass('rounded-lg', 'border')
    expect(screen.getByRole('heading', { name: 'Channel stats' }).tagName).toBe('H3')
    expect(screen.getByText('Last 30 days').tagName).toBe('P')
    expect(screen.getByText('1,200 views')).toHaveClass('p-6')
    expect(screen.getByText('Updated today')).toHaveClass('items-center')
  })

  it('forwards refs and custom class names for every part', () => {
    const refs = {
      card: createRef<HTMLDivElement>(),
      header: createRef<HTMLDivElement>(),
      title: createRef<HTMLHeadingElement>(),
      description: createRef<HTMLParagraphElement>(),
      content: createRef<HTMLDivElement>(),
      footer: createRef<HTMLDivElement>(),
    }
    render(
      <Card ref={refs.card} className="custom-card">
        <CardHeader ref={refs.header} className="custom-header">
          <CardTitle ref={refs.title} className="custom-title">
            T
          </CardTitle>
          <CardDescription ref={refs.description} className="custom-description">
            D
          </CardDescription>
        </CardHeader>
        <CardContent ref={refs.content} className="custom-content">
          C
        </CardContent>
        <CardFooter ref={refs.footer} className="custom-footer">
          F
        </CardFooter>
      </Card>
    )

    expect(refs.card.current).toHaveClass('custom-card')
    expect(refs.header.current).toHaveClass('custom-header')
    expect(refs.title.current).toHaveClass('custom-title')
    expect(refs.description.current).toHaveClass('custom-description')
    expect(refs.content.current).toHaveClass('custom-content')
    expect(refs.footer.current).toHaveClass('custom-footer')
  })
})
