import { ApiClient } from '@/lib/api-client'

type FetchMock = jest.Mock<Promise<Response>, [string, RequestInit?]>

// jsdom does not provide the Response constructor, so build the subset the client reads.
function jsonResponse(body: unknown, status = 200): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
  } as unknown as Response
}

describe('ApiClient', () => {
  let fetchMock: FetchMock

  beforeEach(() => {
    fetchMock = jest.fn() as FetchMock
    global.fetch = fetchMock as unknown as typeof fetch
    ApiClient.setToken(null)
  })

  it('sends GET requests to the API base URL and returns parsed JSON', async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ ok: true }))
    const data = await ApiClient.get('/health')
    expect(data).toEqual({ ok: true })
    expect(fetchMock.mock.calls[0][0]).toMatch(/\/health$/)
    expect(fetchMock.mock.calls[0][1]).toMatchObject({ method: 'GET' })
  })

  it('serialises POST bodies as JSON', async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ id: 1 }, 201))
    await ApiClient.post('/organizations', { name: 'Acme' })
    const init = fetchMock.mock.calls[0][1] as RequestInit
    expect(init.method).toBe('POST')
    expect(init.body).toBe(JSON.stringify({ name: 'Acme' }))
  })

  it('attaches the bearer token once one is set', async () => {
    ApiClient.setToken('abc123')
    fetchMock.mockResolvedValueOnce(jsonResponse({}))
    await ApiClient.get('/auth/me')
    const headers = (fetchMock.mock.calls[0][1] as RequestInit).headers as Record<string, string>
    expect(headers.Authorization).toBe('Bearer abc123')
  })

  it('throws the server detail message on an error response', async () => {
    fetchMock.mockResolvedValueOnce(jsonResponse({ detail: 'Tenant not found' }, 404))
    await expect(ApiClient.get('/tenants/9')).rejects.toThrow('Tenant not found')
  })

  it('falls back to the status code when the error body is not JSON', async () => {
    fetchMock.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: () => Promise.reject(new SyntaxError('Unexpected token')),
    } as unknown as Response)
    await expect(ApiClient.get('/broken')).rejects.toThrow('API Error: 500')
  })
})
