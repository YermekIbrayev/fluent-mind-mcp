"""
Integration tests for edge case error scenarios.

WHY: Validate that the system handles all 8 edge cases from spec.md gracefully,
     providing user-friendly error messages and maintaining stability.

Edge Cases (from spec.md):
1. Flowise API URL is unreachable
2. Authentication failures (invalid API key)
3. Malformed or missing flowData JSON
4. Very large flowData structures (>1MB)
5. Executing chatflow during update (concurrent modification)
6. Rate limiting from Flowise API
7. Chatflow execution timeout
8. Concurrent operations on same chatflow

These tests validate NFR-001 to NFR-004 (observability), NFR-010 to NFR-012 (security),
and FR-005, FR-011, FR-013 (error handling).
"""

import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.client.exceptions import (
    ConnectionError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
)
from fluent_mind_mcp.models.config import FlowiseConfig


@pytest.fixture
def mock_config():
    """
    Provide test configuration.

    WHY: Tests need consistent configuration without requiring environment variables.
    """
    return FlowiseConfig(
        api_url="http://localhost:3000",
        api_key="test-key",
        timeout=60,
        max_connections=10,
        log_level="INFO"
    )


@pytest.fixture
def client(mock_config):
    """
    Provide FlowiseClient for testing.

    WHY: Tests need a client instance with mocked configuration.
    """
    return FlowiseClient(mock_config)


class TestEdgeCase1_UnreachableAPI:
    """
    Edge Case 1: What happens when Flowise API URL is unreachable?

    WHY: Network failures are common. System must provide clear error messages
         and not crash or hang indefinitely.
    """

    @pytest.mark.asyncio
    async def test_unreachable_host_returns_connection_error(self, client):
        """
        GIVEN unreachable Flowise API URL
        WHEN attempting to list chatflows
        THEN ConnectionError is raised with clear message
        """
        with patch.object(client._client, 'get', side_effect=httpx.ConnectError("Connection refused")):
            with pytest.raises(ConnectionError) as exc_info:
                await client.list_chatflows()

            assert "unable to connect" in str(exc_info.value).lower() or "connection" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_timeout_returns_connection_error(self, client):
        """
        GIVEN Flowise API that times out
        WHEN attempting to create chatflow
        THEN ConnectionError is raised mentioning timeout
        """
        with patch.object(client._client, 'post', side_effect=httpx.TimeoutException("Request timed out")):
            with pytest.raises(ConnectionError) as exc_info:
                await client.create_chatflow(
                    name="Test Flow",
                    flow_data='{"nodes": [], "edges": []}',
                    type="CHATFLOW",
                    deployed=False
                )

            assert "timeout" in str(exc_info.value).lower() or "timed out" in str(exc_info.value).lower()


class TestEdgeCase2_AuthenticationFailures:
    """
    Edge Case 2: How does system handle authentication failures (invalid API key)?

    WHY: Authentication failures must be clearly reported without exposing credentials.
         Validates NFR-012 (protect credentials in error messages).
    """

    @pytest.mark.asyncio
    async def test_invalid_api_key_returns_authentication_error(self, client):
        """
        GIVEN invalid API key
        WHEN attempting any operation
        THEN AuthenticationError is raised without exposing API key
        """
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid API key"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=MagicMock(),
            response=mock_response
        )

        with patch.object(client._client, 'get', return_value=mock_response):
            with pytest.raises(AuthenticationError) as exc_info:
                await client.list_chatflows()

            # Error message should NOT contain the actual API key
            error_msg = str(exc_info.value).lower()
            assert "test-key" not in error_msg
            assert "authentication" in error_msg or "unauthorized" in error_msg

    @pytest.mark.asyncio
    async def test_missing_api_key_handled_gracefully(self):
        """
        GIVEN configuration without API key (optional field)
        WHEN Flowise requires authentication
        THEN appropriate error is raised
        """
        config = FlowiseConfig(
            api_url="http://localhost:3000",
            timeout=60,
            max_connections=10,
            log_level="INFO"
        )
        client = FlowiseClient(config)

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "API key required"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=MagicMock(),
            response=mock_response
        )

        with patch.object(client._client, 'get', return_value=mock_response):
            with pytest.raises(AuthenticationError) as exc_info:
                await client.list_chatflows()

            assert "authentication" in str(exc_info.value).lower() or "unauthorized" in str(exc_info.value).lower()


class TestEdgeCase3_MalformedFlowData:
    """
    Edge Case 3: What happens when flowData JSON is malformed or missing required fields?

    WHY: User input validation is critical. System must reject invalid data gracefully
         with clear messages about what's wrong. Validates FR-004 and SC-004.
    """

    @pytest.mark.asyncio
    async def test_invalid_json_returns_validation_error(self, client):
        """
        GIVEN malformed JSON flowData
        WHEN attempting to create chatflow
        THEN ValidationError is raised with helpful message
        """
        with pytest.raises(ValidationError) as exc_info:
            await client.create_chatflow(
                name="Test Flow",
                flow_data='{"nodes": [invalid json',  # Malformed JSON
                type="CHATFLOW",
                deployed=False
            )

        error_msg = str(exc_info.value).lower()
        assert "invalid" in error_msg or "malformed" in error_msg or "json" in error_msg

    @pytest.mark.asyncio
    async def test_missing_nodes_field_returns_validation_error(self, client):
        """
        GIVEN flowData without required 'nodes' field
        WHEN attempting to create chatflow
        THEN ValidationError is raised mentioning missing field
        """
        with pytest.raises(ValidationError) as exc_info:
            await client.create_chatflow(
                name="Test Flow",
                flow_data='{"edges": []}',  # Missing 'nodes'
                type="CHATFLOW",
                deployed=False
            )

        error_msg = str(exc_info.value).lower()
        assert "nodes" in error_msg or "required" in error_msg

    @pytest.mark.asyncio
    async def test_missing_edges_field_returns_validation_error(self, client):
        """
        GIVEN flowData without required 'edges' field
        WHEN attempting to create chatflow
        THEN ValidationError is raised mentioning missing field
        """
        with pytest.raises(ValidationError) as exc_info:
            await client.create_chatflow(
                name="Test Flow",
                flow_data='{"nodes": []}',  # Missing 'edges'
                type="CHATFLOW",
                deployed=False
            )

        error_msg = str(exc_info.value).lower()
        assert "edges" in error_msg or "required" in error_msg


class TestEdgeCase4_LargeFlowData:
    """
    Edge Case 4: How does system handle very large flowData structures (>1MB)?

    WHY: Large payloads can cause memory issues, slow performance, or API rejections.
         System must enforce size limits per data-model.md (<1MB). Validates FR-004.
    """

    @pytest.mark.asyncio
    async def test_flowdata_exceeding_1mb_returns_validation_error(self, client):
        """
        GIVEN flowData exceeding 1MB size limit
        WHEN attempting to create chatflow
        THEN ValidationError is raised mentioning size limit
        """
        # Create a large flowData structure (>1MB)
        large_node_data = {"data": "x" * 500000}  # ~500KB per node
        large_flow_data = json.dumps({
            "nodes": [large_node_data, large_node_data, large_node_data],  # ~1.5MB total
            "edges": []
        })

        with pytest.raises(ValidationError) as exc_info:
            await client.create_chatflow(
                name="Large Flow",
                flow_data=large_flow_data,
                type="CHATFLOW",
                deployed=False
            )

        error_msg = str(exc_info.value).lower()
        assert "size" in error_msg or "large" in error_msg or "1mb" in error_msg or "limit" in error_msg

    @pytest.mark.asyncio
    async def test_flowdata_at_limit_accepted(self, client):
        """
        GIVEN flowData at exactly 1MB (within limit)
        WHEN attempting to create chatflow
        THEN operation proceeds (mock success response)
        """
        # Create flowData at ~1MB (slightly under to account for overhead)
        flow_data_size = 1024 * 1024 - 100  # 1MB - 100 bytes
        flow_data = json.dumps({
            "nodes": [{"data": "x" * (flow_data_size - 50)}],
            "edges": []
        })

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "test-id",
            "name": "Large Flow",
            "type": "CHATFLOW",
            "deployed": False,
            "flowData": flow_data
        }

        with patch.object(client._client, 'post', return_value=mock_response):
            # Should not raise ValidationError for size
            result = await client.create_chatflow(
                name="Large Flow",
                flow_data=flow_data,
                type="CHATFLOW",
                deployed=False
            )

            assert result.id == "test-id"


class TestEdgeCase5_ConcurrentModification:
    """
    Edge Case 5: What happens when attempting to execute a chatflow that is currently being updated?

    WHY: Concurrent operations can cause race conditions or inconsistent state.
         System must handle this gracefully, possibly with retry logic (T101).
    """

    @pytest.mark.asyncio
    async def test_409_conflict_during_execution_handled(self, client):
        """
        GIVEN chatflow being updated concurrently
        WHEN attempting to execute it
        THEN system handles 409 Conflict gracefully
        """
        from fluent_mind_mcp.client.exceptions import ConflictError

        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_response.json.return_value = {"message": "Chatflow is being updated"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "409 Conflict",
            request=MagicMock(),
            response=mock_response
        )

        with patch.object(client._client, 'post', return_value=mock_response):
            # Should raise ConflictError (not crash)
            with pytest.raises(ConflictError) as exc_info:
                await client.run_prediction("test-id", "test question")

            error_msg = str(exc_info.value).lower()
            assert "conflict" in error_msg or "concurrent" in error_msg or "modification" in error_msg


class TestEdgeCase6_RateLimiting:
    """
    Edge Case 6: How does system handle rate limiting from Flowise API?

    WHY: APIs may enforce rate limits. System must recognize 429 status codes
         and provide clear feedback. Validates FR-005, FR-013.
    """

    @pytest.mark.asyncio
    async def test_429_rate_limit_returns_rate_limit_error(self, client):
        """
        GIVEN Flowise API returning 429 Too Many Requests
        WHEN attempting any operation
        THEN RateLimitError is raised with helpful message
        """
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Rate limit exceeded"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "429 Too Many Requests",
            request=MagicMock(),
            response=mock_response
        )

        with patch.object(client._client, 'get', return_value=mock_response):
            with pytest.raises(RateLimitError) as exc_info:
                await client.list_chatflows()

            error_msg = str(exc_info.value).lower()
            assert "rate limit" in error_msg or "too many" in error_msg


class TestEdgeCase7_ExecutionTimeout:
    """
    Edge Case 7: What happens when chatflow execution times out?

    WHY: Long-running chatflows may exceed timeout. System must handle this
         gracefully and inform user. Validates FR-014, NFR-003 (operation timing).
    """

    @pytest.mark.asyncio
    async def test_execution_timeout_returns_connection_error(self, client):
        """
        GIVEN chatflow execution exceeding timeout
        WHEN running prediction
        THEN ConnectionError is raised mentioning timeout
        """
        with patch.object(client._client, 'post', side_effect=httpx.TimeoutException("Request timed out")):
            with pytest.raises(ConnectionError) as exc_info:
                await client.run_prediction("test-id", "complex question")

            error_msg = str(exc_info.value).lower()
            assert "timeout" in error_msg or "timed out" in error_msg


class TestEdgeCase8_ConcurrentOperations:
    """
    Edge Case 8: How does system handle concurrent operations on the same chatflow?

    WHY: Multiple AI assistants may operate on the same chatflow simultaneously.
         System must handle this safely per NFR-005, NFR-006, NFR-007 (5-10 concurrent ops).
    """

    @pytest.mark.asyncio
    async def test_concurrent_updates_detected(self, client):
        """
        GIVEN two concurrent update requests for same chatflow
        WHEN both attempt to update
        THEN system handles conflict gracefully (409 or successful merge)
        """
        from fluent_mind_mcp.client.exceptions import ConflictError

        # This is more of a stress test - actual implementation depends on Flowise API behavior
        # For now, we verify the client can handle 409 responses

        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {
            "id": "test-id",
            "name": "Updated 1",
            "type": "CHATFLOW",
            "deployed": False
        }

        mock_response_2 = MagicMock()
        mock_response_2.status_code = 409
        mock_response_2.json.return_value = {"message": "Concurrent modification detected"}
        mock_response_2.raise_for_status.side_effect = httpx.HTTPStatusError(
            "409 Conflict",
            request=MagicMock(),
            response=mock_response_2
        )

        # First update succeeds
        with patch.object(client._client, 'put', return_value=mock_response_1):
            result1 = await client.update_chatflow("test-id", name="Updated 1")
            assert result1.name == "Updated 1"

        # Second update detects conflict (retry logic will try twice, both fail)
        with patch.object(client._client, 'put', return_value=mock_response_2):
            with pytest.raises(ConflictError):
                await client.update_chatflow("test-id", name="Updated 2")


class TestUserFriendlyErrorMessages:
    """
    Validate that all error messages are user-friendly (not raw exceptions).

    WHY: AI assistants must be able to communicate issues clearly to end users.
         Validates SC-007 (clear error messages for all failure scenarios).
    """

    @pytest.mark.asyncio
    async def test_connection_errors_are_user_friendly(self, client):
        """
        GIVEN connection failure
        WHEN error is raised
        THEN message is clear and actionable
        """
        with patch.object(client._client, 'get', side_effect=httpx.ConnectError("Connection refused")):
            with pytest.raises(ConnectionError) as exc_info:
                await client.list_chatflows()

            error_msg = str(exc_info.value)
            # Should not contain raw technical stack traces or cryptic codes
            assert len(error_msg) > 0
            assert "connection" in error_msg.lower() or "connect" in error_msg.lower()

    @pytest.mark.asyncio
    async def test_validation_errors_mention_specific_field(self, client):
        """
        GIVEN invalid input (missing required field)
        WHEN validation error is raised
        THEN message mentions which field is problematic
        """
        with pytest.raises(ValidationError) as exc_info:
            await client.create_chatflow(
                name="Test",
                flow_data='{"nodes": []}',  # Missing 'edges'
                type="CHATFLOW",
                deployed=False
            )

        error_msg = str(exc_info.value).lower()
        # Should mention the specific field that's missing
        assert "edges" in error_msg or "field" in error_msg or "required" in error_msg

    @pytest.mark.asyncio
    async def test_not_found_error_is_clear(self, client):
        """
        GIVEN non-existent chatflow ID
        WHEN attempting to retrieve it
        THEN error clearly states chatflow not found
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Chatflow not found"}
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=MagicMock(),
            response=mock_response
        )

        with patch.object(client._client, 'get', return_value=mock_response):
            with pytest.raises(Exception) as exc_info:  # Could be NotFoundError or ValidationError
                await client.get_chatflow("non-existent-id")

            error_msg = str(exc_info.value).lower()
            assert "not found" in error_msg or "does not exist" in error_msg
