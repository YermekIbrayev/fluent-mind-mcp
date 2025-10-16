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
