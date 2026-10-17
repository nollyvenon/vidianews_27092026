/**
 * Turns an API failure into a message that is safe to render.
 *
 * The backend answers errors in two shapes: plain `{ detail: "text" }` (HTTPException) and
 * `{ detail: { success, error: { code, message } } }` (APIException). Anything else falls
 * back to the caller's message, so an object is never passed to React as a child.
 */

export function messageFromDetail(detail: unknown): string | null {
  if (typeof detail === 'string' && detail.trim()) return detail
  if (detail && typeof detail === 'object') {
    const shaped = detail as { error?: { message?: unknown }; message?: unknown }
    if (typeof shaped.error?.message === 'string' && shaped.error.message) return shaped.error.message
    if (typeof shaped.message === 'string' && shaped.message) return shaped.message
  }
  return null
}

/**
 * An error raised by the API client for a non-2xx response. Its message is the server's own
 * detail, so it is safe to show. Other errors (network failures, programming errors) are not.
 */
export class ApiError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ApiError'
  }
}

/** Message for an error thrown by the API client, the axios client, or anything else. */
export function errorMessage(error: unknown, fallback: string): string {
  if (error && typeof error === 'object' && 'response' in error) {
    const response = (error as { response?: { data?: { detail?: unknown } } }).response
    const fromResponse = messageFromDetail(response?.data?.detail)
    if (fromResponse) return fromResponse
  }
  if (error instanceof ApiError && error.message) return error.message
  return fallback
}
