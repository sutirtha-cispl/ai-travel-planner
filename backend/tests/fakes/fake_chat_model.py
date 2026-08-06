"""Fake chat model used in agent and graph tests.

`GenericFakeChatModel` does not implement `with_structured_output`, which the
agents use in production. This fake overrides `bind_tools` so that the real
`with_structured_output` path works and exercises genuine Pydantic validation.
"""

import json
from collections.abc import Iterable
from typing import Any

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class FakeStructuredChatModel(BaseChatModel):
    """Returns a scripted JSON tool call per invocation.

    Each dict in ``responses`` is returned as the arguments of a synthetic
    tool call named after the bound schema, mirroring OpenAI function calling.
    """

    def __init__(self, responses: Iterable[dict[str, Any]]) -> None:
        super().__init__()
        self._responses = iter(responses)
        self._tool_name = "Tool"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        data = next(self._responses)
        message = AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": [
                    {
                        "id": "call_fake_1",
                        "type": "function",
                        "function": {
                            "name": self._tool_name,
                            "arguments": json.dumps(data),
                        },
                    }
                ]
            },
        )
        return ChatResult(generations=[ChatGeneration(message=message)])

    def bind_tools(self, tools: list[Any], **kwargs: Any) -> "FakeStructuredChatModel":
        if tools:
            schema = tools[0]
            config = getattr(schema, "model_config", None) or {}
            self._tool_name = config.get("title") or schema.__name__
        return self

    @property
    def _llm_type(self) -> str:
        return "fake-structured"
