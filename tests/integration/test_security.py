"""Integration tests for security features.

Tests credential masking in real operations and validates that API keys
never appear in logs during actual HTTP requests.
"""

import logging
import os

import pytest

from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.logging.operation_logger import OperationLogger
from fluent_mind_mcp.models.config import FlowiseConfig
from fluent_mind_mcp.services.chatflow_service import ChatflowService


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("FLOWISE_API_URL"),
    reason="FLOWISE_API_URL not set - requires live Flowise instance"
)
class TestCredentialLeakage:
    """Test that credentials never leak into logs during real operations."""

    @pytest.mark.asyncio
    async def test_api_key_never_logged_in_list_operation(self, caplog):
        """API key should never appear in logs during list_chatflows operation."""
        # Get real config (which may have API key)
        config = FlowiseConfig.from_env()

        # Extract API key to verify it doesn't leak
        api_key = config.api_key

        # Skip if no API key configured
        if not api_key:
            pytest.skip("No API key configured - test requires authentication")

        logger = OperationLogger("test_security")

        async with FlowiseClient(config) as client:
            service = ChatflowService(client, logger)

            # Capture all logs at DEBUG level
            with caplog.at_level(logging.DEBUG):
                try:
                    await service.list_chatflows()
                except Exception:
                    # Even if operation fails, check logs
                    pass

            # Verify API key never appears in any log
            all_logs = caplog.text
            assert api_key not in all_logs, \
                f"API key leaked in logs! Found: {api_key[:5]}..."

            # Verify masking marker present (if credentials were attempted to be logged)
            # This is defensive - we shouldn't log credentials at all
            if "api_key" in all_logs.lower():
                assert "***" in all_logs, "Credentials mentioned but not masked"

    @pytest.mark.asyncio
    async def test_api_key_never_logged_in_create_operation(self, caplog):
        """API key should never appear in logs during create_chatflow operation."""
        config = FlowiseConfig.from_env()
        api_key = config.api_key

        if not api_key:
            pytest.skip("No API key configured")

        logger = OperationLogger("test_security")

        async with FlowiseClient(config) as client:
            service = ChatflowService(client, logger)

            flow_data = '{"nodes": [], "edges": []}'

            with caplog.at_level(logging.DEBUG):
                try:
                    await service.create_chatflow(
                        name="Security Test Flow",
                        flow_data=flow_data,
                        deployed=False
                    )
                except Exception:
                    pass  # We only care about logs

            # Verify API key never appears
            all_logs = caplog.text
            assert api_key not in all_logs, \
                f"API key leaked in logs during create! Found: {api_key[:5]}..."

    @pytest.mark.asyncio
    async def test_logger_masks_api_key_in_error_context(self, caplog):
        """API key should be masked even when included in error context."""
        logger = OperationLogger("test_security")

        # Simulate an error with API key in context
        fake_api_key = "sk_test_12345_secret_key_67890"

        with caplog.at_level(logging.ERROR):
            logger.log_error(
                "authentication_failed",
                exception=None,
                api_key=fake_api_key,
                reason="Invalid credentials"
            )

        # Verify the fake API key is masked
        assert fake_api_key not in caplog.text, \
            "API key leaked in error context!"
        assert "api_key" in caplog.text.lower(), \
            "api_key field name should appear"
        assert "***" in caplog.text, \
            "Masking marker should be present"

    @pytest.mark.asyncio
    async def test_bearer_token_format_masked(self, caplog):
        """Bearer token format should be masked in logs."""
        logger = OperationLogger("test_security")

        # Simulate log with bearer token
        bearer_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123"

        with caplog.at_level(logging.INFO):
            logger.info(f"Authenticating with token={bearer_token}")

        # Verify token is masked
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in caplog.text, \
            "JWT token leaked in logs!"
        assert "***" in caplog.text, \
            "Token should be masked"


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("FLOWISE_API_URL"),
    reason="FLOWISE_API_URL not set"
)
class TestInputSanitization:
    """Test that user inputs are properly sanitized."""

    @pytest.mark.asyncio
    async def test_chatflow_name_sql_injection_attempt(self):
        """Chatflow names with SQL injection attempts should be validated."""
        config = FlowiseConfig.from_env()
        logger = OperationLogger("test_security")

        async with FlowiseClient(config) as client:
            service = ChatflowService(client, logger)

            # Attempt SQL injection in name
            malicious_name = "Test'; DROP TABLE chatflows; --"
            flow_data = '{"nodes": [], "edges": []}'

            try:
                # This should either succeed (Flowise handles it) or fail gracefully
                result = await service.create_chatflow(
                    name=malicious_name,
                    flow_data=flow_data,
                    deployed=False
                )
                # If it succeeds, verify name is stored as-is (no execution)
                assert result.name == malicious_name

                # Clean up
                await service.delete_chatflow(result.id)
            except Exception as e:
                # If it fails, verify it's a validation error, not server crash
                assert "validation" in str(e).lower() or "invalid" in str(e).lower()

    @pytest.mark.asyncio
    async def test_question_xss_attempt(self):
        """Questions with XSS attempts should be handled safely."""
        config = FlowiseConfig.from_env()
        logger = OperationLogger("test_security")

        async with FlowiseClient(config) as client:
            service = ChatflowService(client, logger)

            # Get a test chatflow
            chatflows = await service.list_chatflows()
            if not chatflows:
                pytest.skip("No chatflows available for testing")

            test_chatflow = chatflows[0]

            # Attempt XSS in question
            malicious_question = "<script>alert('XSS')</script>What is AI?"

            try:
                # This should be handled by Flowise - we just verify no crash
                response = await service.run_prediction(
                    chatflow_id=test_chatflow.id,
                    question=malicious_question
                )
                # If successful, verify response is text (not executed script)
                assert isinstance(response.text, str)
                assert "<script>" not in response.text or response.text == malicious_question
            except Exception:
                # Expected - chatflow may not be deployed or may reject input
                pass


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("FLOWISE_API_URL"),
    reason="FLOWISE_API_URL not set"
)
class TestResponseValidation:
    """Test that API responses are validated before processing."""

    @pytest.mark.asyncio
    async def test_list_chatflows_validates_response_structure(self):
        """list_chatflows should validate response is a list."""
        config = FlowiseConfig.from_env()

        async with FlowiseClient(config) as client:
            # This should succeed with valid response
            chatflows = await client.list_chatflows()

            # Verify we got a list (not None, dict, etc.)
            assert isinstance(chatflows, list), \
                f"Expected list, got {type(chatflows)}"

            # If list is not empty, verify items are Chatflow objects
            if chatflows:
                from fluent_mind_mcp.models.chatflow import Chatflow
                assert all(isinstance(cf, Chatflow) for cf in chatflows), \
                    "All items should be Chatflow objects"

    @pytest.mark.asyncio
    async def test_get_chatflow_validates_required_fields(self):
        """get_chatflow should validate response has required fields."""
        config = FlowiseConfig.from_env()

        async with FlowiseClient(config) as client:
            # Get list to find a valid ID
            chatflows = await client.list_chatflows()
            if not chatflows:
                pytest.skip("No chatflows available")

            test_id = chatflows[0].id

            # Get specific chatflow
            chatflow = await client.get_chatflow(test_id)

            # Verify required fields are present
            assert chatflow.id is not None, "id is required"
            assert chatflow.name is not None, "name is required"
            assert chatflow.type is not None, "type is required"
            assert chatflow.deployed is not None, "deployed is required"

    @pytest.mark.asyncio
    async def test_prediction_response_validates_text_field(self):
        """run_prediction should validate response has text field."""
        config = FlowiseConfig.from_env()

        async with FlowiseClient(config) as client:
            # Get a deployed chatflow
            chatflows = await client.list_chatflows()
            deployed = [cf for cf in chatflows if cf.deployed]

            if not deployed:
                pytest.skip("No deployed chatflows available")

            # Try to find a working deployed chatflow
            response = None
            for chatflow in deployed:
                try:
                    # Execute chatflow
                    response = await client.run_prediction(
                        chatflow_id=chatflow.id,
                        question="Test question"
                    )
                    break  # Success! Use this chatflow
                except Exception:
                    # This chatflow may not be properly configured, try next
                    continue

            if response is None:
                pytest.skip("No working deployed chatflows available")

            # Verify response has required text field
            assert hasattr(response, 'text'), "Response must have text field"
            assert isinstance(response.text, str), "text must be a string"
            assert len(response.text) > 0, "text should not be empty"
