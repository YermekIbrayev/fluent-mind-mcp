"""
Base and core exceptions for Chatflow Automation System.

Provides base exception class and search/template-related errors.
"""

from typing import Optional


class ChatflowAutomationError(Exception):
    """
    Base exception for all chatflow automation errors.

    All custom exceptions inherit from this class for consistent
    error handling and reporting.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize base exception.

        Args:
            message: User-friendly error message (<50 tokens per NFR-006)
            error_code: Optional error code for programmatic handling
            details: Optional additional context (not shown to users)
        """
        self.message = message
        self.error_code = error_code or "AUTOMATION_ERROR"
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return user-friendly error message."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ValidationError(ChatflowAutomationError):
    """
    Input validation failed.

    Raised when user input doesn't meet requirements:
    - Empty or invalid query strings
    - Out-of-range parameters
    - Malformed data structures
    """

    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize validation error.

        Args:
            message: Error description
            field: Name of field that failed validation
            details: Additional context
        """
        error_details = details or {}
        if field:
            error_details["field"] = field

        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=error_details,
        )


class VectorSearchError(ChatflowAutomationError):
    """
    Vector search operation failed.

    Raised when semantic search in ChromaDB fails due to:
    - Embedding generation errors
    - Database query failures
    - Invalid search parameters
    """

    def __init__(
        self,
        message: str = "Vector search failed",
        query: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize vector search error.

        Args:
            message: Error description
            query: Original search query (for debugging)
            details: Additional context
        """
        error_details = details or {}
        if query:
            error_details["query"] = query

        super().__init__(
            message=message,
            error_code="VECTOR_SEARCH_ERROR",
            details=error_details,
        )


class TemplateNotFoundError(ChatflowAutomationError):
    """
    Template not found in vector database.

    Raised when requested template_id doesn't exist or
    semantic search returns no template matches.
    """

    def __init__(
        self,
        template_id: Optional[str] = None,
        query: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize template not found error.

        Args:
            template_id: Template identifier that wasn't found
            query: Search query if using semantic search
            details: Additional context
        """
        if template_id:
            message = f"Template '{template_id}' not found"
        elif query:
            message = f"No templates match query: {query}"
        else:
            message = "Template not found"

        error_details = details or {}
        if template_id:
            error_details["template_id"] = template_id
        if query:
            error_details["query"] = query

        super().__init__(
            message=message,
            error_code="TEMPLATE_NOT_FOUND",
            details=error_details,
        )


class BuildFlowError(ChatflowAutomationError):
    """
    Chatflow build operation failed.

    Raised when build_flow function encounters errors:
    - Invalid node configurations
    - Connection inference failures
    - Flowise API creation errors
    """

    def __init__(
        self,
        message: str = "Failed to build chatflow",
        stage: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize build flow error.

        Args:
            message: Error description
            stage: Build stage where error occurred
            details: Additional context
        """
        error_details = details or {}
        if stage:
            error_details["stage"] = stage

        super().__init__(
            message=message,
            error_code="BUILD_FLOW_ERROR",
            details=error_details,
        )


class ConnectionInferenceError(ChatflowAutomationError):
    """
    Failed to infer connections between nodes.

    Raised when automatic connection inference fails due to:
    - Incompatible node types
    - Ambiguous connection paths
    - Missing required inputs/outputs
    """

    def __init__(
        self,
        message: str = "Cannot infer connections",
        nodes: Optional[list[str]] = None,
        details: Optional[dict] = None,
    ):
        """
        Initialize connection inference error.

        Args:
            message: Error description
            nodes: Node names involved in failed inference
            details: Additional context
        """
        error_details = details or {}
        if nodes:
            error_details["nodes"] = nodes

        super().__init__(
            message=message,
            error_code="CONNECTION_INFERENCE_ERROR",
            details=error_details,
        )
