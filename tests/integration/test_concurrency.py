"""
Integration tests for concurrent operations on Flowise MCP Server.

WHY: Validate that 5-10 simultaneous operations can be handled without
     race conditions, connection pool exhaustion, or data corruption.

Success Criteria (SC-002, SC-003):
- 5-10 concurrent list operations complete in <5s total
- 5-10 concurrent execute operations complete in <5s each
- No connection pool exhaustion errors
- No race conditions or data corruption
"""

import asyncio
import os
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


class TestConcurrentListOperations:
    """Test concurrent list_chatflows() operations."""

    async def test_concurrent_5_list_operations(self, flowise_client):
        """
        Verify 5 concurrent list operations complete successfully.

        WHY: Validate connection pooling handles multiple simultaneous reads
             without exhausting connections or timing out.
        """
        # Launch 5 concurrent list operations
        tasks = [flowise_client.list_chatflows() for _ in range(5)]

        # Execute all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all succeeded
        for i, result in enumerate(results):
            assert not isinstance(
                result, Exception
            ), f"Operation {i} failed: {result}"
            assert isinstance(result, list), f"Operation {i} returned non-list"

        # Verify results are consistent (all should return same chatflow list)
        chatflow_ids_per_result = [
            set(cf.id for cf in result) for result in results
        ]
        assert all(
            ids == chatflow_ids_per_result[0] for ids in chatflow_ids_per_result
        ), "Concurrent operations returned inconsistent data"

    async def test_concurrent_10_list_operations(self, flowise_client):
        """
        Verify 10 concurrent list operations complete successfully.

        WHY: Validate connection pool max_connections (10) is sufficient
             for maximum concurrent load.
        """
        # Launch 10 concurrent list operations (at pool limit)
        tasks = [flowise_client.list_chatflows() for _ in range(10)]

        # Execute all concurrently with timeout
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True), timeout=5.0
        )

        # Verify all succeeded within 5s (SC-002)
        for i, result in enumerate(results):
            assert not isinstance(
                result, Exception
            ), f"Operation {i} failed: {result}"
            assert isinstance(result, list), f"Operation {i} returned non-list"

    async def test_concurrent_list_performance_target(self, flowise_client):
        """
        Verify 10 concurrent list operations complete within 5s total.

        WHY: Validate SC-002 performance target (5s for list operations).
        """
        import time

        start_time = time.time()

        # Launch 10 concurrent list operations
        tasks = [flowise_client.list_chatflows() for _ in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        elapsed_time = time.time() - start_time

        # Verify all succeeded
        for result in results:
            assert not isinstance(result, Exception)

        # Verify total time <5s (SC-002)
        assert (
            elapsed_time < 5.0
        ), f"Concurrent list operations took {elapsed_time:.2f}s (target: <5s)"


class TestConcurrentExecuteOperations:
    """Test concurrent run_prediction() operations."""

    async def test_concurrent_5_execute_operations(self, flowise_client):
        """
        Verify 5 concurrent execute operations complete successfully.

        WHY: Validate chatflow execution can handle multiple simultaneous
             requests without blocking or failing.
        """
        # First, get a chatflow to execute
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id
        test_question = "What is 2+2?"

        # Launch 5 concurrent execute operations
        tasks = [
            flowise_client.run_prediction(chatflow_id, test_question)
            for _ in range(5)
        ]

        # Execute all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all succeeded
        for i, result in enumerate(results):
            assert not isinstance(
                result, Exception
            ), f"Operation {i} failed: {result}"
            assert hasattr(
                result, "text"
            ), f"Operation {i} missing response text"
            assert result.text, f"Operation {i} returned empty text"

    async def test_concurrent_execute_performance_target(self, flowise_client):
        """
        Verify 5 concurrent execute operations each complete within 5s.

        WHY: Validate SC-003 performance target (5s per execute operation).
        """
        import time

        # Get a chatflow to execute
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id
        test_question = "Test concurrent execution"

        # Track start times and results
        async def timed_execute():
            start = time.time()
            result = await flowise_client.run_prediction(chatflow_id, test_question)
            elapsed = time.time() - start
            return result, elapsed

        # Launch 5 concurrent execute operations
        tasks = [timed_execute() for _ in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all succeeded and met performance target
        for i, (result, elapsed) in enumerate(results):
            assert not isinstance(
                result, Exception
            ), f"Operation {i} failed: {result}"
            assert (
                elapsed < 5.0
            ), f"Operation {i} took {elapsed:.2f}s (target: <5s)"


class TestConcurrentMixedOperations:
    """Test concurrent mixed operations (list + get + execute)."""

    async def test_concurrent_mixed_operations(self, flowise_client):
        """
        Verify mixed concurrent operations (list, get, execute) work correctly.

        WHY: Validate real-world scenario where AI assistant performs multiple
             different operations simultaneously.
        """
        # Get a chatflow for get/execute operations
        chatflows = await flowise_client.list_chatflows()
        if not chatflows:
            pytest.skip("No chatflows available for testing")

        chatflow_id = chatflows[0].id

        # Create mixed operation tasks
        tasks = [
            # 3 list operations
            flowise_client.list_chatflows(),
            flowise_client.list_chatflows(),
            flowise_client.list_chatflows(),
            # 3 get operations
            flowise_client.get_chatflow(chatflow_id),
            flowise_client.get_chatflow(chatflow_id),
            flowise_client.get_chatflow(chatflow_id),
            # 2 execute operations
            flowise_client.run_prediction(chatflow_id, "Test 1"),
            flowise_client.run_prediction(chatflow_id, "Test 2"),
        ]

        # Execute all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all succeeded
        for i, result in enumerate(results):
            assert not isinstance(
                result, Exception
            ), f"Operation {i} failed: {result}"

        # Verify result types
        assert all(isinstance(r, list) for r in results[:3]), "List operations failed"
        assert all(
            hasattr(r, "id") and r.id == chatflow_id for r in results[3:6]
        ), "Get operations failed"
        assert all(
            hasattr(r, "text") for r in results[6:]
        ), "Execute operations failed"


class TestConcurrentCreateOperations:
    """Test concurrent create_chatflow() operations."""

    async def test_concurrent_create_no_name_collision(self, flowise_client):
        """
        Verify concurrent create operations with unique names succeed.

        WHY: Validate multiple AI assistants can create chatflows simultaneously
             without race conditions.
        """
        # Create 5 chatflows with unique names concurrently
        flow_data = '{"nodes": [], "edges": []}'

        tasks = [
            flowise_client.create_chatflow(
                name=f"Concurrent Test {i}",
                flow_data=flow_data,
                type="CHATFLOW",
                deployed=False,
            )
            for i in range(5)
        ]

        # Execute all concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Track created IDs for cleanup
        created_ids: List[str] = []

        try:
            # Verify all succeeded
            for i, result in enumerate(results):
                assert not isinstance(
                    result, Exception
                ), f"Create operation {i} failed: {result}"
                assert hasattr(result, "id"), f"Create {i} missing ID"
                created_ids.append(result.id)

            # Verify all IDs are unique
            assert len(created_ids) == len(
                set(created_ids)
            ), "Duplicate chatflow IDs created"

            # Verify all chatflows exist
            for chatflow_id in created_ids:
                chatflow = await flowise_client.get_chatflow(chatflow_id)
                assert chatflow.id == chatflow_id

        finally:
            # Cleanup: delete all created chatflows
            for chatflow_id in created_ids:
                try:
                    await flowise_client.delete_chatflow(chatflow_id)
                except Exception:
                    pass  # Ignore cleanup errors


class TestConnectionPoolBehavior:
    """Test connection pool behavior under concurrent load."""

    async def test_connection_pool_does_not_exhaust(self, flowise_client):
        """
        Verify connection pool (max 10) does not exhaust under load.

        WHY: Validate connection pooling and reuse works correctly,
             preventing "too many connections" errors.
        """
        # Launch 20 concurrent operations (2x pool size)
        # This tests pool reuse and queuing behavior
        tasks = [flowise_client.list_chatflows() for _ in range(20)]

        # Execute all concurrently - should queue, not fail
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify all succeeded (no pool exhaustion)
        for i, result in enumerate(results):
            assert not isinstance(
                result, Exception
            ), f"Operation {i} failed (pool exhausted?): {result}"
            assert isinstance(result, list), f"Operation {i} returned non-list"

    async def test_sequential_operations_after_concurrent(
        self, flowise_client
    ):
        """
        Verify connection pool recovers after concurrent operations.

        WHY: Validate connections are properly released back to pool
             and can be reused.
        """
        # First: 10 concurrent operations
        tasks = [flowise_client.list_chatflows() for _ in range(10)]
        await asyncio.gather(*tasks)

        # Then: sequential operations should still work
        for _ in range(5):
            result = await flowise_client.list_chatflows()
            assert isinstance(result, list)
