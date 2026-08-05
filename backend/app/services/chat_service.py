"""Chat service.

Foundation placeholder only. The AI pipeline (LangGraph -> agents -> LLM)
is intentionally not implemented yet and will be added in later sprints.
"""

from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def send_message(self, request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            response=f"Received: {request.message} | AI planning is not enabled yet."
        )
