"""Centralized LLM provider.

Builds the configured chat model used by every AI agent.
Never hardcode model names, providers, or API keys here.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.config.settings import settings
from app.core.exceptions import ExternalServiceError


def get_llm() -> BaseChatModel:
    """Return the chat model configured for the active provider.

    Raises:
        ExternalServiceError: If the provider is unsupported or no API key is set.
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai":
        if not settings.OPENAI_API_KEY:
            raise ExternalServiceError("OPENAI_API_KEY is not configured.")
        return ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0.2,
            max_tokens=2048,
        )

    raise ExternalServiceError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
