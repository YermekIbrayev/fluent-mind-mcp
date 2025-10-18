"""
Pydantic models for flow templates and template search.

Defines models for pre-built chatflow patterns stored in ChromaDB
with vector embeddings for semantic discovery (User Story 2).
"""

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class FlowTemplate(BaseModel):
    """
    Pre-built chatflow pattern stored in ChromaDB 'templates' collection.

    Templates enable token-efficient chatflow creation via template_id
    reference instead of inline flowData specification.
    """

    template_id: str = Field(
        ...,
        pattern=r"^tmpl_[a-z0-9_]+$",
        description="Unique template identifier (prefix 'tmpl_')",
        examples=["tmpl_simple_chat", "tmpl_rag_flow"]
    )
    name: str = Field(
        ...,
        description="Template name",
        examples=["Simple Chat", "RAG Flow"]
    )
    description: str = Field(
        ...,
        description="Rich template documentation (what/why/when)",
        examples=["Basic conversational chatflow with memory"]
    )
    required_nodes: list[str] = Field(
        default_factory=list,
        description="Node names required in this template",
        examples=[["chatOpenAI", "bufferMemory"]]
    )
    flow_data: dict[str, Any] = Field(
        ...,
        description="Complete Flowise flowData structure (nodes + edges)"
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Customizable parameters with defaults",
        examples=[{"model_name": "gpt-4", "temperature": 0.7}]
    )
    embedding: Optional[list[float]] = Field(
        None,
        description="384-dim vector (all-MiniLM-L6-v2)"
    )

    @field_validator("embedding")
    @classmethod
    def validate_embedding_dimension(cls, v: Optional[list[float]]) -> Optional[list[float]]:
        """Validate embedding is 384 dimensions if provided."""
        if v is not None and len(v) != 384:
            raise ValueError(f"Embedding must be 384 dimensions, got {len(v)}")
        return v

    @field_validator("flow_data")
    @classmethod
    def validate_flow_data_structure(cls, v: dict[str, Any]) -> dict[str, Any]:
        """Validate flowData has required fields."""
        if "nodes" not in v:
            raise ValueError("flowData must contain 'nodes' field")
        if "edges" not in v:
            raise ValueError("flowData must contain 'edges' field")
        return v


class TemplateMetadata(BaseModel):
    """
    Template metadata for catalog management.

    Lightweight representation without full flowData.
    """

    template_id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Brief description")
    required_nodes: list[str] = Field(
        default_factory=list,
        description="Required node names"
    )
    parameter_count: int = Field(
        default=0,
        ge=0,
        description="Number of customizable parameters"
    )


class TemplateSummary(BaseModel):
    """
    Compact template representation for search results (<50 tokens).

    Used in template search responses to minimize token usage.
    """

    template_id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    summary: str = Field(
        ...,
        max_length=150,
        description="Brief description (max 150 chars)"
    )
    node_count: int = Field(
        ...,
        ge=1,
        description="Number of nodes in template"
    )


class TemplateSearchQuery(BaseModel):
    """
    Search query specifically for template discovery.

    Extends SearchQuery with template-specific filters.
    """

    query_text: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Natural language query",
        examples=["simple chat with memory", "RAG for documents"]
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum search results"
    )
    similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score"
    )
    required_nodes: Optional[list[str]] = Field(
        None,
        description="Filter templates that include these nodes",
        examples=[["chatOpenAI", "bufferMemory"]]
    )
    max_node_count: Optional[int] = Field(
        None,
        ge=1,
        description="Filter templates with at most N nodes"
    )
