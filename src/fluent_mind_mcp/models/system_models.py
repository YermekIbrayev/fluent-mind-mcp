"""
Pydantic models for system health and infrastructure.

Defines models for cache metadata, circuit breaker state,
refresh results, and system health monitoring.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CircuitState(str, Enum):
    """Circuit breaker state."""

    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class DependencyName(str, Enum):
    """External dependency names for circuit breaker."""

    FLOWISE_API = "flowise_api"
    VECTOR_DB = "vector_db"
    EMBEDDING_MODEL = "embedding_model"


class RefreshResult(BaseModel):
    """
    Result from dynamic catalog refresh (User Story 6).

    Reports nodes added, updated, and removed.
    """

    nodes_added: int = Field(..., ge=0, description="New nodes added")
    nodes_updated: int = Field(..., ge=0, description="Nodes updated")
    nodes_removed: int = Field(..., ge=0, description="Deprecated nodes removed")
    total_nodes: int = Field(..., ge=0, description="Total nodes in catalog")
    refresh_timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When refresh completed"
    )


class CacheMetadata(BaseModel):
    """
    Vector DB cache freshness tracking.

    Used to determine when catalog refresh is needed.
    """

    last_refresh_timestamp: datetime = Field(
        ...,
        description="Last successful refresh"
    )
    total_node_count: int = Field(
        ...,
        ge=0,
        description="Nodes in cache"
    )
    flowise_version: str | None = Field(
        None,
        description="Flowise server version"
    )
    staleness_threshold_hours: int = Field(
        default=24,
        ge=1,
        description="Refresh trigger threshold"
    )

    def is_stale(self) -> bool:
        """Check if cache is stale based on threshold."""
        age_hours = (datetime.now() - self.last_refresh_timestamp).total_seconds() / 3600
        return age_hours > self.staleness_threshold_hours


class CircuitBreakerState(BaseModel):
    """
    Circuit breaker state per dependency.

    Manages failure tracking and state transitions for resilience.
    """

    dependency_name: DependencyName = Field(
        ...,
        description="External dependency name"
    )
    state: CircuitState = Field(
        default=CircuitState.CLOSED,
        description="Current circuit state"
    )
    failure_count: int = Field(
        default=0,
        ge=0,
        le=3,
        description="Consecutive failures"
    )
    last_failure_time: datetime | None = Field(
        None,
        description="When last failure occurred"
    )
    opened_time: datetime | None = Field(
        None,
        description="When circuit opened"
    )
    failure_threshold: int = Field(
        default=3,
        ge=1,
        description="Failures before opening circuit"
    )
    timeout_seconds: int = Field(
        default=300,
        ge=1,
        description="Time before attempting half-open (5 minutes)"
    )

    def should_attempt_reset(self) -> bool:
        """Check if circuit should attempt transition to half-open."""
        if self.state != CircuitState.OPEN or not self.opened_time:
            return False

        elapsed = (datetime.now() - self.opened_time).total_seconds()
        return elapsed >= self.timeout_seconds


class SystemHealth(BaseModel):
    """
    Overall system health status.

    Aggregates health from all dependencies.
    """

    is_healthy: bool = Field(..., description="Overall health status")
    flowise_api_status: str = Field(
        ...,
        description="Flowise API status",
        examples=["healthy", "degraded", "unavailable"]
    )
    vector_db_status: str = Field(
        ...,
        description="Vector DB status"
    )
    embedding_model_status: str = Field(
        ...,
        description="Embedding model status"
    )
    circuit_breaker_states: dict[str, CircuitState] = Field(
        default_factory=dict,
        description="Circuit states per dependency"
    )
    last_check: datetime = Field(
        default_factory=datetime.now,
        description="When health check was performed"
    )
