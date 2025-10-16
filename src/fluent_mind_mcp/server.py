"""MCP server entry point for Fluent Mind Flowise integration.

This module defines the FastMCP server with 8 MCP tools for managing
Flowise chatflows. Currently implements US1 (read and execute operations).

WHY: Provides MCP protocol interface for AI assistants to interact with Flowise.
"""

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

from mcp.server.fastmcp import FastMCP

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConnectionError,
    FlowiseClientError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.models.config import FlowiseConfig
from fluent_mind_mcp.services.chatflow_service import ChatflowService


# Server context for dependency injection
class ServerContext:
    """Container for server dependencies.

    WHY: Provides type-safe access to initialized dependencies.
    """
    def __init__(
        self,
        config: FlowiseConfig,
        client: FlowiseClient,
        service: ChatflowService,
        logger: OperationLogger
    ):
        self.config = config
        self.client = client
        self.service = service
        self.logger = logger


# Global context (initialized during lifespan)
server_context: ServerContext | None = None


def _translate_error(error: Exception) -> Dict[str, Any]:
    """Translate domain exceptions to user-friendly MCP error responses.

    WHY: Provides consistent, actionable error messages to AI assistants.
    Ensures no sensitive information (API keys, stack traces) leaks to users.

    Args:
        error: Exception from client or service layer

    Returns:
        Dictionary with error type and user-friendly message
    """
    error_type = type(error).__name__

    # Connection errors - network/timeout issues
    if isinstance(error, ConnectionError):
        return {
            "error": "ConnectionError",
            "message": f"Cannot connect to Flowise: {str(error)}",
            "details": {
                "suggestion": "Check that Flowise is running and accessible"
            }
        }

    # Authentication errors - invalid API key
    elif isinstance(error, AuthenticationError):
        return {
            "error": "AuthenticationError",
            "message": "Authentication failed: Invalid API key",
            "details": {
                "suggestion": "Check FLOWISE_API_KEY environment variable"
            }
        }

    # Not found errors - resource doesn't exist
    elif isinstance(error, NotFoundError):
        return {
            "error": "NotFoundError",
            "message": str(error),
            "details": {
                "suggestion": "Verify the chatflow ID exists (use list_chatflows to see all IDs)"
            }
        }

    # Validation errors - invalid input
    elif isinstance(error, ValidationError):
        return {
            "error": "ValidationError",
            "message": str(error),
            "details": {
                "suggestion": "Check parameter format and requirements"
            }
        }

    # Rate limit errors - too many requests
    elif isinstance(error, RateLimitError):
        return {
            "error": "RateLimitError",
            "message": "Too many requests to Flowise API",
            "details": {
                "suggestion": "Wait a moment before retrying"
            }
        }

    # Unknown Flowise client errors
    elif isinstance(error, FlowiseClientError):
        return {
            "error": "FlowiseError",
            "message": str(error),
            "details": {}
        }

    # Unexpected errors (should be rare)
    else:
        return {
            "error": "UnexpectedError",
            "message": f"Unexpected error: {error_type}",
            "details": {
                "suggestion": "Check server logs for details"
            }
        }


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[ServerContext]:
    """Manage server lifecycle with startup and shutdown logic.

    WHY: Initializes dependencies from environment on startup,
    cleans up HTTP connections on shutdown.

    Yields:
        ServerContext with initialized dependencies
    """
    global server_context

    # Startup: Initialize dependencies
    config = FlowiseConfig.from_env()
    logger = OperationLogger(name="fluent-mind-mcp", level=config.log_level)
    client = FlowiseClient(config)
    service = ChatflowService(client=client, logger=logger)

    server_context = ServerContext(
        config=config,
        client=client,
        service=service,
        logger=logger
    )

    logger.info(
        f"Server initialized: api_url={str(config.api_url)}, "
        f"timeout={config.timeout}s, "
        f"max_connections={config.max_connections}"
    )

    try:
        yield server_context
    finally:
        # Shutdown: Clean up resources
        await client.close()
        logger.info("Server shutdown: connections closed")


# Initialize FastMCP server with lifespan
mcp = FastMCP("fluent-mind-mcp", lifespan=server_lifespan)


@mcp.tool()
async def list_chatflows() -> Dict[str, Any]:
    """List all available Flowise chatflows with their metadata.

    Returns all chatflows from the connected Flowise instance including
    their ID, name, type, deployment status, and creation date.

    Returns:
        Array of chatflow objects with metadata

    Raises:
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key

    Performance: ≤5 seconds (SC-002)
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Call service layer which handles logging and orchestration
        chatflows = await server_context.service.list_chatflows()

        # Convert Pydantic models to dicts for JSON serialization
        return {
            "chatflows": [
                {
                    "id": cf.id,
                    "name": cf.name,
                    "type": cf.type.value if hasattr(cf.type, 'value') else cf.type,
                    "deployed": cf.deployed,
                    "createdDate": cf.created_date.isoformat() if cf.created_date else None,
                }
                for cf in chatflows
            ]
        }

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def get_chatflow(chatflow_id: str) -> Dict[str, Any]:
    """Get detailed chatflow information including workflow structure.

    Retrieves complete chatflow details by ID, including the flowData
    which contains the nodes and edges that make up the workflow.

    Args:
        chatflow_id: Unique chatflow identifier (required, non-empty)

    Returns:
        Chatflow object with complete details including flowData

    Raises:
        NotFoundError: Chatflow ID doesn't exist
        ValidationError: Invalid chatflow ID format
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key

    Performance: ≤5 seconds (SC-002)
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Service layer handles validation and logging
        chatflow = await server_context.service.get_chatflow(chatflow_id)

        # Convert Pydantic model to dict
        return {
            "id": chatflow.id,
            "name": chatflow.name,
            "type": chatflow.type.value if hasattr(chatflow.type, 'value') else chatflow.type,
            "deployed": chatflow.deployed,
            "flowData": chatflow.flow_data,
            "isPublic": chatflow.is_public,
            "chatbotConfig": chatflow.chatbot_config,
            "apiConfig": chatflow.api_config,
            "createdDate": chatflow.created_date.isoformat() if chatflow.created_date else None,
            "updatedDate": chatflow.updated_date.isoformat() if chatflow.updated_date else None,
        }

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def run_prediction(chatflow_id: str, question: str) -> Dict[str, Any]:
    """Execute a deployed chatflow with user input.

    Runs the specified chatflow with the provided question/input and
    returns the response. The chatflow must be deployed to execute.

    Args:
        chatflow_id: Chatflow to execute (required, non-empty)
        question: User input or question (required, non-empty)

    Returns:
        Prediction response with chatflow output text and metadata

    Raises:
        NotFoundError: Chatflow doesn't exist
        ValidationError: Invalid parameters or chatflow not deployed
        TimeoutError: Execution exceeded timeout
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key

    Performance: ≤5 seconds (SC-002)
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Service layer handles validation and logging
        response = await server_context.service.run_prediction(chatflow_id, question)

        # Convert Pydantic model to dict
        return {
            "text": response.text,
            "questionMessageId": response.question_message_id,
            "chatMessageId": response.chat_message_id,
            "sessionId": response.session_id,
        }

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


class MCPServer:
    """Test-friendly wrapper for MCP server operations.

    WHY: Provides direct method access for testing without FastMCP's tool layer.
    This allows acceptance tests to call operations directly as methods.
    """

    def __init__(self, config: FlowiseConfig, client: FlowiseClient | None = None):
        """Initialize MCP server with configuration.

        Args:
            config: FlowiseConfig with API URL and settings
            client: Optional FlowiseClient for dependency injection (testing)
        """
        self.config = config
        self.logger = OperationLogger(name="fluent-mind-mcp-test", level=config.log_level)
        self._client = client or FlowiseClient(config)
        self._service = None

    @property
    def client(self):
        """Get or create FlowiseClient."""
        return self._client

    @client.setter
    def client(self, value):
        """Set FlowiseClient and recreate service."""
        self._client = value
        self._service = None  # Force service recreation with new client

    @property
    def service(self):
        """Get or create ChatflowService with current client."""
        if self._service is None:
            self._service = ChatflowService(client=self._client, logger=self.logger)
        return self._service

    async def list_chatflows(self):
        """List all chatflows - test wrapper.

        Returns:
            List of chatflow dicts
        """
        chatflows = await self.service.list_chatflows()
        return [
            {
                "id": cf.id,
                "name": cf.name,
                "type": cf.type.value if hasattr(cf.type, 'value') else cf.type,
                "deployed": cf.deployed,
                "createdDate": cf.created_date.isoformat() if cf.created_date else None,
            }
            for cf in chatflows
        ]

    async def get_chatflow(self, chatflow_id: str):
        """Get chatflow by ID - test wrapper.

        Args:
            chatflow_id: Chatflow identifier

        Returns:
            Chatflow dict with details
        """
        chatflow = await self.service.get_chatflow(chatflow_id)
        return {
            "id": chatflow.id,
            "name": chatflow.name,
            "type": chatflow.type.value if hasattr(chatflow.type, 'value') else chatflow.type,
            "deployed": chatflow.deployed,
            "flowData": chatflow.flow_data,
            "flow_data": chatflow.flow_data,  # Both snake_case and camelCase for test compatibility
            "isPublic": chatflow.is_public,
            "chatbotConfig": chatflow.chatbot_config,
            "apiConfig": chatflow.api_config,
            "createdDate": chatflow.created_date.isoformat() if chatflow.created_date else None,
            "created_date": chatflow.created_date.isoformat() if chatflow.created_date else None,
            "updatedDate": chatflow.updated_date.isoformat() if chatflow.updated_date else None,
        }

    async def run_prediction(self, chatflow_id: str, question: str):
        """Execute chatflow - test wrapper.

        Args:
            chatflow_id: Chatflow to execute
            question: User question

        Returns:
            Prediction response dict
        """
        response = await self.service.run_prediction(chatflow_id, question)
        return {
            "text": response.text,
            "questionMessageId": response.question_message_id,
            "chatMessageId": response.chat_message_id,
            "sessionId": response.session_id,
            "session_id": response.session_id,  # Both for test compatibility
        }

    async def close(self):
        """Close HTTP client connections."""
        await self.client.close()


if __name__ == "__main__":
    # Run MCP server (lifespan handles initialization and cleanup)
    mcp.run()
