"""Domain models for Fluent Mind MCP.

WHY: Provides type-safe Pydantic models for all data structures with automatic validation,
     ensuring data integrity throughout the system.

This package contains:
- Configuration models: FlowiseConfig for API connection settings
- Domain models: Chatflow, FlowData, Node, Edge for workflow representation
- Request/Response models: API interaction structures with validation

Exports:
- FlowiseConfig: Configuration for Flowise API connection
- Chatflow: Main chatflow domain model
- ChatflowType: Enum for chatflow types (CHATFLOW, AGENTFLOW, MULTIAGENT, ASSISTANT)
- FlowData: Workflow graph structure (nodes and edges)
- Node: Individual workflow component
- Edge: Connection between nodes
- PredictionResponse: Chatflow execution result
- ErrorResponse: Standardized error structure
- CreateChatflowRequest: Request model for creating chatflows
- UpdateChatflowRequest: Request model for updating chatflows

All models include comprehensive validation rules and clear error messages.
"""

from fluent_mind_mcp.models.chatflow import Chatflow, ChatflowType, Edge, FlowData, Node
from fluent_mind_mcp.models.config import FlowiseConfig
from fluent_mind_mcp.models.responses import (
    CreateChatflowRequest,
    ErrorResponse,
    PredictionResponse,
    UpdateChatflowRequest,
)

__all__ = [
    "FlowiseConfig",
    "Chatflow",
    "ChatflowType",
    "FlowData",
    "Node",
    "Edge",
    "PredictionResponse",
    "ErrorResponse",
    "CreateChatflowRequest",
    "UpdateChatflowRequest",
]
