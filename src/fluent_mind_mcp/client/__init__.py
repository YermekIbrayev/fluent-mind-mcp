"""Flowise API client and related utilities.

WHY: Provides async HTTP client for all Flowise API operations with connection pooling,
     retry logic, and domain-specific exception handling.

This package contains:
- FlowiseClient: Async HTTP client for Flowise API operations
- Exception hierarchy: Domain-specific exceptions for error handling and translation

Exports:
- FlowiseClient: Main client for Flowise API communication
- FlowiseClientError: Base exception for all client errors
- ConnectionError: Network/timeout errors
- AuthenticationError: Invalid/missing API key errors
- ValidationError: Invalid input data errors
- NotFoundError: Resource not found errors
- RateLimitError: Too many requests errors
"""

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConnectionError,
    FlowiseClientError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from fluent_mind_mcp.client.flowise_client import FlowiseClient

__all__ = [
    "FlowiseClient",
    "FlowiseClientError",
    "ConnectionError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
]
