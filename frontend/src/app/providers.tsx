import type { ReactNode } from 'react'

interface ProvidersProps {
  children: ReactNode
}

/**
 * App-wide providers. Reserved for global providers such as React Query,
 * Zustand store hydration, and theme providers added in later sprints.
 */
export function Providers({ children }: ProvidersProps) {
  return <>{children}</>
}
