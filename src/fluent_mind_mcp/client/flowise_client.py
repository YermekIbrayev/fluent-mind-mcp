"""HTTP client for Flowise API communication.

This module provides the FlowiseClient class for making async HTTP requests
to the Flowise API with connection pooling and error handling.
"""

import asyncio
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

import httpx

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConflictError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from fluent_mind_mcp.models import Chatflow, FlowiseConfig, PredictionResponse

if TYPE_CHECKING:
    from fluent_mind_mcp.models.chatflow import ChatflowType


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

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object) -> None:
        """Exit async context manager and close client.

        WHY: Automatic cleanup when exiting context.
        """
        await self.close()

    async def _retry_on_conflict(self, operation_func: Callable[..., Awaitable[Any]], *args: object, **kwargs: object) -> Any:
        """Retry operation once on 409 conflict with 0.5s delay.

        WHY: Concurrent modifications can cause 409 conflicts. A single retry
             with brief delay usually resolves the conflict as the competing
             operation completes.

        Args:
            operation_func: Async function to execute
            *args, **kwargs: Arguments to pass to operation_func

        Returns:
            Result from operation_func

        Raises:
            ConflictError: If conflict persists after retry
            Other exceptions: Propagated unchanged
        """
        try:
            return await operation_func(*args, **kwargs)
        except ConflictError:
            # Wait 0.5s and retry once
            await asyncio.sleep(0.5)
            # If second attempt also fails, let exception propagate
            return await operation_func(*args, **kwargs)

    def _handle_http_exceptions(self, operation: str, chatflow_id: str | None = None) -> None:
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

        # Check for TimeoutException and all its subclasses (ConnectTimeout, ReadTimeout, WriteTimeout, PoolTimeout)
        if exc_type is not None and issubclass(exc_type, httpx.TimeoutException):
            details: dict[str, object] = {"timeout": self.config.timeout}
            if chatflow_id:
                details["chatflow_id"] = chatflow_id
            raise ConnectionError(
                f"Timeout while {operation.replace('_', ' ')}: {str(exc_value)}",
                details=details,
            )
        elif exc_type is not None and issubclass(exc_type, httpx.ConnectError):
            raise ConnectionError(
                f"Cannot connect to Flowise at {self.base_url}: {str(exc_value)}",
                details={"base_url": self.base_url},
            )
        elif exc_type is not None and (issubclass(exc_type, httpx.HTTPError) or issubclass(exc_type, httpx.NetworkError)):
            details2: dict[str, object] = {"error_type": exc_type.__name__}
            if chatflow_id:
                details2["chatflow_id"] = chatflow_id
            raise ConnectionError(
                f"Network error while {operation.replace('_', ' ')}: {str(exc_value)}",
                details=details2,
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
            ConflictError: On 409 status (concurrent modification)
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
        elif response.status_code == 409:
            raise ConflictError(
                f"Concurrent modification conflict for {operation}",
                details={"status_code": 409, "operation": operation},
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

    async def list_chatflows(self) -> list[Chatflow]:
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
            raise  # This line will never be reached but satisfies mypy

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
            raise  # This line will never be reached but satisfies mypy

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
            raise  # This line will never be reached but satisfies mypy

    async def create_chatflow(
        self,
        name: str,
        flow_data: str,
        type: "ChatflowType | None" = None,
        deployed: bool = False
    ) -> Chatflow:
        """Create new chatflow in Flowise instance.

        WHY: Allows AI assistants to programmatically create new chatflows
             from flowData structures.

        Args:
            name: Chatflow display name
            flow_data: JSON string containing nodes and edges structure
            type: Chatflow type (defaults to CHATFLOW if not provided)
            deployed: Whether chatflow should be deployed (defaults to False)

        Returns:
            Chatflow object with assigned ID and metadata

        Raises:
            ValidationError: Invalid flowData structure (malformed JSON, missing fields, >1MB)
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
            RateLimitError: Too many requests
        """
        # Validate flowData early (edge cases 3 & 4)
        from fluent_mind_mcp.utils.validators import FlowDataValidator
        validator = FlowDataValidator()
        is_valid, error_message, _ = validator.validate(flow_data)
        if not is_valid:
            raise ValidationError(
                f"Invalid flowData: {error_message}",
                details={"operation": "create_chatflow", "field": "flow_data"}
            )

        try:
            # Import ChatflowType here to avoid circular import
            from fluent_mind_mcp.models.chatflow import ChatflowType as CT

            # Use default type if not provided
            if type is None:
                type = CT.CHATFLOW

            # Build request body
            request_body = {
                "name": name,
                "flowData": flow_data,
                "type": type.value if hasattr(type, 'value') else str(type),
                "deployed": deployed
            }

            response = await self._client.post("/chatflows", json=request_body)

            # Flowise returns 201 for successful creation
            if response.status_code not in (200, 201):
                self._handle_error(response, "create_chatflow")

            chatflow_data = response.json()
            return Chatflow(**chatflow_data)

        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            self._handle_http_exceptions("create_chatflow")
            raise  # This line will never be reached but satisfies mypy

    async def update_chatflow(
        self,
        chatflow_id: str,
        name: str | None = None,
        flow_data: str | None = None,
        deployed: bool | None = None
    ) -> Chatflow:
        """Update existing chatflow with optional fields.

        WHY: Allows AI assistants to modify chatflow properties and toggle
             deployment status without recreating the entire chatflow.

        NOTE: Automatically retries once on 409 conflict after 0.5s delay.

        Args:
            chatflow_id: Chatflow to update (required)
            name: New chatflow name (optional)
            flow_data: New JSON string containing nodes and edges (optional)
            deployed: New deployment status (optional)

        Returns:
            Chatflow object with updated fields

        Raises:
            NotFoundError: Chatflow doesn't exist
            ValidationError: Invalid field values, no fields provided, or invalid flowData
            ConflictError: Concurrent modification conflict (after retry)
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
            RateLimitError: Too many requests
        """
        # Validate flowData if provided (edge cases 3 & 4)
        if flow_data is not None:
            from fluent_mind_mcp.utils.validators import FlowDataValidator
            validator = FlowDataValidator()
            is_valid, error_message, _ = validator.validate(flow_data)
            if not is_valid:
                raise ValidationError(
                    f"Invalid flowData: {error_message}",
                    details={"operation": "update_chatflow", "field": "flow_data", "chatflow_id": chatflow_id}
                )

        async def _do_update() -> Chatflow:
            try:
                # Build request body with only provided fields
                request_body: dict[str, object] = {}
                if name is not None:
                    request_body["name"] = name
                if flow_data is not None:
                    request_body["flowData"] = flow_data
                if deployed is not None:
                    request_body["deployed"] = deployed

                # Validate at least one field is provided (done at service layer)
                # Client just sends the request

                response = await self._client.put(f"/chatflows/{chatflow_id}", json=request_body)

                # Flowise returns 200 for successful update
                if response.status_code != 200:
                    self._handle_error(response, "update_chatflow")

                chatflow_data = response.json()
                return Chatflow(**chatflow_data)

            except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
                self._handle_http_exceptions("update_chatflow", chatflow_id)
                raise  # This line will never be reached but satisfies mypy

        # Wrap with retry logic for 409 conflicts
        result = await self._retry_on_conflict(_do_update)
        return result  # type: ignore[no-any-return]

    async def delete_chatflow(self, chatflow_id: str) -> None:
        """Delete existing chatflow permanently.

        WHY: Allows AI assistants to remove chatflows that are no longer needed,
             maintaining clean workspace and managing resource usage.

        NOTE: Automatically retries once on 409 conflict after 0.5s delay.

        Args:
            chatflow_id: Chatflow to delete (required)

        Returns:
            None on successful deletion

        Raises:
            NotFoundError: Chatflow doesn't exist
            ConflictError: Concurrent modification conflict (after retry)
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
            RateLimitError: Too many requests
        """
        async def _do_delete() -> None:
            try:
                response = await self._client.delete(f"/chatflows/{chatflow_id}")

                # Flowise may return 200 or 204 for successful deletion
                if response.status_code not in (200, 204):
                    self._handle_error(response, "delete_chatflow")

                # Successful deletion returns None
                return None

            except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
                self._handle_http_exceptions("delete_chatflow", chatflow_id)
                raise  # This line will never be reached but satisfies mypy

        # Wrap with retry logic for 409 conflicts
        await self._retry_on_conflict(_do_delete)

    async def generate_agentflow_v2(self, description: str) -> dict[str, object]:
        """Generate AgentFlow V2 structure from natural language description.

        WHY: Enables AI assistants to create complex agent workflows from natural
             language, significantly lowering the technical barrier to agent creation.
             Leverages Flowise's built-in generation capabilities.

        Args:
            description: Natural language description of desired agent (min 10 chars)

        Returns:
            Dictionary containing:
                - flowData: JSON string with generated nodes and edges structure
                - name: Generated chatflow name
                - description: Generated chatflow description (optional)

        Raises:
            ValidationError: Description too short or invalid
            AuthenticationError: Invalid API key
            ConnectionError: Network/timeout issues
            RateLimitError: Too many requests
        """
        try:
            response = await self._client.post(
                "/agentflowv2-generator/generate",
                json={"description": description}
            )

            # Flowise returns 200 for successful generation
            if response.status_code != 200:
                self._handle_error(response, "generate_agentflow_v2")

            generation_data: dict[str, Any] = response.json()
            return dict(generation_data)

        except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError, httpx.NetworkError):
            self._handle_http_exceptions("generate_agentflow_v2")
            raise  # This line will never be reached but satisfies mypy
