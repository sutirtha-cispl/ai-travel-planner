"""Tool registry: a named collection of travel tools."""

from collections.abc import Iterable

from app.tools.base import BaseTravelTool


class ToolRegistry:
    """Stores tools by name and exposes them to agents and services."""

    def __init__(self, tools: Iterable[BaseTravelTool]) -> None:
        self._tools: dict[str, BaseTravelTool] = {tool.name: tool for tool in tools}

    @property
    def all(self) -> list[BaseTravelTool]:
        return list(self._tools.values())

    @property
    def names(self) -> list[str]:
        return list(self._tools.keys())

    def get(self, name: str) -> BaseTravelTool | None:
        return self._tools.get(name)

    def __len__(self) -> int:
        return len(self._tools)
