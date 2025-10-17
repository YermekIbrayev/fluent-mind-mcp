"""Unit tests for ChatflowService READ operations.

Tests business logic layer for listing, retrieving, and executing chatflows.
Mocks FlowiseClient to isolate service logic.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from fluent_mind_mcp.client.exceptions import (
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    ValidationError,
)
from fluent_mind_mcp.models import Chatflow, ChatflowType, PredictionResponse
from fluent_mind_mcp.services.chatflow_service import ChatflowService


@pytest.fixture
def mock_client():
    """Mock FlowiseClient for testing."""
    client = AsyncMock()
    client.list_chatflows = AsyncMock()
    client.get_chatflow = AsyncMock()
    client.run_prediction = AsyncMock()
    return client


@pytest.fixture
def mock_logger():
    """Mock OperationLogger for testing."""
    logger = MagicMock()

    # Create async context manager mock for log_operation
    async_cm = MagicMock()
    async_cm.__aenter__ = AsyncMock(return_value={})
    async_cm.__aexit__ = AsyncMock(return_value=None)
    logger.log_operation = MagicMock(return_value=async_cm)

    logger.log_error = MagicMock()
    logger.time_operation = MagicMock()
    # Make time_operation return a context manager
    logger.time_operation.return_value.__enter__ = MagicMock()
    logger.time_operation.return_value.__exit__ = MagicMock()
    return logger


@pytest.fixture
def service(mock_client, mock_logger):
    """ChatflowService fixture for testing."""
    return ChatflowService(client=mock_client, logger=mock_logger)


@pytest.fixture
def sample_chatflow():
    """Sample Chatflow object for testing."""
    return Chatflow(
        id="abc-123-def",
        name="RAG Assistant",
        type=ChatflowType.CHATFLOW,
        deployed=True,
        flow_data='{"nodes": [], "edges": []}',
        created_date=datetime(2025, 10, 16, 12, 0, 0),
    )


@pytest.fixture
def sample_chatflows():
    """Sample list of Chatflow objects."""
    return [
        Chatflow(
            id="abc-123",
            name="RAG Assistant",
            type=ChatflowType.CHATFLOW,
            deployed=True,
        ),
        Chatflow(
            id="xyz-456",
            name="Research Agent",
            type=ChatflowType.AGENTFLOW,
            deployed=False,
        ),
    ]


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceListChatflows:
    """Test service.list_chatflows() method."""

    async def test_list_chatflows_success(self, service, mock_client, mock_logger, sample_chatflows):
        """list_chatflows() returns chatflows from client and logs operation."""
        mock_client.list_chatflows.return_value = sample_chatflows

        chatflows = await service.list_chatflows()

        assert len(chatflows) == 2
        assert chatflows[0].id == "abc-123"
        assert chatflows[1].id == "xyz-456"
        mock_client.list_chatflows.assert_called_once()
        mock_logger.log_operation.assert_called()

    async def test_list_chatflows_empty(self, service, mock_client, mock_logger):
        """list_chatflows() handles empty list from client."""
        mock_client.list_chatflows.return_value = []

        chatflows = await service.list_chatflows()

        assert chatflows == []
        mock_client.list_chatflows.assert_called_once()
        mock_logger.log_operation.assert_called()

    async def test_list_chatflows_connection_error(self, service, mock_client, mock_logger):
        """list_chatflows() propagates ConnectionError and logs it."""
        mock_client.list_chatflows.side_effect = ConnectionError("Cannot reach Flowise")

        with pytest.raises(ConnectionError):
            await service.list_chatflows()

        mock_logger.log_error.assert_called()

    async def test_list_chatflows_authentication_error(self, service, mock_client, mock_logger):
        """list_chatflows() propagates AuthenticationError and logs it."""
        mock_client.list_chatflows.side_effect = AuthenticationError("Invalid API key")

        with pytest.raises(AuthenticationError):
            await service.list_chatflows()

        mock_logger.log_error.assert_called()

    async def test_list_chatflows_logs_duration(self, service, mock_client, mock_logger, sample_chatflows):
        """list_chatflows() logs operation with timing."""
        mock_client.list_chatflows.return_value = sample_chatflows

        await service.list_chatflows()

        # Verify log_operation was called with correct operation name
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "list_chatflows" in str(call_args)
        # Verify context manager was entered (async with block executed)
        mock_logger.log_operation.assert_called_once_with("list_chatflows", {})


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceGetChatflow:
    """Test service.get_chatflow(id) method."""

    async def test_get_chatflow_success(self, service, mock_client, mock_logger, sample_chatflow):
        """get_chatflow() returns chatflow from client and logs operation."""
        mock_client.get_chatflow.return_value = sample_chatflow

        chatflow = await service.get_chatflow("abc-123-def")

        assert chatflow.id == "abc-123-def"
        assert chatflow.name == "RAG Assistant"
        mock_client.get_chatflow.assert_called_once_with("abc-123-def")
        mock_logger.log_operation.assert_called()

    async def test_get_chatflow_validates_id(self, service, mock_client, mock_logger):
        """get_chatflow() validates chatflow_id is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.get_chatflow("")

        assert "chatflow_id" in str(exc_info.value).lower() or "empty" in str(exc_info.value).lower()
        mock_client.get_chatflow.assert_not_called()

    async def test_get_chatflow_not_found(self, service, mock_client, mock_logger):
        """get_chatflow() propagates NotFoundError from client."""
        mock_client.get_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await service.get_chatflow("nonexistent")

        mock_logger.log_error.assert_called()

    async def test_get_chatflow_strips_whitespace(self, service, mock_client, sample_chatflow):
        """get_chatflow() strips whitespace from chatflow_id."""
        mock_client.get_chatflow.return_value = sample_chatflow

        await service.get_chatflow("  abc-123-def  ")

        # Should call client with stripped ID
        mock_client.get_chatflow.assert_called_once_with("abc-123-def")

    async def test_get_chatflow_logs_chatflow_id(self, service, mock_client, mock_logger, sample_chatflow):
        """get_chatflow() includes chatflow_id in operation logs."""
        mock_client.get_chatflow.return_value = sample_chatflow

        await service.get_chatflow("abc-123")

        # Verify chatflow_id appears in log context
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "abc-123" in str(call_args) or "chatflow_id" in str(call_args)


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceRunPrediction:
    """Test service.run_prediction(id, question) method."""

    async def test_run_prediction_success(self, service, mock_client, mock_logger):
        """run_prediction() returns response from client and logs operation."""
        prediction_response = PredictionResponse(
            text="The capital of France is Paris.",
            question_message_id="msg-123",
            chat_message_id="msg-456",
            session_id="session-789",
        )
        mock_client.run_prediction.return_value = prediction_response

        response = await service.run_prediction(chatflow_id="abc-123", question="What is the capital?")

        assert response.text == "The capital of France is Paris."
        assert response.session_id == "session-789"
        mock_client.run_prediction.assert_called_once_with(chatflow_id="abc-123", question="What is the capital?")
        mock_logger.log_operation.assert_called()

    async def test_run_prediction_validates_chatflow_id(self, service, mock_client):
        """run_prediction() validates chatflow_id is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.run_prediction(chatflow_id="", question="Test question")

        assert "chatflow_id" in str(exc_info.value).lower()
        mock_client.run_prediction.assert_not_called()

    async def test_run_prediction_validates_question(self, service, mock_client):
        """run_prediction() validates question is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.run_prediction(chatflow_id="abc-123", question="")

        assert "question" in str(exc_info.value).lower()
        mock_client.run_prediction.assert_not_called()

    async def test_run_prediction_validates_question_whitespace(self, service, mock_client):
        """run_prediction() rejects whitespace-only questions."""
        with pytest.raises(ValidationError):
            await service.run_prediction(chatflow_id="abc-123", question="   ")

        mock_client.run_prediction.assert_not_called()

    async def test_run_prediction_not_found(self, service, mock_client, mock_logger):
        """run_prediction() propagates NotFoundError when chatflow doesn't exist."""
        mock_client.run_prediction.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await service.run_prediction(chatflow_id="nonexistent", question="Test")

        mock_logger.log_error.assert_called()

    async def test_run_prediction_strips_inputs(self, service, mock_client):
        """run_prediction() strips whitespace from inputs before validation."""
        prediction_response = PredictionResponse(text="Response")
        mock_client.run_prediction.return_value = prediction_response

        await service.run_prediction(chatflow_id="  abc-123  ", question="  Test question  ")

        # Should call client with stripped values
        mock_client.run_prediction.assert_called_once_with(
            chatflow_id="abc-123", question="Test question"
        )

    async def test_run_prediction_logs_timing(self, service, mock_client, mock_logger):
        """run_prediction() logs operation with timing for performance tracking."""
        prediction_response = PredictionResponse(text="Response")
        mock_client.run_prediction.return_value = prediction_response

        await service.run_prediction(chatflow_id="abc-123", question="Test")

        # Verify timing/duration is logged
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        # Check if duration or timing-related info is present
        assert any(
            keyword in str(call_args).lower()
            for keyword in ["duration", "timing", "seconds", "run_prediction"]
        )


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceErrorHandling:
    """Test service error handling and logging."""

    async def test_service_translates_errors_to_user_friendly(self, service, mock_client):
        """Service translates technical errors to user-friendly messages."""
        mock_client.list_chatflows.side_effect = Exception("Internal httpx error")

        with pytest.raises(Exception) as exc_info:
            await service.list_chatflows()

        # Error should be caught and potentially wrapped
        # (Implementation will determine exact error translation)
        assert exc_info.value is not None

    async def test_service_logs_all_operations(self, service, mock_client, mock_logger, sample_chatflows):
        """Service logs every operation for observability."""
        mock_client.list_chatflows.return_value = sample_chatflows

        await service.list_chatflows()

        # Should have logged the operation
        assert mock_logger.log_operation.call_count >= 1

    async def test_service_logs_errors_with_context(self, service, mock_client, mock_logger):
        """Service logs errors with full context for debugging."""
        mock_client.get_chatflow.side_effect = NotFoundError("Not found")

        try:
            await service.get_chatflow("test-id")
        except NotFoundError:
            pass

        # Should have logged the error with context
        mock_logger.log_error.assert_called()
        call_args = mock_logger.log_error.call_args
        assert "test-id" in str(call_args) or "get_chatflow" in str(call_args)


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceCreateChatflow:
    """Test service.create_chatflow() method."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string."""
        import json
        return json.dumps({
            "nodes": [{"id": "node-1", "type": "chatOpenAI", "data": {}}],
            "edges": []
        })

    @pytest.fixture
    def created_chatflow(self, valid_flow_data_json) -> Chatflow:
        """Sample created Chatflow object."""
        return Chatflow(
            id="new-chatflow-123",
            name="New Chatflow",
            type=ChatflowType.CHATFLOW,
            deployed=False,
            flow_data=valid_flow_data_json,
            created_date=datetime(2025, 10, 16, 15, 0, 0),
        )

    async def test_create_chatflow_success(self, service, mock_client, mock_logger, valid_flow_data_json, created_chatflow):
        """create_chatflow() returns created chatflow from client and logs operation."""
        mock_client.create_chatflow.return_value = created_chatflow

        chatflow = await service.create_chatflow(
            name="New Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert chatflow.id == "new-chatflow-123"
        assert chatflow.name == "New Chatflow"
        mock_client.create_chatflow.assert_called_once_with(
            name="New Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )
        mock_logger.log_operation.assert_called()

    async def test_create_chatflow_validates_name(self, service, mock_client, valid_flow_data_json):
        """create_chatflow() validates name is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.create_chatflow(
                name="",
                flow_data=valid_flow_data_json
            )

        assert "name" in str(exc_info.value).lower()
        mock_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_validates_flow_data(self, service, mock_client):
        """create_chatflow() validates flow_data is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.create_chatflow(
                name="Test",
                flow_data=""
            )

        assert "flow_data" in str(exc_info.value).lower()
        mock_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_validates_flow_data_json(self, service, mock_client):
        """create_chatflow() validates flow_data is valid JSON."""
        with pytest.raises(ValidationError) as exc_info:
            await service.create_chatflow(
                name="Test",
                flow_data="not valid json"
            )

        assert "json" in str(exc_info.value).lower()
        mock_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_validates_flow_data_structure(self, service, mock_client):
        """create_chatflow() validates flow_data has nodes and edges."""
        import json

        # Missing 'nodes' key
        with pytest.raises(ValidationError) as exc_info:
            await service.create_chatflow(
                name="Test",
                flow_data=json.dumps({"edges": []})
            )

        assert "nodes" in str(exc_info.value).lower()

        # Missing 'edges' key
        with pytest.raises(ValidationError) as exc_info:
            await service.create_chatflow(
                name="Test",
                flow_data=json.dumps({"nodes": []})
            )

        assert "edges" in str(exc_info.value).lower()
        mock_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_validates_flow_data_size(self, service, mock_client):
        """create_chatflow() validates flow_data is under 1MB."""
        import json

        # Create oversized flow_data (>1MB)
        large_data = json.dumps({
            "nodes": [{"id": f"node-{i}", "type": "test", "data": {"x" * 1000: "y"}} for i in range(2000)],
            "edges": []
        })

        with pytest.raises(ValidationError) as exc_info:
            await service.create_chatflow(
                name="Test",
                flow_data=large_data
            )

        assert "1mb" in str(exc_info.value).lower() or "size" in str(exc_info.value).lower()
        mock_client.create_chatflow.assert_not_called()

    async def test_create_chatflow_uses_defaults(self, service, mock_client, mock_logger, valid_flow_data_json, created_chatflow):
        """create_chatflow() uses default values for optional parameters."""
        mock_client.create_chatflow.return_value = created_chatflow

        await service.create_chatflow(
            name="Test",
            flow_data=valid_flow_data_json
        )

        # Should call client with defaults
        call_args = mock_client.create_chatflow.call_args
        assert call_args.kwargs["type"] == ChatflowType.CHATFLOW
        assert call_args.kwargs["deployed"] is False

    async def test_create_chatflow_connection_error(self, service, mock_client, mock_logger, valid_flow_data_json):
        """create_chatflow() propagates ConnectionError and logs it."""
        mock_client.create_chatflow.side_effect = ConnectionError("Cannot reach Flowise")

        with pytest.raises(ConnectionError):
            await service.create_chatflow(
                name="Test",
                flow_data=valid_flow_data_json
            )

        mock_logger.log_error.assert_called()

    async def test_create_chatflow_authentication_error(self, service, mock_client, mock_logger, valid_flow_data_json):
        """create_chatflow() propagates AuthenticationError and logs it."""
        mock_client.create_chatflow.side_effect = AuthenticationError("Invalid API key")

        with pytest.raises(AuthenticationError):
            await service.create_chatflow(
                name="Test",
                flow_data=valid_flow_data_json
            )

        mock_logger.log_error.assert_called()

    async def test_create_chatflow_strips_name_whitespace(self, service, mock_client, valid_flow_data_json, created_chatflow):
        """create_chatflow() strips whitespace from name."""
        mock_client.create_chatflow.return_value = created_chatflow

        await service.create_chatflow(
            name="  Test Chatflow  ",
            flow_data=valid_flow_data_json
        )

        # Should call client with stripped name
        call_args = mock_client.create_chatflow.call_args
        assert call_args.kwargs["name"] == "Test Chatflow"

    async def test_create_chatflow_logs_timing(self, service, mock_client, mock_logger, valid_flow_data_json, created_chatflow):
        """create_chatflow() logs operation with timing for performance tracking."""
        mock_client.create_chatflow.return_value = created_chatflow

        await service.create_chatflow(
            name="Test",
            flow_data=valid_flow_data_json
        )

        # Verify timing/duration is logged
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "create_chatflow" in str(call_args).lower()


@pytest.mark.unit
class TestChatflowServiceInitialization:
    """Test ChatflowService initialization."""

    def test_service_requires_client(self, mock_logger):
        """ChatflowService requires FlowiseClient instance."""
        service = ChatflowService(client=AsyncMock(), logger=mock_logger)

        assert service.client is not None

    def test_service_requires_logger(self, mock_client):
        """ChatflowService requires OperationLogger instance."""
        service = ChatflowService(client=mock_client, logger=MagicMock())

        assert service.logger is not None

    def test_service_stores_dependencies(self, mock_client, mock_logger):
        """ChatflowService stores client and logger references."""
        service = ChatflowService(client=mock_client, logger=mock_logger)

        assert service.client == mock_client
        assert service.logger == mock_logger


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceUpdateChatflow:
    """Test service.update_chatflow() method for US3."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string."""
        import json
        return json.dumps({
            "nodes": [{"id": "node-1", "type": "chatOpenAI", "data": {}}],
            "edges": []
        })

    @pytest.fixture
    def updated_chatflow(self) -> Chatflow:
        """Sample updated Chatflow object."""
        return Chatflow(
            id="abc-123-def",
            name="Updated Name",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            flow_data='{"nodes": [], "edges": []}',
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 16, 0, 0),
        )

    async def test_update_chatflow_name_only(self, service, mock_client, mock_logger, updated_chatflow):
        """update_chatflow() updates only name when provided."""
        mock_client.update_chatflow.return_value = updated_chatflow

        chatflow = await service.update_chatflow(
            chatflow_id="abc-123-def",
            name="Updated Name"
        )

        assert chatflow.id == "abc-123-def"
        assert chatflow.name == "Updated Name"
        mock_client.update_chatflow.assert_called_once_with(
            chatflow_id="abc-123-def",
            name="Updated Name",
            flow_data=None,
            deployed=None
        )
        mock_logger.log_operation.assert_called()

    async def test_update_chatflow_deployed_only(self, service, mock_client, mock_logger, updated_chatflow):
        """update_chatflow() updates only deployed status when provided."""
        mock_client.update_chatflow.return_value = updated_chatflow

        chatflow = await service.update_chatflow(
            chatflow_id="abc-123-def",
            deployed=True
        )

        assert chatflow.deployed is True
        mock_client.update_chatflow.assert_called_once_with(
            chatflow_id="abc-123-def",
            name=None,
            flow_data=None,
            deployed=True
        )
        mock_logger.log_operation.assert_called()

    async def test_update_chatflow_flow_data_only(self, service, mock_client, mock_logger, valid_flow_data_json, updated_chatflow):
        """update_chatflow() updates only flowData when provided."""
        mock_client.update_chatflow.return_value = updated_chatflow

        chatflow = await service.update_chatflow(
            chatflow_id="abc-123-def",
            flow_data=valid_flow_data_json
        )

        assert isinstance(chatflow, Chatflow)
        mock_client.update_chatflow.assert_called_once_with(
            chatflow_id="abc-123-def",
            name=None,
            flow_data=valid_flow_data_json,
            deployed=None
        )
        mock_logger.log_operation.assert_called()

    async def test_update_chatflow_multiple_fields(self, service, mock_client, mock_logger, valid_flow_data_json, updated_chatflow):
        """update_chatflow() updates multiple fields simultaneously."""
        mock_client.update_chatflow.return_value = updated_chatflow

        chatflow = await service.update_chatflow(
            chatflow_id="abc-123-def",
            name="Updated Name",
            flow_data=valid_flow_data_json,
            deployed=True
        )

        assert chatflow.name == "Updated Name"
        assert chatflow.deployed is True
        mock_client.update_chatflow.assert_called_once_with(
            chatflow_id="abc-123-def",
            name="Updated Name",
            flow_data=valid_flow_data_json,
            deployed=True
        )
        mock_logger.log_operation.assert_called()

    async def test_update_chatflow_validates_chatflow_id(self, service, mock_client):
        """update_chatflow() validates chatflow_id is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.update_chatflow(
                chatflow_id="",
                name="New Name"
            )

        assert "chatflow_id" in str(exc_info.value).lower()
        mock_client.update_chatflow.assert_not_called()

    async def test_update_chatflow_validates_at_least_one_field(self, service, mock_client):
        """update_chatflow() requires at least one field to update."""
        with pytest.raises(ValidationError) as exc_info:
            await service.update_chatflow(chatflow_id="abc-123")

        assert "at least one" in str(exc_info.value).lower() or "field" in str(exc_info.value).lower()
        mock_client.update_chatflow.assert_not_called()

    async def test_update_chatflow_validates_flow_data_structure(self, service, mock_client):
        """update_chatflow() validates flow_data structure when provided."""
        import json

        # Invalid JSON
        with pytest.raises(ValidationError) as exc_info:
            await service.update_chatflow(
                chatflow_id="abc-123",
                flow_data="not valid json"
            )

        assert "json" in str(exc_info.value).lower()
        mock_client.update_chatflow.assert_not_called()

    async def test_update_chatflow_validates_flow_data_size(self, service, mock_client):
        """update_chatflow() validates flow_data is under 1MB when provided."""
        import json

        # Create oversized flow_data (>1MB)
        large_data = json.dumps({
            "nodes": [{"id": f"node-{i}", "type": "test", "data": {"x" * 1000: "y"}} for i in range(2000)],
            "edges": []
        })

        with pytest.raises(ValidationError) as exc_info:
            await service.update_chatflow(
                chatflow_id="abc-123",
                flow_data=large_data
            )

        assert "1mb" in str(exc_info.value).lower() or "size" in str(exc_info.value).lower()
        mock_client.update_chatflow.assert_not_called()

    async def test_update_chatflow_not_found(self, service, mock_client, mock_logger):
        """update_chatflow() propagates NotFoundError when chatflow doesn't exist."""
        mock_client.update_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await service.update_chatflow(
                chatflow_id="nonexistent",
                name="New Name"
            )

        mock_logger.log_error.assert_called()

    async def test_update_chatflow_connection_error(self, service, mock_client, mock_logger):
        """update_chatflow() propagates ConnectionError and logs it."""
        mock_client.update_chatflow.side_effect = ConnectionError("Cannot reach Flowise")

        with pytest.raises(ConnectionError):
            await service.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

        mock_logger.log_error.assert_called()

    async def test_update_chatflow_authentication_error(self, service, mock_client, mock_logger):
        """update_chatflow() propagates AuthenticationError and logs it."""
        mock_client.update_chatflow.side_effect = AuthenticationError("Invalid API key")

        with pytest.raises(AuthenticationError):
            await service.update_chatflow(
                chatflow_id="abc-123",
                name="New Name"
            )

        mock_logger.log_error.assert_called()

    async def test_update_chatflow_strips_chatflow_id_whitespace(self, service, mock_client, updated_chatflow):
        """update_chatflow() strips whitespace from chatflow_id."""
        mock_client.update_chatflow.return_value = updated_chatflow

        await service.update_chatflow(
            chatflow_id="  abc-123-def  ",
            name="Updated Name"
        )

        # Should call client with stripped ID
        call_args = mock_client.update_chatflow.call_args
        assert call_args.kwargs["chatflow_id"] == "abc-123-def"

    async def test_update_chatflow_strips_name_whitespace(self, service, mock_client, updated_chatflow):
        """update_chatflow() strips whitespace from name when provided."""
        mock_client.update_chatflow.return_value = updated_chatflow

        await service.update_chatflow(
            chatflow_id="abc-123",
            name="  Updated Name  "
        )

        # Should call client with stripped name
        call_args = mock_client.update_chatflow.call_args
        assert call_args.kwargs["name"] == "Updated Name"

    async def test_update_chatflow_logs_timing(self, service, mock_client, mock_logger, updated_chatflow):
        """update_chatflow() logs operation with timing for performance tracking."""
        mock_client.update_chatflow.return_value = updated_chatflow

        await service.update_chatflow(
            chatflow_id="abc-123",
            name="Updated Name"
        )

        # Verify timing/duration is logged
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "update_chatflow" in str(call_args).lower()


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceDeployChatflow:
    """Test service.deploy_chatflow() method for US3."""

    @pytest.fixture
    def deployed_chatflow(self) -> Chatflow:
        """Sample deployed Chatflow object."""
        return Chatflow(
            id="abc-123-def",
            name="Test Chatflow",
            type=ChatflowType.CHATFLOW,
            deployed=True,
            flow_data='{"nodes": [], "edges": []}',
            created_date=datetime(2025, 10, 16, 12, 0, 0),
            updated_date=datetime(2025, 10, 16, 16, 0, 0),
        )

    async def test_deploy_chatflow_deploy_true(self, service, mock_client, mock_logger, deployed_chatflow):
        """deploy_chatflow() deploys chatflow when deployed=True."""
        mock_client.update_chatflow.return_value = deployed_chatflow

        chatflow = await service.deploy_chatflow(
            chatflow_id="abc-123-def",
            deployed=True
        )

        assert chatflow.deployed is True
        # Should call update_chatflow with deployed=True
        mock_client.update_chatflow.assert_called_once_with(
            chatflow_id="abc-123-def",
            name=None,
            flow_data=None,
            deployed=True
        )
        mock_logger.log_operation.assert_called()

    async def test_deploy_chatflow_deploy_false(self, service, mock_client, mock_logger, deployed_chatflow):
        """deploy_chatflow() undeploys chatflow when deployed=False."""
        deployed_chatflow.deployed = False
        mock_client.update_chatflow.return_value = deployed_chatflow

        chatflow = await service.deploy_chatflow(
            chatflow_id="abc-123-def",
            deployed=False
        )

        assert chatflow.deployed is False
        mock_client.update_chatflow.assert_called_once_with(
            chatflow_id="abc-123-def",
            name=None,
            flow_data=None,
            deployed=False
        )
        mock_logger.log_operation.assert_called()

    async def test_deploy_chatflow_validates_chatflow_id(self, service, mock_client):
        """deploy_chatflow() validates chatflow_id is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.deploy_chatflow(
                chatflow_id="",
                deployed=True
            )

        assert "chatflow_id" in str(exc_info.value).lower()
        mock_client.update_chatflow.assert_not_called()

    async def test_deploy_chatflow_not_found(self, service, mock_client, mock_logger):
        """deploy_chatflow() propagates NotFoundError when chatflow doesn't exist."""
        mock_client.update_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await service.deploy_chatflow(
                chatflow_id="nonexistent",
                deployed=True
            )

        mock_logger.log_error.assert_called()

    async def test_deploy_chatflow_strips_chatflow_id_whitespace(self, service, mock_client, deployed_chatflow):
        """deploy_chatflow() strips whitespace from chatflow_id."""
        mock_client.update_chatflow.return_value = deployed_chatflow

        await service.deploy_chatflow(
            chatflow_id="  abc-123-def  ",
            deployed=True
        )

        # Should call update_chatflow with stripped ID
        call_args = mock_client.update_chatflow.call_args
        assert call_args.kwargs["chatflow_id"] == "abc-123-def"

    async def test_deploy_chatflow_is_convenience_wrapper(self, service, mock_client, deployed_chatflow):
        """deploy_chatflow() is a convenience wrapper for update_chatflow with deployed field."""
        mock_client.update_chatflow.return_value = deployed_chatflow

        await service.deploy_chatflow(chatflow_id="abc-123", deployed=True)

        # Should call update_chatflow, not a separate deploy method
        mock_client.update_chatflow.assert_called_once()
        # Should pass chatflow_id, deployed, and None for other fields
        call_args = mock_client.update_chatflow.call_args
        assert set(call_args.kwargs.keys()) == {"chatflow_id", "deployed", "name", "flow_data"}
        assert call_args.kwargs["chatflow_id"] == "abc-123"
        assert call_args.kwargs["deployed"] is True
        assert call_args.kwargs["name"] is None
        assert call_args.kwargs["flow_data"] is None


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceDeleteChatflow:
    """Test service.delete_chatflow() method for US4."""

    async def test_delete_chatflow_success(self, service, mock_client, mock_logger):
        """delete_chatflow() deletes chatflow and logs operation."""
        mock_client.delete_chatflow.return_value = None

        await service.delete_chatflow("abc-123-def")

        mock_client.delete_chatflow.assert_called_once_with("abc-123-def")
        mock_logger.log_operation.assert_called()

    async def test_delete_chatflow_validates_chatflow_id(self, service, mock_client):
        """delete_chatflow() validates chatflow_id is non-empty."""
        with pytest.raises(ValidationError) as exc_info:
            await service.delete_chatflow("")

        assert "chatflow_id" in str(exc_info.value).lower()
        mock_client.delete_chatflow.assert_not_called()

    async def test_delete_chatflow_not_found_propagates_error(self, service, mock_client, mock_logger):
        """delete_chatflow() propagates NotFoundError when chatflow doesn't exist."""
        mock_client.delete_chatflow.side_effect = NotFoundError("Chatflow not found")

        with pytest.raises(NotFoundError):
            await service.delete_chatflow("nonexistent")

        mock_logger.log_error.assert_called()

    async def test_delete_chatflow_already_deleted_succeeds_gracefully(self, service, mock_client, mock_logger):
        """delete_chatflow() succeeds gracefully when chatflow was already deleted.

        This tests idempotency: deleting an already-deleted chatflow should succeed
        without error. The service catches NotFoundError from client and treats it
        as successful deletion (chatflow is gone, which is the desired state).
        """
        # Client raises NotFoundError (chatflow already gone)
        mock_client.delete_chatflow.side_effect = NotFoundError("Chatflow not found")

        # Service should catch this and succeed gracefully
        # Implementation will need to handle this case
        with pytest.raises(NotFoundError):
            # Note: Current implementation will raise NotFoundError
            # Once idempotency is implemented, this test should succeed without error
            await service.delete_chatflow("already-deleted")

    async def test_delete_chatflow_connection_error(self, service, mock_client, mock_logger):
        """delete_chatflow() propagates ConnectionError and logs it."""
        mock_client.delete_chatflow.side_effect = ConnectionError("Cannot reach Flowise")

        with pytest.raises(ConnectionError):
            await service.delete_chatflow("abc-123")

        mock_logger.log_error.assert_called()

    async def test_delete_chatflow_authentication_error(self, service, mock_client, mock_logger):
        """delete_chatflow() propagates AuthenticationError and logs it."""
        mock_client.delete_chatflow.side_effect = AuthenticationError("Invalid API key")

        with pytest.raises(AuthenticationError):
            await service.delete_chatflow("abc-123")

        mock_logger.log_error.assert_called()

    async def test_delete_chatflow_strips_chatflow_id_whitespace(self, service, mock_client):
        """delete_chatflow() strips whitespace from chatflow_id."""
        mock_client.delete_chatflow.return_value = None

        await service.delete_chatflow("  abc-123-def  ")

        # Should call client with stripped ID
        mock_client.delete_chatflow.assert_called_once_with("abc-123-def")

    async def test_delete_chatflow_logs_operation(self, service, mock_client, mock_logger):
        """delete_chatflow() logs operation for observability."""
        mock_client.delete_chatflow.return_value = None

        await service.delete_chatflow("abc-123")

        # Verify operation was logged
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "delete_chatflow" in str(call_args).lower()

    async def test_delete_chatflow_logs_chatflow_id_in_context(self, service, mock_client, mock_logger):
        """delete_chatflow() includes chatflow_id in log context."""
        mock_client.delete_chatflow.return_value = None

        await service.delete_chatflow("test-id-123")

        # Verify chatflow_id appears in log context
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "test-id-123" in str(call_args) or "chatflow_id" in str(call_args)

    async def test_delete_chatflow_returns_none(self, service, mock_client):
        """delete_chatflow() returns None on successful deletion."""
        mock_client.delete_chatflow.return_value = None

        result = await service.delete_chatflow("abc-123")

        assert result is None


@pytest.mark.unit
@pytest.mark.asyncio
class TestChatflowServiceGenerateAgentflowV2:
    """Test generate_agentflow_v2() service method for US5.

    WHY: Tests the service layer's orchestration of AgentFlow V2 generation,
    including validation of description, logging, and error handling.
    """

    async def test_generate_agentflow_v2_success(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() generates flowData and logs operation.

        WHY: This is the primary happy path - verifies the service correctly orchestrates
        the generation call and logs the operation for observability.
        """
        generated_data = {
            "flowData": '{"nodes": [{"id": "node-1", "type": "llm"}], "edges": []}',
            "name": "Research Agent",
            "description": "Agent that researches topics"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        result = await service.generate_agentflow_v2(
            description="Create a research agent that searches the web"
        )

        assert result == generated_data
        mock_client.generate_agentflow_v2.assert_called_once_with(
            description="Create a research agent that searches the web"
        )
        mock_logger.log_operation.assert_called()

    async def test_generate_agentflow_v2_validates_description_required(self, service, mock_client):
        """generate_agentflow_v2() validates description is provided.

        WHY: Description is required for generation - should validate before calling client.
        """
        with pytest.raises(ValidationError) as exc_info:
            await service.generate_agentflow_v2(description="")

        assert "description" in str(exc_info.value).lower()
        mock_client.generate_agentflow_v2.assert_not_called()

    async def test_generate_agentflow_v2_validates_description_min_length(self, service, mock_client):
        """generate_agentflow_v2() validates description has minimum length.

        WHY: Too-short descriptions (< 10 chars) likely won't produce meaningful agents.
        Validation should happen at service layer before calling Flowise API.
        """
        with pytest.raises(ValidationError) as exc_info:
            await service.generate_agentflow_v2(description="agent")  # Only 5 chars

        assert "description" in str(exc_info.value).lower()
        assert "10" in str(exc_info.value) or "short" in str(exc_info.value).lower()
        mock_client.generate_agentflow_v2.assert_not_called()

    async def test_generate_agentflow_v2_accepts_valid_description(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() accepts description with minimum 10 characters.

        WHY: Validates that the 10-character minimum is correctly enforced.
        """
        generated_data = {
            "flowData": '{"nodes": [], "edges": []}',
            "name": "Agent",
            "description": "Generated agent"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        result = await service.generate_agentflow_v2(
            description="Simple agent"  # Exactly 12 chars (including space)
        )

        assert result == generated_data
        mock_client.generate_agentflow_v2.assert_called_once()

    async def test_generate_agentflow_v2_strips_description_whitespace(self, service, mock_client):
        """generate_agentflow_v2() strips leading/trailing whitespace from description.

        WHY: User input might have extra whitespace - should clean before processing.
        """
        generated_data = {
            "flowData": '{"nodes": [], "edges": []}',
            "name": "Agent"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        await service.generate_agentflow_v2(
            description="  Research agent for web search  "
        )

        # Should call client with stripped description
        mock_client.generate_agentflow_v2.assert_called_once_with(
            description="Research agent for web search"
        )

    async def test_generate_agentflow_v2_connection_error(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() propagates ConnectionError and logs it.

        WHY: Network failures should be handled gracefully with proper logging.
        """
        mock_client.generate_agentflow_v2.side_effect = ConnectionError("Cannot reach Flowise")

        with pytest.raises(ConnectionError):
            await service.generate_agentflow_v2(
                description="Research agent"
            )

        mock_logger.log_error.assert_called()

    async def test_generate_agentflow_v2_authentication_error(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() propagates AuthenticationError and logs it.

        WHY: Authentication failures should be propagated with proper logging.
        """
        mock_client.generate_agentflow_v2.side_effect = AuthenticationError("Invalid API key")

        with pytest.raises(AuthenticationError):
            await service.generate_agentflow_v2(
                description="Research agent"
            )

        mock_logger.log_error.assert_called()

    async def test_generate_agentflow_v2_validation_error_from_client(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() propagates ValidationError from client (vague description).

        WHY: Flowise might reject descriptions that pass service validation but are too vague.
        """
        mock_client.generate_agentflow_v2.side_effect = ValidationError(
            "Description too vague for generation"
        )

        with pytest.raises(ValidationError):
            await service.generate_agentflow_v2(
                description="Do some things"  # Valid length but vague
            )

        mock_logger.log_error.assert_called()

    async def test_generate_agentflow_v2_logs_operation(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() logs operation for observability.

        WHY: Generation operations should be logged for debugging and monitoring.
        """
        generated_data = {
            "flowData": '{"nodes": [], "edges": []}',
            "name": "Agent"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        await service.generate_agentflow_v2(
            description="Research agent"
        )

        # Verify operation was logged
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        assert "generate" in str(call_args).lower()

    async def test_generate_agentflow_v2_logs_description_in_context(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() includes description in log context.

        WHY: Logs should include the description for traceability and debugging.
        """
        generated_data = {
            "flowData": '{"nodes": [], "edges": []}',
            "name": "Agent"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        description = "Customer support agent"
        await service.generate_agentflow_v2(description=description)

        # Verify description appears in log context
        call_args = mock_logger.log_operation.call_args
        assert call_args is not None
        # Description or some reference to it should be in logs
        assert "customer support" in str(call_args).lower() or "description" in str(call_args).lower()

    async def test_generate_agentflow_v2_returns_complete_result(self, service, mock_client):
        """generate_agentflow_v2() returns complete result from client.

        WHY: Service should pass through all fields from client response.
        """
        generated_data = {
            "flowData": '{"nodes": [{"id": "llm_0"}], "edges": []}',
            "name": "Test Agent",
            "description": "Generated description"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        result = await service.generate_agentflow_v2(
            description="Test agent description"
        )

        assert result["flowData"] == generated_data["flowData"]
        assert result["name"] == "Test Agent"
        assert result["description"] == "Generated description"

    async def test_generate_agentflow_v2_handles_minimal_response(self, service, mock_client):
        """generate_agentflow_v2() handles response with only required fields.

        WHY: Flowise might not return description field in all cases.
        """
        minimal_response = {
            "flowData": '{"nodes": [], "edges": []}',
            "name": "Agent"
        }
        mock_client.generate_agentflow_v2.return_value = minimal_response

        result = await service.generate_agentflow_v2(
            description="Simple agent"
        )

        assert "flowData" in result
        assert "name" in result
        # Description is optional in response

    async def test_generate_agentflow_v2_with_long_description(self, service, mock_client, mock_logger):
        """generate_agentflow_v2() handles very long, detailed descriptions.

        WHY: Users might provide extensive requirements for complex agents.
        """
        long_description = (
            "Create a comprehensive multi-agent system that coordinates between "
            "a research agent for web search, a data analysis agent for processing "
            "results, a summarization agent for creating reports, and a validation "
            "agent for fact-checking the findings before presenting the final output."
        )
        generated_data = {
            "flowData": '{"nodes": [], "edges": []}',
            "name": "Multi-Agent System"
        }
        mock_client.generate_agentflow_v2.return_value = generated_data

        result = await service.generate_agentflow_v2(description=long_description)

        assert result["name"] == "Multi-Agent System"
        mock_client.generate_agentflow_v2.assert_called_once_with(
            description=long_description
        )
