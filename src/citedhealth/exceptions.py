"""Exceptions for the CITED Health API client."""

from __future__ import annotations


class CitedHealthError(Exception):
    """Base exception for all CITED Health client errors."""


class NotFoundError(CitedHealthError):
    """Raised when a resource is not found (404)."""

    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}")


class RateLimitError(CitedHealthError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(self, retry_after: int = 0) -> None:
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds.")
