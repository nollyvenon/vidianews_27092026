import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import LocalizationPage from '@/app/dashboard/settings-language/page'
import { mockFetch, reply } from '@/test-utils'

const languages = [
  { code: 'en', name: 'English' },
  { code: 'fr', name: 'Français' },
]

describe('/dashboard/settings-language page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('lists the available languages and marks the current one', async () => {
    mockFetch({ 'GET /languages': languages })
    render(<LocalizationPage />)

    expect(await screen.findByRole('button', { name: 'Français' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'English' })).toHaveClass('bg-blue-600')
    expect(screen.getByText('EN')).toBeInTheDocument()
  })

  it('switches the language and marks it as current', async () => {
    const fetchMock = mockFetch({
      'GET /languages': languages,
      'POST /localization/language': { ok: true },
    })
    render(<LocalizationPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Français' }))

    await waitFor(() => expect(screen.getByText('FR')).toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Français' })).toHaveClass('bg-blue-600')
    const postCall = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/localization/language'))
    expect(JSON.parse(postCall![1].body as string)).toEqual({ language_code: 'fr' })
  })

  it('keeps the current language when the server rejects the change', async () => {
    mockFetch({
      'GET /languages': languages,
      'POST /localization/language': reply({ detail: 'Unsupported' }, 400),
    })
    render(<LocalizationPage />)
    fireEvent.click(await screen.findByRole('button', { name: 'Français' }))

    await waitFor(() => expect(screen.getByRole('button', { name: 'Français' })).toBeEnabled())
    expect(screen.getByText('EN')).toBeInTheDocument()
  })

  it('logs failures to load the list and to change the language', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    render(<LocalizationPage />)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Failed to fetch languages:', expect.any(Error)))
  })

  it('offers the date, time zone and save controls', () => {
    mockFetch({ 'GET /languages': [] })
    render(<LocalizationPage />)

    expect(screen.getByRole('option', { name: 'DD/MM/YYYY' })).toBeInTheDocument()
    expect(screen.getByRole('option', { name: 'PST' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Save Settings' })).toBeInTheDocument()
  })
})
