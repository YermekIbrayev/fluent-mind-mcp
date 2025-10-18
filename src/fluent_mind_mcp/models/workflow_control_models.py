"""
Pydantic models for spec-driven workflow control and coordination.

Defines models for complexity analysis, clarification, feedback,
and workflow orchestration (User Story 7).
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ComplexityLevel(str, Enum):
    """Chatflow complexity classification."""

    SIMPLE = "simple"
    COMPLEX = "complex"


class WorkflowPhase(str, Enum):
    """Spec-driven workflow phase."""

    SPECIFY = "specify"
    CLARIFY = "clarify"
    PLAN = "plan"
    TASKS = "tasks"
    ANALYZE = "analyze"
    APPROVE = "approve"
    IMPLEMENT = "implement"
    COMPLETED = "completed"
    FAILED = "failed"


class ComplexityAnalysis(BaseModel):
    """
    Chatflow complexity analysis result.

    Determines routing between simple build_flow path vs spec-driven workflow.
    Analyzes node count, template confidence, and complexity keywords.
    """

    complexity_level: ComplexityLevel = Field(
        ...,
        description="Simple or complex classification"
    )
    node_count_estimate: int = Field(
        ...,
        ge=0,
        description="Estimated number of nodes required"
    )
    template_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence that existing template matches (0.0-1.0)"
    )
    complexity_indicators: list[str] = Field(
        default_factory=list,
        description="Keywords/phrases indicating complexity",
        examples=[["multiple integrations", "custom logic"]]
    )
    recommended_path: str = Field(
        ...,
        description="'simple' for build_flow, 'spec_driven' for workflow",
        examples=["simple", "spec_driven"]
    )
    reasoning: str = Field(
        ...,
        max_length=200,
        description="Brief explanation for routing decision"
    )


class ClarificationQuestion(BaseModel):
    """
    Clarification question for ambiguous chatflow requirements.

    Used in spec-driven workflow to resolve underspecified areas.
    """

    question_id: str = Field(
        ...,
        description="Unique question identifier",
        examples=["q1", "q2"]
    )
    question_text: str = Field(
        ...,
        max_length=200,
        description="Clarification question (<200 tokens per NFR-016)"
    )
    category: str = Field(
        ...,
        description="Question category",
        examples=["nodes", "connections", "parameters", "behavior"]
    )
    answer: str | None = Field(
        None,
        description="User's answer (if provided)"
    )
    is_answered: bool = Field(
        default=False,
        description="Whether question has been answered"
    )


class FeedbackLoop(BaseModel):
    """
    User feedback iteration tracker.

    Manages design approval feedback loop (max 5 iterations per NFR-021).
    """

    iteration_number: int = Field(
        ...,
        ge=1,
        le=5,
        description="Current iteration (1-5)"
    )
    feedback: str = Field(..., description="User feedback")
    changes_requested: list[str] = Field(
        default_factory=list,
        description="Requested modifications"
    )
    is_approved: bool = Field(
        default=False,
        description="Whether design is approved"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Feedback timestamp"
    )


class WorkflowResponse(BaseModel):
    """
    Spec-driven workflow status response.

    Tracks current phase and provides next steps.
    """

    workflow_id: str = Field(
        ...,
        description="Unique workflow identifier",
        examples=["wf_001"]
    )
    current_phase: WorkflowPhase = Field(
        ...,
        description="Current workflow phase"
    )
    status: str = Field(
        ...,
        description="Status message",
        examples=["Specification generated", "Awaiting approval"]
    )
    next_steps: list[str] = Field(
        default_factory=list,
        description="Actions required to proceed"
    )
    artifacts: dict[str, Any] = Field(
        default_factory=dict,
        description="Generated artifacts (spec, plan, tasks)"
    )
