"""Integration tests for full lifecycle against real Flowise instance.

These tests require a running Flowise instance and test the complete stack:
- FlowiseClient → Flowise API
- ChatflowService → FlowiseClient
- MCP Server → ChatflowService

Tests can be skipped if Flowise is not available using pytest markers.
"""

import json
import os
from datetime import datetime

import pytest

from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.client.exceptions import NotFoundError
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.models import FlowiseConfig
from fluent_mind_mcp.services.chatflow_service import ChatflowService


def get_test_config():
    """Get test configuration from environment.

    WHY: Helper function for skipif decorators to check if Flowise is available.

    Returns:
        tuple: (has_config: bool, api_url: str or None)
    """
    api_url = os.getenv("FLOWISE_API_URL")
    return (bool(api_url), api_url)


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

    async def test_authentication_error_with_wrong_key(self, config):
        """
        GIVEN: Wrong API key configured
        WHEN: Client makes API call
        THEN: Raises AuthenticationError (if Flowise requires auth)

        NOTE: Only runs if Flowise has authentication enabled
        """
        from fluent_mind_mcp.client.exceptions import AuthenticationError

        # Use real API URL but wrong API key
        bad_config = FlowiseConfig(
            api_url=config.api_url,
            api_key="wrong-key-12345678",
            timeout=30,
        )
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


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationCreateChatflow:
    """Integration tests for creating chatflows (User Story 2)."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string for testing."""
        import json
        return json.dumps({
            "nodes": [
                {
                    "id": "chatOpenAI_0",
                    "type": "chatOpenAI",
                    "data": {
                        "name": "chatOpenAI",
                        "model": "gpt-4"
                    },
                    "position": {"x": 250.0, "y": 200.0}
                }
            ],
            "edges": []
        })

    async def test_create_chatflow_against_real_flowise(self, client, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance
        WHEN: Client creates a new chatflow
        THEN: Returns created chatflow with unique ID from Flowise
        """
        from fluent_mind_mcp.models import ChatflowType

        chatflow = await client.create_chatflow(
            name="Integration Test Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        # Should return chatflow with ID assigned by Flowise
        assert chatflow.id
        assert chatflow.name == "Integration Test Chatflow"
        assert chatflow.type == ChatflowType.CHATFLOW
        assert chatflow.deployed is False

        # Clean up: Try to delete (optional, depends on delete implementation)
        # If delete not implemented yet, chatflow will remain in Flowise
        print(f"✅ Created chatflow with ID: {chatflow.id}")

    async def test_create_chatflow_appears_in_list(self, client, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance
        WHEN: Client creates a chatflow
        THEN: Created chatflow appears in subsequent list operation
        """
        from fluent_mind_mcp.models import ChatflowType

        # Create chatflow
        created = await client.create_chatflow(
            name="Test List Integration",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )
        created_id = created.id

        # List chatflows to verify it appears
        chatflows = await client.list_chatflows()

        # Should find the created chatflow
        found = False
        for chatflow in chatflows:
            if chatflow.id == created_id:
                found = True
                assert chatflow.name == "Test List Integration"
                break

        assert found, f"Created chatflow {created_id} not found in list"
        print(f"✅ Created chatflow {created_id} found in list")

    async def test_create_and_retrieve_chatflow(self, client, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance
        WHEN: Client creates a chatflow and retrieves it by ID
        THEN: Retrieved chatflow matches what was created
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        original_flow_data = json.loads(valid_flow_data_json)

        # Create chatflow
        created = await client.create_chatflow(
            name="Test Retrieve Integration",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        # Retrieve chatflow
        retrieved = await client.get_chatflow(created.id)

        # Verify data matches
        assert retrieved.id == created.id
        assert retrieved.name == "Test Retrieve Integration"
        assert retrieved.type == ChatflowType.CHATFLOW
        assert retrieved.deployed is False

        # Verify flowData structure
        if retrieved.flow_data:
            retrieved_flow_data = json.loads(retrieved.flow_data)
            assert "nodes" in retrieved_flow_data
            assert "edges" in retrieved_flow_data
            # Verify node count matches
            assert len(retrieved_flow_data["nodes"]) == len(original_flow_data["nodes"])

        print(f"✅ Created and retrieved chatflow {created.id}")

    async def test_create_chatflow_through_service(self, service, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance
        WHEN: Service creates a chatflow (with validation and logging)
        THEN: Returns created chatflow and logs operation
        """
        from fluent_mind_mcp.models import ChatflowType

        chatflow = await service.create_chatflow(
            name="Service Integration Test",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert chatflow.id
        assert chatflow.name == "Service Integration Test"
        # Service should have logged the operation
        print(f"✅ Service created chatflow {chatflow.id}")

    async def test_create_chatflow_performance(self, client, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance
        WHEN: Client creates a chatflow
        THEN: Completes within 10 seconds (SC-003)
        """
        from fluent_mind_mcp.models import ChatflowType
        import time

        start_time = time.time()

        await client.create_chatflow(
            name="Performance Test Chatflow",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        duration = time.time() - start_time

        assert duration < 10.0, f"create_chatflow took {duration}s, expected <10s (SC-003)"
        print(f"✅ create_chatflow completed in {duration:.2f}s")


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationUS2FullLifecycle:
    """Test complete User Story 2 workflow: create → verify → retrieve."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string for testing."""
        import json
        return json.dumps({
            "nodes": [
                {
                    "id": "conversationChain_0",
                    "type": "conversationChain",
                    "data": {"name": "conversationChain"},
                    "position": {"x": 300.0, "y": 250.0}
                }
            ],
            "edges": []
        })

    async def test_us2_complete_creation_workflow(self, service, valid_flow_data_json):
        """
        SCENARIO: User creates a new chatflow and verifies it exists
        GIVEN: Real Flowise instance
        WHEN: User creates, lists, and retrieves the chatflow
        THEN: All operations succeed with consistent data
        """
        from fluent_mind_mcp.models import ChatflowType
        import time

        start_time = time.time()

        # Step 1: Create new chatflow
        created = await service.create_chatflow(
            name="US2 Full Lifecycle Test",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert created.id
        created_id = created.id
        print(f"✅ Step 1: Created chatflow {created_id}")

        # Step 2: Verify it appears in list
        chatflows = await service.list_chatflows()
        found_in_list = any(cf.id == created_id for cf in chatflows)
        assert found_in_list, "Created chatflow should appear in list"
        print(f"✅ Step 2: Found chatflow in list")

        # Step 3: Retrieve full details
        details = await service.get_chatflow(created_id)
        assert details.id == created_id
        assert details.name == "US2 Full Lifecycle Test"
        assert details.flow_data is not None
        print(f"✅ Step 3: Retrieved chatflow details")

        # Step 4: Verify total time
        duration = time.time() - start_time
        print(f"✅ Complete US2 workflow took {duration:.2f}s")

        # Cleanup note: Chatflow remains in Flowise (delete not implemented yet)
        print(f"⚠️  Note: Chatflow {created_id} remains in Flowise for manual cleanup")


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationUpdateChatflow:
    """Integration tests for updating chatflows (User Story 3)."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string for testing."""
        import json
        return json.dumps({
            "nodes": [
                {
                    "id": "chatOpenAI_updated",
                    "type": "chatOpenAI",
                    "data": {
                        "name": "chatOpenAI_updated",
                        "model": "gpt-4-turbo"
                    },
                    "position": {"x": 300.0, "y": 250.0}
                }
            ],
            "edges": []
        })

    async def test_update_chatflow_name_against_real_flowise(self, client):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Client updates chatflow name
        THEN: Returns updated chatflow with new name from Flowise
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # First, create a chatflow to update
        create_data = json.dumps({
            "nodes": [{"id": "node-1", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="Original Name for Update Test",
            flow_data=create_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} for update test")

        # Now update the name
        updated = await client.update_chatflow(
            chatflow_id=chatflow_id,
            name="Updated Name via Integration Test"
        )

        assert updated.id == chatflow_id
        assert updated.name == "Updated Name via Integration Test"
        print(f"✅ Updated chatflow {chatflow_id} name successfully")

    async def test_update_chatflow_flowdata_against_real_flowise(self, client, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Client updates chatflow flowData
        THEN: Returns updated chatflow with new structure from Flowise
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create a chatflow to update
        original_data = json.dumps({
            "nodes": [{"id": "original-node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="FlowData Update Test",
            flow_data=original_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} for flowData update test")

        # Update the flowData
        updated = await client.update_chatflow(
            chatflow_id=chatflow_id,
            flow_data=valid_flow_data_json
        )

        assert updated.id == chatflow_id
        # Verify flowData was updated
        if updated.flow_data:
            flow_data = json.loads(updated.flow_data)
            assert "chatOpenAI_updated" in str(flow_data)
        print(f"✅ Updated chatflow {chatflow_id} flowData successfully")

    async def test_update_chatflow_deployment_status_against_real_flowise(self, client):
        """
        GIVEN: Real Flowise instance with undeployed chatflow
        WHEN: Client updates deployed status to true
        THEN: Returns updated chatflow with deployed=true from Flowise
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create undeployed chatflow
        flow_data = json.dumps({
            "nodes": [{"id": "node-1", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="Deployment Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        assert created.deployed is False
        print(f"✅ Created undeployed chatflow {chatflow_id}")

        # Deploy the chatflow
        updated = await client.update_chatflow(
            chatflow_id=chatflow_id,
            deployed=True
        )

        assert updated.id == chatflow_id
        assert updated.deployed is True
        print(f"✅ Deployed chatflow {chatflow_id} successfully")

    async def test_update_chatflow_multiple_fields_against_real_flowise(self, client, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Client updates name, flowData, and deployed simultaneously
        THEN: All fields are updated successfully
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create chatflow
        original_data = json.dumps({
            "nodes": [{"id": "original", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="Multi-Field Update Test",
            flow_data=original_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} for multi-field update")

        # Update all fields at once
        updated = await client.update_chatflow(
            chatflow_id=chatflow_id,
            name="Updated Multi-Field Name",
            flow_data=valid_flow_data_json,
            deployed=True
        )

        assert updated.id == chatflow_id
        assert updated.name == "Updated Multi-Field Name"
        assert updated.deployed is True
        if updated.flow_data:
            flow_data = json.loads(updated.flow_data)
            assert "chatOpenAI_updated" in str(flow_data)
        print(f"✅ Updated all fields for chatflow {chatflow_id} successfully")

    async def test_update_chatflow_through_service(self, service, valid_flow_data_json):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Service updates a chatflow (with validation and logging)
        THEN: Returns updated chatflow and logs operation
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create chatflow first
        create_data = json.dumps({
            "nodes": [{"id": "node-1", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await service.create_chatflow(
            name="Service Update Test",
            flow_data=create_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} via service")

        # Update through service
        updated = await service.update_chatflow(
            chatflow_id=chatflow_id,
            name="Service Updated Name",
            deployed=True
        )

        assert updated.id == chatflow_id
        assert updated.name == "Service Updated Name"
        assert updated.deployed is True
        print(f"✅ Service updated chatflow {chatflow_id} successfully")

    async def test_update_chatflow_performance(self, client):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Client updates a chatflow
        THEN: Completes within 10 seconds (SC-003)
        """
        from fluent_mind_mcp.models import ChatflowType
        import json
        import time

        # Create chatflow first
        flow_data = json.dumps({
            "nodes": [{"id": "node-1", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="Performance Update Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id

        # Measure update performance
        start_time = time.time()

        await client.update_chatflow(
            chatflow_id=chatflow_id,
            name="Updated for Performance"
        )

        duration = time.time() - start_time

        assert duration < 10.0, f"update_chatflow took {duration}s, expected <10s (SC-003)"
        print(f"✅ update_chatflow completed in {duration:.2f}s")

    async def test_update_chatflow_not_found_raises_error(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: Client updates nonexistent chatflow
        THEN: Raises NotFoundError
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(NotFoundError):
            await client.update_chatflow(
                chatflow_id=nonexistent_id,
                name="This should fail"
            )


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationUS3FullLifecycle:
    """Test complete User Story 3 workflow: create → update name → update flowData → deploy."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string for testing."""
        import json
        return json.dumps({
            "nodes": [
                {
                    "id": "final_node",
                    "type": "conversationChain",
                    "data": {"name": "conversationChain"},
                    "position": {"x": 400.0, "y": 300.0}
                }
            ],
            "edges": []
        })

    async def test_us3_complete_update_workflow(self, service, valid_flow_data_json):
        """
        SCENARIO: User creates chatflow and iterates on it through updates and deployment
        GIVEN: Real Flowise instance
        WHEN: User creates, updates name, updates flowData, and deploys chatflow
        THEN: All operations succeed with consistent data
        """
        from fluent_mind_mcp.models import ChatflowType
        import json
        import time

        start_time = time.time()

        # Step 1: Create new chatflow
        original_data = json.dumps({
            "nodes": [{"id": "initial_node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await service.create_chatflow(
            name="US3 Full Lifecycle Test",
            flow_data=original_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert created.id
        chatflow_id = created.id
        print(f"✅ Step 1: Created chatflow {chatflow_id}")

        # Step 2: Update name
        updated_name = await service.update_chatflow(
            chatflow_id=chatflow_id,
            name="US3 Updated Name"
        )

        assert updated_name.id == chatflow_id
        assert updated_name.name == "US3 Updated Name"
        print(f"✅ Step 2: Updated chatflow name")

        # Step 3: Update flowData
        updated_flow = await service.update_chatflow(
            chatflow_id=chatflow_id,
            flow_data=valid_flow_data_json
        )

        assert updated_flow.id == chatflow_id
        if updated_flow.flow_data:
            flow_data = json.loads(updated_flow.flow_data)
            assert "final_node" in str(flow_data)
        print(f"✅ Step 3: Updated chatflow flowData")

        # Step 4: Deploy chatflow
        deployed = await service.deploy_chatflow(
            chatflow_id=chatflow_id,
            deployed=True
        )

        assert deployed.id == chatflow_id
        assert deployed.deployed is True
        print(f"✅ Step 4: Deployed chatflow")

        # Step 5: Verify final state by retrieving
        final = await service.get_chatflow(chatflow_id)
        assert final.id == chatflow_id
        assert final.name == "US3 Updated Name"
        assert final.deployed is True
        print(f"✅ Step 5: Verified final chatflow state")

        # Verify total time
        duration = time.time() - start_time
        print(f"✅ Complete US3 workflow took {duration:.2f}s")

        # Cleanup note: Chatflow remains in Flowise (delete not implemented yet)
        print(f"⚠️  Note: Chatflow {chatflow_id} remains in Flowise for manual cleanup")

    async def test_us3_toggle_deployment_workflow(self, service):
        """
        SCENARIO: User toggles deployment status multiple times
        GIVEN: Real Flowise instance with chatflow
        WHEN: User deploys, undeploys, and redeploys chatflow
        THEN: Each toggle succeeds and state persists
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create chatflow
        flow_data = json.dumps({
            "nodes": [{"id": "toggle-node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await service.create_chatflow(
            name="Toggle Deployment Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        assert created.deployed is False
        print(f"✅ Created undeployed chatflow {chatflow_id}")

        # Deploy
        deployed = await service.deploy_chatflow(chatflow_id=chatflow_id, deployed=True)
        assert deployed.deployed is True
        print(f"✅ Deployed chatflow {chatflow_id}")

        # Undeploy
        undeployed = await service.deploy_chatflow(chatflow_id=chatflow_id, deployed=False)
        assert undeployed.deployed is False
        print(f"✅ Undeployed chatflow {chatflow_id}")

        # Redeploy
        redeployed = await service.deploy_chatflow(chatflow_id=chatflow_id, deployed=True)
        assert redeployed.deployed is True
        print(f"✅ Redeployed chatflow {chatflow_id}")

        # Verify final state
        final = await service.get_chatflow(chatflow_id)
        assert final.deployed is True
        print(f"✅ Verified final deployed state for {chatflow_id}")


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationDeleteChatflow:
    """Integration tests for deleting chatflows (User Story 4)."""

    async def test_delete_chatflow_against_real_flowise(self, client):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Client deletes the chatflow
        THEN: Chatflow is permanently removed from Flowise
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # First, create a chatflow to delete
        flow_data = json.dumps({
            "nodes": [{"id": "delete-test-node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="Delete Test Chatflow",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} for deletion test")

        # Verify chatflow exists before deletion
        retrieved = await client.get_chatflow(chatflow_id)
        assert retrieved.id == chatflow_id
        print(f"✅ Verified chatflow {chatflow_id} exists before deletion")

        # Delete the chatflow
        await client.delete_chatflow(chatflow_id)
        print(f"✅ Deleted chatflow {chatflow_id}")

        # Verify chatflow is gone (should raise NotFoundError)
        with pytest.raises(NotFoundError):
            await client.get_chatflow(chatflow_id)
        print(f"✅ Verified chatflow {chatflow_id} no longer exists")

    async def test_delete_chatflow_not_in_list_after_deletion(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: Client deletes a chatflow
        THEN: Chatflow no longer appears in list_chatflows response
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create a chatflow to delete
        flow_data = json.dumps({
            "nodes": [{"id": "list-test-node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="List Delete Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} for list deletion test")

        # Verify chatflow appears in list before deletion
        chatflows_before = await client.list_chatflows()
        assert any(cf.id == chatflow_id for cf in chatflows_before)
        print(f"✅ Verified chatflow {chatflow_id} appears in list before deletion")

        # Delete the chatflow
        await client.delete_chatflow(chatflow_id)
        print(f"✅ Deleted chatflow {chatflow_id}")

        # Verify chatflow no longer in list
        chatflows_after = await client.list_chatflows()
        assert not any(cf.id == chatflow_id for cf in chatflows_after)
        print(f"✅ Verified chatflow {chatflow_id} no longer in list after deletion")

    async def test_delete_chatflow_not_found_raises_error(self, client):
        """
        GIVEN: Real Flowise instance
        WHEN: Client attempts to delete non-existent chatflow
        THEN: Raises NotFoundError
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(NotFoundError):
            await client.delete_chatflow(nonexistent_id)

        print(f"✅ NotFoundError correctly raised for non-existent chatflow")

    async def test_delete_chatflow_through_service(self, service):
        """
        GIVEN: Real Flowise instance
        WHEN: Service deletes a chatflow (with validation and logging)
        THEN: Chatflow is deleted and operation is logged
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create chatflow first
        flow_data = json.dumps({
            "nodes": [{"id": "service-delete-node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await service.create_chatflow(
            name="Service Delete Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} via service")

        # Delete through service
        await service.delete_chatflow(chatflow_id)
        print(f"✅ Service deleted chatflow {chatflow_id}")

        # Verify chatflow is gone
        with pytest.raises(NotFoundError):
            await service.get_chatflow(chatflow_id)
        print(f"✅ Verified chatflow {chatflow_id} was deleted via service")

    async def test_delete_chatflow_performance(self, client):
        """
        GIVEN: Real Flowise instance with existing chatflow
        WHEN: Client deletes a chatflow
        THEN: Completes within 10 seconds (SC-003)
        """
        from fluent_mind_mcp.models import ChatflowType
        import json
        import time

        # Create chatflow first
        flow_data = json.dumps({
            "nodes": [{"id": "perf-delete-node", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await client.create_chatflow(
            name="Performance Delete Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id

        # Measure delete performance
        start_time = time.time()

        await client.delete_chatflow(chatflow_id)

        duration = time.time() - start_time

        assert duration < 10.0, f"delete_chatflow took {duration}s, expected <10s (SC-003)"
        print(f"✅ delete_chatflow completed in {duration:.2f}s")


@pytest.mark.integration
@pytest.mark.asyncio
class TestIntegrationUS4FullLifecycle:
    """Test complete User Story 4 workflow: create → delete → verify gone."""

    @pytest.fixture
    def valid_flow_data_json(self) -> str:
        """Valid FlowData as JSON string for testing."""
        import json
        return json.dumps({
            "nodes": [
                {
                    "id": "us4_lifecycle_node",
                    "type": "conversationChain",
                    "data": {"name": "conversationChain"},
                    "position": {"x": 400.0, "y": 300.0}
                }
            ],
            "edges": []
        })

    async def test_us4_complete_deletion_workflow(self, service, valid_flow_data_json):
        """
        SCENARIO: User creates chatflow and then permanently removes it
        GIVEN: Real Flowise instance
        WHEN: User creates chatflow, deletes it, and verifies deletion
        THEN: All operations succeed with chatflow permanently removed
        """
        from fluent_mind_mcp.models import ChatflowType
        import time

        start_time = time.time()

        # Step 1: Create new chatflow
        created = await service.create_chatflow(
            name="US4 Full Lifecycle Test",
            flow_data=valid_flow_data_json,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        assert created.id
        chatflow_id = created.id
        print(f"✅ Step 1: Created chatflow {chatflow_id}")

        # Step 2: Verify it appears in list
        chatflows = await service.list_chatflows()
        found_in_list = any(cf.id == chatflow_id for cf in chatflows)
        assert found_in_list, "Created chatflow should appear in list"
        print(f"✅ Step 2: Found chatflow in list")

        # Step 3: Verify can retrieve details
        details = await service.get_chatflow(chatflow_id)
        assert details.id == chatflow_id
        assert details.name == "US4 Full Lifecycle Test"
        print(f"✅ Step 3: Retrieved chatflow details")

        # Step 4: Delete chatflow
        await service.delete_chatflow(chatflow_id)
        print(f"✅ Step 4: Deleted chatflow {chatflow_id}")

        # Step 5: Verify no longer in list
        chatflows_after = await service.list_chatflows()
        still_in_list = any(cf.id == chatflow_id for cf in chatflows_after)
        assert not still_in_list, "Deleted chatflow should not appear in list"
        print(f"✅ Step 5: Verified chatflow no longer in list")

        # Step 6: Verify get returns NotFoundError
        with pytest.raises(NotFoundError):
            await service.get_chatflow(chatflow_id)
        print(f"✅ Step 6: Verified get_chatflow returns NotFoundError")

        # Verify total time
        duration = time.time() - start_time
        print(f"✅ Complete US4 workflow took {duration:.2f}s")
        print(f"✅ Chatflow {chatflow_id} permanently removed from Flowise")

    async def test_us4_multiple_deletions(self, service):
        """
        SCENARIO: User performs workspace hygiene by deleting multiple chatflows
        GIVEN: Real Flowise instance with multiple test chatflows
        WHEN: User deletes selected chatflows
        THEN: Only selected chatflows are removed, others remain
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create 3 test chatflows
        flow_data = json.dumps({
            "nodes": [{"id": "multi-delete", "type": "llm", "data": {}}],
            "edges": []
        })

        chatflow_ids = []
        for i in range(3):
            created = await service.create_chatflow(
                name=f"Multi Delete Test {i}",
                flow_data=flow_data,
                type=ChatflowType.CHATFLOW,
                deployed=False
            )
            chatflow_ids.append(created.id)
            print(f"✅ Created chatflow {i+1}/3: {created.id}")

        # Delete chatflows 0 and 2 (keep 1)
        await service.delete_chatflow(chatflow_ids[0])
        print(f"✅ Deleted chatflow 1: {chatflow_ids[0]}")

        await service.delete_chatflow(chatflow_ids[2])
        print(f"✅ Deleted chatflow 3: {chatflow_ids[2]}")

        # Verify chatflow 1 still exists
        still_exists = await service.get_chatflow(chatflow_ids[1])
        assert still_exists.id == chatflow_ids[1]
        print(f"✅ Verified chatflow 2 still exists: {chatflow_ids[1]}")

        # Verify chatflows 0 and 2 are gone
        with pytest.raises(NotFoundError):
            await service.get_chatflow(chatflow_ids[0])
        print(f"✅ Verified chatflow 1 is gone: {chatflow_ids[0]}")

        with pytest.raises(NotFoundError):
            await service.get_chatflow(chatflow_ids[2])
        print(f"✅ Verified chatflow 3 is gone: {chatflow_ids[2]}")

        # Cleanup: Delete remaining chatflow
        await service.delete_chatflow(chatflow_ids[1])
        print(f"✅ Cleanup: Deleted remaining chatflow {chatflow_ids[1]}")

    async def test_us4_delete_deployed_chatflow(self, service):
        """
        SCENARIO: User deletes a deployed chatflow
        GIVEN: Real Flowise instance with deployed chatflow
        WHEN: User deletes the deployed chatflow
        THEN: Chatflow is deleted regardless of deployment status
        """
        from fluent_mind_mcp.models import ChatflowType
        import json

        # Create and deploy chatflow
        flow_data = json.dumps({
            "nodes": [{"id": "deployed-delete", "type": "llm", "data": {}}],
            "edges": []
        })

        created = await service.create_chatflow(
            name="Delete Deployed Test",
            flow_data=flow_data,
            type=ChatflowType.CHATFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id}")

        # Deploy it
        deployed = await service.deploy_chatflow(chatflow_id=chatflow_id, deployed=True)
        assert deployed.deployed is True
        print(f"✅ Deployed chatflow {chatflow_id}")

        # Delete deployed chatflow
        await service.delete_chatflow(chatflow_id)
        print(f"✅ Deleted deployed chatflow {chatflow_id}")

        # Verify it's gone
        with pytest.raises(NotFoundError):
            await service.get_chatflow(chatflow_id)
        print(f"✅ Verified deployed chatflow {chatflow_id} was deleted")


@pytest.mark.integration
@pytest.mark.skipif(not get_test_config()[0], reason="FLOWISE_API_URL not set")
@pytest.mark.asyncio
class TestIntegrationGenerateAgentflowV2:
    """Integration tests for User Story 5: Generate AgentFlow V2 from Description.

    WHY: These tests verify that the AgentFlow V2 generation feature works correctly
    against a real Flowise instance, including:
    - Generating flowData from natural language descriptions
    - Creating chatflows from generated structures
    - End-to-end workflow from description to deployed agent

    Tests require a real Flowise instance with AgentFlow V2 generation capability.
    """

    async def test_us5_generate_agentflow_v2_from_description(self, service):
        """
        SCENARIO: User generates AgentFlow V2 from natural language description
        GIVEN: Real Flowise instance with generation endpoint
        WHEN: User provides natural language description of desired agent
        THEN: Flowise returns complete AgentFlow V2 structure (flowData, name, description)
        """
        description = "Create a research agent that searches the web and summarizes findings"

        result = await service.generate_agentflow_v2(description=description)

        print(f"✅ Generated AgentFlow V2 from description")
        print(f"   Name: {result.get('name')}")
        print(f"   Description: {result.get('description', 'N/A')}")

        # Verify structure
        assert "flowData" in result
        assert "name" in result
        assert result["name"] is not None

        # Verify flowData is valid JSON
        flow_data = json.loads(result["flowData"])
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) > 0

        print(f"   Nodes: {len(flow_data['nodes'])}")
        print(f"   Edges: {len(flow_data['edges'])}")

    async def test_us5_create_chatflow_from_generated_agentflow(self, service):
        """
        SCENARIO: User creates chatflow from generated AgentFlow V2
        GIVEN: Real Flowise instance, generated AgentFlow V2 structure
        WHEN: User creates chatflow using generated flowData
        THEN: Chatflow is created successfully and appears in Flowise
        """
        from fluent_mind_mcp.models import ChatflowType

        # Step 1: Generate AgentFlow V2
        description = "Customer support agent for handling user inquiries"
        generated = await service.generate_agentflow_v2(description=description)

        print(f"✅ Generated AgentFlow V2: {generated['name']}")

        # Step 2: Create chatflow from generated structure
        created = await service.create_chatflow(
            name=f"Test {generated['name']}",
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} from generated AgentFlow V2")

        try:
            # Step 3: Verify chatflow exists and has correct structure
            retrieved = await service.get_chatflow(chatflow_id)
            assert retrieved.id == chatflow_id
            assert retrieved.type == ChatflowType.AGENTFLOW
            assert retrieved.flow_data is not None

            # Verify flowData matches what was generated
            retrieved_flow_data = json.loads(retrieved.flow_data)
            original_flow_data = json.loads(generated["flowData"])

            assert len(retrieved_flow_data["nodes"]) == len(original_flow_data["nodes"])
            assert len(retrieved_flow_data["edges"]) == len(original_flow_data["edges"])

            print(f"✅ Verified chatflow structure matches generated AgentFlow V2")

        finally:
            # Cleanup
            await service.delete_chatflow(chatflow_id)
            print(f"✅ Cleanup: Deleted test chatflow {chatflow_id}")

    async def test_us5_end_to_end_generate_create_deploy_workflow(self, service):
        """
        SCENARIO: Complete workflow from description to deployed agent
        GIVEN: Real Flowise instance
        WHEN: User generates AgentFlow V2, creates chatflow, and deploys it
        THEN: Each step succeeds and agent is ready for use

        WHY: This validates SC-008 - AI assistant can generate and create functional
        AgentFlow V2 in single interaction.
        """
        from fluent_mind_mcp.models import ChatflowType

        # Step 1: Generate AgentFlow V2
        description = "Research agent that searches web and summarizes findings"
        print(f"\n🔄 Generating AgentFlow V2 from description...")

        generated = await service.generate_agentflow_v2(description=description)
        print(f"✅ Generated: {generated['name']}")

        # Verify generated structure
        flow_data = json.loads(generated["flowData"])
        print(f"   Structure: {len(flow_data['nodes'])} nodes, {len(flow_data['edges'])} edges")

        # Step 2: Create chatflow
        print(f"\n🔄 Creating chatflow from generated structure...")

        created = await service.create_chatflow(
            name=f"Integration Test - {generated['name']}",
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id}")

        try:
            # Step 3: Deploy chatflow
            print(f"\n🔄 Deploying chatflow...")

            deployed = await service.deploy_chatflow(
                chatflow_id=chatflow_id,
                deployed=True
            )

            assert deployed.deployed is True
            print(f"✅ Deployed chatflow {chatflow_id}")

            # Step 4: Verify final state
            print(f"\n🔄 Verifying final state...")

            final_state = await service.get_chatflow(chatflow_id)
            assert final_state.id == chatflow_id
            assert final_state.deployed is True
            assert final_state.type == ChatflowType.AGENTFLOW

            print(f"✅ SUCCESS: Complete workflow validated")
            print(f"   - Generated AgentFlow V2 from description ✓")
            print(f"   - Created chatflow from generated structure ✓")
            print(f"   - Deployed chatflow successfully ✓")
            print(f"   - Agent ready for use ✓")

        finally:
            # Cleanup
            print(f"\n🔄 Cleaning up...")
            await service.delete_chatflow(chatflow_id)
            print(f"✅ Deleted test chatflow {chatflow_id}")

    async def test_us5_generate_with_different_descriptions(self, service):
        """
        SCENARIO: Generate multiple agents with different descriptions
        GIVEN: Real Flowise instance
        WHEN: User generates agents with various descriptions
        THEN: Each generation produces unique, appropriate agent structure

        WHY: Validates that generation adapts to different use cases.
        """
        from fluent_mind_mcp.models import ChatflowType

        descriptions = [
            "Simple customer support agent",
            "Data analysis agent for processing CSV files",
            "Multi-step research agent with web search and summarization"
        ]

        created_ids = []

        try:
            for idx, description in enumerate(descriptions, 1):
                print(f"\n🔄 Test {idx}/3: Generating from: '{description}'")

                # Generate
                generated = await service.generate_agentflow_v2(description=description)
                print(f"   ✅ Generated: {generated['name']}")

                # Verify structure
                flow_data = json.loads(generated["flowData"])
                nodes_count = len(flow_data["nodes"])
                edges_count = len(flow_data["edges"])
                print(f"   Structure: {nodes_count} nodes, {edges_count} edges")

                assert nodes_count > 0, "Generated flowData should have at least one node"

                # Create chatflow to verify structure is valid
                created = await service.create_chatflow(
                    name=f"Test Gen {idx}",
                    flow_data=generated["flowData"],
                    type=ChatflowType.AGENTFLOW
                )

                created_ids.append(created.id)
                print(f"   ✅ Created chatflow {created.id}")

        finally:
            # Cleanup all created chatflows
            print(f"\n🔄 Cleaning up {len(created_ids)} test chatflows...")
            for chatflow_id in created_ids:
                try:
                    await service.delete_chatflow(chatflow_id)
                    print(f"   ✅ Deleted {chatflow_id}")
                except Exception as e:
                    print(f"   ⚠️  Failed to delete {chatflow_id}: {e}")

            print(f"✅ Cleanup complete")

    async def test_us5_generated_agentflow_can_be_updated(self, service):
        """
        SCENARIO: User updates chatflow created from generated AgentFlow V2
        GIVEN: Chatflow created from generated structure
        WHEN: User updates the chatflow name or deployment status
        THEN: Updates succeed without issues

        WHY: Verifies that generated chatflows are fully manageable like any other chatflow.
        """
        from fluent_mind_mcp.models import ChatflowType

        # Generate and create
        generated = await service.generate_agentflow_v2(
            description="Test agent for update operations"
        )

        created = await service.create_chatflow(
            name="Original Name",
            flow_data=generated["flowData"],
            type=ChatflowType.AGENTFLOW,
            deployed=False
        )

        chatflow_id = created.id
        print(f"✅ Created chatflow {chatflow_id} from generated AgentFlow V2")

        try:
            # Update name
            updated = await service.update_chatflow(
                chatflow_id=chatflow_id,
                name="Updated Name"
            )

            assert updated.name == "Updated Name"
            print(f"✅ Updated chatflow name")

            # Deploy
            deployed = await service.deploy_chatflow(
                chatflow_id=chatflow_id,
                deployed=True
            )

            assert deployed.deployed is True
            print(f"✅ Deployed generated chatflow")

        finally:
            # Cleanup
            await service.delete_chatflow(chatflow_id)
            print(f"✅ Cleanup: Deleted chatflow {chatflow_id}")
