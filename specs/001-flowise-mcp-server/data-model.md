# Data Model: Fluent Mind MCP Server

**Feature**: Fluent Mind MCP Server
**Branch**: `001-flowise-mcp-server`
**Date**: 2025-10-16
**Phase**: Phase 1 - Design & Contracts

---

## Overview

This document defines the domain model for the Fluent Mind MCP Server. All entities are defined as Pydantic models for type safety and validation. The models represent Flowise concepts and MCP server configuration.

---

## Entity Relationship Diagram

```
┌─────────────────────┐
│  FlowiseConfig      │
│  (Configuration)    │
└─────────────────────┘
          │
          │ uses
          ▼
┌─────────────────────┐       ┌──────────────────────┐
│  FlowiseClient      │──────>│  Chatflow            │
│  (HTTP Client)      │ manages│  (Domain Model)      │
└─────────────────────┘       └──────────────────────┘
          │                            │
          │                            │ contains
          │                            ▼
          │                   ┌──────────────────────┐
          │                   │  FlowData            │
          │                   │  (Workflow Structure)│
          │                   └──────────────────────┘
          │                            │
          │                            │ composed of
          │                            ▼
          │                   ┌──────────────────────┐
          │                   │  Node                │
          │                   │  (Workflow Component)│
          │                   └──────────────────────┘
          │                            │
          │                            │ connected by
          │                            ▼
          │                   ┌──────────────────────┐
          │                   │  Edge                │
          │                   │  (Connection)        │
          │                   └──────────────────────┘
          │
          │ produces
          ▼
┌─────────────────────┐
│  PredictionResponse │
│  (Execution Result) │
└─────────────────────┘
```

---

## Core Entities

### 1. FlowiseConfig

**Purpose**: Configuration for Flowise API connection

**Source**: Environment variables

**Fields**:

| Field | Type | Required | Default | Description | Validation |
|-------|------|----------|---------|-------------|------------|
| `api_url` | `str` | Yes | - | Flowise instance URL | Valid URL format, HTTP/HTTPS |
| `api_key` | `Optional[str]` | No | None | API key for secured instances | Min length 8 chars if provided |
| `timeout` | `int` | No | 60 | Request timeout in seconds | 1-600 seconds |
| `max_connections` | `int` | No | 10 | Connection pool size | 1-50 connections |
| `log_level` | `str` | No | "INFO" | Logging level | DEBUG, INFO, WARNING, ERROR |
| `flowise_version` | `str` | No | "v1.x" | Target Flowise version | Informational only |

**Example**:
```python
config = FlowiseConfig(
    api_url="http://localhost:3000",
    api_key="my-secret-key",
    timeout=60,
    max_connections=10,
    log_level="INFO"
)
```

**Validation Rules**:
- `api_url` must be valid HTTP/HTTPS URL
- `timeout` must be positive integer ≤600
- `max_connections` must be positive integer ≤50
- `log_level` must be valid logging level

**State**: Immutable after creation (load once at startup)

---

### 2. Chatflow

**Purpose**: Represents a Flowise workflow

**Source**: Flowise API responses

**Fields** (camelCase to match Flowise API):

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | `str` | Yes | Unique chatflow identifier | Non-empty string (UUID format) |
| `name` | `str` | Yes | Human-readable chatflow name | Min length 1, Max length 255 |
| `type` | `ChatflowType` | Yes | Chatflow type enum | Must be valid ChatflowType |
| `deployed` | `bool` | Yes | Deployment status | Boolean |
| `isPublic` | `Optional[bool]` | No | Public access flag | Boolean |
| `flowData` | `Optional[str]` | No | JSON string of workflow structure | Valid JSON if provided |
| `chatbotConfig` | `Optional[str]` | No | JSON string of chatbot settings | Valid JSON if provided |
| `apiConfig` | `Optional[str]` | No | JSON string of API settings | Valid JSON if provided |
| `apikeyid` | `Optional[str]` | No | API key identifier | String |
| `analytic` | `Optional[str]` | No | Analytics configuration | Valid JSON if provided |
| `speechToText` | `Optional[str]` | No | Speech-to-text configuration | Valid JSON if provided |
| `textToSpeech` | `Optional[str]` | No | Text-to-speech configuration | Valid JSON if provided |
| `followUpPrompts` | `Optional[str]` | No | Follow-up prompts configuration | Valid JSON if provided |
| `category` | `Optional[str]` | No | Chatflow category | String |
| `workspaceId` | `Optional[str]` | No | Workspace identifier | UUID format |
| `createdDate` | `Optional[datetime]` | No | Creation timestamp | ISO 8601 format |
| `updatedDate` | `Optional[datetime]` | No | Last update timestamp | ISO 8601 format |

**Example**:
```python
chatflow = Chatflow(
    id="abc-123-def",
    name="My RAG Assistant",
    type=ChatflowType.CHATFLOW,
    deployed=True,
    flowData='{"nodes": [...], "edges": [...]}',
    workspaceId="workspace-uuid"
)
```

**Relationships**:
- Contains one `FlowData` (when `flowData` field is parsed)
- Managed by one `FlowiseClient`
- Belongs to one workspace (via `workspaceId`)

**State Transitions**:
```
Created (deployed=False) → Deployed (deployed=True) → Undeployed (deployed=False)
                          ↓
                       Deleted (removed from system)
```

**Validation Rules**:
- `id` must be non-empty UUID format
- `name` must be 1-255 characters
- `type` must be valid enum value
- `flowData` must be valid JSON if provided
- `workspaceId` must be valid UUID format if provided
- Size limit: Total serialized size <1MB (validated at service layer)

**Field Naming Note**:
- All fields use camelCase to match Flowise API responses
- Pydantic models should use `Field(alias=...)` for snake_case compatibility if needed

---

### 3. ChatflowType

**Purpose**: Enum for chatflow types

**Values**:

| Value | Description |
|-------|-------------|
| `CHATFLOW` | Standard chatflow |
| `AGENTFLOW` | Agent-based flow |
| `MULTIAGENT` | Multi-agent system |
| `ASSISTANT` | Assistant configuration |

**Source**: Flowise API specification

**Example**:
```python
from enum import Enum

class ChatflowType(str, Enum):
    CHATFLOW = "CHATFLOW"
    AGENTFLOW = "AGENTFLOW"
    MULTIAGENT = "MULTIAGENT"
    ASSISTANT = "ASSISTANT"
```

---

### 4. FlowData

**Purpose**: Workflow graph structure (nodes and edges)

**Source**: Parsed from `Chatflow.flowData` JSON string

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `nodes` | `List[Node]` | Yes | Workflow components | Min 0 nodes |
| `edges` | `List[Edge]` | Yes | Connections between nodes | Min 0 edges |
| `viewport` | `Optional[Dict[str, Any]]` | No | UI viewport state (x, y, zoom) | Valid dict with x, y, zoom keys |

**Example**:
```python
flow_data = FlowData(
    nodes=[
        Node(id="node-1", type="llm", data={"model": "gpt-4"}),
        Node(id="node-2", type="vectorStore", data={"provider": "pinecone"})
    ],
    edges=[
        Edge(id="edge-1", source="node-1", target="node-2")
    ],
    viewport={"x": 0, "y": 0, "zoom": 1}
)
```

**Relationships**:
- Contained by one `Chatflow`
- Composed of many `Node` objects
- Composed of many `Edge` objects

**Validation Rules**:
- `nodes` must be list (can be empty for new chatflows)
- `edges` must be list (can be empty)
- Edge `source` and `target` must reference existing node IDs
- No circular dependencies (optional validation)

---

### 5. Node

**Purpose**: Workflow component (LLM, vector store, tool, etc.)

**Source**: Part of FlowData structure

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | `str` | Yes | Unique node identifier | Non-empty string |
| `type` | `str` | Yes | Node type (llm, vectorStore, tool, etc.) | Non-empty string |
| `data` | `Dict[str, Any]` | Yes | Node configuration | Valid dict |
| `position` | `Optional[Dict[str, float]]` | No | UI position (x, y) | {x: float, y: float} |
| `width` | `Optional[int]` | No | UI node width in pixels | Positive integer |
| `height` | `Optional[int]` | No | UI node height in pixels | Positive integer |
| `selected` | `Optional[bool]` | No | UI selection state | Boolean |
| `positionAbsolute` | `Optional[Dict[str, float]]` | No | Absolute UI position | {x: float, y: float} |
| `dragging` | `Optional[bool]` | No | UI dragging state | Boolean |

**Example**:
```python
node = Node(
    id="node-1",
    type="chatOpenAI",
    data={
        "model": "gpt-4",
        "temperature": 0.7,
        "maxTokens": 1000
    },
    position={"x": 100, "y": 200}
)
```

**Validation Rules**:
- `id` must be unique within FlowData
- `type` must be non-empty
- `data` must be valid dict (contents not validated by MCP server)
- `position` if provided must have x and y floats

---

### 6. Edge

**Purpose**: Connection between workflow nodes

**Source**: Part of FlowData structure

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `id` | `str` | Yes | Unique edge identifier | Non-empty string |
| `source` | `str` | Yes | Source node ID | Must match existing Node.id |
| `target` | `str` | Yes | Target node ID | Must match existing Node.id |
| `source_handle` | `Optional[str]` | No | Source output handle | - |
| `target_handle` | `Optional[str]` | No | Target input handle | - |

**Example**:
```python
edge = Edge(
    id="edge-1",
    source="node-1",
    target="node-2",
    source_handle="output",
    target_handle="input"
)
```

**Validation Rules**:
- `id` must be unique within FlowData
- `source` and `target` must reference existing nodes
- `source` and `target` must be different (no self-loops)

---

### 7. PredictionResponse

**Purpose**: Result from chatflow execution

**Source**: Flowise API response from `/api/v1/prediction/{id}`

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `text` | `str` | Yes | Response text from chatflow | Non-empty string |
| `question_message_id` | `Optional[str]` | No | Question message identifier | - |
| `chat_message_id` | `Optional[str]` | No | Response message identifier | - |
| `session_id` | `Optional[str]` | No | Conversation session identifier | - |

**Example**:
```python
response = PredictionResponse(
    text="The capital of France is Paris.",
    question_message_id="msg-123",
    chat_message_id="msg-456",
    session_id="session-789"
)
```

**Validation Rules**:
- `text` must be non-empty string

---

### 8. CreateChatflowRequest

**Purpose**: Request model for creating chatflow

**Source**: MCP tool parameters

**Fields**:

| Field | Type | Required | Default | Description | Validation |
|-------|------|----------|---------|-------------|------------|
| `name` | `str` | Yes | - | Chatflow name | 1-255 characters |
| `type` | `ChatflowType` | No | CHATFLOW | Chatflow type | Valid enum |
| `flow_data` | `str` | Yes | - | JSON string of workflow | Valid JSON, <1MB |
| `deployed` | `bool` | No | False | Initial deployment status | Boolean |

**Example**:
```python
request = CreateChatflowRequest(
    name="My Flow",
    type=ChatflowType.CHATFLOW,
    flow_data='{"nodes": [], "edges": []}',
    deployed=False
)
```

**Validation Rules**:
- `name` length 1-255 characters
- `flow_data` must be valid JSON
- `flow_data` size <1MB (1,048,576 bytes)
- Must contain `nodes` and `edges` keys

---

### 9. UpdateChatflowRequest

**Purpose**: Request model for updating chatflow

**Source**: MCP tool parameters

**Fields**:

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `chatflow_id` | `str` | Yes | Chatflow to update | Non-empty string |
| `name` | `Optional[str]` | No | New name | 1-255 characters if provided |
| `flow_data` | `Optional[str]` | No | New workflow structure | Valid JSON, <1MB if provided |
| `deployed` | `Optional[bool]` | No | New deployment status | Boolean if provided |

**Example**:
```python
request = UpdateChatflowRequest(
    chatflow_id="abc-123",
    name="Updated Name",
    deployed=True
)
```

**Validation Rules**:
- `chatflow_id` must be non-empty
- At least one optional field must be provided
- If `name` provided, length 1-255
- If `flow_data` provided, valid JSON and <1MB

---

## Supporting Models

### 10. ErrorResponse

**Purpose**: Standardized error response format

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error` | `str` | Yes | Error type/code |
| `message` | `str` | Yes | User-friendly error message |
| `details` | `Optional[Dict[str, Any]]` | No | Additional error context |

**Example**:
```python
error = ErrorResponse(
    error="ValidationError",
    message="Chatflow name must be between 1 and 255 characters",
    details={"field": "name", "value": "", "constraint": "min_length"}
)
```

---

## Validation Summary

### Field-Level Validations

| Entity | Field | Validation |
|--------|-------|------------|
| FlowiseConfig | api_url | Valid URL, HTTP/HTTPS |
| FlowiseConfig | timeout | 1-600 seconds |
| FlowiseConfig | max_connections | 1-50 |
| Chatflow | name | 1-255 characters |
| Chatflow | flowData | Valid JSON if provided |
| Chatflow | workspaceId | Valid UUID format if provided |
| FlowData | nodes | List of Node objects |
| FlowData | edges | List of Edge objects, valid references |
| FlowData | viewport | Valid dict with x, y, zoom keys |
| Node | id | Non-empty, unique within FlowData |
| Node | width, height | Positive integers if provided |
| Edge | source, target | Must reference existing nodes |
| CreateChatflowRequest | flowData | Valid JSON, <1MB |
| UpdateChatflowRequest | At least one optional field | - |

### Business Rule Validations (Service Layer)

| Rule | Where Enforced |
|------|----------------|
| Chatflow ID must exist for get/update/delete operations | ChatflowService |
| Flow data size limit (1MB) | ChatflowService.validate_flow_data() |
| No duplicate chatflow names | Optional, not enforced |
| Edge source/target must reference existing nodes | FlowData.validate() |
| At least one update field provided | UpdateChatflowRequest.validate() |

---

## Model Relationships

```
FlowiseConfig
    ↓ used by
FlowiseClient
    ↓ manages
Chatflow
    ├── contains FlowData
    │     ├── contains List[Node]
    │     └── contains List[Edge]
    └── executed to produce PredictionResponse
```

---

## Data Flow

### Create Chatflow
```
CreateChatflowRequest → Validation → FlowiseClient.create()
    → Flowise API → Chatflow (returned)
```

### Update Chatflow
```
UpdateChatflowRequest → Validation → Get existing Chatflow
    → Merge changes → FlowiseClient.update()
    → Flowise API → Chatflow (updated)
```

### Execute Chatflow
```
chatflow_id + question → FlowiseClient.run_prediction()
    → Flowise API → PredictionResponse
```

---

## Persistence

**Source of Truth**: Flowise PostgreSQL database (external)

**MCP Server**:
- No local persistence
- All data fetched from Flowise API on demand
- No caching (fresh data every request)

**Lifecycle**:
1. Create: POST to Flowise API
2. Read: GET from Flowise API
3. Update: PUT to Flowise API
4. Delete: DELETE from Flowise API

---

## Model File Organization

```
src/fluent_mind_mcp/models/
├── __init__.py              # Re-export all models
├── chatflow.py              # Chatflow, ChatflowType, FlowData, Node, Edge
├── config.py                # FlowiseConfig
└── responses.py             # PredictionResponse, ErrorResponse, CreateChatflowRequest, UpdateChatflowRequest
```

---

## References

- **Feature Spec**: [spec.md](spec.md) - Key Entities section
- **Clean Code Plan**: [plan_cc.md](plan_cc.md) - Domain Models section
- **Flowise API**: [FLOWISE_API.md](../../../FLOWISE_API.md) - API response formats
- **Pydantic Docs**: https://docs.pydantic.dev/ - Validation patterns

---

**Data Model Complete**: ✅

All entities defined with validation rules. Ready to generate API contracts.
