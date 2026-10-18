import { act, fireEvent, render, screen } from '@testing-library/react'
import { Toaster } from '@/components/toaster'
import { toast } from '@/hooks/use-toast'

describe('Toaster', () => {
  it('renders nothing when there are no notifications', () => {
    const { container } = render(<Toaster />)

    expect(container).toBeEmptyDOMElement()
  })

  it('shows a notification with its title and description', () => {
    render(<Toaster />)

    let created: ReturnType<typeof toast> | undefined
    act(() => {
      created = toast({ title: 'Saved', description: 'Your changes are live' })
    })

    expect(screen.getByRole('status')).toHaveTextContent('Saved')
    expect(screen.getByText('Your changes are live')).toBeInTheDocument()
    act(() => created?.dismiss())
  })

  it('styles destructive notifications differently from default ones', () => {
    render(<Toaster />)

    let failed: ReturnType<typeof toast> | undefined
    let info: ReturnType<typeof toast> | undefined
    act(() => {
      failed = toast({ title: 'Failed', variant: 'destructive' })
      info = toast({ title: 'Info' })
    })

    const [failedNode, infoNode] = screen.getAllByRole('status')
    expect(failedNode).toHaveClass('bg-red-50')
    expect(infoNode).toHaveClass('bg-white')
    act(() => {
      failed?.dismiss()
      info?.dismiss()
    })
  })

  it('removes a notification when its dismiss button is pressed', () => {
    render(<Toaster />)

    let created: ReturnType<typeof toast> | undefined
    act(() => {
      created = toast({ title: 'Temporary' })
    })
    fireEvent.click(screen.getByRole('button', { name: 'Dismiss notification' }))

    expect(screen.queryByText('Temporary')).not.toBeInTheDocument()
    act(() => created?.dismiss())
  })

  it('omits the title and description elements when they are not provided', () => {
    render(<Toaster />)

    let created: ReturnType<typeof toast> | undefined
    act(() => {
      created = toast({})
    })

    const notification = screen.getByRole('status')
    expect(notification.querySelector('p')).toBeNull()
    act(() => created?.dismiss())
  })
})
