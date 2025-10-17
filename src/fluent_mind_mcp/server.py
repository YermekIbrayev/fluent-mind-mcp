"""MCP server entry point for Fluent Mind Flowise integration.

This module defines the FastMCP server with 9 MCP tools for managing
Flowise chatflows. Currently implements:
- US1 (P1): Read and execute operations (list, get, run)
- US2 (P2): Create new chatflows
- US3 (P3): Update chatflows (update, deploy, delete)
- US4 (P4): Generate AgentFlow V2 from descriptions
- US5 (P5): Connect nodes with automatic beautiful layout

WHY: Provides MCP protocol interface for AI assistants to interact with Flowise.
"""

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

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
from fluent_mind_mcp.models.chatflow import ChatflowType
from fluent_mind_mcp.models.config import FlowiseConfig
from fluent_mind_mcp.services.chatflow_service import ChatflowService
from fluent_mind_mcp.utils.layout import apply_hierarchical_layout


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


def _chatflow_to_dict(chatflow: Any, include_flow_data: bool = True, test_mode: bool = False) -> dict[str, Any]:
    """Convert Chatflow model to dictionary for JSON serialization.

    WHY: Centralizes chatflow serialization logic to eliminate duplication
    across all 8 MCP tools and test wrappers. Ensures consistent field naming.

    Args:
        chatflow: Chatflow Pydantic model
        include_flow_data: Whether to include flowData field (default: True)
        test_mode: If True, include both snake_case and camelCase for test compatibility (default: False)

    Returns:
        Dictionary with chatflow fields ready for JSON serialization
    """
    result = {
        "id": chatflow.id,
        "name": chatflow.name,
        "type": chatflow.type.value if hasattr(chatflow.type, 'value') else chatflow.type,
        "deployed": chatflow.deployed,
        "createdDate": chatflow.created_date.isoformat() if chatflow.created_date else None,
        "updatedDate": chatflow.updated_date.isoformat() if chatflow.updated_date else None,
    }

    if include_flow_data:
        result["flowData"] = chatflow.flow_data
        result["isPublic"] = chatflow.is_public
        result["chatbotConfig"] = chatflow.chatbot_config
        result["apiConfig"] = chatflow.api_config

    # Add snake_case aliases for test compatibility
    if test_mode:
        if include_flow_data:
            result["flow_data"] = chatflow.flow_data
        result["created_date"] = chatflow.created_date.isoformat() if chatflow.created_date else None
        result["updated_date"] = chatflow.updated_date.isoformat() if chatflow.updated_date else None

    return result


def _translate_error(error: Exception) -> dict[str, Any]:
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
async def server_lifespan(_server: FastMCP) -> AsyncIterator[ServerContext]:
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
async def list_chatflows() -> dict[str, Any]:
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
                _chatflow_to_dict(cf, include_flow_data=False)
                for cf in chatflows
            ]
        }

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def get_chatflow(chatflow_id: str) -> dict[str, Any]:
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
        return _chatflow_to_dict(chatflow, include_flow_data=True)

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def run_prediction(chatflow_id: str, question: str) -> dict[str, Any]:
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


@mcp.tool()
async def create_chatflow(
    name: str,
    flow_data: str,
    type: str = "CHATFLOW",
    deployed: bool = False
) -> dict[str, Any]:
    """Create a new Flowise chatflow from flowData structure.

    Creates a new chatflow in Flowise with the specified name and workflow
    structure. The flowData must be a valid JSON string with nodes and edges.

    Args:
        name: Display name for the chatflow (required, non-empty)
        flow_data: JSON string containing workflow nodes and edges (required)
        type: Chatflow type - "CHATFLOW" or "AGENTFLOW" (default: "CHATFLOW")
        deployed: Whether to deploy the chatflow immediately (default: False)

    Returns:
        Created chatflow object with assigned ID and metadata

    Raises:
        ValidationError: Invalid name, flowData structure, or size exceeds 1MB
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key
        RateLimitError: Too many requests

    Performance: ≤10 seconds (SC-003)

    Example:
        flow_data = json.dumps({
            "nodes": [{"id": "node-1", "type": "llm", "data": {}}],
            "edges": []
        })
        result = await create_chatflow(
            name="My Assistant",
            flow_data=flow_data,
            type="CHATFLOW",
            deployed=False
        )
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Convert string type to ChatflowType enum
        chatflow_type = ChatflowType(type)

        # Service layer handles validation, logging, and orchestration
        chatflow = await server_context.service.create_chatflow(
            name=name,
            flow_data=flow_data,
            type=chatflow_type,
            deployed=deployed
        )

        # Convert Pydantic model to dict
        return _chatflow_to_dict(chatflow, include_flow_data=True)

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def update_chatflow(
    chatflow_id: str,
    name: str | None = None,
    flow_data: str | None = None,
    deployed: bool | None = None
) -> dict[str, Any]:
    """Update an existing Flowise chatflow's properties.

    WHY: Allows AI assistants to modify chatflow properties (name, structure,
    deployment) without recreating the entire chatflow. Supports partial
    updates for flexibility and efficiency.

    Updates one or more properties of an existing chatflow. At least one
    optional parameter must be provided. Can be used to rename, modify
    workflow structure, or change deployment status.

    Args:
        chatflow_id: Unique chatflow identifier (required, non-empty)
        name: New display name for the chatflow (optional)
        flow_data: New JSON string containing workflow nodes and edges (optional)
        deployed: New deployment status - True or False (optional)

    Returns:
        Updated chatflow object with new field values

    Raises:
        NotFoundError: Chatflow ID doesn't exist
        ValidationError: Invalid chatflow_id, no fields provided, or invalid field values
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key
        RateLimitError: Too many requests

    Performance: ≤10 seconds (similar to create)

    Example:
        # Update just the name
        result = await update_chatflow(
            chatflow_id="abc-123-def",
            name="My Updated Assistant"
        )

        # Toggle deployment
        result = await update_chatflow(
            chatflow_id="abc-123-def",
            deployed=True
        )

        # Update multiple fields
        result = await update_chatflow(
            chatflow_id="abc-123-def",
            name="New Name",
            deployed=True
        )
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Service layer handles validation, logging, and orchestration
        chatflow = await server_context.service.update_chatflow(
            chatflow_id=chatflow_id,
            name=name,
            flow_data=flow_data,
            deployed=deployed
        )

        # Convert Pydantic model to dict
        return _chatflow_to_dict(chatflow, include_flow_data=True)

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def deploy_chatflow(
    chatflow_id: str,
    deployed: bool
) -> dict[str, Any]:
    """Toggle chatflow deployment status (deploy or undeploy).

    WHY: Provides a focused, user-friendly method for the common operation
    of toggling deployment. Simplifies the API by not requiring users to
    understand update_chatflow's multi-field structure for this single-purpose task.

    Convenience method for changing only the deployment status of a chatflow
    without modifying other properties. Wraps update_chatflow with only the
    deployed field.

    Args:
        chatflow_id: Unique chatflow identifier (required, non-empty)
        deployed: True to deploy the chatflow, False to undeploy it

    Returns:
        Updated chatflow object with new deployment status

    Raises:
        NotFoundError: Chatflow ID doesn't exist
        ValidationError: Invalid chatflow_id format
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key

    Performance: ≤10 seconds (similar to update)

    Example:
        # Deploy a chatflow
        result = await deploy_chatflow(
            chatflow_id="abc-123-def",
            deployed=True
        )

        # Undeploy a chatflow
        result = await deploy_chatflow(
            chatflow_id="abc-123-def",
            deployed=False
        )
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Service layer handles validation, logging, and orchestration
        # deploy_chatflow is a convenience wrapper around update_chatflow
        chatflow = await server_context.service.deploy_chatflow(
            chatflow_id=chatflow_id,
            deployed=deployed
        )

        # Convert Pydantic model to dict
        return _chatflow_to_dict(chatflow, include_flow_data=True)

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def delete_chatflow(chatflow_id: str) -> dict[str, Any]:
    """Permanently delete a Flowise chatflow.

    WHY: Enables AI assistants to maintain clean workspace and manage resource
    usage by removing chatflows that are no longer needed. Supports workspace
    hygiene and efficient resource management.

    Deletes the specified chatflow permanently from Flowise. This operation
    cannot be undone. The chatflow will be removed from the list and will
    no longer be accessible.

    Args:
        chatflow_id: Unique chatflow identifier (required, non-empty)

    Returns:
        Confirmation message with deleted chatflow ID

    Raises:
        NotFoundError: Chatflow doesn't exist
        ValidationError: Invalid chatflow_id format
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key
        RateLimitError: Too many requests

    Performance: ≤5 seconds (similar to other operations)

    Example:
        # Delete a test chatflow
        result = await delete_chatflow(
            chatflow_id="abc-123-def"
        )
        # Returns: {"success": True, "message": "Chatflow abc-123-def deleted successfully"}
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Service layer handles validation, logging, and orchestration
        await server_context.service.delete_chatflow(chatflow_id)

        # Return success confirmation
        return {
            "success": True,
            "message": f"Chatflow {chatflow_id} deleted successfully",
            "chatflow_id": chatflow_id
        }

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def generate_agentflow_v2(description: str) -> dict[str, Any]:
    """Generate AgentFlow V2 structure from natural language description.

    WHY: Enables AI assistants to create complex agent workflows from natural
    language, significantly lowering the technical barrier to agent creation.
    Leverages Flowise's built-in generation capabilities.

    Generates a complete AgentFlow V2 flowData structure from a natural language
    description of the desired agent. The generated structure includes nodes and
    edges ready to be used with create_chatflow. Supports vague descriptions by
    generating reasonable defaults.

    Args:
        description: Natural language description of desired agent (min 10 chars)

    Returns:
        Dictionary containing:
            - flowData: JSON string with generated nodes and edges structure
            - name: Generated chatflow name suggestion
            - description: Generated chatflow description (optional)

    Raises:
        ValidationError: Description too short (<10 chars) or invalid
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key
        RateLimitError: Too many requests

    Performance: ≤10 seconds (generation can take time)

    Example:
        # Generate research agent
        result = await generate_agentflow_v2(
            description="Create a research agent that searches the web and summarizes findings"
        )
        # Returns: {"flowData": "...", "name": "Research Agent", "description": "..."}

        # Create chatflow from generated structure
        chatflow = await create_chatflow(
            name=result["name"],
            flow_data=result["flowData"],
            type="AGENTFLOW",
            deployed=True
        )
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Service layer handles validation (min 10 chars), logging, and orchestration
        result = await server_context.service.generate_agentflow_v2(description)

        # Return generated structure directly (already a dict from client)
        return result

    except Exception as e:
        # Translate exception to user-friendly error
        error_response = _translate_error(e)
        raise RuntimeError(f"{error_response['error']}: {error_response['message']}")


@mcp.tool()
async def connect_nodes(
    chatflow_id: str,
    source_node_id: str,
    target_node_id: str,
    auto_layout: bool = True
) -> dict[str, Any]:
    """Connect two nodes in a Flowise chatflow with automatic beautiful layout.

    WHY: Enables programmatic flow construction by connecting nodes and automatically
    positioning them to avoid overlaps. Creates professional-looking diagrams without
    manual positioning in the UI.

    Connects a source node's output to a target node's input by creating an edge.
    Automatically finds compatible output/input anchors and creates the connection.
    Optionally applies hierarchical layout to position all nodes beautifully.

    Args:
        chatflow_id: Unique chatflow identifier (required, non-empty)
        source_node_id: ID of node providing output (required, non-empty)
        target_node_id: ID of node receiving input (required, non-empty)
        auto_layout: Apply automatic layout to prevent overlaps (default: True)

    Returns:
        Updated chatflow with new edge and repositioned nodes

    Raises:
        NotFoundError: Chatflow or nodes don't exist
        ValidationError: Incompatible node types or no matching anchors
        ConnectionError: Flowise API unreachable
        AuthenticationError: Invalid API key

    Performance: ≤10 seconds

    Example:
        # Connect LLM output to Agent input
        result = await connect_nodes(
            chatflow_id="abc-123",
            source_node_id="chatOpenAI_0",
            target_node_id="agent_1",
            auto_layout=True
        )
        # Returns: Updated chatflow with new edge and beautified layout
    """
    try:
        if server_context is None:
            raise RuntimeError("Service not initialized")

        # Fetch current chatflow
        chatflow = await server_context.service.get_chatflow(chatflow_id)

        # Parse flowData
        flow_data = json.loads(chatflow.flow_data)
        nodes = flow_data.get("nodes", [])
        edges = flow_data.get("edges", [])

        # Find source and target nodes
        source_node = next((n for n in nodes if n["id"] == source_node_id), None)
        target_node = next((n for n in nodes if n["id"] == target_node_id), None)

        if not source_node:
            raise ValidationError(f"Source node '{source_node_id}' not found in chatflow")
        if not target_node:
            raise ValidationError(f"Target node '{target_node_id}' not found in chatflow")

        # Find compatible output/input anchors
        source_outputs = source_node.get("data", {}).get("outputAnchors", [])
        target_inputs = target_node.get("data", {}).get("inputAnchors", [])

        if not source_outputs:
            raise ValidationError(f"Source node '{source_node_id}' has no output anchors")
        if not target_inputs:
            raise ValidationError(f"Target node '{target_node_id}' has no input anchors")

        # Find type-compatible anchors
        source_anchor = None
        target_anchor = None

        # Try to match anchors by type compatibility
        for s_anchor in source_outputs:
            # Get source types (e.g., "ChatOpenAI | BaseChatModel | BaseLanguageModel")
            s_types = s_anchor.get("type", "").split(" | ")
            s_types = [t.strip() for t in s_types]

            for t_anchor in target_inputs:
                # Get target type (e.g., "BaseChatModel")
                t_type = t_anchor.get("type", "")

                # Check if any source type matches target type
                if t_type in s_types:
                    source_anchor = s_anchor
                    target_anchor = t_anchor
                    break

            if source_anchor:
                break

        # Fallback: use first anchors if no type match found
        if not source_anchor:
            source_anchor = source_outputs[0]
            target_anchor = target_inputs[0]

        # Create edge
        edge_id = f"{source_node_id}-{source_anchor['id']}-{target_node_id}-{target_anchor['id']}"

        # Check if edge already exists
        existing_edge = next((e for e in edges if e["id"] == edge_id), None)
        if existing_edge:
            raise ValidationError(
                f"Edge already exists between '{source_node_id}' and '{target_node_id}'"
            )

        new_edge = {
            "id": edge_id,
            "source": source_node_id,
            "sourceHandle": source_anchor["id"],
            "target": target_node_id,
            "targetHandle": target_anchor["id"],
            "type": "buttonedge"
        }

        edges.append(new_edge)

        # Apply auto-layout if requested
        if auto_layout:
            nodes = apply_hierarchical_layout(nodes, edges)

        # Update flowData
        flow_data["nodes"] = nodes
        flow_data["edges"] = edges
        updated_flow_data = json.dumps(flow_data)

        # Update chatflow
        updated_chatflow = await server_context.service.update_chatflow(
            chatflow_id=chatflow_id,
            flow_data=updated_flow_data
        )

        # Return updated chatflow with connection info
        return {
            **_chatflow_to_dict(updated_chatflow, include_flow_data=True),
            "connection": {
                "source": source_node_id,
                "target": target_node_id,
                "edge_id": edge_id,
                "auto_layout_applied": auto_layout
            }
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
        self._service: ChatflowService | None = None

    @property
    def client(self) -> FlowiseClient:
        """Get or create FlowiseClient."""
        return self._client

    @client.setter
    def client(self, value: FlowiseClient) -> None:
        """Set FlowiseClient and recreate service."""
        self._client = value
        self._service = None  # Force service recreation with new client

    @property
    def service(self) -> ChatflowService:
        """Get or create ChatflowService with current client."""
        if self._service is None:
            self._service = ChatflowService(client=self._client, logger=self.logger)
        assert self._service is not None  # Help mypy understand the type
        return self._service

    async def list_chatflows(self) -> list[dict[str, Any]]:
        """List all chatflows - test wrapper.

        Returns:
            List of chatflow dicts
        """
        chatflows = await self.service.list_chatflows()
        return [_chatflow_to_dict(cf, include_flow_data=False, test_mode=True) for cf in chatflows]

    async def get_chatflow(self, chatflow_id: str) -> dict[str, Any]:
        """Get chatflow by ID - test wrapper.

        Args:
            chatflow_id: Chatflow identifier

        Returns:
            Chatflow dict with details
        """
        chatflow = await self.service.get_chatflow(chatflow_id)
        return _chatflow_to_dict(chatflow, include_flow_data=True, test_mode=True)

    async def run_prediction(self, chatflow_id: str, question: str) -> dict[str, Any]:
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

    async def create_chatflow(
        self,
        name: str,
        flow_data: str,
        type: ChatflowType = ChatflowType.CHATFLOW,
        deployed: bool = False
    ) -> dict[str, Any]:
        """Create new chatflow - test wrapper.

        Args:
            name: Chatflow name
            flow_data: JSON string with nodes and edges
            type: Chatflow type (default: CHATFLOW)
            deployed: Whether to deploy (default: False)

        Returns:
            Created chatflow dict
        """
        chatflow = await self.service.create_chatflow(
            name=name,
            flow_data=flow_data,
            type=type,
            deployed=deployed
        )
        return _chatflow_to_dict(chatflow, include_flow_data=True, test_mode=True)

    async def update_chatflow(
        self,
        chatflow_id: str,
        name: str | None = None,
        flow_data: str | None = None,
        deployed: bool | None = None
    ) -> dict[str, Any]:
        """Update existing chatflow - test wrapper.

        WHY: Provides direct access to update_chatflow functionality for
        acceptance tests without FastMCP's tool layer overhead.

        Args:
            chatflow_id: Chatflow identifier (required)
            name: New chatflow name (optional)
            flow_data: New JSON string with nodes and edges (optional)
            deployed: New deployment status (optional)

        Returns:
            Updated chatflow dict
        """
        chatflow = await self.service.update_chatflow(
            chatflow_id=chatflow_id,
            name=name,
            flow_data=flow_data,
            deployed=deployed
        )
        return _chatflow_to_dict(chatflow, include_flow_data=True, test_mode=True)

    async def deploy_chatflow(self, chatflow_id: str, deployed: bool) -> dict[str, Any]:
        """Toggle chatflow deployment - test wrapper.

        WHY: Provides direct access to deploy_chatflow functionality for
        acceptance tests without FastMCP's tool layer overhead.

        Args:
            chatflow_id: Chatflow identifier (required)
            deployed: True to deploy, False to undeploy

        Returns:
            Updated chatflow dict
        """
        chatflow = await self.service.deploy_chatflow(
            chatflow_id=chatflow_id,
            deployed=deployed
        )
        return _chatflow_to_dict(chatflow, include_flow_data=True, test_mode=True)

    async def delete_chatflow(self, chatflow_id: str) -> None:
        """Delete chatflow permanently - test wrapper.

        WHY: Provides direct access to delete_chatflow functionality for
        acceptance tests without FastMCP's tool layer overhead.

        Args:
            chatflow_id: Chatflow identifier (required)

        Returns:
            None on successful deletion
        """
        await self.service.delete_chatflow(chatflow_id)
        return None

    async def generate_agentflow_v2(self, description: str) -> dict[str, object]:
        """Generate AgentFlow V2 from description - test wrapper.

        WHY: Provides direct access to generate_agentflow_v2 functionality for
        acceptance tests without FastMCP's tool layer overhead.

        Args:
            description: Natural language description of desired agent (min 10 chars)

        Returns:
            Dictionary with flowData, name, and optional description
        """
        result = await self.service.generate_agentflow_v2(description)
        # Return result directly (already a dict)
        return result

    async def connect_nodes(
        self,
        chatflow_id: str,
        source_node_id: str,
        target_node_id: str,
        auto_layout: bool = True
    ) -> dict[str, Any]:
        """Connect two nodes with auto-layout - test wrapper.

        WHY: Provides direct access to connect_nodes functionality for
        acceptance tests without FastMCP's tool layer overhead.

        Args:
            chatflow_id: Unique chatflow identifier
            source_node_id: ID of node providing output
            target_node_id: ID of node receiving input
            auto_layout: Apply automatic layout (default: True)

        Returns:
            Updated chatflow dict with new edge and connection info
        """
        # Fetch current chatflow
        chatflow = await self.service.get_chatflow(chatflow_id)

        # Parse flowData
        flow_data = json.loads(chatflow.flow_data)
        nodes = flow_data.get("nodes", [])
        edges = flow_data.get("edges", [])

        # Find source and target nodes
        source_node = next((n for n in nodes if n["id"] == source_node_id), None)
        target_node = next((n for n in nodes if n["id"] == target_node_id), None)

        if not source_node:
            raise ValidationError(f"Source node '{source_node_id}' not found in chatflow")
        if not target_node:
            raise ValidationError(f"Target node '{target_node_id}' not found in chatflow")

        # Find compatible output/input anchors
        source_outputs = source_node.get("data", {}).get("outputAnchors", [])
        target_inputs = target_node.get("data", {}).get("inputAnchors", [])

        if not source_outputs:
            raise ValidationError(f"Source node '{source_node_id}' has no output anchors")
        if not target_inputs:
            raise ValidationError(f"Target node '{target_node_id}' has no input anchors")

        # Find type-compatible anchors
        source_anchor = None
        target_anchor = None

        # Try to match anchors by type compatibility
        for s_anchor in source_outputs:
            # Get source types (e.g., "ChatOpenAI | BaseChatModel | BaseLanguageModel")
            s_types = s_anchor.get("type", "").split(" | ")
            s_types = [t.strip() for t in s_types]

            for t_anchor in target_inputs:
                # Get target type (e.g., "BaseChatModel")
                t_type = t_anchor.get("type", "")

                # Check if any source type matches target type
                if t_type in s_types:
                    source_anchor = s_anchor
                    target_anchor = t_anchor
                    break

            if source_anchor:
                break

        # Fallback: use first anchors if no type match found
        if not source_anchor:
            source_anchor = source_outputs[0]
            target_anchor = target_inputs[0]

        # Create edge
        edge_id = f"{source_node_id}-{source_anchor['id']}-{target_node_id}-{target_anchor['id']}"

        # Check if edge already exists
        existing_edge = next((e for e in edges if e["id"] == edge_id), None)
        if existing_edge:
            raise ValidationError(
                f"Edge already exists between '{source_node_id}' and '{target_node_id}'"
            )

        new_edge = {
            "id": edge_id,
            "source": source_node_id,
            "sourceHandle": source_anchor["id"],
            "target": target_node_id,
            "targetHandle": target_anchor["id"],
            "type": "buttonedge"
        }

        edges.append(new_edge)

        # Apply auto-layout if requested
        if auto_layout:
            nodes = apply_hierarchical_layout(nodes, edges)

        # Update flowData
        flow_data["nodes"] = nodes
        flow_data["edges"] = edges
        updated_flow_data = json.dumps(flow_data)

        # Update chatflow
        updated_chatflow = await self.service.update_chatflow(
            chatflow_id=chatflow_id,
            flow_data=updated_flow_data
        )

        # Return updated chatflow with connection info
        return {
            **_chatflow_to_dict(updated_chatflow, include_flow_data=True, test_mode=True),
            "connection": {
                "source": source_node_id,
                "target": target_node_id,
                "edge_id": edge_id,
                "auto_layout_applied": auto_layout
            }
        }

    async def close(self) -> None:
        """Close HTTP client connections."""
        await self.client.close()


if __name__ == "__main__":
    # Run MCP server (lifespan handles initialization and cleanup)
    mcp.run()
