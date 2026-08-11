"""Shared helpers for deterministic mock providers."""

import hashlib


def stable_seed(value: str) -> int:
    """Return a stable 32-bit integer derived from a string.

    Mock providers use this to generate deterministic, offline responses so
    tests and local development behave consistently across runs.
    """
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()
    return int(digest, 16) % (2**32)
