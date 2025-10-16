"""Unit tests for custom exception hierarchy.

Tests that exceptions inherit correctly and can be caught appropriately.
"""

import pytest

from fluent_mind_mcp.client.exceptions import (
    FlowiseClientError,
    ConnectionError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
)


@pytest.mark.unit
class TestExceptionHierarchy:
    """Test exception inheritance structure."""

    def test_base_exception_creation(self):
        """FlowiseClientError can be created with a message."""
        error = FlowiseClientError("Base error message")

        assert str(error) == "Base error message"
        assert isinstance(error, Exception)

    def test_connection_error_inherits_from_base(self):
        """ConnectionError inherits from FlowiseClientError."""
        error = ConnectionError("Connection failed")

        assert isinstance(error, FlowiseClientError)
        assert isinstance(error, Exception)
        assert str(error) == "Connection failed"

    def test_authentication_error_inherits_from_base(self):
        """AuthenticationError inherits from FlowiseClientError."""
        error = AuthenticationError("Invalid API key")

        assert isinstance(error, FlowiseClientError)
        assert isinstance(error, Exception)
        assert str(error) == "Invalid API key"

    def test_validation_error_inherits_from_base(self):
        """ValidationError inherits from FlowiseClientError."""
        error = ValidationError("Invalid request data")

        assert isinstance(error, FlowiseClientError)
        assert isinstance(error, Exception)
        assert str(error) == "Invalid request data"

    def test_not_found_error_inherits_from_base(self):
        """NotFoundError inherits from FlowiseClientError."""
        error = NotFoundError("Chatflow not found")

        assert isinstance(error, FlowiseClientError)
        assert isinstance(error, Exception)
        assert str(error) == "Chatflow not found"

    def test_rate_limit_error_inherits_from_base(self):
        """RateLimitError inherits from FlowiseClientError."""
        error = RateLimitError("Too many requests")

        assert isinstance(error, FlowiseClientError)
        assert isinstance(error, Exception)
        assert str(error) == "Too many requests"


@pytest.mark.unit
class TestExceptionCatching:
    """Test that exceptions can be caught at different levels."""

    def test_catch_specific_connection_error(self):
        """ConnectionError can be caught specifically."""
        with pytest.raises(ConnectionError) as exc_info:
            raise ConnectionError("Connection timeout")

        assert "Connection timeout" in str(exc_info.value)

    def test_catch_all_via_base_exception(self):
        """All custom exceptions can be caught via FlowiseClientError."""
        exceptions_to_test = [
            ConnectionError("test"),
            AuthenticationError("test"),
            ValidationError("test"),
            NotFoundError("test"),
            RateLimitError("test"),
        ]

        for error in exceptions_to_test:
            with pytest.raises(FlowiseClientError):
                raise error

    def test_catch_authentication_error_does_not_catch_connection_error(self):
        """Catching AuthenticationError doesn't catch ConnectionError."""
        with pytest.raises(ConnectionError):
            # This should NOT be caught by AuthenticationError handler
            try:
                raise ConnectionError("Connection issue")
            except AuthenticationError:
                pytest.fail("ConnectionError should not be caught by AuthenticationError")


@pytest.mark.unit
class TestExceptionDetails:
    """Test exception details and additional context."""

    def test_exception_with_details_dict(self):
        """Exceptions can store additional details dictionary."""
        details = {"status_code": 500, "url": "http://localhost:3000"}
        error = FlowiseClientError("Server error", details=details)

        assert str(error) == "Server error"
        assert error.details == details
        assert error.details["status_code"] == 500

    def test_exception_without_details(self):
        """Exceptions work without details dictionary."""
        error = FlowiseClientError("Simple error")

        assert str(error) == "Simple error"
        assert error.details is None or error.details == {}

    def test_authentication_error_with_details(self):
        """AuthenticationError can include response details."""
        details = {"status_code": 401, "response": "Unauthorized"}
        error = AuthenticationError("Invalid credentials", details=details)

        assert isinstance(error, FlowiseClientError)
        assert error.details["status_code"] == 401

    def test_not_found_error_with_chatflow_id(self):
        """NotFoundError can include the missing chatflow ID."""
        details = {"chatflow_id": "abc-123-def", "status_code": 404}
        error = NotFoundError("Chatflow not found", details=details)

        assert isinstance(error, FlowiseClientError)
        assert error.details["chatflow_id"] == "abc-123-def"


@pytest.mark.unit
def test_exception_repr():
    """Exception __repr__ includes class name and message."""
    error = ConnectionError("Connection failed")

    repr_str = repr(error)
    assert "ConnectionError" in repr_str
    assert "Connection failed" in repr_str
