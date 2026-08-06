"""Chat endpoint.

Receives a user message and returns the AI travel plan produced by the
LangGraph workflow. The route only validates the request, calls the service,
and returns the response.
"""

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return await ChatService().send_message(request)
