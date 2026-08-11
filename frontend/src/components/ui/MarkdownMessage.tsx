import type { ReactNode } from 'react'

type InlineToken =
  | { type: 'text'; value: string }
  | { type: 'bold'; value: string }
  | { type: 'italic'; value: string }
  | { type: 'code'; value: string }

const INLINE_PATTERN = /\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`/g

function tokenizeInline(text: string): InlineToken[] {
  const tokens: InlineToken[] = []
  let lastIndex = 0
  let match: RegExpExecArray | null

  while ((match = INLINE_PATTERN.exec(text)) !== null) {
    if (match.index > lastIndex) {
      tokens.push({ type: 'text', value: text.slice(lastIndex, match.index) })
    }
    if (match[1] !== undefined) {
      tokens.push({ type: 'bold', value: match[1] })
    } else if (match[2] !== undefined) {
      tokens.push({ type: 'italic', value: match[2] })
    } else {
      tokens.push({ type: 'code', value: match[3] })
    }
    lastIndex = INLINE_PATTERN.lastIndex
  }

  if (lastIndex < text.length) {
    tokens.push({ type: 'text', value: text.slice(lastIndex) })
  }
  return tokens
}

function renderInline(text: string): ReactNode[] {
  return tokenizeInline(text).map((token, index) => {
    switch (token.type) {
      case 'bold':
        return (
          <strong key={index} className="font-semibold text-slate-900">
            {token.value}
          </strong>
        )
      case 'italic':
        return <em key={index}>{token.value}</em>
      case 'code':
        return (
          <code
            key={index}
            className="rounded bg-slate-200 px-1 py-0.5 font-mono text-xs"
          >
            {token.value}
          </code>
        )
      default:
        return <span key={index}>{token.value}</span>
    }
  })
}

export default function MarkdownMessage({ content }: { content: string }) {
  const elements: ReactNode[] = []
  let listItems: ReactNode[] = []
  let listKey = 0

  const flushList = () => {
    if (listItems.length === 0) return
    elements.push(
      <ul key={`list-${listKey}`} className="mt-1 list-disc space-y-1 pl-5">
        {listItems}
      </ul>,
    )
    listKey += 1
    listItems = []
  }

  content.split('\n').forEach((rawLine, index) => {
    const line = rawLine.trim()

    if (!line) {
      flushList()
      return
    }

    if (line.startsWith('## ')) {
      flushList()
      elements.push(
        <h2 key={`h2-${index}`} className="text-lg font-bold text-slate-900">
          {renderInline(line.slice(3))}
        </h2>,
      )
      return
    }

    if (line.startsWith('### ')) {
      flushList()
      elements.push(
        <h3
          key={`h3-${index}`}
          className="mt-3 text-base font-semibold text-slate-800"
        >
          {renderInline(line.slice(4))}
        </h3>,
      )
      return
    }

    if (line.startsWith('- ')) {
      listItems.push(
        <li key={`li-${index}`}>{renderInline(line.slice(2))}</li>,
      )
      return
    }

    flushList()
    elements.push(
      <p key={`p-${index}`} className="mt-1">
        {renderInline(line)}
      </p>,
    )
  })

  flushList()

  return <div className="text-sm leading-relaxed text-slate-800">{elements}</div>
}
