"""Base classes for travel tools.

Every travel tool exposes a LangChain tool interface (name, description,
args_schema) and delegates execution to a provider through a small protocol:

    Agent -> LangChain Tool -> Provider -> External API / Mock Provider

The base class enforces:

- Pydantic input validation,
- Pydantic output validation (malformed provider responses fail safely),
- a per-tool timeout,
- user-safe error messages (never expose internal exceptions or keys).

Mock providers live in ``app.tools.mocks``. Real providers can be swapped in
later without changing agents, the graph, or the tool schemas.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any

from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, PrivateAttr, ValidationError

logger = logging.getLogger(__name__)


class TravelProvider(ABC):
    """Provider interface implemented by mock and future real data providers."""

    @abstractmethod
    async def execute(self, request: BaseModel) -> BaseModel:
        """Fetch and return a typed result for the given request."""


class BaseTravelTool(BaseTool, ABC):
    """LangChain tool wrapper around a travel provider.

    Subclasses declare ``name``, ``description``, ``args_schema``, and the
    concrete input/output schema models. The provider is injected at runtime
    so the tool layer is decoupled from the data source.
    """

    _provider: Any = PrivateAttr()
    _timeout_seconds: float = PrivateAttr(default=10.0)

    input_schema_model: type[BaseModel]
    output_schema_model: type[BaseModel]

    def __init__(
        self,
        provider: TravelProvider,
        timeout_seconds: float = 10.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._provider = provider
        self._timeout_seconds = timeout_seconds

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        raise ToolException(f"{self.name} only supports asynchronous execution.")

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        request = self._validate_input(dict(kwargs))
        output = await self._call_provider(request)
        return self._serialize_output(output)

    def _validate_input(self, kwargs: dict[str, Any]) -> BaseModel:
        schema = self.args_schema
        try:
            return schema(**kwargs)
        except ValidationError as exc:
            detail = "; ".join(
                f"{'.'.join(str(loc) for loc in error['loc'])}: {error['msg']}"
                for error in exc.errors()
            )
            raise ToolException(f"Invalid input for {self.name}: {detail}") from exc

    async def _call_provider(self, request: BaseModel) -> BaseModel:
        try:
            return await asyncio.wait_for(
                self._provider.execute(request),
                timeout=self._timeout_seconds,
            )
        except TimeoutError as exc:
            logger.warning(
                "Tool '%s' timed out after %.1fs", self.name, self._timeout_seconds
            )
            raise ToolException(
                f"{self.name} timed out after {self._timeout_seconds:.0f} seconds. "
                "Please try again later."
            ) from exc
        except ToolException:
            raise
        except Exception as exc:
            logger.error("Tool '%s' provider failed: %s", self.name, exc, exc_info=True)
            raise ToolException(
                f"{self.name} is temporarily unavailable. Please try again later."
            ) from exc

    def _serialize_output(self, output: BaseModel) -> dict[str, Any]:
        output_model = self.output_schema_model
        if output_model is not None and not isinstance(output, output_model):
            if isinstance(output, dict):
                try:
                    output = output_model(**output)
                except ValidationError as exc:
                    logger.error(
                        "Tool '%s' returned a malformed response: %s",
                        self.name,
                        exc,
                    )
                    raise ToolException(
                        f"{self.name} returned a malformed response."
                    ) from exc
            else:
                logger.error(
                    "Tool '%s' returned an unexpected type: %s",
                    self.name,
                    type(output).__name__,
                )
                raise ToolException(f"{self.name} returned a malformed response.")
        return output.model_dump(mode="json")
