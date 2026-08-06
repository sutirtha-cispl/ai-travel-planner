"""Reusable base class for all AI agents.

An agent is a single-responsibility LangChain chain that:
- reads from the shared travel state,
- runs a prompt against the LLM,
- validates the output against a Pydantic schema,
- returns a partial state update for the keys it owns.

The LLM is resolved lazily so that building the graph never fails when
OPENAI_API_KEY is not configured; failures are caught and reported as a
"failed" status instead of crashing the workflow.
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from app.config.llm import get_llm

logger = logging.getLogger(__name__)

STATUS_FAILED = "failed"


class BaseAgent(ABC):
    """Abstract agent that executes a prompt + LLM chain against a state dict."""

    name: str = "base_agent"
    output_schema: type[BaseModel] | None = None

    def __init__(self, llm: BaseChatModel | None = None) -> None:
        self.llm = llm
        self._chain: Runnable | None = None

    @property
    @abstractmethod
    def prompt_template(self) -> ChatPromptTemplate:
        """ChatPromptTemplate used to build the agent chain."""

    @abstractmethod
    def _prompt_input(self, state: dict[str, Any]) -> dict[str, Any]:
        """Build the variable map passed to the prompt template."""

    @abstractmethod
    def _state_update(self, state: dict[str, Any], output: Any) -> dict[str, Any]:
        """Map the validated agent output to the state keys it owns."""

    def _build_chain(self) -> Runnable:
        llm = self.llm or get_llm()
        if self.output_schema is not None:
            return self.prompt_template | llm.with_structured_output(self.output_schema)
        return self.prompt_template | llm

    def _ensure_chain(self) -> Runnable:
        if self._chain is None:
            self._chain = self._build_chain()
        return self._chain

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Run the agent and return a partial state update."""
        started = time.perf_counter()
        try:
            output = await self._ensure_chain().ainvoke(self._prompt_input(state))
            update = self._state_update(state, output)
            logger.info(
                "Agent '%s' executed successfully in %.3fs",
                self.name,
                time.perf_counter() - started,
            )
            return update
        except Exception as exc:
            logger.error(
                "Agent '%s' failed in %.3fs: %s",
                self.name,
                time.perf_counter() - started,
                exc,
                exc_info=True,
            )
            return {"status": STATUS_FAILED, "error": f"{self.name} failed: {exc}"}
