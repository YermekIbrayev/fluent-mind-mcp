"""
Custom exceptions for Chatflow Automation System.

Re-exports all exception classes from specialized sub-modules for
backwards compatibility and unified imports.

Split into:
- base_exceptions: Base class and core search/template errors
- service_exceptions: External dependency errors (API, DB, circuit breaker)
"""

# Base and core exceptions
from .base_exceptions import (
    BuildFlowError,
    ChatflowAutomationError,
    ConnectionInferenceError,
    TemplateNotFoundError,
    ValidationError,
    VectorSearchError,
)

# Service-specific exceptions
from .service_exceptions import (
    CircuitOpenError,
    EmbeddingError,
    FlowiseApiError,
    VectorDatabaseError,
)

__all__ = [
    # Base exception
    "ChatflowAutomationError",
    # Core exceptions
    "ValidationError",
    "VectorSearchError",
    "TemplateNotFoundError",
    "BuildFlowError",
    "ConnectionInferenceError",
    # Service exceptions
    "CircuitOpenError",
    "FlowiseApiError",
    "VectorDatabaseError",
    "EmbeddingError",
]
