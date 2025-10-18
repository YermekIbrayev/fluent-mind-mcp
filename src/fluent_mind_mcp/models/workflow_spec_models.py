"""
Pydantic models for spec-driven workflow specification artifacts.

Defines models for chatflow specification, implementation plan,
and task breakdown (User Story 7).
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ChatflowSpecification(BaseModel):
    """
    Formal chatflow specification generated from requirements.

    Includes nodes, connections, parameters, and acceptance criteria.
    """

    spec_id: str = Field(
        ...,
        description="Unique specification identifier",
        examples=["spec_001"]
    )
    title: str = Field(..., description="Chatflow title")
    description: str = Field(..., description="What the chatflow does")
    required_nodes: list[str] = Field(
        ...,
        description="Node names required"
    )
    connections: list[dict[str, str]] = Field(
        default_factory=list,
        description="Node connections (from_node, to_node)",
        examples=[[{"from": "chatOpenAI", "to": "bufferMemory"}]]
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration parameters"
    )
    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="Success criteria for validation"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Specification creation time"
    )


class ImplementationPlan(BaseModel):
    """
    Technical implementation plan for chatflow.

    Includes architecture, file structure, and build strategy.
    """

    plan_id: str = Field(
        ...,
        description="Unique plan identifier",
        examples=["plan_001"]
    )
    architecture: str = Field(
        ...,
        description="High-level architecture description"
    )
    node_layout: dict[str, Any] = Field(
        ...,
        description="Node positioning and flow structure"
    )
    build_approach: str = Field(
        ...,
        description="How to construct flowData",
        examples=["template_based", "custom_assembly"]
    )
    estimated_complexity: int = Field(
        ...,
        ge=1,
        le=10,
        description="Complexity score (1-10)"
    )


class TaskBreakdown(BaseModel):
    """
    Task breakdown for chatflow implementation.

    Dependency-ordered tasks for execution.
    """

    task_id: str = Field(
        ...,
        description="Unique task identifier",
        examples=["T001", "T002"]
    )
    description: str = Field(..., description="Task description")
    dependencies: list[str] = Field(
        default_factory=list,
        description="Task IDs that must complete first"
    )
    estimated_duration: str | None = Field(
        None,
        description="Estimated time to complete",
        examples=["5 minutes", "10 minutes"]
    )
    status: str = Field(
        default="pending",
        description="Task status",
        examples=["pending", "in_progress", "completed"]
    )


class ConsistencyAnalysis(BaseModel):
    """
    Cross-artifact consistency check result.

    Validates spec, plan, and tasks alignment.
    """

    is_consistent: bool = Field(
        ...,
        description="Whether artifacts are consistent"
    )
    issues: list[str] = Field(
        default_factory=list,
        description="Inconsistencies found"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Suggested fixes"
    )


class ChatflowDesignSummary(BaseModel):
    """
    Compact design summary for user approval (<500 tokens per NFR-017).

    Includes nodes, connections, and key parameters.
    """

    title: str = Field(..., description="Chatflow title")
    summary: str = Field(
        ...,
        max_length=500,
        description="Brief design description (<500 tokens)"
    )
    nodes_summary: list[str] = Field(
        ...,
        description="List of node names",
        examples=[["chatOpenAI", "bufferMemory", "conversationChain"]]
    )
    connections_count: int = Field(
        ...,
        ge=0,
        description="Number of connections"
    )
    key_parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Important configuration values"
    )
