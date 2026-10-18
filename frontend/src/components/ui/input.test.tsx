import { createRef } from 'react'
import { render, screen } from '@testing-library/react'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

describe('Input', () => {
  it('defaults to a text input and forwards the ref and props', () => {
    const ref = createRef<HTMLInputElement>()
    render(<Input ref={ref} placeholder="Title" className="extra" />)

    const input = screen.getByPlaceholderText('Title')
    expect(input).toHaveAttribute('type', 'text')
    expect(input).toHaveClass('extra', 'rounded-md')
    expect(ref.current).toBe(input)
  })

  it('honours an explicit input type', () => {
    render(<Input type="email" placeholder="Email" />)

    expect(screen.getByPlaceholderText('Email')).toHaveAttribute('type', 'email')
  })
})

describe('Textarea', () => {
  it('renders a textarea and forwards the ref and props', () => {
    const ref = createRef<HTMLTextAreaElement>()
    render(<Textarea ref={ref} placeholder="Notes" rows={5} className="extra" />)

    const area = screen.getByPlaceholderText('Notes')
    expect(area.tagName).toBe('TEXTAREA')
    expect(area).toHaveAttribute('rows', '5')
    expect(area).toHaveClass('extra', 'min-h-[80px]')
    expect(ref.current).toBe(area)
  })
})
