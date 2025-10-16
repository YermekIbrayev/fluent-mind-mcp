"""Integration tests for full lifecycle against real Flowise instance.

These tests require a running Flowise instance and test the complete stack:
- FlowiseClient → Flowise API
- ChatflowService → FlowiseClient
- MCP Server → ChatflowService

Tests can be skipped if Flowise is not available using pytest markers.
"""

import os
from datetime import datetime

import pytest

from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.client.exceptions import NotFoundError
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.models import FlowiseConfig
from fluent_mind_mcp.services.chatflow_service import ChatflowService


# Skip all integration tests if FLOWISE_API_URL not set
# Note: Individual tests can override this by setting their own skipif
pytestmark = pytest.mark.skipif(
    not os.getenv("FLOWISE_API_URL"), reason="FLOWISE_API_URL not configured for integration tests"
)


@pytest.fixture
def config():
    """Load FlowiseConfig from environment."""
    return FlowiseConfig.from_env()


@pytest.fixture
async def client(config):
    """FlowiseClient connected to real Flowise instance."""
    client = FlowiseClient(config)
    yield client
    await client.close()


@pytest.fixture
def logger():
    """OperationLogger for integration tests."""
    return OperationLogger("integration_test", level="DEBUG")


@pytest.fixture
def service(client, logger):
    """ChatflowService for integration tests."""
    return ChatflowService(client=client, logger=logger)


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationListChatflows:
    """Integration tests for listing chatflows."""

    async def test_list_chatflows_returns_real_data(self, client):
        """
        GIVEN: Real Flowise instance with chatflows
        WHEN: Client lists chatflows
        THEN: Returns actual chatflow data from database
        """
        chatflows = await client.list_chatflows()

        # Should get list (may be empty if no chatflows exist)
        assert isinstance(chatflows, list)

        # If chatflows exist, verify structure
        if len(chatflows) > 0:
            first_chatflow = chatflows[0]
            assert hasattr(first_chatflow, "id")
            assert hasattr(first_chatflow, "name")
            assert hasattr(first_chatflow, "type")
            assert hasattr(first_chatflow, "deployed")
            assert first_chatflow.id  # ID should be non-empty
            assert first_chatflow.name  # Name should be non-empty

    async def test_list_chatflows_through_service(self, service):
        """
        GIVEN: Real Flowise instance
        WHEN: Service lists chatflows
        THEN: Returns chatflows with logging
        """
        chatflows = await service.list_chatflows()

        assert isinstance(chatflows, list)
        # Service should return same data as client

    async def test_list_chatflows_performance(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: Client lists chatflows
        THEN: Completes within 5 seconds (SC-002)
        """
        import time

        start_time = time.time()
        await client.list_chatflows()
        duration = time.time() - start_time

        assert duration < 5.0, f"list_chatflows took {duration}s, expected <5s (SC-002)"


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationGetChatflow:
    """Integration tests for getting chatflow details."""

    async def test_get_chatflow_retrieves_real_chatflow(self, client):
        """
        GIVEN: Real Flowise instance with at least one chatflow
        WHEN: Client gets chatflow by ID
        THEN: Returns complete chatflow data including flowData
        """
        # First, list chatflows to get a valid ID
        chatflows = await client.list_chatflows()
        if len(chatflows) == 0:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id

        # Get detailed chatflow
        chatflow = await client.get_chatflow(chatflow_id)

        assert chatflow.id == chatflow_id
        assert chatflow.name
        assert chatflow.type
        # flowData may be None for some chatflows
        # But if present, should be valid JSON string
        if chatflow.flow_data:
            import json

            flow_data = json.loads(chatflow.flow_data)
            assert "nodes" in flow_data
            assert "edges" in flow_data

    async def test_get_chatflow_not_found_raises_error(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: Client requests nonexistent chatflow
        THEN: Raises NotFoundError
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(NotFoundError):
            await client.get_chatflow(nonexistent_id)

    async def test_get_chatflow_through_service_validates(self, service):
        """
        GIVEN: Real Flowise instance
        WHEN: Service gets chatflow with invalid ID
        THEN: Raises ValidationError before API call
        """
        from fluent_mind_mcp.client.exceptions import ValidationError

        with pytest.raises(ValidationError):
            await service.get_chatflow("")

    async def test_get_chatflow_performance(self, client):
        """
        GIVEN: Real Flowise instance with chatflow
        WHEN: Client gets chatflow details
        THEN: Completes within 5 seconds (SC-002)
        """
        chatflows = await client.list_chatflows()
        if len(chatflows) == 0:
            pytest.skip("No chatflows available for performance testing")

        chatflow_id = chatflows[0].id

        import time

        start_time = time.time()
        await client.get_chatflow(chatflow_id)
        duration = time.time() - start_time

        assert duration < 5.0, f"get_chatflow took {duration}s, expected <5s (SC-002)"


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationRunPrediction:
    """Integration tests for executing chatflows."""

    async def test_run_prediction_executes_real_chatflow(self, client):
        """
        GIVEN: Real Flowise instance with deployed chatflow
        WHEN: Client runs prediction with question
        THEN: Returns actual chatflow response
        """
        # Find a deployed chatflow
        chatflows = await client.list_chatflows()
        deployed_chatflows = [cf for cf in chatflows if cf.deployed]

        if len(deployed_chatflows) == 0:
            pytest.skip("No deployed chatflows available for testing")

        chatflow_id = deployed_chatflows[0].id

        # Execute chatflow
        response = await client.run_prediction(chatflow_id=chatflow_id, question="Hello, this is a test.")

        assert response.text
        assert len(response.text) > 0
        # Response may include session, message IDs
        # These are optional but should be strings if present
        if response.session_id:
            assert isinstance(response.session_id, str)

    async def test_run_prediction_not_found_for_invalid_chatflow(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: Client runs prediction on nonexistent chatflow
        THEN: Raises NotFoundError
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(NotFoundError):
            await client.run_prediction(chatflow_id=nonexistent_id, question="Test")

    async def test_run_prediction_through_service_validates(self, service):
        """
        GIVEN: Real Flowise instance
        WHEN: Service runs prediction with empty question
        THEN: Raises ValidationError before API call
        """
        from fluent_mind_mcp.client.exceptions import ValidationError

        chatflows = await service.list_chatflows()
        if len(chatflows) == 0:
            pytest.skip("No chatflows available")

        with pytest.raises(ValidationError):
            await service.run_prediction(chatflow_id=chatflows[0].id, question="")

    async def test_run_prediction_performance(self, client):
        """
        GIVEN: Real Flowise instance with deployed chatflow
        WHEN: Client runs prediction
        THEN: Completes within 5 seconds (SC-002)

        NOTE: Actual LLM execution time may vary, this tests API response time
        """
        chatflows = await client.list_chatflows()
        deployed_chatflows = [cf for cf in chatflows if cf.deployed]

        if len(deployed_chatflows) == 0:
            pytest.skip("No deployed chatflows for performance testing")

        chatflow_id = deployed_chatflows[0].id

        import time

        start_time = time.time()
        await client.run_prediction(chatflow_id=chatflow_id, question="Quick test")
        duration = time.time() - start_time

        # Note: This may fail if LLM is slow, but tests the target
        assert duration < 5.0, f"run_prediction took {duration}s, expected <5s (SC-002)"


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationFullLifecycle:
    """Test complete workflow: list → get → execute."""

    async def test_complete_lifecycle_with_real_flowise(self, service):
        """
        SCENARIO: Complete user journey against real Flowise
        GIVEN: Real Flowise instance with deployed chatflow
        WHEN: User lists, gets details, and executes chatflow
        THEN: All operations succeed with real data
        """
        # Step 1: List chatflows
        chatflows = await service.list_chatflows()
        assert len(chatflows) > 0, "No chatflows found in Flowise instance"

        # Find a deployed chatflow for execution
        deployed_chatflows = [cf for cf in chatflows if cf.deployed]
        if len(deployed_chatflows) == 0:
            pytest.skip("No deployed chatflows for full lifecycle test")

        chatflow_id = deployed_chatflows[0].id

        # Step 2: Get detailed info
        chatflow_details = await service.get_chatflow(chatflow_id)
        assert chatflow_details.id == chatflow_id
        assert chatflow_details.name

        # Step 3: Execute chatflow
        response = await service.run_prediction(chatflow_id=chatflow_id, question="Integration test question")
        assert response.text
        assert len(response.text) > 0

        # All steps completed successfully
        print(f"✅ Full lifecycle test passed with chatflow: {chatflow_details.name}")

    async def test_full_lifecycle_performance(self, service):
        """
        GIVEN: Real Flowise instance
        WHEN: User completes full lifecycle (list + get + execute)
        THEN: Total time is under 60 seconds (SC-006)
        """
        import time

        chatflows = await service.list_chatflows()
        if len(chatflows) == 0:
            pytest.skip("No chatflows for lifecycle performance test")

        deployed = [cf for cf in chatflows if cf.deployed]
        if len(deployed) == 0:
            pytest.skip("No deployed chatflows for performance test")

        chatflow_id = deployed[0].id

        start_time = time.time()

        # Complete lifecycle
        await service.list_chatflows()
        await service.get_chatflow(chatflow_id)
        await service.run_prediction(chatflow_id=chatflow_id, question="Performance test")

        duration = time.time() - start_time

        assert duration < 60.0, f"Full lifecycle took {duration}s, expected <60s (SC-006)"


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationErrorScenarios:
    """Test error handling with real Flowise instance."""

    async def test_connection_error_with_invalid_url(self):
        """
        GIVEN: Invalid Flowise URL (unreachable host)
        WHEN: Client attempts connection
        THEN: Raises ConnectionError with connection-specific message
        """
        from fluent_mind_mcp.client.exceptions import ConnectionError as FlowiseConnectionError

        # Use a non-routable IP address (RFC 5737 TEST-NET-1)
        # This ensures connection failure without relying on specific port behavior
        # Note: We use model_construct to bypass environment variable loading
        bad_config = FlowiseConfig.model_construct(
            api_url="http://192.0.2.1:3000",
            timeout=2,
            max_connections=10,
            log_level="INFO",
            flowise_version="v1.x"
        )
        client = FlowiseClient(bad_config)

        try:
            with pytest.raises(FlowiseConnectionError) as exc_info:
                await client.list_chatflows()

            # Verify the error message contains connection-related information
            error_message = str(exc_info.value).lower()
            assert any(
                keyword in error_message
                for keyword in ["connect", "timeout", "network", "unreachable"]
            ), f"Expected connection error message, got: {exc_info.value}"
        finally:
            await client.close()

    async def test_authentication_error_with_wrong_key(self):
        """
        GIVEN: Wrong API key configured
        WHEN: Client makes API call
        THEN: Raises AuthenticationError (if Flowise requires auth)

        NOTE: Only runs if Flowise has authentication enabled
        """
        config_dict = {
            "api_url": os.getenv("FLOWISE_API_URL", "http://localhost:3000"),
            "api_key": "wrong-key-12345678",
            "timeout": 30,
        }

        from fluent_mind_mcp.client.exceptions import AuthenticationError

        bad_config = FlowiseConfig(**config_dict)
        client = FlowiseClient(bad_config)

        # This test only makes sense if Flowise requires authentication
        # If no auth required, it will succeed (skip test in that case)
        try:
            await client.list_chatflows()
            pytest.skip("Flowise instance does not require authentication")
        except AuthenticationError:
            pass  # Expected
        finally:
            await client.close()


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationDataConsistency:
    """Test data consistency across operations."""

    async def test_chatflow_list_and_get_match(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: User lists chatflows and gets one by ID
        THEN: Data matches between list and get operations
        """
        chatflows = await client.list_chatflows()
        if len(chatflows) == 0:
            pytest.skip("No chatflows for consistency test")

        # Get first chatflow from list
        list_chatflow = chatflows[0]

        # Get same chatflow by ID
        get_chatflow = await client.get_chatflow(list_chatflow.id)

        # Core fields should match
        assert list_chatflow.id == get_chatflow.id
        assert list_chatflow.name == get_chatflow.name
        assert list_chatflow.type == get_chatflow.type
        assert list_chatflow.deployed == get_chatflow.deployed

        # get_chatflow should have additional detail (flowData)
        # while list_chatflows may not include it
        if get_chatflow.flow_data:
            assert len(get_chatflow.flow_data) > 0
