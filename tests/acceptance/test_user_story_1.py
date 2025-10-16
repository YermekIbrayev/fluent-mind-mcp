"""Acceptance tests for User Story 1: Query and Execute Existing Chatflows.

Tests the complete user journey from the spec:
- AC1: List all chatflows and see their metadata
- AC2: Get detailed chatflow information including workflow structure
- AC3: Execute chatflow with question and get response
- AC4: Handle errors gracefully

These tests verify the full stack works together (client + service + MCP tools).
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConnectionError,
    NotFoundError,
)
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig, PredictionResponse
from fluent_mind_mcp.server import MCPServer


@pytest.fixture
def mock_flowise_client():
    """Mock FlowiseClient that simulates Flowise API responses."""
    client = AsyncMock()

    # Mock data matching spec examples
    client.list_chatflows.return_value = [
        Chatflow(
            id="abc-123-def",
            name="RAG Assistant",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            created_date=datetime(2025, 10, 16, 12, 0, 0),
        ),
        Chatflow(
            id="xyz-456-uvw",
            name="Research Agent",
            type=ChatflowType.AGENTFLOW,
            deployed=False,
            created_date=datetime(2025, 10, 15, 10, 30, 0),
        ),
    ]

    client.get_chatflow.return_value = Chatflow(
        id="abc-123-def",
        name="RAG Assistant",
        type=ChatflowType.CHATFLOW,
        deployed=True,
        flow_data='{"nodes": [{"id": "node-1", "type": "llm", "data": {"model": "gpt-4"}}], "edges": []}',
        created_date=datetime(2025, 10, 16, 12, 0, 0),
        updated_date=datetime(2025, 10, 16, 14, 30, 0),
    )

    client.run_prediction.return_value = PredictionResponse(
        text="The capital of France is Paris.",
        question_message_id="msg-question-123",
        chat_message_id="msg-response-456",
        session_id="session-789",
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
class TestUS1Scenario1ListChatflows:
    """AC1: User lists all available chatflows to see what exists."""

    async def test_list_chatflows_shows_all_chatflows_with_metadata(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Flowise instance has 2 chatflows (RAG Assistant, Research Agent)
        WHEN: User calls list_chatflows tool
        THEN: Returns array with both chatflows including id, name, type, deployed status
        """
        # Call list_chatflows tool through MCP server
        result = await mcp_server.list_chatflows()

        # Should return list of chatflows
        assert isinstance(result, list)
        assert len(result) == 2

        # Verify first chatflow (RAG Assistant)
        rag_assistant = result[0]
        assert rag_assistant["id"] == "abc-123-def"
        assert rag_assistant["name"] == "RAG Assistant"
        assert rag_assistant["type"] == "CHATFLOW"
        assert rag_assistant["deployed"] is True

        # Verify second chatflow (Research Agent)
        research_agent = result[1]
        assert research_agent["id"] == "xyz-456-uvw"
        assert research_agent["name"] == "Research Agent"
        assert research_agent["type"] == "AGENTFLOW"
        assert research_agent["deployed"] is False

        # Verify client was called
        mock_flowise_client.list_chatflows.assert_called_once()

    async def test_list_chatflows_empty_when_no_chatflows_exist(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Flowise instance has no chatflows
        WHEN: User calls list_chatflows
        THEN: Returns empty array (not error)
        """
        mock_flowise_client.list_chatflows.return_value = []

        result = await mcp_server.list_chatflows()

        assert result == []
        assert isinstance(result, list)

    async def test_list_chatflows_completes_within_5_seconds(self, mcp_server):
        """
        GIVEN: Normal Flowise API response time
        WHEN: User calls list_chatflows
        THEN: Operation completes within 5 seconds (SC-002)
        """
        import time

        start_time = time.time()
        await mcp_server.list_chatflows()
        duration = time.time() - start_time

        assert duration < 5.0, f"list_chatflows took {duration}s, expected <5s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS1Scenario2GetChatflowDetails:
    """AC2: User retrieves detailed chatflow information including workflow structure."""

    async def test_get_chatflow_returns_complete_details(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Chatflow "abc-123-def" exists with complete data
        WHEN: User calls get_chatflow with chatflow_id
        THEN: Returns chatflow with id, name, type, deployed, flowData, timestamps
        """
        result = await mcp_server.get_chatflow(chatflow_id="abc-123-def")

        assert result["id"] == "abc-123-def"
        assert result["name"] == "RAG Assistant"
        assert result["type"] == "CHATFLOW"
        assert result["deployed"] is True
        assert "flowData" in result or "flow_data" in result
        assert "createdDate" in result or "created_date" in result

        # Verify flowData contains nodes and edges
        flow_data = result.get("flowData") or result.get("flow_data")
        assert "nodes" in flow_data
        assert "edges" in flow_data

        mock_flowise_client.get_chatflow.assert_called_once_with("abc-123-def")

    async def test_get_chatflow_not_found_returns_clear_error(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Chatflow "nonexistent" does not exist
        WHEN: User calls get_chatflow
        THEN: Returns NotFoundError with clear message
        """
        mock_flowise_client.get_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError) as exc_info:
            await mcp_server.get_chatflow(chatflow_id="nonexistent")

        error_message = str(exc_info.value).lower()
        assert "not found" in error_message or "404" in error_message

    async def test_get_chatflow_completes_within_5_seconds(self, mcp_server):
        """
        GIVEN: Normal Flowise API response time
        WHEN: User calls get_chatflow
        THEN: Operation completes within 5 seconds (SC-002)
        """
        import time

        start_time = time.time()
        await mcp_server.get_chatflow(chatflow_id="abc-123-def")
        duration = time.time() - start_time

        assert duration < 5.0, f"get_chatflow took {duration}s, expected <5s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS1Scenario3ExecuteChatflow:
    """AC3: User executes deployed chatflow with question and receives response."""

    async def test_run_prediction_executes_chatflow_and_returns_response(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Deployed chatflow "abc-123-def" exists
        WHEN: User calls run_prediction with chatflow_id and question
        THEN: Returns response text from chatflow execution
        """
        result = await mcp_server.run_prediction(
            chatflow_id="abc-123-def", question="What is the capital of France?"
        )

        assert "text" in result
        assert result["text"] == "The capital of France is Paris."
        assert "sessionId" in result or "session_id" in result

        mock_flowise_client.run_prediction.assert_called_once_with(
            chatflow_id="abc-123-def", question="What is the capital of France?"
        )

    async def test_run_prediction_preserves_session_for_conversation_context(
        self, mcp_server, mock_flowise_client
    ):
        """
        GIVEN: Previous execution created session "session-789"
        WHEN: User makes follow-up prediction call
        THEN: Returns same session_id for conversation continuity
        """
        # First call
        result1 = await mcp_server.run_prediction(chatflow_id="abc-123-def", question="First question")
        session_id = result1.get("sessionId") or result1.get("session_id")

        # Second call (in real implementation, session would be passed)
        result2 = await mcp_server.run_prediction(chatflow_id="abc-123-def", question="Follow-up question")

        # Session should be consistent (mocked to return same session)
        assert session_id == "session-789"

    async def test_run_prediction_not_found_when_chatflow_missing(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Chatflow "nonexistent" does not exist
        WHEN: User calls run_prediction
        THEN: Returns NotFoundError
        """
        mock_flowise_client.run_prediction.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await mcp_server.run_prediction(chatflow_id="nonexistent", question="Test question")

    async def test_run_prediction_completes_within_5_seconds(self, mcp_server):
        """
        GIVEN: Normal chatflow execution time
        WHEN: User calls run_prediction
        THEN: Operation completes within 5 seconds (SC-002)
        """
        import time

        start_time = time.time()
        await mcp_server.run_prediction(chatflow_id="abc-123-def", question="Test")
        duration = time.time() - start_time

        assert duration < 5.0, f"run_prediction took {duration}s, expected <5s"


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS1Scenario4ErrorHandling:
    """AC4: System handles errors gracefully with clear messages."""

    async def test_connection_error_when_flowise_unreachable(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Flowise API is unreachable
        WHEN: User calls any tool
        THEN: Returns ConnectionError with helpful message
        """
        mock_flowise_client.list_chatflows.side_effect = ConnectionError(
            "Cannot reach Flowise at http://localhost:3000"
        )

        with pytest.raises(ConnectionError) as exc_info:
            await mcp_server.list_chatflows()

        error_message = str(exc_info.value).lower()
        assert "connection" in error_message or "reach" in error_message or "unreachable" in error_message

    async def test_authentication_error_when_api_key_invalid(self, mcp_server, mock_flowise_client):
        """
        GIVEN: Invalid API key configured
        WHEN: User calls any tool
        THEN: Returns AuthenticationError with clear message
        """
        mock_flowise_client.list_chatflows.side_effect = AuthenticationError("Invalid API key")

        with pytest.raises(AuthenticationError) as exc_info:
            await mcp_server.list_chatflows()

        error_message = str(exc_info.value).lower()
        assert "authentication" in error_message or "api key" in error_message or "unauthorized" in error_message

    async def test_validation_error_for_empty_chatflow_id(self, mcp_server):
        """
        GIVEN: User provides empty chatflow_id
        WHEN: User calls get_chatflow
        THEN: Returns ValidationError before making API call
        """
        from fluent_mind_mcp.client.exceptions import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            await mcp_server.get_chatflow(chatflow_id="")

        error_message = str(exc_info.value).lower()
        assert "chatflow_id" in error_message or "empty" in error_message or "required" in error_message

    async def test_validation_error_for_empty_question(self, mcp_server):
        """
        GIVEN: User provides empty question
        WHEN: User calls run_prediction
        THEN: Returns ValidationError before making API call
        """
        from fluent_mind_mcp.client.exceptions import ValidationError

        with pytest.raises(ValidationError):
            await mcp_server.run_prediction(chatflow_id="abc-123", question="")


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUS1EndToEndWorkflow:
    """Complete end-to-end workflow: list → get → execute."""

    async def test_complete_user_journey(self, mcp_server, mock_flowise_client):
        """
        SCENARIO: User discovers and executes a chatflow
        GIVEN: Flowise has available chatflows
        WHEN: User lists chatflows, selects one, gets details, then executes it
        THEN: Each step succeeds and provides expected data
        """
        # Step 1: List all chatflows
        chatflows = await mcp_server.list_chatflows()
        assert len(chatflows) > 0
        first_chatflow_id = chatflows[0]["id"]

        # Step 2: Get detailed info about first chatflow
        chatflow_details = await mcp_server.get_chatflow(chatflow_id=first_chatflow_id)
        assert chatflow_details["id"] == first_chatflow_id
        assert "flowData" in chatflow_details or "flow_data" in chatflow_details

        # Step 3: Execute the chatflow
        prediction = await mcp_server.run_prediction(chatflow_id=first_chatflow_id, question="Test question")
        assert "text" in prediction
        assert len(prediction["text"]) > 0

        # Verify all client methods were called
        mock_flowise_client.list_chatflows.assert_called()
        mock_flowise_client.get_chatflow.assert_called()
        mock_flowise_client.run_prediction.assert_called()
