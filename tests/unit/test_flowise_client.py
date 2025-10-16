"""Unit tests for FlowiseClient READ operations.

Tests HTTP client methods for listing, retrieving, and executing chatflows.
Uses httpx mocking to test without real Flowise instance.
"""

import json
from datetime import datetime
from typing import Any, Dict

import httpx
import pytest
import respx

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
)
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig, PredictionResponse


@pytest.fixture
def config():
    """FlowiseConfig fixture for testing."""
    return FlowiseConfig(
        api_url="http://localhost:3000",
        api_key="test-api-key-12345",
        timeout=30,
    )


@pytest.fixture
async def client(config):
    """FlowiseClient fixture for testing."""
    client = FlowiseClient(config)
    yield client
    await client.close()


@pytest.fixture
def sample_chatflow_data() -> Dict[str, Any]:
    """Sample chatflow API response data."""
    return {
        "id": "abc-123-def",
        "name": "RAG Assistant",
        "type": "CHATFLOW",
        "deployed": True,
        "flowData": '{"nodes": [{"id": "node-1", "type": "llm", "data": {}}], "edges": []}',
        "createdDate": "2025-10-16T12:00:00Z",
        "updatedDate": "2025-10-16T14:30:00Z",
    }


@pytest.fixture
def sample_chatflows_list() -> list[Dict[str, Any]]:
    """Sample list of chatflows from API."""
    return [
        {
            "id": "abc-123-def",
            "name": "RAG Assistant",
            "type": "CHATFLOW",
            "deployed": True,
            "createdDate": "2025-10-16T12:00:00Z",
        },
        {
            "id": "xyz-456-uvw",
            "name": "Research Agent",
            "type": "AGENTFLOW",
            "deployed": False,
            "createdDate": "2025-10-15T10:30:00Z",
        },
    ]


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientListChatflows:
    """Test list_chatflows() method."""

    @respx.mock
    async def test_list_chatflows_success(self, client, sample_chatflows_list):
        """list_chatflows() returns list of Chatflow objects on success."""
        # Mock successful API response
        respx.get("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(200, json=sample_chatflows_list)
        )

        chatflows = await client.list_chatflows()

        assert len(chatflows) == 2
        assert all(isinstance(cf, Chatflow) for cf in chatflows)
        assert chatflows[0].id == "abc-123-def"
        assert chatflows[0].name == "RAG Assistant"
        assert chatflows[0].type == ChatflowType.CHATFLOW
        assert chatflows[0].deployed is True
        assert chatflows[1].id == "xyz-456-uvw"
        assert chatflows[1].type == ChatflowType.AGENTFLOW

    @respx.mock
    async def test_list_chatflows_empty_list(self, client):
        """list_chatflows() handles empty list response."""
        respx.get("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(200, json=[])
        )

        chatflows = await client.list_chatflows()

        assert chatflows == []
        assert isinstance(chatflows, list)

    @respx.mock
    async def test_list_chatflows_authentication_error(self, client):
        """list_chatflows() raises AuthenticationError on 401."""
        respx.get("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await client.list_chatflows()

        assert "401" in str(exc_info.value) or "authentication" in str(exc_info.value).lower()

    @respx.mock
    async def test_list_chatflows_connection_error(self, client):
        """list_chatflows() raises ConnectionError on network failure."""
        respx.get("http://localhost:3000/api/v1/chatflows").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.list_chatflows()

        assert "connection" in str(exc_info.value).lower()

    @respx.mock
    async def test_list_chatflows_rate_limit(self, client):
        """list_chatflows() raises RateLimitError on 429."""
        respx.get("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(429, json={"error": "Too many requests"})
        )

        with pytest.raises(RateLimitError):
            await client.list_chatflows()


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientGetChatflow:
    """Test get_chatflow(id) method."""

    @respx.mock
    async def test_get_chatflow_success(self, client, sample_chatflow_data):
        """get_chatflow() returns Chatflow object with complete data."""
        respx.get("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json=sample_chatflow_data)
        )

        chatflow = await client.get_chatflow("abc-123-def")

        assert isinstance(chatflow, Chatflow)
        assert chatflow.id == "abc-123-def"
        assert chatflow.name == "RAG Assistant"
        assert chatflow.type == ChatflowType.CHATFLOW
        assert chatflow.deployed is True
        assert chatflow.flow_data is not None
        assert "nodes" in chatflow.flow_data
        assert chatflow.created_date is not None

    @respx.mock
    async def test_get_chatflow_not_found(self, client):
        """get_chatflow() raises NotFoundError on 404."""
        respx.get("http://localhost:3000/api/v1/chatflows/nonexistent").mock(
            return_value=httpx.Response(404, json={"error": "Chatflow not found"})
        )

        with pytest.raises(NotFoundError) as exc_info:
            await client.get_chatflow("nonexistent")

        assert "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()

    @respx.mock
    async def test_get_chatflow_authentication_error(self, client):
        """get_chatflow() raises AuthenticationError on 401."""
        respx.get("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError):
            await client.get_chatflow("abc-123")

    @respx.mock
    async def test_get_chatflow_with_uuid(self, client, sample_chatflow_data):
        """get_chatflow() works with UUID format chatflow IDs."""
        uuid_id = "550e8400-e29b-41d4-a716-446655440000"
        sample_chatflow_data["id"] = uuid_id

        respx.get(f"http://localhost:3000/api/v1/chatflows/{uuid_id}").mock(
            return_value=httpx.Response(200, json=sample_chatflow_data)
        )

        chatflow = await client.get_chatflow(uuid_id)

        assert chatflow.id == uuid_id


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientRunPrediction:
    """Test run_prediction(id, question) method."""

    @respx.mock
    async def test_run_prediction_success(self, client):
        """run_prediction() returns PredictionResponse with text."""
        prediction_response = {
            "text": "The capital of France is Paris.",
            "questionMessageId": "msg-question-123",
            "chatMessageId": "msg-chat-456",
            "sessionId": "session-789",
        }

        respx.post("http://localhost:3000/api/v1/prediction/abc-123-def").mock(
            return_value=httpx.Response(200, json=prediction_response)
        )

        response = await client.run_prediction(
            chatflow_id="abc-123-def", question="What is the capital of France?"
        )

        assert isinstance(response, PredictionResponse)
        assert response.text == "The capital of France is Paris."
        assert response.question_message_id == "msg-question-123"
        assert response.chat_message_id == "msg-chat-456"
        assert response.session_id == "session-789"

    @respx.mock
    async def test_run_prediction_minimal_response(self, client):
        """run_prediction() handles response with only required text field."""
        prediction_response = {"text": "Simple response without IDs"}

        respx.post("http://localhost:3000/api/v1/prediction/abc-123").mock(
            return_value=httpx.Response(200, json=prediction_response)
        )

        response = await client.run_prediction(chatflow_id="abc-123", question="Hello")

        assert response.text == "Simple response without IDs"
        assert response.question_message_id is None
        assert response.chat_message_id is None
        assert response.session_id is None

    @respx.mock
    async def test_run_prediction_with_question_data(self, client):
        """run_prediction() sends question as POST data."""
        prediction_response = {"text": "Response"}

        route = respx.post("http://localhost:3000/api/v1/prediction/abc-123").mock(
            return_value=httpx.Response(200, json=prediction_response)
        )

        await client.run_prediction(chatflow_id="abc-123", question="Test question")

        # Verify the request was made with correct data
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert request_data["question"] == "Test question"

    @respx.mock
    async def test_run_prediction_not_found(self, client):
        """run_prediction() raises NotFoundError when chatflow doesn't exist."""
        respx.post("http://localhost:3000/api/v1/prediction/nonexistent").mock(
            return_value=httpx.Response(404, json={"error": "Chatflow not found"})
        )

        with pytest.raises(NotFoundError):
            await client.run_prediction(chatflow_id="nonexistent", question="Test")

    @respx.mock
    async def test_run_prediction_connection_timeout(self, client):
        """run_prediction() raises ConnectionError on timeout."""
        respx.post("http://localhost:3000/api/v1/prediction/abc-123").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.run_prediction(chatflow_id="abc-123", question="Test")

        assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientConnectionManagement:
    """Test client connection lifecycle."""

    async def test_client_initialization(self, config):
        """FlowiseClient initializes with config and creates httpx client."""
        client = FlowiseClient(config)

        assert client.config == config
        assert client.base_url == "http://localhost:3000/api/v1"
        assert client._client is not None

        await client.close()

    async def test_client_close(self, config):
        """FlowiseClient closes httpx client properly."""
        client = FlowiseClient(config)

        await client.close()

        # After close, client should be closed
        assert client._client.is_closed

    async def test_client_context_manager(self, config):
        """FlowiseClient works as async context manager."""
        async with FlowiseClient(config) as client:
            assert client._client is not None
            assert not client._client.is_closed

        # After context exit, client should be closed
        assert client._client.is_closed


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientHeaders:
    """Test API request headers and authentication."""

    @respx.mock
    async def test_api_key_header_included(self, client, sample_chatflows_list):
        """FlowiseClient includes API key in headers when configured."""
        route = respx.get("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(200, json=sample_chatflows_list)
        )

        await client.list_chatflows()

        assert route.called
        request = route.calls.last.request
        assert "Authorization" in request.headers or "x-api-key" in request.headers.get("Authorization", "")

    @respx.mock
    async def test_content_type_header(self, client):
        """FlowiseClient sets correct Content-Type for POST requests."""
        prediction_response = {"text": "Response"}

        route = respx.post("http://localhost:3000/api/v1/prediction/abc-123").mock(
            return_value=httpx.Response(200, json=prediction_response)
        )

        await client.run_prediction(chatflow_id="abc-123", question="Test")

        assert route.called
        request = route.calls.last.request
        assert "application/json" in request.headers.get("content-type", "").lower()
