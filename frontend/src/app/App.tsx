import { Link, Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <nav className="mx-auto flex max-w-4xl items-center justify-between">
          <Link to="/" className="text-lg font-semibold">
            AI Travel Planner
          </Link>
          <div className="flex gap-4">
            <Link to="/" className="text-sm hover:underline">
              Home
            </Link>
            <Link to="/planner" className="text-sm hover:underline">
              Planner
            </Link>
          </div>
        </nav>
      </header>
      <main className="mx-auto max-w-4xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  )
}
