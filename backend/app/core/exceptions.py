"""Custom application exceptions."""

from typing import Any


class AppError(Exception):
    """Base class for application errors."""

    status_code: int = 500
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    message = "Resource not found."


class ValidationError(AppError):
    status_code = 400
    message = "Invalid input."


class ConflictError(AppError):
    status_code = 409
    message = "Resource already exists."


class ExternalServiceError(AppError):
    status_code = 502
    message = "External service unavailable."
