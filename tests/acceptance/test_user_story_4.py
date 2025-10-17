"""Acceptance tests for User Story 4: Delete Chatflows.

User Story 4 (Priority P4): AI assistants need to permanently remove chatflows
that are no longer needed to maintain clean workspace and manage resource usage.

Acceptance Scenarios:
1. Given an existing chatflow ID, When AI assistant calls delete_chatflow,
   Then chatflow is permanently removed
2. Given a deleted chatflow ID, When AI assistant calls get_chatflow,
   Then "not found" error is returned
3. Given a non-existent chatflow ID, When AI assistant calls delete_chatflow,
   Then appropriate error message is returned
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from fluent_mind_mcp.client.exceptions import NotFoundError
from fluent_mind_mcp.models import Chatflow, ChatflowType, FlowiseConfig
from fluent_mind_mcp.services.chatflow_service import ChatflowService


@pytest.fixture
def mock_client():
    """Mock FlowiseClient for acceptance tests."""
    client = AsyncMock()
    client.list_chatflows = AsyncMock()
    client.get_chatflow = AsyncMock()
    client.create_chatflow = AsyncMock()
    client.delete_chatflow = AsyncMock()
    return client


@pytest.fixture
def mock_logger():
    """Mock OperationLogger for acceptance tests."""
    logger = MagicMock()

    # Create async context manager mock for log_operation
    async_cm = MagicMock()
    async_cm.__aenter__ = AsyncMock(return_value={})
    async_cm.__aexit__ = AsyncMock(return_value=None)
    logger.log_operation = MagicMock(return_value=async_cm)

    logger.log_error = MagicMock()
    logger.time_operation = MagicMock()
    logger.time_operation.return_value.__enter__ = MagicMock()
    logger.time_operation.return_value.__exit__ = MagicMock()
    return logger


@pytest.fixture
def service(mock_client, mock_logger):
    """ChatflowService for acceptance tests."""
    return ChatflowService(client=mock_client, logger=mock_logger)


@pytest.fixture
def sample_chatflow():
    """Sample chatflow for deletion tests."""
    return Chatflow(
        id="test-chatflow-delete-123",
        name="Test Chatflow for Deletion",
        type=ChatflowType.CHATFLOW,
        deployed=False,
        flow_data=json.dumps({
            "nodes": [{"id": "node-1", "type": "llm", "data": {}}],
            "edges": []
        }),
    )


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUserStory4DeleteChatflows:
    """Acceptance tests for User Story 4: Delete Chatflows (P4)."""

    async def test_scenario_1_delete_existing_chatflow(self, service, mock_client, sample_chatflow):
        """
        Scenario 1: Delete existing chatflow

        GIVEN: An existing chatflow ID
        WHEN: AI assistant calls delete_chatflow
        THEN: Chatflow is permanently removed
        """
        chatflow_id = sample_chatflow.id

        # Setup: Chatflow exists before deletion
        mock_client.get_chatflow.return_value = sample_chatflow
        mock_client.delete_chatflow.return_value = None

        # AI assistant checks chatflow exists
        existing_chatflow = await service.get_chatflow(chatflow_id)
        assert existing_chatflow.id == chatflow_id
        assert existing_chatflow.name == "Test Chatflow for Deletion"

        # AI assistant deletes chatflow
        await service.delete_chatflow(chatflow_id)

        # Verify delete was called with correct ID
        mock_client.delete_chatflow.assert_called_once_with(chatflow_id)

        # Simulate chatflow is now gone (list doesn't contain it)
        mock_client.list_chatflows.return_value = []

        # AI assistant verifies chatflow was removed from list
        chatflows = await service.list_chatflows()
        assert not any(cf.id == chatflow_id for cf in chatflows)

        print(f"✅ Scenario 1 passed: Chatflow {chatflow_id} was successfully deleted")

    async def test_scenario_2_get_deleted_chatflow_returns_not_found(
        self, service, mock_client, sample_chatflow
    ):
        """
        Scenario 2: Get deleted chatflow returns not found error

        GIVEN: A deleted chatflow ID
        WHEN: AI assistant calls get_chatflow
        THEN: "not found" error is returned
        """
        chatflow_id = sample_chatflow.id

        # Setup: Chatflow was deleted (get_chatflow raises NotFoundError)
        mock_client.delete_chatflow.return_value = None
        mock_client.get_chatflow.side_effect = NotFoundError(f"Chatflow {chatflow_id} not found")

        # AI assistant deletes chatflow
        await service.delete_chatflow(chatflow_id)

        # AI assistant tries to get deleted chatflow
        with pytest.raises(NotFoundError) as exc_info:
            await service.get_chatflow(chatflow_id)

        # Verify error message indicates chatflow was not found
        error_message = str(exc_info.value).lower()
        assert "not found" in error_message or chatflow_id in error_message

        print(f"✅ Scenario 2 passed: get_chatflow correctly returns 'not found' for deleted chatflow")

    async def test_scenario_3_delete_nonexistent_chatflow_returns_error(
        self, service, mock_client
    ):
        """
        Scenario 3: Delete non-existent chatflow returns error

        GIVEN: A non-existent chatflow ID
        WHEN: AI assistant calls delete_chatflow
        THEN: Appropriate error message is returned
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"

        # Setup: Chatflow doesn't exist (delete raises NotFoundError)
        mock_client.delete_chatflow.side_effect = NotFoundError(
            f"Chatflow {nonexistent_id} not found"
        )

        # AI assistant tries to delete non-existent chatflow
        with pytest.raises(NotFoundError) as exc_info:
            await service.delete_chatflow(nonexistent_id)

        # Verify appropriate error message is returned
        error_message = str(exc_info.value).lower()
        assert "not found" in error_message or nonexistent_id in error_message

        print(f"✅ Scenario 3 passed: delete_chatflow correctly returns error for non-existent chatflow")

    async def test_us4_complete_deletion_workflow(self, service, mock_client, sample_chatflow):
        """
        Complete User Story 4 workflow: Create → Delete → Verify Gone

        This comprehensive test validates the full deletion lifecycle:
        1. Create a test chatflow
        2. Verify it exists in the list
        3. Delete the chatflow
        4. Verify it no longer appears in list
        5. Verify get_chatflow returns NotFoundError
        """
        chatflow_id = sample_chatflow.id

        # Step 1: AI assistant creates test chatflow
        mock_client.create_chatflow.return_value = sample_chatflow
        created = await service.create_chatflow(
            name="Test Chatflow for Deletion",
            flow_data=sample_chatflow.flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False,
        )
        assert created.id == chatflow_id
        print(f"✅ Step 1: Created test chatflow {chatflow_id}")

        # Step 2: Verify chatflow appears in list
        mock_client.list_chatflows.return_value = [sample_chatflow]
        chatflows = await service.list_chatflows()
        assert any(cf.id == chatflow_id for cf in chatflows)
        print(f"✅ Step 2: Chatflow {chatflow_id} appears in list")

        # Step 3: Delete chatflow
        mock_client.delete_chatflow.return_value = None
        await service.delete_chatflow(chatflow_id)
        print(f"✅ Step 3: Deleted chatflow {chatflow_id}")

        # Step 4: Verify chatflow no longer in list
        mock_client.list_chatflows.return_value = []
        chatflows = await service.list_chatflows()
        assert not any(cf.id == chatflow_id for cf in chatflows)
        print(f"✅ Step 4: Chatflow {chatflow_id} no longer in list")

        # Step 5: Verify get_chatflow returns NotFoundError
        mock_client.get_chatflow.side_effect = NotFoundError(f"Chatflow {chatflow_id} not found")
        with pytest.raises(NotFoundError):
            await service.get_chatflow(chatflow_id)
        print(f"✅ Step 5: get_chatflow correctly returns NotFoundError")

        print(f"✅ Complete US4 workflow validated: Deletion lifecycle works end-to-end")

    async def test_us4_deletion_workspace_hygiene(self, service, mock_client):
        """
        User Story 4 Value: Maintain clean workspace and manage resource usage

        This test validates that deletion enables workspace hygiene by:
        1. Creating multiple test chatflows
        2. Deleting some of them
        3. Verifying only non-deleted chatflows remain
        """
        # Create 5 test chatflows
        chatflows = [
            Chatflow(
                id=f"test-chatflow-{i}",
                name=f"Test Chatflow {i}",
                type=ChatflowType.CHATFLOW,
                deployed=False,
                flow_data=json.dumps({"nodes": [], "edges": []}),
            )
            for i in range(5)
        ]

        mock_client.list_chatflows.return_value = chatflows
        all_chatflows = await service.list_chatflows()
        assert len(all_chatflows) == 5
        print(f"✅ Created 5 test chatflows")

        # Delete chatflows 1, 2, 3 (keep 0 and 4)
        mock_client.delete_chatflow.return_value = None
        for i in [1, 2, 3]:
            await service.delete_chatflow(f"test-chatflow-{i}")
        print(f"✅ Deleted 3 chatflows (test-chatflow-1, 2, 3)")

        # Verify only chatflows 0 and 4 remain
        remaining_chatflows = [chatflows[0], chatflows[4]]
        mock_client.list_chatflows.return_value = remaining_chatflows
        final_list = await service.list_chatflows()

        assert len(final_list) == 2
        assert any(cf.id == "test-chatflow-0" for cf in final_list)
        assert any(cf.id == "test-chatflow-4" for cf in final_list)
        assert not any(cf.id == "test-chatflow-1" for cf in final_list)
        assert not any(cf.id == "test-chatflow-2" for cf in final_list)
        assert not any(cf.id == "test-chatflow-3" for cf in final_list)

        print(f"✅ Workspace hygiene maintained: Only non-deleted chatflows remain")

    async def test_us4_deletion_validates_inputs(self, service, mock_client):
        """
        User Story 4 Edge Case: Deletion validates inputs

        This test validates that deletion properly validates inputs:
        1. Empty chatflow ID should be rejected
        2. Whitespace-only ID should be rejected
        3. Proper error messages are returned
        """
        from fluent_mind_mcp.client.exceptions import ValidationError

        # Test 1: Empty chatflow ID
        with pytest.raises(ValidationError) as exc_info:
            await service.delete_chatflow("")
        assert "chatflow_id" in str(exc_info.value).lower()
        print(f"✅ Validation: Empty chatflow_id rejected")

        # Test 2: Whitespace-only ID
        with pytest.raises(ValidationError) as exc_info:
            await service.delete_chatflow("   ")
        assert "chatflow_id" in str(exc_info.value).lower()
        print(f"✅ Validation: Whitespace-only chatflow_id rejected")

        # Verify no delete calls were made for invalid inputs
        mock_client.delete_chatflow.assert_not_called()
        print(f"✅ No delete operations performed for invalid inputs")


@pytest.mark.acceptance
@pytest.mark.asyncio
class TestUserStory4ErrorHandling:
    """Error handling tests for User Story 4."""

    async def test_delete_with_connection_error(self, service, mock_client):
        """
        GIVEN: Network connection to Flowise is unavailable
        WHEN: AI assistant attempts to delete chatflow
        THEN: ConnectionError is raised with clear message
        """
        from fluent_mind_mcp.client.exceptions import ConnectionError as FlowiseConnectionError

        mock_client.delete_chatflow.side_effect = FlowiseConnectionError(
            "Cannot connect to Flowise API"
        )

        with pytest.raises(FlowiseConnectionError) as exc_info:
            await service.delete_chatflow("test-id")

        assert "connect" in str(exc_info.value).lower() or "connection" in str(exc_info.value).lower()
        print(f"✅ ConnectionError properly raised when Flowise unreachable")

    async def test_delete_with_authentication_error(self, service, mock_client):
        """
        GIVEN: Invalid API key configured
        WHEN: AI assistant attempts to delete chatflow
        THEN: AuthenticationError is raised with clear message
        """
        from fluent_mind_mcp.client.exceptions import AuthenticationError

        mock_client.delete_chatflow.side_effect = AuthenticationError(
            "Invalid API key"
        )

        with pytest.raises(AuthenticationError) as exc_info:
            await service.delete_chatflow("test-id")

        assert "auth" in str(exc_info.value).lower() or "api key" in str(exc_info.value).lower()
        print(f"✅ AuthenticationError properly raised for invalid API key")

    async def test_delete_logs_operation_for_observability(self, service, mock_client, mock_logger):
        """
        GIVEN: AI assistant performs deletion operation
        WHEN: Operation completes (success or failure)
        THEN: Operation is logged for observability and debugging
        """
        mock_client.delete_chatflow.return_value = None

        await service.delete_chatflow("test-id")

        # Verify operation was logged
        assert mock_logger.log_operation.called
        call_args = mock_logger.log_operation.call_args
        assert "delete_chatflow" in str(call_args).lower()
        print(f"✅ Deletion operation logged for observability")
