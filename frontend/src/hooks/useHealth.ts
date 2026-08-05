import { useEffect, useState } from 'react'
import { getHealth } from '../services/chat.service'

interface UseHealthResult {
  status: { status: string } | null
  loading: boolean
  error: string | null
}

export function useHealth(): UseHealthResult {
  const [status, setStatus] = useState<{ status: string } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    getHealth()
      .then((data) => {
        if (!cancelled) setStatus(data)
      })
      .catch((err: unknown) => {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Unknown error')
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [])

  return { status, loading, error }
}
