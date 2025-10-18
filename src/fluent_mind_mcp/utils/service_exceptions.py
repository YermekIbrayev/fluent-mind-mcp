"""
Service-specific exceptions for external dependencies.

Provides exception classes for circuit breaker, API clients,
vector database, and embedding operations.
"""

from typing import Optional

from .base_exceptions import ChatflowAutomationError


class CircuitOpenError(ChatflowAutomationError):
    """
    Circuit breaker is open for dependency.

    Raised when operation cannot proceed because circuit breaker
    is open due to repeated failures of external dependency.
    """

    def __init__(
        self,
        dependency: str,
        failure_count: int = 0,
        timeout_seconds: int = 300,
        details: Optional[dict] = None,
    ):
        """
        Initialize circuit open error.

        Args:
            dependency: Name of failing dependency
            failure_count: Number of consecutive failures
            timeout_seconds: Time before retry attempt
            details: Additional context
        """
        message = (
            f"Circuit breaker open for {dependency}. "
            f"Retry in {timeout_seconds}s"
        )

        error_details = details or {}
        error_details.update({
            "dependency": dependency,
            "failure_count": failure_count,
            "timeout_seconds": timeout_seconds,
        })

        super().__init__(
            message=message,
            error_code="CIRCUIT_OPEN",
            details=error_details,
        )


class FlowiseApiError(ChatflowAutomationError):
    """
    Flowise API operation failed.

    Raised when Flowise HTTP API calls fail due to:
    - Connection errors
    - Authentication failures
    - Invalid requests
    - Server errors
    """

    def __init__(
        self,
        message: str = "Flowise API error",
        status_code: Optional[int] = None,
        endpoint: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize Flowise API error.

        Args:
            message: Error description
            status_code: HTTP status code if available
            endpoint: API endpoint that failed
            details: Additional context
        """
        error_details = details or {}
        if status_code:
            error_details["status_code"] = status_code
        if endpoint:
            error_details["endpoint"] = endpoint

        super().__init__(
            message=message,
            error_code="FLOWISE_API_ERROR",
            details=error_details,
        )


class VectorDatabaseError(ChatflowAutomationError):
    """
    ChromaDB vector database operation failed.

    Raised when ChromaDB operations fail due to:
    - Connection errors
    - Collection not found
    - Invalid operations
    - Persistence errors
    """

    def __init__(
        self,
        message: str = "Vector database error",
        collection: Optional[str] = None,
        operation: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize vector database error.

        Args:
            message: Error description
            collection: Collection name if applicable
            operation: Operation that failed (query, add, update, delete)
            details: Additional context
        """
        error_details = details or {}
        if collection:
            error_details["collection"] = collection
        if operation:
            error_details["operation"] = operation

        super().__init__(
            message=message,
            error_code="VECTOR_DB_ERROR",
            details=error_details,
        )


class EmbeddingError(ChatflowAutomationError):
    """
    Embedding generation failed.

    Raised when sentence-transformers embedding generation fails due to:
    - Model loading errors
    - Invalid input text
    - Memory errors
    - Computation failures
    """

    def __init__(
        self,
        message: str = "Embedding generation failed",
        text: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize embedding error.

        Args:
            message: Error description
            text: Text that failed to embed (truncated for privacy)
            details: Additional context
        """
        error_details = details or {}
        if text:
            # Truncate text for logging (avoid exposing full content)
            error_details["text_preview"] = text[:100] + ("..." if len(text) > 100 else "")

        super().__init__(
            message=message,
            error_code="EMBEDDING_ERROR",
            details=error_details,
        )
