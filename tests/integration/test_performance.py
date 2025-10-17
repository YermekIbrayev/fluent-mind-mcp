"""
Integration tests for performance targets on Flowise MCP Server.

WHY: Validate that all operations meet the performance requirements
     defined in Success Criteria (SC-002, SC-003, SC-006).

Performance Targets:
- SC-002: List/Get operations complete in <5s
- SC-003: Execute operations complete in <5s
- SC-006: Full lifecycle (create → update → execute → delete) completes in <60s
"""

import os
import time
from typing import List

import pytest

from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.models.config import FlowiseConfig


# Skip if no Flowise instance configured
pytestmark = pytest.mark.skipif(
    not os.getenv("FLOWISE_API_URL"),
    reason="FLOWISE_API_URL not set - requires live Flowise instance",
)


@pytest.fixture
async def flowise_client():
    """Create FlowiseClient for integration tests."""
    config = FlowiseConfig(
        api_url=os.getenv("FLOWISE_API_URL"),
        api_key=os.getenv("FLOWISE_API_KEY"),
        timeout=60,
        max_connections=10,
    )
    client = FlowiseClient(config)
    yield client
    # Cleanup: client auto-closes connection pool


class TestListPerformance:
    """Test list_chatflows() performance (SC-002: <5s)."""

    async def test_list_chatflows_under_5s(self, flowise_client):
        """
        Verify list_chatflows() completes in <5s.

        WHY: SC-002 requires list operations complete in <5s for responsive
             AI assistant experience.
        """
        start_time = time.time()

        result = await flowise_client.list_chatflows()

        elapsed_time = time.time() - start_time

        # Verify succeeded
        assert isinstance(result, list), "list_chatflows() did not return a list"

        # Verify performance target
        assert (
            elapsed_time < 5.0
        ), f"list_chatflows() took {elapsed_time:.2f}s (target: <5s)"

    async def test_list_chatflows_multiple_iterations_average(
        self, flowise_client
    ):
        """
        Verify average list_chatflows() time over 10 iterations is <5s.

        WHY: Validate performance is consistent, not just a one-time success.
        """
        iterations = 10
        total_time = 0.0

        for _ in range(iterations):
            start_time = time.time()
            result = await flowise_client.list_chatflows()
            elapsed_time = time.time() - start_time

            total_time += elapsed_time

            # Each iteration should also meet target
            assert elapsed_time < 5.0, f"Iteration took {elapsed_time:.2f}s"

        average_time = total_time / iterations

        assert (
            average_time < 5.0
        ), f"Average list time {average_time:.2f}s exceeds 5s target"


class TestGetPerformance:
    """Test get_chatflow() performance (SC-002: <5s)."""

    async def test_get_chatflow_under_5s(self, flowise_client):
        """
        Verify get_chatflow() completes in <5s.

        WHY: SC-002 requires get operations complete in <5s for responsive
             AI assistant experience.
        """
        # First, get a chatflow ID to test with
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id

        # Measure get_chatflow performance
        start_time = time.time()

        result = await flowise_client.get_chatflow(chatflow_id)

        elapsed_time = time.time() - start_time

        # Verify succeeded
        assert result.id == chatflow_id, "get_chatflow() returned wrong chatflow"

        # Verify performance target
        assert (
            elapsed_time < 5.0
        ), f"get_chatflow() took {elapsed_time:.2f}s (target: <5s)"

    async def test_get_chatflow_multiple_iterations_average(
        self, flowise_client
    ):
        """
        Verify average get_chatflow() time over 10 iterations is <5s.

        WHY: Validate performance is consistent across multiple requests.
        """
        # Get a chatflow ID
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id

        iterations = 10
        total_time = 0.0

        for _ in range(iterations):
            start_time = time.time()
            result = await flowise_client.get_chatflow(chatflow_id)
            elapsed_time = time.time() - start_time

            total_time += elapsed_time

            # Each iteration should also meet target
            assert elapsed_time < 5.0, f"Iteration took {elapsed_time:.2f}s"

        average_time = total_time / iterations

        assert (
            average_time < 5.0
        ), f"Average get time {average_time:.2f}s exceeds 5s target"


class TestExecutePerformance:
    """Test run_prediction() performance (SC-003: <5s)."""

    async def test_execute_chatflow_under_5s(self, flowise_client):
        """
        Verify run_prediction() completes in <5s.

        WHY: SC-003 requires execute operations complete in <5s for responsive
             AI assistant interactions.

        NOTE: This assumes the chatflow itself is optimized. If chatflow
              execution is slow (e.g., complex RAG), this test may need
              adjustment or use a simple test chatflow.
        """
        # Get a chatflow to execute
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id
        test_question = "What is 2+2?"

        # Measure execute performance
        start_time = time.time()

        result = await flowise_client.run_prediction(chatflow_id, test_question)

        elapsed_time = time.time() - start_time

        # Verify succeeded
        assert hasattr(result, "text"), "run_prediction() missing response text"
        assert result.text, "run_prediction() returned empty text"

        # Verify performance target
        # NOTE: If this fails, it may be due to chatflow complexity, not MCP server
        assert (
            elapsed_time < 5.0
        ), f"run_prediction() took {elapsed_time:.2f}s (target: <5s)"

    async def test_execute_chatflow_warmup_performance(self, flowise_client):
        """
        Verify run_prediction() performance after warmup.

        WHY: First execution may be slower due to cold start. Validate
             subsequent executions meet performance target.
        """
        # Get a chatflow to execute
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id
        test_question = "Warmup test"

        # Warmup execution (don't measure)
        await flowise_client.run_prediction(chatflow_id, test_question)

        # Now measure performance
        start_time = time.time()

        result = await flowise_client.run_prediction(chatflow_id, test_question)

        elapsed_time = time.time() - start_time

        # Verify succeeded
        assert result.text, "run_prediction() returned empty text"

        # Verify performance target (should be faster after warmup)
        assert (
            elapsed_time < 5.0
        ), f"run_prediction() (warmed) took {elapsed_time:.2f}s (target: <5s)"


class TestCreatePerformance:
    """Test create_chatflow() performance (SC-002 implies <10s for write ops)."""

    async def test_create_chatflow_under_10s(self, flowise_client):
        """
        Verify create_chatflow() completes in <10s.

        WHY: While SC-002 specifies <5s for reads, write operations like
             create should complete in reasonable time (<10s) for good UX.
        """
        flow_data = '{"nodes": [], "edges": []}'

        start_time = time.time()

        result = await flowise_client.create_chatflow(
            name="Performance Test Create",
            flow_data=flow_data,
            type="CHATFLOW",
            deployed=False,
        )

        elapsed_time = time.time() - start_time

        # Cleanup
        try:
            await flowise_client.delete_chatflow(result.id)
        except Exception:
            pass

        # Verify succeeded
        assert hasattr(result, "id"), "create_chatflow() missing ID"

        # Verify performance target
        assert (
            elapsed_time < 10.0
        ), f"create_chatflow() took {elapsed_time:.2f}s (target: <10s)"


class TestUpdatePerformance:
    """Test update_chatflow() performance."""

    async def test_update_chatflow_under_10s(self, flowise_client):
        """
        Verify update_chatflow() completes in <10s.

        WHY: Write operations should complete in reasonable time for good UX.
        """
        # Create a test chatflow
        flow_data = '{"nodes": [], "edges": []}'
        chatflow = await flowise_client.create_chatflow(
            name="Performance Test Update",
            flow_data=flow_data,
            type="CHATFLOW",
            deployed=False,
        )

        try:
            # Measure update performance
            start_time = time.time()

            result = await flowise_client.update_chatflow(
                chatflow_id=chatflow.id,
                name="Updated Name",
                deployed=True,
            )

            elapsed_time = time.time() - start_time

            # Verify succeeded
            assert result.name == "Updated Name"
            assert result.deployed is True

            # Verify performance target
            assert (
                elapsed_time < 10.0
            ), f"update_chatflow() took {elapsed_time:.2f}s (target: <10s)"

        finally:
            # Cleanup
            try:
                await flowise_client.delete_chatflow(chatflow.id)
            except Exception:
                pass


class TestDeletePerformance:
    """Test delete_chatflow() performance."""

    async def test_delete_chatflow_under_10s(self, flowise_client):
        """
        Verify delete_chatflow() completes in <10s.

        WHY: Write operations should complete in reasonable time for good UX.
        """
        # Create a test chatflow
        flow_data = '{"nodes": [], "edges": []}'
        chatflow = await flowise_client.create_chatflow(
            name="Performance Test Delete",
            flow_data=flow_data,
            type="CHATFLOW",
            deployed=False,
        )

        # Measure delete performance
        start_time = time.time()

        await flowise_client.delete_chatflow(chatflow.id)

        elapsed_time = time.time() - start_time

        # Verify performance target
        assert (
            elapsed_time < 10.0
        ), f"delete_chatflow() took {elapsed_time:.2f}s (target: <10s)"

        # Verify chatflow is gone
        chatflows = await flowise_client.list_chatflows()
        assert not any(
            cf.id == chatflow.id for cf in chatflows
        ), "Chatflow not deleted"


class TestFullLifecyclePerformance:
    """Test complete lifecycle performance (SC-006: <60s)."""

    async def test_full_lifecycle_under_60s(self, flowise_client):
        """
        Verify full lifecycle (create → update → execute → delete) completes in <60s.

        WHY: SC-006 requires complete chatflow lifecycle completes in <60s
             to ensure good developer experience when testing workflows.
        """
        flow_data = '{"nodes": [], "edges": []}'

        start_time = time.time()

        # Step 1: Create
        chatflow = await flowise_client.create_chatflow(
            name="Full Lifecycle Test",
            flow_data=flow_data,
            type="CHATFLOW",
            deployed=False,
        )

        # Step 2: Update
        updated_chatflow = await flowise_client.update_chatflow(
            chatflow_id=chatflow.id,
            name="Updated Lifecycle Test",
            deployed=True,
        )

        # Step 3: Execute
        try:
            # NOTE: Execution may fail if chatflow is not properly configured
            # We attempt execution but don't fail test if chatflow execution fails
            await flowise_client.run_prediction(
                chatflow.id, "Lifecycle test execution"
            )
        except Exception:
            # Chatflow may not be executable (no nodes), that's okay for perf test
            pass

        # Step 4: Delete
        await flowise_client.delete_chatflow(chatflow.id)

        elapsed_time = time.time() - start_time

        # Verify performance target (SC-006)
        assert (
            elapsed_time < 60.0
        ), f"Full lifecycle took {elapsed_time:.2f}s (target: <60s)"

    async def test_full_lifecycle_with_large_flow_data(self, flowise_client):
        """
        Verify full lifecycle with larger flowData still completes in <60s.

        WHY: Validate performance target holds even with more realistic
             chatflow sizes (not just empty flows).
        """
        # Create a larger flow_data (simulating a more complex workflow)
        nodes = [
            {
                "id": f"node-{i}",
                "type": "chatOpenAI",
                "data": {
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "maxTokens": 1000,
                },
                "position": {"x": i * 100, "y": i * 100},
            }
            for i in range(10)
        ]

        edges = [
            {
                "id": f"edge-{i}",
                "source": f"node-{i}",
                "target": f"node-{i+1}",
            }
            for i in range(9)
        ]

        import json

        flow_data = json.dumps({"nodes": nodes, "edges": edges})

        start_time = time.time()

        # Full lifecycle
        chatflow = await flowise_client.create_chatflow(
            name="Large Flow Lifecycle Test",
            flow_data=flow_data,
            type="CHATFLOW",
            deployed=False,
        )

        updated = await flowise_client.update_chatflow(
            chatflow_id=chatflow.id, deployed=True
        )

        try:
            await flowise_client.run_prediction(chatflow.id, "Test execution")
        except Exception:
            pass  # Execution may fail, that's okay

        await flowise_client.delete_chatflow(chatflow.id)

        elapsed_time = time.time() - start_time

        # Verify performance target
        assert (
            elapsed_time < 60.0
        ), f"Full lifecycle (large flow) took {elapsed_time:.2f}s (target: <60s)"


class TestPerformanceUnderLoad:
    """Test performance under concurrent load."""

    async def test_list_performance_under_concurrent_load(
        self, flowise_client
    ):
        """
        Verify list_chatflows() performance degrades gracefully under concurrent load.

        WHY: Validate that when 10 concurrent list operations are running,
             each still completes in reasonable time (<10s, 2x normal target).
        """
        import asyncio

        async def timed_list():
            start = time.time()
            result = await flowise_client.list_chatflows()
            elapsed = time.time() - start
            return result, elapsed

        # Launch 10 concurrent list operations
        tasks = [timed_list() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # Verify all completed in reasonable time (allow 2x target under load)
        for i, (result, elapsed) in enumerate(results):
            assert isinstance(result, list), f"Operation {i} failed"
            assert (
                elapsed < 10.0
            ), f"Operation {i} took {elapsed:.2f}s under load (target: <10s)"

    async def test_execute_performance_under_concurrent_load(
        self, flowise_client
    ):
        """
        Verify run_prediction() performance degrades gracefully under concurrent load.

        WHY: Validate that when 5 concurrent execute operations are running,
             each still completes in reasonable time (<10s, 2x normal target).
        """
        import asyncio

        # Get a chatflow to execute
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id

        async def timed_execute():
            start = time.time()
            result = await flowise_client.run_prediction(
                chatflow_id, "Concurrent load test"
            )
            elapsed = time.time() - start
            return result, elapsed

        # Launch 5 concurrent execute operations
        tasks = [timed_execute() for _ in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all completed in reasonable time
        for i, item in enumerate(results):
            if isinstance(item, Exception):
                # Execution may fail due to chatflow issues, skip if so
                continue

            result, elapsed = item
            assert hasattr(result, "text"), f"Operation {i} failed"
            assert (
                elapsed < 10.0
            ), f"Operation {i} took {elapsed:.2f}s under load (target: <10s)"
