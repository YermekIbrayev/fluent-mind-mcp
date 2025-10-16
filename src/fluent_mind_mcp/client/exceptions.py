"""Custom exceptions for Flowise client operations.

This module defines the exception hierarchy for handling errors from
the Flowise API and client-side validation.
"""

from typing import Any, Dict, Optional


class FlowiseClientError(Exception):
    """Base exception for all Flowise client errors.

    All custom exceptions inherit from this base class, allowing
    callers to catch all Flowise-related errors with a single handler.

    Attributes:
        message: Human-readable error message
        details: Optional dictionary with additional error context
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize FlowiseClientError.

        Args:
            message: Error description
            details: Additional context (status_code, url, etc.)
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of error.

        WHY: Provides clean error message for logging and display.
        """
        return self.message

    def __repr__(self) -> str:
        """Return detailed representation for debugging.

        WHY: Includes class name and message for debugging.
        """
        return f"{self.__class__.__name__}('{self.message}')"


class ConnectionError(FlowiseClientError):
    """Network connection error to Flowise API.

    Raised when unable to reach the Flowise server due to:
    - Network timeout
    - Connection refused
    - DNS resolution failure
    - SSL/TLS errors
    """

    pass


class AuthenticationError(FlowiseClientError):
    """Authentication failure with Flowise API.

    Raised when:
    - API key is invalid or expired (401)
    - API key is missing when required
    - Authentication headers are malformed
    """

    pass


class ValidationError(FlowiseClientError):
    """Request validation error.

    Raised when:
    - Request data is malformed (400)
    - Required fields are missing
    - Field values are invalid
    - JSON parsing fails
    """

    pass


class NotFoundError(FlowiseClientError):
    """Resource not found error.

    Raised when:
    - Chatflow ID does not exist (404)
    - Endpoint not found
    - Resource has been deleted
    """

    pass


class RateLimitError(FlowiseClientError):
    """Rate limit exceeded error.

    Raised when:
    - Too many requests to Flowise API (429)
    - Quota exceeded
    - Throttling applied
    """

    pass
