import type { ChatRequest, ChatResponse } from '../types/chat'
import { request } from './api'

export async function getHealth(): Promise<{ status: string }> {
  return request<{ status: string }>('/health')
}

export async function sendMessage(payload: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>('/chat', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}
