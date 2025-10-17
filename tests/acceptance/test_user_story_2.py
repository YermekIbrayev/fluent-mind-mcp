"""Acceptance tests for User Story 2: Create New Chatflows.

Tests the complete user journey from the spec:
- AC1: Create chatflow with valid name and flowData, receive ID
- AC2: Verify created chatflow appears in Flowise with correct structure
- AC3: Handle invalid flowData (malformed JSON) with validation error
- AC4: Handle Flowise API unavailability with connection error

These tests verify the full stack works together (client + service + MCP tools).
"""

import json
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from fluent_mind_mcp.client.exceptions import (
    ConnectionError,
    ValidationError,
)
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig
from fluent_mind_mcp.server import MCPServer


@pytest.fixture
def valid_flow_data_json() -> str:
    """Valid FlowData as JSON string for testing."""
    return json.dumps({
        "nodes": [
            {
                "id": "chatOpenAI_0",
                "type": "chatOpenAI",
                "data": {
                    "name": "chatOpenAI",
                    "model": "gpt-4"
                },
                "position": {"x": 100.0, "y": 100.0}
            }
        ],
        "edges": []
    })


@pytest.fixture
def mock_flowise_client(valid_flow_data_json):
    """Mock FlowiseClient that simulates Flowise API responses."""
    client = AsyncMock()

    # Track created chatflows and generate unique IDs
    created_chatflows = {}
    chatflow_counter = [0]  # Use list to allow modification in nested function

    # Mock create_chatflow to dynamically create chatflow with provided name
    def create_chatflow_side_effect(name, flow_data, type=ChatflowType.CHATFLOW, deployed=False):
        chatflow_counter[0] += 1
        chatflow_id = f"new-chatflow-abc-{chatflow_counter[0]:03d}"
        chatflow = Chatflow(
            id=chatflow_id,
            name=name,  # Use the actual name passed in
            type=type,
            deployed=deployed,
            flow_data=flow_data,
            created_date=datetime(2025, 10, 16, 15, 0, 0),
            updated_date=datetime(2025, 10, 16, 15, 0, 0),
        )
        created_chatflows[chatflow.id] = chatflow
        return chatflow

    client.create_chatflow.side_effect = create_chatflow_side_effect

    # Mock list_chatflows to return created chatflows
    def list_chatflows_side_effect():
        return list(created_chatflows.values())

    client.list_chatflows.side_effect = list_chatflows_side_effect

    # Mock get_chatflow to return the created chatflow details
    def get_chatflow_side_effect(chatflow_id):
        return created_chatflows.get(chatflow_id)

    client.get_chatflow.side_effect = get_chatflow_side_effect

    return client


@pytest.fixture
async def mcp_server(mock_flowise_client):
    """MCP Server fixture with mocked client."""
    config = FlowiseConfig(api_url="http://localhost:3000", timeout=30)
    server = MCPServer(config=config)
    # Inject mock client
    server.client = mock_flowise_client
    return server


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS2Scenario1CreateChatflow:
    """AC1: User creates chatflow with valid name and flowData, receives new ID."""

    async def test_create_chatflow_returns_new_id(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Valid chatflow name "Test Chatflow" and valid flowData structure
        WHEN: User calls create_chatflow tool
        THEN: Returns created chatflow with unique ID assigned
        """
        result = await mcp_server.create_chatflow(
            name="Test Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        # Should return created chatflow with ID
        assert "id" in result
        assert result["id"].startswith("new-chatflow-abc-")
        assert result["name"] == "Test Chatflow"
        assert result["type"] == "CHATFLOW"
        assert result["deployed"] is False

        # Verify client was called with correct parameters
        mock_flowise_client.create_chatflow.assert_called_once()
        call_kwargs = mock_flowise_client.create_chatflow.call_args.kwargs
        assert call_kwargs["name"] == "Test Chatflow"
        assert call_kwargs["flow_data"] == valid_flow_data_json

    async def test_create_chatflow_with_default_values(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Minimal parameters (name and flowData only)
        WHEN: User calls create_chatflow without specifying type or deployed
        THEN: Returns chatflow with defaults (type=CHATFLOW, deployed=False)
        """
        result = await mcp_server.create_chatflow(
            name="Minimal Chatflow",
            flow_data=valid_flow_data_json
        )

        assert result["id"] is not None
        assert result["type"] == "CHATFLOW"  # Default
        assert result["deployed"] is False  # Default

    async def test_create_chatflow_completes_within_10_seconds(
        self, mcp_server, valid_flow_data_json
    ):
        """
        GIVEN: Normal Flowise API response time
        WHEN: User calls create_chatflow
        THEN: Operation completes within 10 seconds (SC-003)
        """
        import time

        start_time = time.time()
        await mcp_server.create_chatflow(
            name="Performance Test",
            flow_data=valid_flow_data_json
        )
        duration = time.time() - start_time

        assert duration < 10.0, f"create_chatflow took {duration}s, expected <10s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS2Scenario2VerifyCreatedChatflow:
    """AC2: User verifies newly created chatflow appears in Flowise with correct structure."""

    async def test_created_chatflow_appears_in_list(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Chatflow "Test Chatflow" was just created
        WHEN: User calls list_chatflows
        THEN: Created chatflow appears in the list with correct name
        """
        # Create chatflow
        created = await mcp_server.create_chatflow(
            name="Test Chatflow",
            flow_data=valid_flow_data_json
        )
        created_id = created["id"]

        # List chatflows to verify it appears
        chatflows = await mcp_server.list_chatflows()

        # Should find the created chatflow
        found = False
        for chatflow in chatflows:
            if chatflow["id"] == created_id:
                found = True
                assert chatflow["name"] == "Test Chatflow"
                break

        assert found, f"Created chatflow {created_id} not found in list"

    async def test_created_chatflow_retrievable_with_details(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Chatflow "Test Chatflow" was just created
        WHEN: User calls get_chatflow with the new ID
        THEN: Returns complete chatflow details including flowData structure
        """
        # Create chatflow
        created = await mcp_server.create_chatflow(
            name="Test Chatflow",
            flow_data=valid_flow_data_json
        )
        created_id = created["id"]

        # Retrieve chatflow details
        details = await mcp_server.get_chatflow(chatflow_id=created_id)

        # Should return complete details with flowData
        assert details["id"] == created_id
        assert details["name"] == "Test Chatflow"
        assert "flowData" in details or "flow_data" in details

        # Verify flowData structure is correct
        flow_data = details.get("flowData") or details.get("flow_data")
        flow_dict = json.loads(flow_data) if isinstance(flow_data, str) else flow_data
        assert "nodes" in flow_dict
        assert "edges" in flow_dict
        assert len(flow_dict["nodes"]) > 0

    async def test_created_chatflow_has_correct_structure(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Chatflow created with specific flowData structure
        WHEN: User retrieves the chatflow
        THEN: Returned flowData matches what was submitted
        """
        original_flow_data = json.loads(valid_flow_data_json)

        # Create chatflow
        created = await mcp_server.create_chatflow(
            name="Structure Test",
            flow_data=valid_flow_data_json
        )

        # Retrieve and verify structure
        details = await mcp_server.get_chatflow(chatflow_id=created["id"])
        flow_data = details.get("flowData") or details.get("flow_data")
        returned_flow_data = json.loads(flow_data) if isinstance(flow_data, str) else flow_data

        # Verify nodes match
        assert len(returned_flow_data["nodes"]) == len(original_flow_data["nodes"])
        assert returned_flow_data["nodes"][0]["type"] == original_flow_data["nodes"][0]["type"]


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS2Scenario3InvalidFlowData:
    """AC3: System handles invalid flowData with appropriate validation errors."""

    async def test_create_chatflow_rejects_malformed_json(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Malformed JSON string as flowData
        WHEN: User calls create_chatflow
        THEN: Returns ValidationError with clear message
        """
        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.create_chatflow(
                name="Invalid Chatflow",
                flow_data="not valid json {{"
            )

        error_message = str(exc_info.value).lower()
        assert "json" in error_message or "invalid" in error_message

        # Should not make API call
        mock_flowise_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_rejects_missing_nodes_key(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Valid JSON but missing 'nodes' key
        WHEN: User calls create_chatflow
        THEN: Returns ValidationError indicating nodes are required
        """
        invalid_flow_data = json.dumps({"edges": []})

        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.create_chatflow(
                name="Missing Nodes",
                flow_data=invalid_flow_data
            )

        error_message = str(exc_info.value).lower()
        assert "nodes" in error_message

        mock_flowise_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_rejects_missing_edges_key(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Valid JSON but missing 'edges' key
        WHEN: User calls create_chatflow
        THEN: Returns ValidationError indicating edges are required
        """
        invalid_flow_data = json.dumps({"nodes": []})

        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.create_chatflow(
                name="Missing Edges",
                flow_data=invalid_flow_data
            )

        error_message = str(exc_info.value).lower()
        assert "edges" in error_message

        mock_flowise_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_rejects_oversized_flow_data(self, mcp_server, mock_flowise_client):
        """
        GIVEN: flowData larger than 1MB
        WHEN: User calls create_chatflow
        THEN: Returns ValidationError about size limit
        """
        # Create oversized flowData (>1MB)
        large_flow_data = json.dumps({
            "nodes": [
                {"id": f"node-{i}", "type": "test", "data": {"x" * 1000: "y"}}
                for i in range(2000)
            ],
            "edges": []
        })

        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.create_chatflow(
                name="Oversized Chatflow",
                flow_data=large_flow_data
            )

        error_message = str(exc_info.value).lower()
        assert "1mb" in error_message or "size" in error_message

        mock_flowise_client.create_chatflow.assert_not_called()


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS2Scenario4FlowiseUnavailable:
    """AC4: System handles Flowise API unavailability with clear connection errors."""

    async def test_create_chatflow_fails_when_api_unreachable(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Flowise API is unreachable
        WHEN: User calls create_chatflow
        THEN: Returns ConnectionError with clear message
        """
        mock_flowise_client.create_chatflow.side_effect = ConnectionError(
            "Cannot reach Flowise at http://localhost:3000"
        )

        with pytest.raises(ConnectionError) as exc_info:
            await mcp_server.create_chatflow(
                name="Test Chatflow",
                flow_data=valid_flow_data_json
            )

        error_message = str(exc_info.value).lower()
        assert any(
            keyword in error_message
            for keyword in ["connection", "reach", "unreachable", "unavailable"]
        )

    async def test_create_chatflow_fails_on_timeout(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        GIVEN: Flowise API times out
        WHEN: User calls create_chatflow
        THEN: Returns ConnectionError indicating timeout
        """
        mock_flowise_client.create_chatflow.side_effect = ConnectionError(
            "Request timed out after 30 seconds"
        )

        with pytest.raises(ConnectionError) as exc_info:
            await mcp_server.create_chatflow(
                name="Test Chatflow",
                flow_data=valid_flow_data_json
            )

        error_message = str(exc_info.value).lower()
        assert "timeout" in error_message or "timed out" in error_message


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS2EndToEndWorkflow:
    """Complete end-to-end workflow: create → verify in list → retrieve details."""

    async def test_complete_creation_workflow(
        self, mcp_server, mock_flowise_client, valid_flow_data_json
    ):
        """
        SCENARIO: User creates a new chatflow and verifies it exists
        GIVEN: User wants to create a new RAG Assistant chatflow
        WHEN: User creates, lists, and retrieves the chatflow
        THEN: Each step succeeds and chatflow is fully accessible
        """
        # Step 1: Create new chatflow
        created = await mcp_server.create_chatflow(
            name="RAG Assistant",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert "id" in created
        created_id = created["id"]
        assert created["name"] == "RAG Assistant"

        # Step 2: Verify it appears in list
        chatflows = await mcp_server.list_chatflows()
        found_in_list = any(cf["id"] == created_id for cf in chatflows)
        assert found_in_list, "Created chatflow should appear in list"

        # Step 3: Retrieve full details
        details = await mcp_server.get_chatflow(chatflow_id=created_id)
        assert details["id"] == created_id
        assert details["name"] == "RAG Assistant"
        assert "flowData" in details or "flow_data" in details

        # Verify all client methods were called
        mock_flowise_client.create_chatflow.assert_called()
        mock_flowise_client.list_chatflows.assert_called()
        mock_flowise_client.get_chatflow.assert_called()
