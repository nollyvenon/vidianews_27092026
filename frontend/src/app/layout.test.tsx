import { render, screen } from '@testing-library/react'
import RootLayout, { metadata } from '@/app/layout'
import AuthLayout from '@/app/auth/layout'
import { Providers } from '@/components/providers'

describe('root layout', () => {
  it('declares English metadata for the app', () => {
    expect(metadata.title).toBe('VidiaNews - AI-Powered Video Platform')
    expect(metadata.description).toMatch(/video management/i)
  })

  it('wraps every page in the document shell and the shared providers', () => {
    const child = <p>page content</p>
    const tree = RootLayout({ children: child }) as React.ReactElement<{ lang: string; children: React.ReactElement }>

    expect(tree.type).toBe('html')
    expect(tree.props.lang).toBe('en')

    const body = tree.props.children as React.ReactElement<{ children: React.ReactElement }>
    expect(body.type).toBe('body')
    const providers = body.props.children as React.ReactElement<{ children: React.ReactNode }>
    expect(providers.type).toBe(Providers)
    expect(providers.props.children).toBe(child)
  })
})

describe('auth layout', () => {
  it('renders the auth pages without adding chrome', () => {
    render(<AuthLayout>{<span>sign in form</span>}</AuthLayout>)

    expect(screen.getByText('sign in form')).toBeInTheDocument()
  })
})
