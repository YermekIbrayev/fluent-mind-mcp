"""Acceptance tests for User Story 3: Update and Deploy Chatflows.

Tests the complete user journey from the spec:
- AC1: Update chatflow name
- AC2: Update chatflow flowData structure
- AC3: Deploy chatflow (toggle deployed=true)
- AC4: Undeploy chatflow (toggle deployed=false)

These tests verify the full stack works together (client + service + MCP tools).
"""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from fluent_mind_mcp.client.exceptions import NotFoundError, ValidationError
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig
from fluent_mind_mcp.server import MCPServer


@pytest.fixture
def mock_flowise_client():
    """Mock FlowiseClient that simulates Flowise API responses."""
    client = AsyncMock()

    # Mock existing chatflow
    client.get_chatflow.return_value = Chatflow(
        id="abc-123-def",
        name="Original Name",
        type=ChatflowType.CHATFLOW,
        deployed=False,
        flow_data='{"nodes": [{"id": "node-1", "type": "llm"}], "edges": []}',
        created_date=datetime(2025, 10, 16, 12, 0, 0),
        updated_date=datetime(2025, 10, 16, 12, 0, 0),
    )

    # Mock update_chatflow responses
    client.update_chatflow.return_value = Chatflow(
        id="abc-123-def",
        name="Updated Name",
        type=ChatflowType.CHATFLOW,
        deployed=True,
        flow_data='{"nodes": [{"id": "node-2", "type": "chatOpenAI"}], "edges": []}',
        created_date=datetime(2025, 10, 16, 12, 0, 0),
        updated_date=datetime(2025, 10, 16, 16, 0, 0),
    )

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
class TestUS3Scenario1UpdateName:
    """AC1: User updates chatflow name to organize and identify workflows."""

    async def test_update_chatflow_name_changes_display_name(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Existing chatflow "abc-123-def" with name "Original Name"
        WHEN: User calls update_chatflow with new name "Updated Name"
        THEN: Chatflow name is updated successfully
        """
        result = await mcp_server.update_chatflow(chatflow_id="abc-123-def", name="Updated Name")

        assert result["id"] == "abc-123-def"
        assert result["name"] == "Updated Name"

        # Verify update_chatflow was called with correct parameters
        mock_flowise_client.update_chatflow.assert_called_once()
        call_args = mock_flowise_client.update_chatflow.call_args
        assert call_args.kwargs["chatflow_id"] == "abc-123-def"
        assert call_args.kwargs["name"] == "Updated Name"

    async def test_update_chatflow_name_with_whitespace_strips_input(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Existing chatflow
        WHEN: User calls update_chatflow with name containing whitespace
        THEN: Name is trimmed and chatflow is updated
        """
        result = await mcp_server.update_chatflow(chatflow_id="abc-123-def", name="  Updated Name  ")

        assert result["name"] == "Updated Name"

    async def test_update_chatflow_name_not_found_returns_error(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Chatflow "nonexistent" does not exist
        WHEN: User calls update_chatflow
        THEN: Returns NotFoundError with clear message
        """
        mock_flowise_client.update_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError) as exc_info:
            await mcp_server.update_chatflow(chatflow_id="nonexistent", name="New Name")

        error_message = str(exc_info.value).lower()
        assert "not found" in error_message or "404" in error_message

    async def test_update_chatflow_completes_within_10_seconds(self, mcp_server):
        """
        GIVEN: Normal Flowise API response time
        WHEN: User calls update_chatflow
        THEN: Operation completes within 10 seconds (SC-003)
        """
        import time

        start_time = time.time()
        await mcp_server.update_chatflow(chatflow_id="abc-123-def", name="Updated Name")
        duration = time.time() - start_time

        assert duration < 10.0, f"update_chatflow took {duration}s, expected <10s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS3Scenario2UpdateFlowData:
    """AC2: User updates chatflow flowData to modify workflow structure."""

    async def test_update_chatflow_flowdata_changes_workflow_structure(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Existing chatflow with simple structure
        WHEN: User calls update_chatflow with new flowData
        THEN: Chatflow structure is updated successfully
        """
        import json

        new_flow_data = json.dumps(
            {"nodes": [{"id": "node-2", "type": "chatOpenAI", "data": {"model": "gpt-4"}}], "edges": []}
        )

        result = await mcp_server.update_chatflow(chatflow_id="abc-123-def", flow_data=new_flow_data)

        assert result["id"] == "abc-123-def"
        # Verify flowData was updated (mock returns updated version)
        flow_data = result.get("flowData") or result.get("flow_data")
        assert "chatOpenAI" in flow_data

        # Verify update_chatflow was called with flowData
        mock_flowise_client.update_chatflow.assert_called_once()
        call_args = mock_flowise_client.update_chatflow.call_args
        assert call_args.kwargs["chatflow_id"] == "abc-123-def"
        assert "flow_data" in call_args.kwargs

    async def test_update_chatflow_flowdata_validates_json_structure(self, mcp_server):
        """
        GIVEN: Existing chatflow
        WHEN: User calls update_chatflow with invalid flowData (not JSON)
        THEN: Returns ValidationError before making API call
        """
        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.update_chatflow(chatflow_id="abc-123-def", flow_data="not valid json")

        error_message = str(exc_info.value).lower()
        assert "json" in error_message or "invalid" in error_message

    async def test_update_chatflow_flowdata_requires_nodes_and_edges(self, mcp_server):
        """
        GIVEN: Existing chatflow
        WHEN: User calls update_chatflow with flowData missing nodes or edges
        THEN: Returns ValidationError
        """
        import json

        # Missing 'nodes' key
        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.update_chatflow(chatflow_id="abc-123-def", flow_data=json.dumps({"edges": []}))

        assert "nodes" in str(exc_info.value).lower()

        # Missing 'edges' key
        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.update_chatflow(chatflow_id="abc-123-def", flow_data=json.dumps({"nodes": []}))

        assert "edges" in str(exc_info.value).lower()

    async def test_update_chatflow_flowdata_enforces_size_limit(self, mcp_server):
        """
        GIVEN: Existing chatflow
        WHEN: User calls update_chatflow with flowData > 1MB
        THEN: Returns ValidationError
        """
        import json

        # Create oversized flowData (>1MB)
        large_data = json.dumps(
            {"nodes": [{"id": f"node-{i}", "type": "test", "data": {"x" * 1000: "y"}} for i in range(2000)], "edges": []}
        )

        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.update_chatflow(chatflow_id="abc-123-def", flow_data=large_data)

        error_message = str(exc_info.value).lower()
        assert "1mb" in error_message or "size" in error_message


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS3Scenario3DeployChatflow:
    """AC3: User deploys chatflow to make it available for execution."""

    async def test_deploy_chatflow_makes_chatflow_available(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Undeployed chatflow "abc-123-def"
        WHEN: User calls deploy_chatflow with deployed=true
        THEN: Chatflow becomes deployed and available for execution
        """
        # Mock chatflow transitions from undeployed to deployed
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id="abc-123-def",
            name="Test Chatflow",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            flow_data='{"nodes": [], "edges": []}',
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 16, 0, 0),
        )

        result = await mcp_server.deploy_chatflow(chatflow_id="abc-123-def", deployed=True)

        assert result["id"] == "abc-123-def"
        assert result["deployed"] is True

        # Verify update_chatflow was called with deployed=True
        mock_flowise_client.update_chatflow.assert_called_once()
        call_args = mock_flowise_client.update_chatflow.call_args
        assert call_args.kwargs["chatflow_id"] == "abc-123-def"
        assert call_args.kwargs["deployed"] is True

    async def test_deploy_chatflow_not_found_returns_error(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Chatflow "nonexistent" does not exist
        WHEN: User calls deploy_chatflow
        THEN: Returns NotFoundError
        """
        mock_flowise_client.update_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await mcp_server.deploy_chatflow(chatflow_id="nonexistent", deployed=True)

    async def test_deploy_chatflow_validates_chatflow_id(self, mcp_server):
        """
        GIVEN: Empty chatflow_id
        WHEN: User calls deploy_chatflow
        THEN: Returns ValidationError before making API call
        """
        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.deploy_chatflow(chatflow_id="", deployed=True)

        error_message = str(exc_info.value).lower()
        assert "chatflow_id" in error_message or "empty" in error_message

    async def test_deploy_chatflow_completes_within_10_seconds(self, mcp_server):
        """
        GIVEN: Normal Flowise API response time
        WHEN: User calls deploy_chatflow
        THEN: Operation completes within 10 seconds (SC-003)
        """
        import time

        start_time = time.time()
        await mcp_server.deploy_chatflow(chatflow_id="abc-123-def", deployed=True)
        duration = time.time() - start_time

        assert duration < 10.0, f"deploy_chatflow took {duration}s, expected <10s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS3Scenario4UndeployChatflow:
    """AC4: User undeploys chatflow to make it unavailable for execution."""

    async def test_undeploy_chatflow_makes_chatflow_unavailable(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Deployed chatflow "abc-123-def"
        WHEN: User calls deploy_chatflow with deployed=false
        THEN: Chatflow becomes undeployed and unavailable for execution
        """
        # Mock chatflow transitions from deployed to undeployed
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id="abc-123-def",
            name="Test Chatflow",
            type=ChatflowType.CHATFLOW,
            deployed=False,
            flow_data='{"nodes": [], "edges": []}',
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 16, 0, 0),
        )

        result = await mcp_server.deploy_chatflow(chatflow_id="abc-123-def", deployed=False)

        assert result["id"] == "abc-123-def"
        assert result["deployed"] is False

        # Verify update_chatflow was called with deployed=False
        mock_flowise_client.update_chatflow.assert_called_once()
        call_args = mock_flowise_client.update_chatflow.call_args
        assert call_args.kwargs["chatflow_id"] == "abc-123-def"
        assert call_args.kwargs["deployed"] is False

    async def test_toggle_deployment_status_multiple_times(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Chatflow exists
        WHEN: User toggles deployment status multiple times
        THEN: Each toggle succeeds and reflects current state
        """
        # First: Deploy
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id="abc-123-def",
            name="Test",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            flow_data="{}",
            created_date=datetime(2025, 10, 16, 12, 0, 0),
        )
        result1 = await mcp_server.deploy_chatflow(chatflow_id="abc-123-def", deployed=True)
        assert result1["deployed"] is True

        # Then: Undeploy
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id="abc-123-def",
            name="Test",
            type=ChatflowType.CHATFLOW,
            deployed=False,
            flow_data="{}",
            created_date=datetime(2025, 10, 16, 12, 0, 0),
        )
        result2 = await mcp_server.deploy_chatflow(chatflow_id="abc-123-def", deployed=False)
        assert result2["deployed"] is False

        # Verify called twice
        assert mock_flowise_client.update_chatflow.call_count == 2


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS3EndToEndWorkflow:
    """Complete end-to-end workflow: create → update name → update flowData → deploy."""

    async def test_complete_update_workflow(self, mcp_server, mock_flowise_client):
        """
        SCENARIO: User creates chatflow and iterates on it
        GIVEN: Chatflow exists
        WHEN: User updates name, then flowData, then deploys
        THEN: Each step succeeds with expected changes
        """
        import json

        chatflow_id = "abc-123-def"

        # Step 1: Update name
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id=chatflow_id,
            name="Updated Name",
            type=ChatflowType.CHATFLOW,
            deployed=False,
            flow_data='{"nodes": [{"id": "node-1"}], "edges": []}',
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 14, 0, 0),
        )
        result1 = await mcp_server.update_chatflow(chatflow_id=chatflow_id, name="Updated Name")
        assert result1["name"] == "Updated Name"

        # Step 2: Update flowData
        new_flow_data = json.dumps({"nodes": [{"id": "node-2", "type": "chatOpenAI"}], "edges": []})
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id=chatflow_id,
            name="Updated Name",
            type=ChatflowType.CHATFLOW,
            deployed=False,
            flow_data=new_flow_data,
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 15, 0, 0),
        )
        result2 = await mcp_server.update_chatflow(chatflow_id=chatflow_id, flow_data=new_flow_data)
        flow_data = result2.get("flowData") or result2.get("flow_data")
        assert "chatOpenAI" in flow_data

        # Step 3: Deploy
        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id=chatflow_id,
            name="Updated Name",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            flow_data=new_flow_data,
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 16, 0, 0),
        )
        result3 = await mcp_server.deploy_chatflow(chatflow_id=chatflow_id, deployed=True)
        assert result3["deployed"] is True

        # Verify all operations called the client
        assert mock_flowise_client.update_chatflow.call_count == 3

    async def test_update_multiple_fields_simultaneously(self, mcp_server, mock_flowise_client):
        """
        SCENARIO: User updates multiple fields in one call
        GIVEN: Chatflow exists
        WHEN: User calls update_chatflow with name, flowData, and deployed
        THEN: All fields are updated successfully
        """
        import json

        new_flow_data = json.dumps({"nodes": [{"id": "node-3"}], "edges": []})

        mock_flowise_client.update_chatflow.return_value = Chatflow(
            id="abc-123-def",
            name="Multi-Update",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            flow_data=new_flow_data,
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 16, 0, 0),
        )

        result = await mcp_server.update_chatflow(
            chatflow_id="abc-123-def", name="Multi-Update", flow_data=new_flow_data, deployed=True
        )

        assert result["name"] == "Multi-Update"
        assert result["deployed"] is True
        flow_data = result.get("flowData") or result.get("flow_data")
        assert "node-3" in flow_data

        # Verify all fields were passed to client
        call_args = mock_flowise_client.update_chatflow.call_args
        assert call_args.kwargs["name"] == "Multi-Update"
        assert "flow_data" in call_args.kwargs
        assert call_args.kwargs["deployed"] is True
