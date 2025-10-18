"""
Pydantic models for Flowise flowData structures.

Defines models for nodes, edges, positions, and flowData graph
used in chatflow creation (User Story 3).
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class ChatflowStatus(str, Enum):
    """Chatflow operation status."""

    SUCCESS = "success"
    ERROR = "error"


class Position(BaseModel):
    """Node position in flowData graph."""

    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")


class Node(BaseModel):
    """
    Flowise flowData node structure.

    Represents a single node in the chatflow graph.
    """

    id: str = Field(..., description="Unique node ID in flow")
    position: Position = Field(..., description="Node position")
    type: str = Field(
        default="customNode",
        description="Node type (usually 'customNode')"
    )
    data: dict[str, Any] = Field(
        ...,
        description="Node configuration and parameters"
    )


class Edge(BaseModel):
    """
    Flowise flowData edge structure.

    Represents a connection between two nodes.
    """

    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    sourceHandle: str | None = Field(
        None,
        description="Source output handle"
    )
    targetHandle: str | None = Field(
        None,
        description="Target input handle"
    )
    id: str | None = Field(
        None,
        description="Edge ID (auto-generated if not provided)"
    )


class ChatflowResponse(BaseModel):
    """
    Response from chatflow operations (create, update, delete).

    Compact response format for token efficiency (<30 tokens for success).
    """

    chatflow_id: str = Field(..., description="Chatflow identifier")
    name: str = Field(..., description="Chatflow name")
    status: ChatflowStatus = Field(..., description="Operation status")
    error: str | None = Field(
        None,
        max_length=200,
        description="Error message if failed (<50 tokens per NFR-006)"
    )


class BuildFlowRequest(BaseModel):
    """
    Input to build_flow function (User Story 3).

    Supports two modes: template-based (via template_id) or
    custom assembly (via nodes list).
    """

    template_id: str | None = Field(
        None,
        description="Template to instantiate",
        examples=["tmpl_simple_chat"]
    )
    nodes: list[str] | None = Field(
        None,
        description="Custom node list for assembly",
        examples=[["chatOpenAI", "bufferMemory", "conversationChain"]]
    )
    connections: str | None = Field(
        None,
        description="'auto' for automatic or manual edge specification",
        examples=["auto"]
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional customizations"
    )

    @field_validator("parameters")
    @classmethod
    def validate_exactly_one_mode(cls, v: dict[str, Any], info) -> dict[str, Any]:
        """Validate exactly one of template_id or nodes is provided."""
        template_id = info.data.get("template_id")
        nodes = info.data.get("nodes")

        if template_id and nodes:
            raise ValueError("Provide either template_id or nodes, not both")
        if not template_id and not nodes:
            raise ValueError("Must provide either template_id or nodes")

        return v


class FlowTemplate(BaseModel):
    """
    Template retrieved from vector database.

    WHY: Proper model class for template data structure ensures type safety
    and provides attribute access (template.template_id) while maintaining
    dict compatibility through model_dump().
    """

    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Human-readable template name")
    flow_data: dict[str, Any] = Field(
        ...,
        description="Complete flowData structure (nodes, edges, viewport)"
    )
    nodes: list[dict] = Field(
        default_factory=list,
        description="Node list for backward compatibility with tests"
    )

    def __getitem__(self, key: str) -> Any:
        """Support dict-style access template['key'].

        WHY: Maintains backward compatibility with code expecting dict access.
        """
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        """Support dict.get() method.

        WHY: Maintains backward compatibility with template.get('key', default).
        """
        return getattr(self, key, default)


class BuildFlowResponse(BaseModel):
    """
    Output from build_flow function.

    Compact success response (<30 tokens per NFR-005).
    """

    chatflow_id: str = Field(..., description="Created chatflow ID")
    name: str = Field(..., description="Chatflow name")
    status: ChatflowStatus = Field(..., description="Operation status")
    error: str | None = Field(
        None,
        max_length=200,
        description="Error message if failed (<50 tokens)"
    )
