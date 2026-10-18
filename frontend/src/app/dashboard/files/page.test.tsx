import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import FilesPage from '@/app/dashboard/files/page'
import { mockFetch, reply } from '@/test-utils'

function selectFile(container: HTMLElement, file: File) {
  const input = container.querySelector('input[type="file"]') as HTMLInputElement
  fireEvent.change(input, { target: { files: [file] } })
}

const pdf = new File(['%PDF-1.4'], 'report.pdf', { type: 'application/pdf' })

describe('/dashboard/files page', () => {
  let consoleError: jest.SpyInstance

  beforeEach(() => {
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => undefined)
    localStorage.setItem('token', 'upload-token')
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  it('uploads the chosen file with the stored token and lists it with its size', async () => {
    const fetchMock = mockFetch({
      'POST /resources/files/upload': { id: 11, filename: 'report.pdf', file_size: 2097152, url: '/files/11' },
    })
    const { container } = render(<FilesPage />)

    selectFile(container, pdf)

    expect(await screen.findByRole('heading', { name: 'report.pdf' })).toBeInTheDocument()
    expect(screen.getByText('2.00 MB')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Download' })).toHaveAttribute('href', '/files/11')

    const [url, init] = fetchMock.mock.calls[0]
    expect(String(url)).toMatch(/\/api\/v1\/resources\/files\/upload$/)
    expect(init.method).toBe('POST')
    expect(init.headers).toMatchObject({ Authorization: 'Bearer upload-token' })
    expect(init.body).toBeInstanceOf(FormData)
    expect((init.body as FormData).get('file')).toBeInstanceOf(File)
  })

  it('shows progress while the upload is running', async () => {
    global.fetch = jest.fn(() => new Promise(() => undefined)) as unknown as typeof fetch
    const { container } = render(<FilesPage />)

    selectFile(container, pdf)

    expect(await screen.findByRole('button', { name: 'Uploading...' })).toBeDisabled()
  })

  it('does not list a file the server rejected', async () => {
    mockFetch({ 'POST /resources/files/upload': reply({ detail: 'Too large' }, 413) })
    const { container } = render(<FilesPage />)

    selectFile(container, pdf)

    await waitFor(() => expect(screen.getByRole('button', { name: 'Upload File' })).toBeEnabled())
    expect(screen.queryByRole('link', { name: 'Download' })).not.toBeInTheDocument()
  })

  it('ignores a change event that carries no file selection', () => {
    const fetchMock = mockFetch({})
    const { container } = render(<FilesPage />)
    const input = container.querySelector('input[type="file"]') as HTMLInputElement

    fireEvent.change(input, { target: { files: null } })

    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('logs a failed upload and re-enables the button', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('offline')) as unknown as typeof fetch
    const { container } = render(<FilesPage />)

    selectFile(container, pdf)

    await waitFor(() => expect(consoleError).toHaveBeenCalledWith('Upload failed', expect.any(Error)))
    expect(screen.getByRole('button', { name: 'Upload File' })).toBeEnabled()
  })

  it('opens the hidden file picker from the upload button', () => {
    const { container } = render(<FilesPage />)
    const input = container.querySelector('input[type="file"]') as HTMLInputElement
    const clickSpy = jest.spyOn(input, 'click')

    fireEvent.click(screen.getByRole('button', { name: 'Upload File' }))

    expect(clickSpy).toHaveBeenCalledTimes(1)
  })
})
