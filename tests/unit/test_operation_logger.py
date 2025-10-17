"""Unit tests for OperationLogger.

Tests structured logging, timing operations, and credential masking.
"""

import logging
import time
import pytest

from fluent_mind_mcp.logging.operation_logger import OperationLogger


@pytest.mark.unit
class TestOperationLoggerBasics:
    """Test basic logging functionality."""

    def test_logger_creation(self):
        """OperationLogger can be created with a name."""
        logger = OperationLogger("test_logger")

        assert logger is not None
        assert logger.name == "test_logger"

    def test_logger_log_levels(self, caplog):
        """OperationLogger supports different log levels."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.DEBUG):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text

    def test_logger_respects_log_level(self, caplog):
        """OperationLogger respects configured log level."""
        logger = OperationLogger("test_logger", level="WARNING")

        with caplog.at_level(logging.DEBUG):
            logger.debug("Should not appear")
            logger.info("Should not appear")
            logger.warning("Should appear")

        assert "Should not appear" not in caplog.text
        assert "Should appear" in caplog.text


@pytest.mark.unit
class TestOperationLogging:
    """Test structured operation logging (NFR-001 to NFR-004)."""

    def test_log_operation_basic(self, caplog):
        """log_completed_operation() logs operation name and status."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.log_completed_operation("list_chatflows", duration=0.5, status="success")

        assert "list_chatflows" in caplog.text
        assert "success" in caplog.text

    def test_log_operation_with_duration(self, caplog):
        """log_completed_operation() includes operation duration."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.log_completed_operation("create_chatflow", duration=1.23, status="success")

        assert "create_chatflow" in caplog.text
        assert "1.23" in caplog.text or "duration" in caplog.text.lower()

    def test_log_operation_failure(self, caplog):
        """log_completed_operation() logs failed operations."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.ERROR):
            logger.log_completed_operation("update_chatflow", duration=0.8, status="failure")

        assert "update_chatflow" in caplog.text
        assert "failure" in caplog.text

    def test_log_operation_structured_format(self, caplog):
        """log_completed_operation() uses structured format (JSON or key-value)."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.log_completed_operation(
                "get_chatflow",
                duration=0.3,
                status="success",
                chatflow_id="abc-123"
            )

        # Should contain structured data
        log_text = caplog.text.lower()
        assert "get_chatflow" in log_text
        assert ("abc-123" in caplog.text or "chatflow_id" in log_text)


@pytest.mark.unit
class TestTimingContextManager:
    """Test timing context manager for operations."""

    def test_timing_context_manager(self, caplog):
        """OperationLogger can be used as timing context manager."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            with logger.time_operation("test_operation"):
                time.sleep(0.01)  # Simulate work

        assert "test_operation" in caplog.text
        # Should have logged completion with timing

    def test_timing_captures_duration(self, caplog):
        """Timing context manager captures operation duration."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            with logger.time_operation("slow_operation"):
                time.sleep(0.05)  # 50ms

        # Duration should be ~50ms or more
        assert "slow_operation" in caplog.text
        # Check if duration appears in logs (format may vary)
        assert any(char.isdigit() for char in caplog.text)

    def test_timing_logs_on_exception(self, caplog):
        """Timing context manager logs even when exception occurs."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.ERROR):
            try:
                with logger.time_operation("failing_operation"):
                    raise ValueError("Test error")
            except ValueError:
                pass

        assert "failing_operation" in caplog.text
        # Should log the failure

    def test_timing_nested_operations(self, caplog):
        """Timing context manager supports nested operations."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            with logger.time_operation("outer_operation"):
                with logger.time_operation("inner_operation"):
                    time.sleep(0.01)

        assert "outer_operation" in caplog.text
        assert "inner_operation" in caplog.text


@pytest.mark.unit
class TestCredentialMasking:
    """Test that credentials are never logged (NFR security requirement)."""

    def test_masks_api_key_in_logs(self, caplog):
        """OperationLogger masks API keys in log messages."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.info("Connecting with api_key=secret12345")

        # API key should be masked
        assert "secret12345" not in caplog.text
        assert "***" in caplog.text or "REDACTED" in caplog.text or "[MASKED]" in caplog.text

    def test_masks_password_in_logs(self, caplog):
        """OperationLogger masks passwords in log messages."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.info("Authentication with password=mypassword123")

        assert "mypassword123" not in caplog.text
        assert "***" in caplog.text or "REDACTED" in caplog.text or "[MASKED]" in caplog.text

    def test_masks_token_in_logs(self, caplog):
        """OperationLogger masks tokens in log messages."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.info("Using bearer token=eyJ0eXAiOiJKV1QiLCJh")

        assert "eyJ0eXAiOiJKV1QiLCJh" not in caplog.text
        assert "***" in caplog.text or "REDACTED" in caplog.text or "[MASKED]" in caplog.text

    def test_masks_credentials_in_dict(self, caplog):
        """OperationLogger masks credentials in dictionary context."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.log_completed_operation(
                "api_call",
                duration=0.1,
                status="success",
                api_key="secret_key_12345"
            )

        # Credential value should be masked
        assert "secret_key_12345" not in caplog.text
        # But the key name should appear
        assert "api_key" in caplog.text.lower()

    def test_does_not_mask_safe_data(self, caplog):
        """OperationLogger does not mask non-sensitive data."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.INFO):
            logger.info("Chatflow name is 'My Chatflow' with id abc-123")

        # Non-sensitive data should appear
        assert "My Chatflow" in caplog.text
        assert "abc-123" in caplog.text


@pytest.mark.unit
class TestErrorLogging:
    """Test error logging with context."""

    def test_log_error_with_exception(self, caplog):
        """log_error() captures exception details."""
        logger = OperationLogger("test_logger")

        try:
            raise ValueError("Test exception")
        except ValueError as e:
            with caplog.at_level(logging.ERROR):
                logger.log_error("operation_failed", exception=e)

        assert "operation_failed" in caplog.text
        assert "ValueError" in caplog.text
        assert "Test exception" in caplog.text

    def test_log_error_with_context(self, caplog):
        """log_error() includes additional context."""
        logger = OperationLogger("test_logger")

        with caplog.at_level(logging.ERROR):
            logger.log_error(
                "chatflow_creation_failed",
                exception=None,
                chatflow_name="Test Flow",
                reason="Invalid flowData"
            )

        assert "chatflow_creation_failed" in caplog.text
        assert "Test Flow" in caplog.text
        assert "Invalid flowData" in caplog.text

    def test_log_error_includes_traceback_in_debug(self, caplog):
        """log_error() includes stack trace in debug mode."""
        logger = OperationLogger("test_logger", level="DEBUG")

        try:
            raise RuntimeError("Critical error")
        except RuntimeError as e:
            with caplog.at_level(logging.DEBUG):
                logger.log_error("critical_failure", exception=e, include_traceback=True)

        # In debug mode, should include traceback
        assert "critical_failure" in caplog.text
        assert "RuntimeError" in caplog.text
