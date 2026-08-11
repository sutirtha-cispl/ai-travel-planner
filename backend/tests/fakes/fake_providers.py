"""Fake providers that simulate upstream tool failures, timeouts, and
malformed responses. These never contact an external service."""

import asyncio

from app.tools.base import TravelProvider


class BoomProvider(TravelProvider):
    """Raises an internal exception to simulate an upstream provider failure.

    The message contains a fake secret to verify that sensitive internals are
    never surfaced to tool callers.
    """

    async def execute(self, request):
        raise RuntimeError("upstream boom: api_key=supersecret-internal-detail")


class SlowProvider(TravelProvider):
    """Sleeps longer than the tool timeout to trigger timeout handling."""

    def __init__(self, delay: float = 0.2) -> None:
        self._delay = delay

    async def execute(self, request):
        await asyncio.sleep(self._delay)
        raise AssertionError("provider should have been cancelled by the timeout")


class MalformedProvider(TravelProvider):
    """Returns a response that does not match the output schema."""

    async def execute(self, request):
        return {"options": "not-a-list", "provider": "broken"}
