import '@testing-library/jest-dom'

// Next.js App Router hooks only exist inside a running Next app. Replace them with
// stable mocks so every page test shares one router object that tests can assert on.
const mockRouter = {
  push: jest.fn(),
  replace: jest.fn(),
  back: jest.fn(),
  forward: jest.fn(),
  refresh: jest.fn(),
  prefetch: jest.fn(),
}

jest.mock('next/navigation', () => ({
  useRouter: () => mockRouter,
  usePathname: jest.fn(() => '/dashboard'),
  useParams: jest.fn(() => ({})),
  useSearchParams: jest.fn(() => new URLSearchParams()),
  redirect: jest.fn(),
  notFound: jest.fn(),
}))

// Each test starts with empty mock call history; implementations set by the setup survive.
beforeEach(() => {
  jest.clearAllMocks()
  window.localStorage.clear()
})

// jsdom does not implement these browser APIs, which several dashboard components call.
if (!Element.prototype.scrollIntoView) {
  Element.prototype.scrollIntoView = jest.fn()
}
if (!global.URL.createObjectURL) {
  global.URL.createObjectURL = jest.fn(() => 'blob:mock-object-url')
}
if (!global.URL.revokeObjectURL) {
  global.URL.revokeObjectURL = jest.fn()
}
