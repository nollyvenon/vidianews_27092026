import { useState } from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

function ControlledTabs({ onChange }: { onChange?: (value: string) => void }) {
  const [value, setValue] = useState('overview')
  return (
    <Tabs
      value={value}
      onValueChange={(next) => {
        setValue(next)
        onChange?.(next)
      }}
    >
      <TabsList>
        <TabsTrigger value="overview">Overview</TabsTrigger>
        <TabsTrigger value="security">Security</TabsTrigger>
      </TabsList>
      <TabsContent value="overview">Overview panel</TabsContent>
      <TabsContent value="security">Security panel</TabsContent>
    </Tabs>
  )
}

describe('Tabs', () => {
  it('shows only the content for the active tab', () => {
    render(<ControlledTabs />)
    expect(screen.getByText('Overview panel')).toBeInTheDocument()
    expect(screen.queryByText('Security panel')).not.toBeInTheDocument()
  })

  it('switches content and reports the change when another tab is clicked', () => {
    const onChange = jest.fn()
    render(<ControlledTabs onChange={onChange} />)
    fireEvent.click(screen.getByRole('tab', { name: 'Security' }))
    expect(screen.getByText('Security panel')).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: 'Security' })).toHaveAttribute('aria-selected', 'true')
    expect(onChange).toHaveBeenCalledWith('security')
  })

  it('uses defaultValue for uncontrolled tabs', () => {
    render(
      <Tabs defaultValue="b">
        <TabsList>
          <TabsTrigger value="a">A</TabsTrigger>
          <TabsTrigger value="b">B</TabsTrigger>
        </TabsList>
        <TabsContent value="a">Panel A</TabsContent>
        <TabsContent value="b">Panel B</TabsContent>
      </Tabs>,
    )
    expect(screen.getByText('Panel B')).toBeInTheDocument()
  })

  it('throws when a trigger is rendered outside Tabs', () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})
    expect(() => render(<TabsTrigger value="x">X</TabsTrigger>)).toThrow('within <Tabs>')
    consoleError.mockRestore()
  })
})
