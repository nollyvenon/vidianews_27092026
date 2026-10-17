import { render, screen } from '@testing-library/react'
import { Progress } from '@/components/ui/progress'

function barWidth(container: HTMLElement): string {
  const bar = container.querySelector('[role="progressbar"] > div') as HTMLElement
  return bar.style.width
}

describe('Progress', () => {
  it('exposes the value to assistive technology', () => {
    render(<Progress value={40} />)
    const bar = screen.getByRole('progressbar')
    expect(bar).toHaveAttribute('aria-valuenow', '40')
    expect(bar).toHaveAttribute('aria-valuemax', '100')
  })

  it('fills the bar in proportion to the value', () => {
    const { container } = render(<Progress value={72.5} />)
    expect(barWidth(container)).toBe('72.5%')
  })

  it('clamps values above the maximum and below zero', () => {
    const { container, rerender } = render(<Progress value={250} />)
    expect(barWidth(container)).toBe('100%')
    rerender(<Progress value={-5} />)
    expect(barWidth(container)).toBe('0%')
  })

  it('treats a missing value as zero', () => {
    const { container } = render(<Progress value={null} />)
    expect(barWidth(container)).toBe('0%')
  })

  it('scales against a custom maximum', () => {
    const { container } = render(<Progress value={5} max={20} />)
    expect(barWidth(container)).toBe('25%')
  })
})
