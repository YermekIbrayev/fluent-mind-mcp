"""Chatflow domain models for Flowise workflow management.

This module defines the core domain models for representing Flowise chatflows,
their workflow structure (nodes and edges), and chatflow types.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChatflowType(str, Enum):
    """Enum for chatflow types.

    Represents different types of workflows supported by Flowise.
    """

    CHATFLOW = "CHATFLOW"
    AGENTFLOW = "AGENTFLOW"
    MULTIAGENT = "MULTIAGENT"
    ASSISTANT = "ASSISTANT"


class Node(BaseModel):
    """Workflow component (LLM, vector store, tool, etc.).

    Represents a single node in a Flowise workflow graph.

    Attributes:
        id: Unique node identifier within the workflow
        type: Node type (e.g., "chatOpenAI", "vectorStore", "tool")
        data: Node configuration as key-value pairs
        position: Optional UI position with x and y coordinates
    """

    id: str = Field(..., min_length=1, description="Unique node identifier")
    type: str = Field(..., min_length=1, description="Node type")
    data: Dict[str, Any] = Field(..., description="Node configuration")
    position: Optional[Dict[str, float]] = Field(
        None, description="UI position {x: float, y: float}"
    )

    @field_validator("position")
    @classmethod
    def validate_position(cls, v: Optional[Dict[str, float]]) -> Optional[Dict[str, float]]:
        """Validate position has x and y coordinates.

        WHY: Ensures position dict structure is correct if provided.
        """
        if v is not None:
            if not isinstance(v, dict):
                raise ValueError("position must be a dictionary")
            if "x" not in v or "y" not in v:
                raise ValueError("position must contain 'x' and 'y' keys")
            if not isinstance(v["x"], (int, float)) or not isinstance(v["y"], (int, float)):
                raise ValueError("position x and y must be numeric")
        return v


class Edge(BaseModel):
    """Connection between workflow nodes.

    Represents a directed edge connecting two nodes in a workflow graph.

    Attributes:
        id: Unique edge identifier within the workflow
        source: Source node ID
        target: Target node ID
        source_handle: Optional source output handle name
        target_handle: Optional target input handle name
    """

    id: str = Field(..., min_length=1, description="Unique edge identifier")
    source: str = Field(..., min_length=1, description="Source node ID")
    target: str = Field(..., min_length=1, description="Target node ID")
    source_handle: Optional[str] = Field(None, description="Source output handle")
    target_handle: Optional[str] = Field(None, description="Target input handle")

    @field_validator("target")
    @classmethod
    def validate_no_self_loops(cls, v: str, info) -> str:
        """Prevent self-referencing edges.

        WHY: Self-loops are not meaningful in Flowise workflows.
        """
        if "source" in info.data and v == info.data["source"]:
            raise ValueError("Edge cannot connect a node to itself (no self-loops)")
        return v


class FlowData(BaseModel):
    """Workflow graph structure (nodes and edges).

    Represents the complete workflow graph for a chatflow,
    including all nodes and their connections.

    Attributes:
        nodes: List of workflow components
        edges: List of connections between nodes
    """

    nodes: List[Node] = Field(..., description="Workflow components")
    edges: List[Edge] = Field(..., description="Connections between nodes")

    @field_validator("edges")
    @classmethod
    def validate_edge_references(cls, v: List[Edge], info) -> List[Edge]:
        """Validate that edges reference existing nodes.

        WHY: Ensures graph integrity - edges must connect real nodes.
        """
        if "nodes" in info.data:
            node_ids = {node.id for node in info.data["nodes"]}
            for edge in v:
                if edge.source not in node_ids:
                    raise ValueError(f"Edge {edge.id} references non-existent source node: {edge.source}")
                if edge.target not in node_ids:
                    raise ValueError(f"Edge {edge.id} references non-existent target node: {edge.target}")
        return v

    @field_validator("nodes")
    @classmethod
    def validate_unique_node_ids(cls, v: List[Node]) -> List[Node]:
        """Validate that node IDs are unique.

        WHY: Node IDs must be unique for proper graph traversal.
        """
        node_ids = [node.id for node in v]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("Node IDs must be unique within FlowData")
        return v


class Chatflow(BaseModel):
    """Flowise workflow representation.

    Represents a complete Flowise chatflow with metadata,
    configuration, and workflow structure.

    Attributes:
        id: Unique chatflow identifier (UUID format)
        name: Human-readable chatflow name
        type: Chatflow type enum (CHATFLOW, AGENTFLOW, etc.)
        deployed: Deployment status flag
        is_public: Optional public access flag
        flow_data: Optional JSON string of workflow structure
        chatbot_config: Optional JSON string of chatbot settings
        api_config: Optional JSON string of API settings
        created_date: Optional creation timestamp
        updated_date: Optional last update timestamp
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., min_length=1, description="Unique chatflow identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Chatflow name")
    type: ChatflowType = Field(..., description="Chatflow type")
    deployed: bool = Field(..., description="Deployment status")
    is_public: Optional[bool] = Field(None, alias="isPublic", description="Public access flag")
    flow_data: Optional[str] = Field(None, alias="flowData", description="JSON string of workflow structure")
    chatbot_config: Optional[str] = Field(None, alias="chatbotConfig", description="JSON string of chatbot settings")
    api_config: Optional[str] = Field(None, alias="apiConfig", description="JSON string of API settings")
    created_date: Optional[datetime] = Field(None, alias="createdDate", description="Creation timestamp")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate", description="Last update timestamp")
