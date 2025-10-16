"""Configuration model for Flowise API connection.

This module provides the FlowiseConfig Pydantic model for validating
and loading configuration from environment variables.
"""

import os
from typing import Literal, Optional

from pydantic import Field, field_validator, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class FlowiseConfig(BaseSettings):
    """Configuration for Flowise API connection.

    Loads configuration from environment variables with validation.
    All fields follow the validation rules from data-model.md.

    Attributes:
        api_url: Flowise instance URL (HTTP/HTTPS only)
        api_key: Optional API key for authentication (min 8 chars)
        timeout: Request timeout in seconds (1-600)
        max_connections: Connection pool size (1-50)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        flowise_version: Target Flowise version (informational)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        # Allow both programmatic and env var initialization
        populate_by_name=True,
    )

    api_url: HttpUrl = Field(
        ...,
        description="Flowise instance URL",
        alias="FLOWISE_API_URL",
    )

    api_key: Optional[str] = Field(
        None,
        min_length=8,
        description="API key for Flowise authentication",
        alias="FLOWISE_API_KEY",
    )

    timeout: int = Field(
        60,
        ge=1,
        le=600,
        description="Request timeout in seconds",
        alias="FLOWISE_TIMEOUT",
    )

    max_connections: int = Field(
        10,
        ge=1,
        le=50,
        description="Connection pool size",
        alias="FLOWISE_MAX_CONNECTIONS",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        "INFO",
        description="Logging level",
        alias="LOG_LEVEL",
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
        # Pydantic Settings automatically loads from environment
        return cls()

    @property
    def name(self) -> str:
        """Get a friendly name for logging.

        WHY: Useful for identifying this config in logs without exposing sensitive data.
        """
        return "FlowiseConfig"
