import ChatWindow from '../features/chat/ChatWindow'

export default function Planner() {
  return (
    <section className="flex h-[70vh] flex-col">
      <h1 className="text-2xl font-bold">AI Travel Planner</h1>
      <p className="mt-1 text-sm text-slate-600">
        Ask for travel recommendations. Specialized AI agents arrive in a
        later sprint.
      </p>
      <ChatWindow />
    </section>
  )
}
