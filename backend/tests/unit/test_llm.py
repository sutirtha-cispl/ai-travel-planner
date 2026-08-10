"""Tests for the centralized LLM provider factory."""

import pytest
from langchain_openai import ChatOpenAI

from app.config.llm import get_llm
from app.core.exceptions import ExternalServiceError


def test_get_llm_returns_chat_openai_for_openai_provider(monkeypatch):
    monkeypatch.setattr("app.config.settings.settings.LLM_PROVIDER", "openai")
    monkeypatch.setattr(
        "app.config.settings.settings.MODEL_NAME", "llama-3.3-70b-versatile"
    )
    monkeypatch.setattr("app.config.settings.settings.OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(
        "app.config.settings.settings.OPENAI_BASE_URL",
        "https://api.groq.com/openai/v1",
    )

    llm = get_llm()

    assert isinstance(llm, ChatOpenAI)
    assert llm.model_name == "llama-3.3-70b-versatile"
    assert llm.openai_api_key.get_secret_value() == "test-key"
    assert llm.openai_api_base == "https://api.groq.com/openai/v1"


def test_get_llm_accepts_empty_base_url(monkeypatch):
    monkeypatch.setattr("app.config.settings.settings.LLM_PROVIDER", "openai")
    monkeypatch.setattr("app.config.settings.settings.OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("app.config.settings.settings.OPENAI_BASE_URL", "")

    llm = get_llm()

    assert isinstance(llm, ChatOpenAI)
    assert llm.openai_api_base is None


def test_get_llm_raises_when_api_key_missing(monkeypatch):
    monkeypatch.setattr("app.config.settings.settings.LLM_PROVIDER", "openai")
    monkeypatch.setattr("app.config.settings.settings.OPENAI_API_KEY", "")

    with pytest.raises(ExternalServiceError):
        get_llm()


def test_get_llm_raises_for_unsupported_provider(monkeypatch):
    monkeypatch.setattr("app.config.settings.settings.LLM_PROVIDER", "not-a-provider")
    monkeypatch.setattr("app.config.settings.settings.OPENAI_API_KEY", "test-key")

    with pytest.raises(ExternalServiceError):
        get_llm()