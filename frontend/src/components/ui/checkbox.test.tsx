import { render, screen, fireEvent } from '@testing-library/react'
import { Checkbox } from '@/components/ui/checkbox'

describe('Checkbox', () => {
  it('reports the new checked state through onCheckedChange', () => {
    const onCheckedChange = jest.fn()
    render(<Checkbox aria-label="Grammar" checked={false} onCheckedChange={onCheckedChange} />)
    fireEvent.click(screen.getByRole('checkbox', { name: 'Grammar' }))
    expect(onCheckedChange).toHaveBeenCalledWith(true)
  })

  it('renders as a native checkbox with the given checked state', () => {
    render(<Checkbox aria-label="Style" checked readOnly />)
    expect(screen.getByRole('checkbox', { name: 'Style' })).toBeChecked()
  })
})
