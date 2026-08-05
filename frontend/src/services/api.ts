const API_BASE: string = import.meta.env.VITE_API_URL ?? '/api/v1'

export interface ApiError extends Error {
  status?: number
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
    ...init,
  })

  if (!response.ok) {
    const error = new Error(
      `Request failed: ${response.status} ${response.statusText}`,
    ) as ApiError
    error.status = response.status
    throw error
  }

  return (await response.json()) as T
}

export { API_BASE, request }
