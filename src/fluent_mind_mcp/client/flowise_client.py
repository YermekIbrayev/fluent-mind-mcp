"""HTTP client for Flowise API communication.

This module provides the FlowiseClient class for making async HTTP requests
to the Flowise API with connection pooling and error handling.
"""

from typing import List, Optional

import httpx

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from fluent_mind_mcp.models import Chatflow, FlowiseConfig, PredictionResponse


class FlowiseClient:
    """Async HTTP client for Flowise API operations.

    Handles all HTTP communication with Flowise instance including:
    - Connection pooling for performance
    - Authentication with API key
    - Error translation from HTTP to domain exceptions
    - Request/response serialization

    Attributes:
        config: FlowiseConfig with API URL and credentials
        base_url: Base API URL for Flowise endpoints
        _client: Internal httpx.AsyncClient for HTTP operations
    """

    def __init__(self, config: FlowiseConfig) -> None:
        """Initialize FlowiseClient with configuration.

        Args:
            config: FlowiseConfig with API URL, key, timeout, etc.
        """
        self.config = config
        self.base_url = f"{str(config.api_url).rstrip('/')}/api/v1"

        # Build headers with authentication
        headers = {"Content-Type": "application/json"}
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"

        # Create async client with connection pooling
        # WHY: Optimized for 5-10 concurrent AI assistants (NFR-005)
        #      Keep-alive set to half of max to balance connection reuse and resource usage
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=config.timeout,
            limits=httpx.Limits(
                max_connections=config.max_connections,
                max_keepalive_connections=max(1, config.max_connections // 2),
            ),
        )

    async def close(self) -> None:
        """Close the HTTP client and release connections.

        WHY: Proper cleanup of connection pool resources.
        """
        await self._client.aclose()

    async def __aenter__(self) -> "FlowiseClient":
        """Enter async context manager.

        WHY: Allows using FlowiseClient with async with statement.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager and close client.

        WHY: Automatic cleanup when exiting context.
        """
        await self.close()

    def _handle_http_exceptions(self, operation: str, chatflow_id: str = None) -> None:
        """Handle common httpx exceptions and translate to domain exceptions.

        WHY: Centralized exception handling reduces code duplication and ensures
             consistent error messages across all API operations.

        Args:
            operation: Operation name for error context (e.g., "list_chatflows")
            chatflow_id: Optional chatflow ID for operations on specific chatflows

        This method should be called in an except block to handle httpx exceptions.
        """
        import sys
        exc_type, exc_value, _ = sys.exc_info()

        if exc_type == httpx.TimeoutException:
            details = {"timeout": self.config.timeout}
            if chatflow_id:
                details["chatflow_id"] = chatflow_id
            raise ConnectionError(
                f"Timeout while {operation.replace('_', ' ')}: {str(exc_value)}",
                details=details,
            )
        elif exc_type == httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to Flowise at {self.base_url}: {str(exc_value)}",
                details={"base_url": self.base_url},
            )
        elif exc_type in (httpx.HTTPError, httpx.NetworkError):
            details = {"error_type": exc_type.__name__}
            if chatflow_id:
                details["chatflow_id"] = chatflow_id
            raise ConnectionError(
                f"Network error while {operation.replace('_', ' ')}: {str(exc_value)}",
                details=details,
            )
        else:
            # Re-raise if not an httpx exception we handle
            raise

    def _handle_error(self, response: httpx.Response, operation: str) -> None:
        """Translate HTTP errors to domain exceptions.

        WHY: Provides consistent error handling across all operations.
             Flowise returns 500 for non-existent resources, so we check response body.

        Args:
            response: HTTP response that may contain error
            operation: Operation name for error context

        Raises:
            AuthenticationError: On 401 status
            NotFoundError: On 404 status or 500 with not-found indicators
            RateLimitError: On 429 status
            ValidationError: On 400 status
            ConnectionError: On other errors
        """
        if response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed for {operation}: Invalid API key",
                details={"status_code": 401, "operation": operation},
            )
        elif response.status_code == 404:
            raise NotFoundError(
                f"Resource not found for {operation}",
                details={"status_code": 404, "operation": operation},
            )
        elif response.status_code == 500:
            # Flowise returns 500 for non-existent resources
            # Check if error message indicates "not found"
            try:
                error_data = response.json()
                # Check both the entire response and the 'message' field specifically
                error_message = str(error_data).lower()
                if isinstance(error_data, dict) and "message" in error_data:
                    error_message = error_data["message"].lower()

                if "not found" in error_message or "does not exist" in error_message:
                    raise NotFoundError(
                        f"Resource not found for {operation}",
                        details={"status_code": 500, "operation": operation, "error": error_data},
                    )
            except NotFoundError:
                # Re-raise NotFoundError
                raise
            except Exception:
                # If we can't parse response, fall through to generic error
                pass

            raise ConnectionError(
                f"HTTP {response.status_code} error for {operation}",
                details={"status_code": response.status_code, "operation": operation},
            )
        elif response.status_code == 429:
            raise RateLimitError(
                f"Rate limit exceeded for {operation}",
                details={"status_code": 429, "operation": operation},
            )
        elif response.status_code == 400:
            raise ValidationError(
                f"Invalid request for {operation}",
                details={"status_code": 400, "operation": operation},
            )
        else:
            raise ConnectionError(
                f"HTTP {response.status_code} error for {operation}",
                details={"status_code": response.status_code, "operation": operation},
            )

    async def list_chatflows(self) -> List[Chatflow]:
        """List all chatflows from Flowise instance.

        WHY: Provides discovery of available chatflows for execution.

        Returns:
            List of Chatflow objects with metadata

        Raises:
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
            RateLimitError: Too many requests
        """
        try:
            response = await self._client.get("/chatflows")

            if response.status_code != 200:
                self._handle_error(response, "list_chatflows")

            chatflows_data = response.json()
            return [Chatflow(**chatflow) for chatflow in chatflows_data]

        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            self._handle_http_exceptions("list_chatflows")

    async def get_chatflow(self, chatflow_id: str) -> Chatflow:
        """Get detailed chatflow by ID including flowData.

        WHY: Retrieves complete chatflow information for inspection/editing.

        Args:
            chatflow_id: Unique chatflow identifier

        Returns:
            Chatflow object with complete details

        Raises:
            NotFoundError: Chatflow doesn't exist
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
        """
        try:
            response = await self._client.get(f"/chatflows/{chatflow_id}")

            if response.status_code != 200:
                self._handle_error(response, "get_chatflow")

            chatflow_data = response.json()
            return Chatflow(**chatflow_data)

        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            self._handle_http_exceptions("get_chatflow", chatflow_id)

    async def run_prediction(self, chatflow_id: str, question: str) -> PredictionResponse:
        """Execute chatflow with user input.

        WHY: Runs chatflow to generate response for user question.

        Args:
            chatflow_id: Chatflow to execute
            question: User input/question

        Returns:
            PredictionResponse with chatflow output

        Raises:
            NotFoundError: Chatflow doesn't exist
            ValidationError: Invalid input
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
        """
        try:
            response = await self._client.post(
                f"/prediction/{chatflow_id}", json={"question": question}
            )

            if response.status_code != 200:
                self._handle_error(response, "run_prediction")

            prediction_data = response.json()
            return PredictionResponse(**prediction_data)

        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            self._handle_http_exceptions("run_prediction", chatflow_id)
