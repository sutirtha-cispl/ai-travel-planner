"""Chat endpoint.

Foundation placeholder only. AI agent integration is intentionally not
implemented yet (see Sprint 2). The route delegates to the chat service.
"""

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatService().send_message(request)
