"""Configuration model for Flowise API connection.

This module provides the FlowiseConfig Pydantic model for validating
and loading configuration from environment variables.
"""

import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field, HttpUrl, field_validator


class FlowiseConfig(BaseModel):
    """Configuration for Flowise API connection.

    Can be initialized programmatically or loaded from environment variables.
    All fields follow the validation rules from data-model.md.

    Attributes:
        api_url: Flowise instance URL (HTTP/HTTPS only)
        api_key: Optional API key for authentication (min 8 chars)
        timeout: Request timeout in seconds (1-600)
        max_connections: Connection pool size (1-50)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        flowise_version: Target Flowise version (informational)
    """

    api_url: HttpUrl = Field(
        ...,
        description="Flowise instance URL",
    )

    api_key: str | None = Field(
        None,
        min_length=8,
        description="API key for Flowise authentication",
    )

    timeout: int = Field(
        60,
        ge=1,
        le=600,
        description="Request timeout in seconds",
    )

    max_connections: int = Field(
        10,
        ge=1,
        le=50,
        description="Connection pool size",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        "INFO",
        description="Logging level",
    )

    flowise_version: str = Field(
        "v1.x",
        description="Target Flowise version (informational)",
    )

    @field_validator("api_url")
    @classmethod
    def validate_http_url(cls, v: HttpUrl) -> HttpUrl:
        """Ensure URL is HTTP or HTTPS only.

        WHY: Flowise API only supports HTTP/HTTPS protocols.
        """
        url_str = str(v)
        if not (url_str.startswith("http://") or url_str.startswith("https://")):
            raise ValueError("api_url must be HTTP or HTTPS")
        return v

    @classmethod
    def from_env(cls) -> "FlowiseConfig":
        """Load configuration from environment variables.

        Reads from .env file if present, falls back to system environment.

        Returns:
            FlowiseConfig instance with validated configuration

        Raises:
            ValidationError: If required variables missing or invalid
        """
        # Load .env file if not running tests
        if not os.getenv("PYTEST_CURRENT_TEST"):
            load_dotenv()

        # WHY: Manually load from environment to avoid BaseSettings
        # which always prioritizes env vars over constructor args
        api_url = os.getenv("FLOWISE_API_URL")
        if not api_url:
            from pydantic_core import ValidationError as CoreValidationError

            raise CoreValidationError.from_exception_data(
                "Value error",
                [
                    {
                        "type": "missing",
                        "loc": ("FLOWISE_API_URL",),
                        "input": {},
                    }
                ],
            )

        return cls(
            api_url=api_url,  # type: ignore[arg-type]
            api_key=os.getenv("FLOWISE_API_KEY"),
            timeout=int(os.getenv("FLOWISE_TIMEOUT", "60")),
            max_connections=int(os.getenv("FLOWISE_MAX_CONNECTIONS", "10")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),  # type: ignore
            flowise_version=os.getenv("FLOWISE_VERSION", "v1.x"),
        )

    @property
    def name(self) -> str:
        """Get a friendly name for logging.

        WHY: Useful for identifying this config in logs without exposing sensitive data.
        """
        return "FlowiseConfig"
