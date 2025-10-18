"""
Pydantic models for Flowise node catalog and search operations.

Defines models for node metadata, descriptions, and search queries/results
used in vector-enhanced semantic search (User Story 1).
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class QueryType(str, Enum):
    """Search query target type."""

    NODE = "node"
    TEMPLATE = "template"


class SearchQuery(BaseModel):
    """
    Natural language query for vector search.

    Used by AI assistants to discover nodes via semantic search.
    Example: "I need a node for OpenAI chat completions"
    """

    query_text: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Natural language query",
        examples=["OpenAI chat node", "memory for conversations"]
    )
    query_type: QueryType = Field(
        default=QueryType.NODE,
        description="Target search type (node or template)"
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum search results to return"
    )
    similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score (0.0-1.0)"
    )


class SearchResult(BaseModel):
    """
    Compact search result (<50 tokens).

    Returned from vector search with minimal metadata for token efficiency.
    """

    result_id: str = Field(
        ...,
        description="Node name or template_id",
        examples=["chatOpenAI", "bufferMemory"]
    )
    name: str = Field(
        ...,
        description="Display name",
        examples=["ChatOpenAI", "Buffer Memory"]
    )
    description: str = Field(
        ...,
        max_length=200,
        description="One-line summary (max 200 chars)"
    )
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Similarity score"
    )
    metadata: dict = Field(
        default_factory=dict,
        description="Category, baseClass, deprecated status",
        examples=[{"category": "Chat Models", "deprecated": False}]
    )


class NodeMetadata(BaseModel):
    """
    Live node catalog metadata from Flowise /api/v1/nodes-list.

    Represents real-time node information from Flowise server.
    Used in dynamic catalog refresh (User Story 6).
    """

    node_name: str = Field(..., description="Unique node identifier")
    label: str = Field(..., description="Display label")
    version: str = Field(..., description="Node version")
    category: str = Field(..., description="Node category")
    base_classes: list[str] = Field(
        default_factory=list,
        description="Type hierarchy"
    )
    description: str = Field(..., description="Node documentation")
    deprecated: bool = Field(default=False, description="Deprecation status")
    fetch_timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When metadata was fetched"
    )


class NodeDescription(BaseModel):
    """
    Flowise node documentation for semantic search.

    Stored in ChromaDB 'nodes' collection with vector embeddings.
    Enriched with what/why/how documentation for intelligent search.
    """

    node_name: str = Field(..., description="Unique node identifier")
    label: str = Field(..., description="Display label")
    category: str = Field(..., description="Node category")
    base_classes: list[str] = Field(
        default_factory=list,
        description="Type hierarchy"
    )
    description: str = Field(
        ...,
        description="What/why/how documentation"
    )
    use_cases: list[str] = Field(
        default_factory=list,
        description="Example scenarios",
        examples=[["Chat with memory", "Q&A over documents"]]
    )
    version: str = Field(..., description="Node version")
    deprecated: bool = Field(default=False, description="Deprecation status")
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


class NodeSummary(BaseModel):
    """
    Compact node representation for search results.

    Used in search responses to minimize token usage.
    """

    node_name: str = Field(..., description="Node identifier")
    label: str = Field(..., description="Display label")
    category: str = Field(..., description="Category")
    summary: str = Field(
        ...,
        max_length=150,
        description="Brief description (max 150 chars)"
    )
