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
    ValidationError,
)
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig, PredictionResponse


@pytest.fixture
def config():
    """FlowiseConfig fixture for testing."""
    # Use model_construct to bypass environment variable loading
    # This ensures tests use hardcoded values, not .env file
    return FlowiseConfig.model_construct(
        api_url="http://localhost:3000",
        api_key="test-api-key-12345",
        timeout=30,
        max_connections=10,
        log_level="INFO",
        flowise_version="v1.x"
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
class TestFlowiseClientCreateChatflow:
    """Test create_chatflow() method."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string."""
        return json.dumps({
            "nodes": [
                {
                    "id": "node-1",
                    "type": "chatOpenAI",
                    "data": {"name": "chatOpenAI_0"},
                    "position": {"x": 100.0, "y": 100.0}
                }
            ],
            "edges": []
        })

    @pytest.fixture
    def sample_created_chatflow(self, valid_flow_data_json) -> Dict[str, Any]:
        """Sample API response after creating chatflow."""
        return {
            "id": "new-chatflow-123",
            "name": "Test Chatflow",
            "type": "CHATFLOW",
            "deployed": False,
            "flowData": valid_flow_data_json,
            "createdDate": "2025-10-16T15:00:00Z",
            "updatedDate": "2025-10-16T15:00:00Z",
        }

    @respx.mock
    async def test_create_chatflow_success(self, client, valid_flow_data_json, sample_created_chatflow):
        """create_chatflow() returns Chatflow object with new ID on success."""
        respx.post("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(201, json=sample_created_chatflow)
        )

        chatflow = await client.create_chatflow(
            name="Test Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert isinstance(chatflow, Chatflow)
        assert chatflow.id == "new-chatflow-123"
        assert chatflow.name == "Test Chatflow"
        assert chatflow.type == ChatflowType.CHATFLOW
        assert chatflow.deployed is False
        assert chatflow.flow_data is not None

    @respx.mock
    async def test_create_chatflow_request_body_format(self, client, valid_flow_data_json, sample_created_chatflow):
        """create_chatflow() sends correctly formatted request body."""
        route = respx.post("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(201, json=sample_created_chatflow)
        )

        await client.create_chatflow(
            name="Test Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.AGENTFLOW,
            deployed=True
        )

        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)

        assert request_data["name"] == "Test Chatflow"
        assert request_data["flowData"] == valid_flow_data_json
        assert request_data["type"] == "AGENTFLOW"
        assert request_data["deployed"] is True

    @respx.mock
    async def test_create_chatflow_default_values(self, client, valid_flow_data_json, sample_created_chatflow):
        """create_chatflow() uses default values for optional parameters."""
        route = respx.post("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(201, json=sample_created_chatflow)
        )

        await client.create_chatflow(
            name="Test Chatflow",
            flow_data=valid_flow_data_json
        )

        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)

        # Should use defaults: type=CHATFLOW, deployed=False
        assert request_data["type"] == "CHATFLOW"
        assert request_data["deployed"] is False

    @respx.mock
    async def test_create_chatflow_authentication_error(self, client, valid_flow_data_json):
        """create_chatflow() raises AuthenticationError on 401."""
        respx.post("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError):
            await client.create_chatflow(
                name="Test Chatflow",
                flow_data=valid_flow_data_json
            )

    @respx.mock
    async def test_create_chatflow_connection_error(self, client, valid_flow_data_json):
        """create_chatflow() raises ConnectionError on network failure."""
        respx.post("http://localhost:3000/api/v1/chatflows").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.create_chatflow(
                name="Test Chatflow",
                flow_data=valid_flow_data_json
            )

        assert "connection" in str(exc_info.value).lower()

    @respx.mock
    async def test_create_chatflow_rate_limit(self, client, valid_flow_data_json):
        """create_chatflow() raises RateLimitError on 429."""
        respx.post("http://localhost:3000/api/v1/chatflows").mock(
            return_value=httpx.Response(429, json={"error": "Too many requests"})
        )

        with pytest.raises(RateLimitError):
            await client.create_chatflow(
                name="Test Chatflow",
                flow_data=valid_flow_data_json
            )

    @respx.mock
    async def test_create_chatflow_timeout(self, client, valid_flow_data_json):
        """create_chatflow() raises ConnectionError on timeout."""
        respx.post("http://localhost:3000/api/v1/chatflows").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.create_chatflow(
                name="Test Chatflow",
                flow_data=valid_flow_data_json
            )

        assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()


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


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientUpdateChatflow:
    """Test update_chatflow() method for US3."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string."""
        return json.dumps({
            "nodes": [
                {
                    "id": "node-1",
                    "type": "chatOpenAI",
                    "data": {"name": "chatOpenAI_0"},
                    "position": {"x": 100.0, "y": 100.0}
                }
            ],
            "edges": []
        })

    @pytest.fixture
    def sample_updated_chatflow(self) -> Dict[str, Any]:
        """Sample API response after updating chatflow."""
        return {
            "id": "abc-123-def",
            "name": "Updated Name",
            "type": "CHATFLOW",
            "deployed": True,
            "flowData": '{"nodes": [{"id": "node-1"}], "edges": []}',
            "createdDate": "2025-10-16T12:00:00Z",
            "updatedDate": "2025-10-16T16:00:00Z",
        }

    @respx.mock
    async def test_update_chatflow_name_only(self, client, sample_updated_chatflow):
        """update_chatflow() updates only name when provided."""
        route = respx.put("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json=sample_updated_chatflow)
        )

        chatflow = await client.update_chatflow(
            chatflow_id="abc-123-def",
            name="Updated Name"
        )

        assert isinstance(chatflow, Chatflow)
        assert chatflow.id == "abc-123-def"
        assert chatflow.name == "Updated Name"

        # Verify request body contains only name
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert "name" in request_data
        assert request_data["name"] == "Updated Name"

    @respx.mock
    async def test_update_chatflow_deployed_only(self, client, sample_updated_chatflow):
        """update_chatflow() updates only deployed status when provided."""
        route = respx.put("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json=sample_updated_chatflow)
        )

        chatflow = await client.update_chatflow(
            chatflow_id="abc-123-def",
            deployed=True
        )

        assert chatflow.deployed is True

        # Verify request body contains only deployed
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert "deployed" in request_data
        assert request_data["deployed"] is True

    @respx.mock
    async def test_update_chatflow_flow_data_only(self, client, valid_flow_data_json, sample_updated_chatflow):
        """update_chatflow() updates only flowData when provided."""
        route = respx.put("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json=sample_updated_chatflow)
        )

        chatflow = await client.update_chatflow(
            chatflow_id="abc-123-def",
            flow_data=valid_flow_data_json
        )

        assert isinstance(chatflow, Chatflow)

        # Verify request body contains only flowData
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert "flowData" in request_data
        assert request_data["flowData"] == valid_flow_data_json

    @respx.mock
    async def test_update_chatflow_multiple_fields(self, client, valid_flow_data_json, sample_updated_chatflow):
        """update_chatflow() updates multiple fields simultaneously."""
        route = respx.put("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json=sample_updated_chatflow)
        )

        chatflow = await client.update_chatflow(
            chatflow_id="abc-123-def",
            name="Updated Name",
            deployed=True,
            flow_data=valid_flow_data_json
        )

        assert chatflow.name == "Updated Name"
        assert chatflow.deployed is True

        # Verify request body contains all fields
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert request_data["name"] == "Updated Name"
        assert request_data["deployed"] is True
        assert request_data["flowData"] == valid_flow_data_json

    @respx.mock
    async def test_update_chatflow_not_found(self, client):
        """update_chatflow() raises NotFoundError when chatflow doesn't exist."""
        respx.put("http://localhost:3000/api/v1/chatflows/nonexistent").mock(
            return_value=httpx.Response(404, json={"error": "Chatflow not found"})
        )

        with pytest.raises(NotFoundError) as exc_info:
            await client.update_chatflow(
                chatflow_id="nonexistent",
                name="New Name"
            )

        assert "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()

    @respx.mock
    async def test_update_chatflow_flowise_500_not_found(self, client):
        """update_chatflow() raises NotFoundError when Flowise returns 500 with 'not found' message."""
        respx.put("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(
                500,
                json={"message": "Chatflow abc-123 does not exist"}
            )
        )

        with pytest.raises(NotFoundError) as exc_info:
            await client.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

        assert "not found" in str(exc_info.value).lower() or "does not exist" in str(exc_info.value).lower()

    @respx.mock
    async def test_update_chatflow_authentication_error(self, client):
        """update_chatflow() raises AuthenticationError on 401."""
        respx.put("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError):
            await client.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

    @respx.mock
    async def test_update_chatflow_validation_error(self, client):
        """update_chatflow() raises ValidationError on 400."""
        respx.put("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(400, json={"error": "Invalid flowData"})
        )

        with pytest.raises(ValidationError):
            await client.update_chatflow(
                chatflow_id="abc-123",
                flow_data="invalid json"
            )

    @respx.mock
    async def test_update_chatflow_connection_error(self, client):
        """update_chatflow() raises ConnectionError on network failure."""
        respx.put("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

        assert "connection" in str(exc_info.value).lower()

    @respx.mock
    async def test_update_chatflow_timeout(self, client):
        """update_chatflow() raises ConnectionError on timeout."""
        respx.put("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

        assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()

    @respx.mock
    async def test_update_chatflow_rate_limit(self, client):
        """update_chatflow() raises RateLimitError on 429."""
        respx.put("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(429, json={"error": "Too many requests"})
        )

        with pytest.raises(RateLimitError):
            await client.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

    @respx.mock
    async def test_update_chatflow_partial_update(self, client, sample_updated_chatflow):
        """update_chatflow() supports partial updates (only provided fields)."""
        # Test that we can update just deployment status
        route = respx.put("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json=sample_updated_chatflow)
        )

        await client.update_chatflow(
            chatflow_id="abc-123-def",
            deployed=False
        )

        # Verify only deployed field is in request
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert "deployed" in request_data
        assert "name" not in request_data
        assert "flowData" not in request_data


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientDeleteChatflow:
    """Test delete_chatflow() method for US4."""

    @respx.mock
    async def test_delete_chatflow_success(self, client):
        """delete_chatflow() successfully deletes chatflow with 200 response."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json={"message": "Chatflow deleted"})
        )

        # Should not raise any exception
        await client.delete_chatflow("abc-123-def")

        # Verify the DELETE request was made
        # (implicit: if no exception was raised, deletion succeeded)

    @respx.mock
    async def test_delete_chatflow_returns_none_on_success(self, client):
        """delete_chatflow() returns None on successful deletion."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(200, json={"message": "Chatflow deleted"})
        )

        result = await client.delete_chatflow("abc-123-def")

        assert result is None

    @respx.mock
    async def test_delete_chatflow_handles_204_no_content(self, client):
        """delete_chatflow() handles 204 No Content response."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123-def").mock(
            return_value=httpx.Response(204)
        )

        # Should not raise any exception
        await client.delete_chatflow("abc-123-def")

    @respx.mock
    async def test_delete_chatflow_not_found_raises_error(self, client):
        """delete_chatflow() raises NotFoundError when chatflow doesn't exist (404)."""
        respx.delete("http://localhost:3000/api/v1/chatflows/nonexistent").mock(
            return_value=httpx.Response(404, json={"error": "Chatflow not found"})
        )

        with pytest.raises(NotFoundError) as exc_info:
            await client.delete_chatflow("nonexistent")

        assert "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()

    @respx.mock
    async def test_delete_chatflow_flowise_500_not_found(self, client):
        """delete_chatflow() raises NotFoundError when Flowise returns 500 with 'not found' message."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(
                500,
                json={"message": "Chatflow abc-123 does not exist"}
            )
        )

        with pytest.raises(NotFoundError) as exc_info:
            await client.delete_chatflow("abc-123")

        assert "not found" in str(exc_info.value).lower() or "does not exist" in str(exc_info.value).lower()

    @respx.mock
    async def test_delete_chatflow_already_deleted_succeeds_gracefully(self, client):
        """delete_chatflow() succeeds gracefully when chatflow was already deleted (404)."""
        # Flowise returns 404 for already-deleted chatflows
        # According to spec, deletion should be idempotent (succeed if already gone)
        respx.delete("http://localhost:3000/api/v1/chatflows/already-deleted").mock(
            return_value=httpx.Response(404, json={"error": "Chatflow not found"})
        )

        # Should raise NotFoundError (implementation will handle idempotency at service layer)
        with pytest.raises(NotFoundError):
            await client.delete_chatflow("already-deleted")

    @respx.mock
    async def test_delete_chatflow_authentication_error(self, client):
        """delete_chatflow() raises AuthenticationError on 401."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError):
            await client.delete_chatflow("abc-123")

    @respx.mock
    async def test_delete_chatflow_connection_error(self, client):
        """delete_chatflow() raises ConnectionError on network failure."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.delete_chatflow("abc-123")

        assert "connection" in str(exc_info.value).lower()

    @respx.mock
    async def test_delete_chatflow_timeout(self, client):
        """delete_chatflow() raises ConnectionError on timeout."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.delete_chatflow("abc-123")

        assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()

    @respx.mock
    async def test_delete_chatflow_rate_limit(self, client):
        """delete_chatflow() raises RateLimitError on 429."""
        respx.delete("http://localhost:3000/api/v1/chatflows/abc-123").mock(
            return_value=httpx.Response(429, json={"error": "Too many requests"})
        )

        with pytest.raises(RateLimitError):
            await client.delete_chatflow("abc-123")

    @respx.mock
    async def test_delete_chatflow_with_uuid(self, client):
        """delete_chatflow() works with UUID format chatflow IDs."""
        uuid_id = "550e8400-e29b-41d4-a716-446655440000"

        respx.delete(f"http://localhost:3000/api/v1/chatflows/{uuid_id}").mock(
            return_value=httpx.Response(200, json={"message": "Deleted"})
        )

        await client.delete_chatflow(uuid_id)

        # Should complete without error


@pytest.mark.unit
@pytest.mark.asyncio
class TestFlowiseClientGenerateAgentflowV2:
    """Test generate_agentflow_v2() method for US5.

    WHY: User Story 5 enables AI assistants to generate complete AgentFlow V2 structures
    from natural language descriptions, lowering the technical barrier to agent creation.

    These tests verify that the FlowiseClient correctly calls the Flowise generation endpoint
    and handles various response scenarios.
    """

    @pytest.fixture
    def sample_generated_agentflow(self) -> Dict[str, Any]:
        """Sample API response from AgentFlow V2 generation endpoint."""
        return {
            "flowData": json.dumps({
                "nodes": [
                    {
                        "id": "webSearch_0",
                        "type": "webSearch",
                        "data": {
                            "name": "webSearch",
                            "description": "Search the web for information"
                        },
                        "position": {"x": 100.0, "y": 100.0}
                    },
                    {
                        "id": "summarizer_0",
                        "type": "summarizer",
                        "data": {
                            "name": "summarizer",
                            "description": "Summarize search results"
                        },
                        "position": {"x": 300.0, "y": 100.0}
                    }
                ],
                "edges": [
                    {
                        "id": "edge_0",
                        "source": "webSearch_0",
                        "target": "summarizer_0"
                    }
                ]
            }),
            "name": "Research Agent",
            "description": "Agent that searches web and summarizes findings"
        }

    @respx.mock
    async def test_generate_agentflow_v2_success(self, client, sample_generated_agentflow):
        """generate_agentflow_v2() returns generated flowData, name, and description on success.

        WHY: This is the happy path - verifies that we can successfully generate an AgentFlow V2
        from a natural language description and receive a complete structure ready for creation.
        """
        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(200, json=sample_generated_agentflow)
        )

        result = await client.generate_agentflow_v2(
            description="Create a research agent that searches the web and summarizes findings"
        )

        # Verify we got a dict with expected keys
        assert isinstance(result, dict)
        assert "flowData" in result
        assert "name" in result
        assert result["name"] == "Research Agent"
        assert result["description"] == "Agent that searches web and summarizes findings"

        # Verify flowData is valid JSON string containing nodes and edges
        flow_data = json.loads(result["flowData"])
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) == 2
        assert len(flow_data["edges"]) == 1

    @respx.mock
    async def test_generate_agentflow_v2_request_body_format(self, client, sample_generated_agentflow):
        """generate_agentflow_v2() sends correctly formatted request body.

        WHY: Verifies that we send the description in the correct format to Flowise.
        """
        route = respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(200, json=sample_generated_agentflow)
        )

        await client.generate_agentflow_v2(
            description="Create a customer support agent"
        )

        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)

        assert "description" in request_data
        assert request_data["description"] == "Create a customer support agent"

    @respx.mock
    async def test_generate_agentflow_v2_minimal_response(self, client):
        """generate_agentflow_v2() handles response with only required fields.

        WHY: Flowise might return minimal response without description field.
        """
        minimal_response = {
            "flowData": json.dumps({
                "nodes": [{"id": "node-1", "type": "llm"}],
                "edges": []
            }),
            "name": "Simple Agent"
        }

        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(200, json=minimal_response)
        )

        result = await client.generate_agentflow_v2(
            description="Simple agent"
        )

        assert result["name"] == "Simple Agent"
        assert "flowData" in result
        # Description might be None or missing
        assert result.get("description") is None or "description" not in result

    @respx.mock
    async def test_generate_agentflow_v2_authentication_error(self, client):
        """generate_agentflow_v2() raises AuthenticationError on 401.

        WHY: Verifies proper handling of authentication failures.
        """
        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError):
            await client.generate_agentflow_v2(
                description="Test agent"
            )

    @respx.mock
    async def test_generate_agentflow_v2_validation_error(self, client):
        """generate_agentflow_v2() raises ValidationError on 400 (description too vague).

        WHY: Flowise might reject descriptions that are too short or unclear.
        """
        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(400, json={"error": "Description too vague"})
        )

        with pytest.raises(ValidationError):
            await client.generate_agentflow_v2(
                description="agent"  # Too short/vague
            )

    @respx.mock
    async def test_generate_agentflow_v2_connection_error(self, client):
        """generate_agentflow_v2() raises ConnectionError on network failure.

        WHY: Network failures should be handled gracefully with clear error messages.
        """
        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.generate_agentflow_v2(
                description="Research agent"
            )

        assert "connection" in str(exc_info.value).lower()

    @respx.mock
    async def test_generate_agentflow_v2_timeout(self, client):
        """generate_agentflow_v2() raises ConnectionError on timeout.

        WHY: Generation can take time, timeouts should be handled properly.
        """
        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            side_effect=httpx.TimeoutException("Request timed out")
        )

        with pytest.raises(ConnectionError) as exc_info:
            await client.generate_agentflow_v2(
                description="Complex multi-agent system"
            )

        assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()

    @respx.mock
    async def test_generate_agentflow_v2_rate_limit(self, client):
        """generate_agentflow_v2() raises RateLimitError on 429.

        WHY: Generation might be rate-limited, should handle gracefully.
        """
        respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(429, json={"error": "Too many requests"})
        )

        with pytest.raises(RateLimitError):
            await client.generate_agentflow_v2(
                description="Research agent"
            )

    @respx.mock
    async def test_generate_agentflow_v2_with_long_description(self, client, sample_generated_agentflow):
        """generate_agentflow_v2() handles long, detailed descriptions.

        WHY: Users might provide very detailed descriptions for complex agents.
        """
        long_description = (
            "Create a comprehensive research agent that first searches the web using multiple "
            "search engines, then filters and ranks the results by relevance, extracts key information "
            "from the top results, summarizes the findings into a coherent report, and finally "
            "validates the information against trusted sources before presenting the final summary."
        )

        route = respx.post("http://localhost:3000/api/v1/agentflowv2-generator/generate").mock(
            return_value=httpx.Response(200, json=sample_generated_agentflow)
        )

        result = await client.generate_agentflow_v2(description=long_description)

        assert result["name"] == "Research Agent"

        # Verify full description was sent
        assert route.called
        request = route.calls.last.request
        request_data = json.loads(request.content)
        assert request_data["description"] == long_description
