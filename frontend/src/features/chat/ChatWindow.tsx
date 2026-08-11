import { useState } from 'react'
import type { FormEvent } from 'react'
import { sendMessage } from '../../services/chat.service'
import type { ChatMessage } from '../../types/chat'
import MarkdownMessage from '../../components/ui/MarkdownMessage'

export default function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const content = input.trim()
    if (!content) return

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: 'user',
        content,
        createdAt: new Date().toISOString(),
      },
    ])
    setInput('')
    setLoading(true)

    try {
      const { response } = await sendMessage({ message: content })
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: response,
          createdAt: new Date().toISOString(),
        },
      ])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `Error: ${error instanceof Error ? error.message : 'Request failed'}`,
          createdAt: new Date().toISOString(),
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-4 flex flex-1 flex-col">
      <div className="flex-1 overflow-y-auto rounded-lg border border-slate-200 bg-white p-4">
        {messages.length === 0 && (
          <p className="text-sm text-slate-400">Start a conversation...</p>
        )}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-3 ${message.role === 'user' ? 'text-right' : ''}`}
          >
            {message.role === 'user' ? (
              <div className="inline-block rounded-lg bg-blue-600 px-3 py-2 text-sm text-white">
                {message.content}
              </div>
            ) : (
              <div className="rounded-lg bg-slate-100 px-4 py-3">
                <MarkdownMessage content={message.content} />
              </div>
            )}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Plan a 5 day Japan trip"
          className="flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm"
          aria-label="Message"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  )
}
