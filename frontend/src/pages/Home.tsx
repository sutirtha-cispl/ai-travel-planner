import { useHealth } from '../hooks/useHealth'

export default function Home() {
  const { status, loading, error } = useHealth()

  return (
    <section>
      <h1 className="text-3xl font-bold">Plan your next trip with AI</h1>
      <p className="mt-2 text-slate-600">
        AI Travel Planner helps you research destinations, compare travel
        options, and build personalized itineraries.
      </p>

      <div className="mt-8 rounded-lg border border-slate-200 bg-white p-4">
        <h2 className="font-semibold">Backend status</h2>
        <p className="mt-1 text-sm text-slate-600">
          {loading && 'Checking backend connection...'}
          {error && `Backend unreachable: ${error}`}
          {status && `Backend is ${status.status}`}
        </p>
      </div>

      <a
        href="/planner"
        className="mt-6 inline-block rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
      >
        Open AI Planner
      </a>
    </section>
  )
}
