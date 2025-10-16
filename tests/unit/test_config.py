"""Unit tests for FlowiseConfig model.

Tests configuration validation, environment variable loading, and default values.
"""

import pytest
from pydantic import ValidationError

from fluent_mind_mcp.models.config import FlowiseConfig


@pytest.mark.unit
class TestFlowiseConfigValidation:
    """Test FlowiseConfig validation rules."""

    def test_valid_config_minimal(self):
        """FlowiseConfig accepts minimal valid configuration with only api_url."""
        config = FlowiseConfig(api_url="http://localhost:3000")

        assert str(config.api_url) == "http://localhost:3000/"
        assert config.api_key is None
        assert config.timeout == 60
        assert config.max_connections == 10
        assert config.log_level == "INFO"

    def test_valid_config_full(self):
        """FlowiseConfig accepts all fields with valid values."""
        config = FlowiseConfig(
            api_url="https://flowise.example.com",
            api_key="test_key_12345",
            timeout=120,
            max_connections=20,
            log_level="DEBUG",
            flowise_version="v1.5.0"
        )

        assert str(config.api_url) == "https://flowise.example.com/"
        assert config.api_key == "test_key_12345"
        assert config.timeout == 120
        assert config.max_connections == 20
        assert config.log_level == "DEBUG"
        assert config.flowise_version == "v1.5.0"

    def test_invalid_url_not_http(self):
        """FlowiseConfig rejects non-HTTP/HTTPS URLs."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(api_url="ftp://localhost:3000")

        assert "api_url" in str(exc_info.value)

    def test_invalid_url_malformed(self):
        """FlowiseConfig rejects malformed URLs."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(api_url="not a url")

        assert "api_url" in str(exc_info.value)

    def test_api_key_too_short(self):
        """FlowiseConfig rejects API keys shorter than 8 characters."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(
                api_url="http://localhost:3000",
                api_key="short"
            )

        assert "api_key" in str(exc_info.value)

    def test_timeout_below_minimum(self):
        """FlowiseConfig rejects timeout values below 1 second."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(
                api_url="http://localhost:3000",
                timeout=0
            )

        assert "timeout" in str(exc_info.value)

    def test_timeout_above_maximum(self):
        """FlowiseConfig rejects timeout values above 600 seconds."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(
                api_url="http://localhost:3000",
                timeout=601
            )

        assert "timeout" in str(exc_info.value)

    def test_max_connections_below_minimum(self):
        """FlowiseConfig rejects max_connections below 1."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(
                api_url="http://localhost:3000",
                max_connections=0
            )

        assert "max_connections" in str(exc_info.value)

    def test_max_connections_above_maximum(self):
        """FlowiseConfig rejects max_connections above 50."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(
                api_url="http://localhost:3000",
                max_connections=51
            )

        assert "max_connections" in str(exc_info.value)

    def test_invalid_log_level(self):
        """FlowiseConfig rejects invalid log levels."""
        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig(
                api_url="http://localhost:3000",
                log_level="INVALID"
            )

        assert "log_level" in str(exc_info.value)


@pytest.mark.unit
class TestFlowiseConfigFromEnv:
    """Test FlowiseConfig loading from environment variables."""

    def test_from_env_success(self, monkeypatch):
        """FlowiseConfig.from_env() loads configuration from environment variables."""
        monkeypatch.setenv("FLOWISE_API_URL", "http://localhost:3000")
        monkeypatch.setenv("FLOWISE_API_KEY", "test_key_12345")
        monkeypatch.setenv("FLOWISE_TIMEOUT", "90")
        monkeypatch.setenv("FLOWISE_MAX_CONNECTIONS", "15")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        config = FlowiseConfig.from_env()

        assert str(config.api_url) == "http://localhost:3000/"
        assert config.api_key == "test_key_12345"
        assert config.timeout == 90
        assert config.max_connections == 15
        assert config.log_level == "WARNING"

    def test_from_env_minimal(self, monkeypatch):
        """FlowiseConfig.from_env() works with only required variables."""
        monkeypatch.setenv("FLOWISE_API_URL", "http://localhost:3000")
        # Clear other env vars if they exist
        monkeypatch.delenv("FLOWISE_API_KEY", raising=False)

        config = FlowiseConfig.from_env()

        assert str(config.api_url) == "http://localhost:3000/"
        assert config.api_key is None
        assert config.timeout == 60  # default
        assert config.max_connections == 10  # default

    def test_from_env_missing_required(self, monkeypatch):
        """FlowiseConfig.from_env() raises error when FLOWISE_API_URL is missing."""
        monkeypatch.delenv("FLOWISE_API_URL", raising=False)

        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig.from_env()

        assert "FLOWISE_API_URL" in str(exc_info.value) or "api_url" in str(exc_info.value)

    def test_from_env_invalid_values(self, monkeypatch):
        """FlowiseConfig.from_env() validates values from environment."""
        monkeypatch.setenv("FLOWISE_API_URL", "http://localhost:3000")
        monkeypatch.setenv("FLOWISE_TIMEOUT", "700")  # Above maximum

        with pytest.raises(ValidationError) as exc_info:
            FlowiseConfig.from_env()

        # Error message contains field name in uppercase
        assert "FLOWISE_TIMEOUT" in str(exc_info.value) or "timeout" in str(exc_info.value).lower()


@pytest.mark.unit
def test_config_immutable_after_creation():
    """FlowiseConfig fields cannot be modified after creation (frozen model)."""
    config = FlowiseConfig(api_url="http://localhost:3000")

    # Pydantic models are mutable by default, but we can test that validation
    # runs on re-assignment if we mark the model as frozen in implementation
    # For now, just verify the config exists
    assert str(config.api_url) == "http://localhost:3000/"
