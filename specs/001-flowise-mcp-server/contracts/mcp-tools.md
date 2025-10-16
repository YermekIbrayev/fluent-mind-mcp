# MCP Tools Contract: Fluent Mind MCP Server

**Feature**: Fluent Mind MCP Server
**Branch**: `001-flowise-mcp-server`
**Date**: 2025-10-16
**Protocol**: Model Context Protocol (MCP)

---

## Overview

This document defines the 8 MCP tools exposed by the Fluent Mind MCP Server. Each tool follows the MCP protocol specification with JSON Schema for parameters and responses.

---

## Tool 1: list_chatflows

**Purpose**: List all chatflows from Flowise instance

**Parameters**: None

**Returns**: Array of chatflow objects

**Schema**:
```json
{
  "name": "list_chatflows",
  "description": "List all available Flowise chatflows with their metadata",
  "inputSchema": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "outputSchema": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "Unique chatflow identifier"
        },
        "name": {
          "type": "string",
          "description": "Chatflow name"
        },
        "type": {
          "type": "string",
          "enum": ["CHATFLOW", "AGENTFLOW", "MULTIAGENT", "ASSISTANT"],
          "description": "Chatflow type"
        },
        "deployed": {
          "type": "boolean",
          "description": "Whether chatflow is deployed"
        },
        "createdDate": {
          "type": "string",
          "format": "date-time",
          "description": "Creation timestamp"
        }
      },
      "required": ["id", "name", "type", "deployed"]
    }
  }
}
```

**Example Call**:
```json
{
  "tool": "list_chatflows",
  "params": {}
}
```

**Example Response**:
```json
[
  {
    "id": "abc-123-def",
    "name": "RAG Assistant",
    "type": "CHATFLOW",
    "deployed": true,
    "createdDate": "2025-10-16T12:00:00Z"
  },
  {
    "id": "xyz-456-uvw",
    "name": "Research Agent",
    "type": "AGENTFLOW",
    "deployed": false,
    "createdDate": "2025-10-15T10:30:00Z"
  }
]
```

**Error Responses**:
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key
- `UnexpectedError`: Other failures

**Performance Target**: ≤5 seconds (SC-002)

---

## Tool 2: get_chatflow

**Purpose**: Get detailed chatflow by ID including flowData

**Parameters**:
- `chatflow_id` (string, required): Chatflow identifier

**Returns**: Chatflow object with complete details

**Schema**:
```json
{
  "name": "get_chatflow",
  "description": "Get detailed chatflow information including workflow structure",
  "inputSchema": {
    "type": "object",
    "properties": {
      "chatflow_id": {
        "type": "string",
        "description": "Unique chatflow identifier",
        "minLength": 1
      }
    },
    "required": ["chatflow_id"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "name": {"type": "string"},
      "type": {
        "type": "string",
        "enum": ["CHATFLOW", "AGENTFLOW", "MULTIAGENT", "ASSISTANT"]
      },
      "deployed": {"type": "boolean"},
      "flowData": {
        "type": "string",
        "description": "JSON string containing nodes and edges"
      },
      "createdDate": {"type": "string", "format": "date-time"},
      "updatedDate": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "type", "deployed"]
  }
}
```

**Example Call**:
```json
{
  "tool": "get_chatflow",
  "params": {
    "chatflow_id": "abc-123-def"
  }
}
```

**Example Response**:
```json
{
  "id": "abc-123-def",
  "name": "RAG Assistant",
  "type": "CHATFLOW",
  "deployed": true,
  "flowData": "{\"nodes\":[...],\"edges\":[...]}",
  "createdDate": "2025-10-16T12:00:00Z",
  "updatedDate": "2025-10-16T14:30:00Z"
}
```

**Error Responses**:
- `NotFoundError`: Chatflow ID doesn't exist
- `ValidationError`: Invalid chatflow ID format
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤5 seconds (SC-002)

---

## Tool 3: create_chatflow

**Purpose**: Create new chatflow from workflow structure

**Parameters**:
- `name` (string, required): Chatflow name (1-255 chars)
- `flow_data` (string, required): JSON string with nodes and edges (<1MB)
- `type` (string, optional): Chatflow type (default: "CHATFLOW")
- `deployed` (boolean, optional): Initial deployment status (default: false)

**Returns**: Created chatflow object with generated ID

**Schema**:
```json
{
  "name": "create_chatflow",
  "description": "Create a new Flowise chatflow from workflow structure",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "Chatflow name",
        "minLength": 1,
        "maxLength": 255
      },
      "flow_data": {
        "type": "string",
        "description": "JSON string containing workflow structure (nodes and edges)",
        "minLength": 1
      },
      "type": {
        "type": "string",
        "enum": ["CHATFLOW", "AGENTFLOW", "MULTIAGENT", "ASSISTANT"],
        "description": "Chatflow type",
        "default": "CHATFLOW"
      },
      "deployed": {
        "type": "boolean",
        "description": "Whether to deploy immediately",
        "default": false
      }
    },
    "required": ["name", "flow_data"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "name": {"type": "string"},
      "type": {"type": "string"},
      "deployed": {"type": "boolean"},
      "createdDate": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "type", "deployed"]
  }
}
```

**Example Call**:
```json
{
  "tool": "create_chatflow",
  "params": {
    "name": "My New Flow",
    "flow_data": "{\"nodes\":[{\"id\":\"node-1\",\"type\":\"llm\",\"data\":{}}],\"edges\":[]}",
    "type": "CHATFLOW",
    "deployed": false
  }
}
```

**Example Response**:
```json
{
  "id": "new-abc-123",
  "name": "My New Flow",
  "type": "CHATFLOW",
  "deployed": false,
  "createdDate": "2025-10-16T15:00:00Z"
}
```

**Error Responses**:
- `ValidationError`: Invalid flow_data JSON or exceeds 1MB
- `ValidationError`: Name too long or empty
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤10 seconds (SC-003)

---

## Tool 4: update_chatflow

**Purpose**: Update existing chatflow (partial updates supported)

**Parameters**:
- `chatflow_id` (string, required): Chatflow identifier
- `name` (string, optional): New name (1-255 chars)
- `flow_data` (string, optional): New workflow structure (<1MB)
- `deployed` (boolean, optional): New deployment status

**Returns**: Updated chatflow object

**Schema**:
```json
{
  "name": "update_chatflow",
  "description": "Update existing chatflow properties (partial updates supported)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "chatflow_id": {
        "type": "string",
        "description": "Chatflow to update",
        "minLength": 1
      },
      "name": {
        "type": "string",
        "description": "New chatflow name",
        "minLength": 1,
        "maxLength": 255
      },
      "flow_data": {
        "type": "string",
        "description": "New workflow structure"
      },
      "deployed": {
        "type": "boolean",
        "description": "New deployment status"
      }
    },
    "required": ["chatflow_id"],
    "anyOf": [
      {"required": ["name"]},
      {"required": ["flow_data"]},
      {"required": ["deployed"]}
    ]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "name": {"type": "string"},
      "type": {"type": "string"},
      "deployed": {"type": "boolean"},
      "updatedDate": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "type", "deployed"]
  }
}
```

**Example Call**:
```json
{
  "tool": "update_chatflow",
  "params": {
    "chatflow_id": "abc-123-def",
    "name": "Updated Name",
    "deployed": true
  }
}
```

**Example Response**:
```json
{
  "id": "abc-123-def",
  "name": "Updated Name",
  "type": "CHATFLOW",
  "deployed": true,
  "updatedDate": "2025-10-16T16:00:00Z"
}
```

**Error Responses**:
- `NotFoundError`: Chatflow doesn't exist
- `ValidationError`: No update fields provided or invalid values
- `ValidationError`: flow_data malformed or exceeds 1MB
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤10 seconds

---

## Tool 5: delete_chatflow

**Purpose**: Permanently delete chatflow

**Parameters**:
- `chatflow_id` (string, required): Chatflow identifier

**Returns**: Success confirmation message

**Schema**:
```json
{
  "name": "delete_chatflow",
  "description": "Permanently delete a chatflow from Flowise",
  "inputSchema": {
    "type": "object",
    "properties": {
      "chatflow_id": {
        "type": "string",
        "description": "Chatflow to delete",
        "minLength": 1
      }
    },
    "required": ["chatflow_id"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "Confirmation message"
      },
      "deleted_id": {
        "type": "string",
        "description": "ID of deleted chatflow"
      }
    },
    "required": ["message", "deleted_id"]
  }
}
```

**Example Call**:
```json
{
  "tool": "delete_chatflow",
  "params": {
    "chatflow_id": "abc-123-def"
  }
}
```

**Example Response**:
```json
{
  "message": "Chatflow deleted successfully",
  "deleted_id": "abc-123-def"
}
```

**Error Responses**:
- `NotFoundError`: Chatflow doesn't exist (gracefully handled)
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤5 seconds

---

## Tool 6: run_prediction

**Purpose**: Execute chatflow with user input

**Parameters**:
- `chatflow_id` (string, required): Chatflow identifier
- `question` (string, required): User input/question

**Returns**: Chatflow execution result

**Schema**:
```json
{
  "name": "run_prediction",
  "description": "Execute a deployed chatflow with user input",
  "inputSchema": {
    "type": "object",
    "properties": {
      "chatflow_id": {
        "type": "string",
        "description": "Chatflow to execute",
        "minLength": 1
      },
      "question": {
        "type": "string",
        "description": "User input or question",
        "minLength": 1
      }
    },
    "required": ["chatflow_id", "question"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "text": {
        "type": "string",
        "description": "Response from chatflow"
      },
      "questionMessageId": {
        "type": "string",
        "description": "Question message ID"
      },
      "chatMessageId": {
        "type": "string",
        "description": "Response message ID"
      },
      "sessionId": {
        "type": "string",
        "description": "Conversation session ID"
      }
    },
    "required": ["text"]
  }
}
```

**Example Call**:
```json
{
  "tool": "run_prediction",
  "params": {
    "chatflow_id": "abc-123-def",
    "question": "What is the capital of France?"
  }
}
```

**Example Response**:
```json
{
  "text": "The capital of France is Paris.",
  "questionMessageId": "msg-123",
  "chatMessageId": "msg-456",
  "sessionId": "session-789"
}
```

**Error Responses**:
- `NotFoundError`: Chatflow doesn't exist
- `ValidationError`: Chatflow not deployed
- `TimeoutError`: Execution exceeded timeout
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤5 seconds (SC-002)

---

## Tool 7: deploy_chatflow

**Purpose**: Toggle chatflow deployment status

**Parameters**:
- `chatflow_id` (string, required): Chatflow identifier
- `deployed` (boolean, required): Desired deployment state

**Returns**: Updated chatflow object

**Schema**:
```json
{
  "name": "deploy_chatflow",
  "description": "Toggle chatflow deployment status (convenience wrapper for update)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "chatflow_id": {
        "type": "string",
        "description": "Chatflow to deploy/undeploy",
        "minLength": 1
      },
      "deployed": {
        "type": "boolean",
        "description": "true to deploy, false to undeploy"
      }
    },
    "required": ["chatflow_id", "deployed"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "name": {"type": "string"},
      "deployed": {"type": "boolean"},
      "updatedDate": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "name", "deployed"]
  }
}
```

**Example Call**:
```json
{
  "tool": "deploy_chatflow",
  "params": {
    "chatflow_id": "abc-123-def",
    "deployed": true
  }
}
```

**Example Response**:
```json
{
  "id": "abc-123-def",
  "name": "RAG Assistant",
  "deployed": true,
  "updatedDate": "2025-10-16T17:00:00Z"
}
```

**Error Responses**:
- `NotFoundError`: Chatflow doesn't exist
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤10 seconds

---

## Tool 8: generate_agentflow_v2

**Purpose**: Generate AgentFlow V2 structure from natural language description

**Parameters**:
- `description` (string, required): Natural language description of desired agent

**Returns**: Generated workflow structure with metadata

**Schema**:
```json
{
  "name": "generate_agentflow_v2",
  "description": "Generate AgentFlow V2 workflow from natural language description",
  "inputSchema": {
    "type": "object",
    "properties": {
      "description": {
        "type": "string",
        "description": "Natural language description of desired agent behavior",
        "minLength": 10
      }
    },
    "required": ["description"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "flowData": {
        "type": "string",
        "description": "Generated workflow structure as JSON string"
      },
      "name": {
        "type": "string",
        "description": "Suggested chatflow name"
      },
      "description": {
        "type": "string",
        "description": "Generated description"
      }
    },
    "required": ["flowData", "name"]
  }
}
```

**Example Call**:
```json
{
  "tool": "generate_agentflow_v2",
  "params": {
    "description": "Create a research agent that searches the web and summarizes findings"
  }
}
```

**Example Response**:
```json
{
  "flowData": "{\"nodes\":[{\"id\":\"search-1\",\"type\":\"webSearch\",...}],\"edges\":[...]}",
  "name": "Research Agent",
  "description": "Agent that searches web and summarizes findings"
}
```

**Error Responses**:
- `ValidationError`: Description too short or unclear
- `ConnectionError`: Flowise API unreachable
- `AuthenticationError`: Invalid API key

**Performance Target**: ≤10 seconds

**Note**: Generated flowData can be used directly with `create_chatflow` tool

---

## Error Response Format

All tools return errors in consistent format:

```json
{
  "error": {
    "type": "ValidationError",
    "message": "Chatflow name must be between 1 and 255 characters",
    "details": {
      "field": "name",
      "value": "",
      "constraint": "minLength"
    }
  }
}
```

**Error Types**:
- `ConnectionError`: Network/timeout issues
- `AuthenticationError`: Invalid API key
- `ValidationError`: Invalid input parameters
- `NotFoundError`: Resource doesn't exist
- `RateLimitError`: Too many requests
- `TimeoutError`: Operation exceeded timeout
- `UnexpectedError`: Other failures

---

## Performance Targets Summary

| Tool | Target | Source |
|------|--------|--------|
| list_chatflows | ≤5s | SC-002 |
| get_chatflow | ≤5s | SC-002 |
| create_chatflow | ≤10s | SC-003 |
| update_chatflow | ≤10s | Derived |
| delete_chatflow | ≤5s | Derived |
| run_prediction | ≤5s | SC-002 |
| deploy_chatflow | ≤10s | Derived |
| generate_agentflow_v2 | ≤10s | Derived |
| **Full lifecycle** | ≤60s | SC-006 |

---

## Concurrency Requirements

- Support 5-10 concurrent tool calls (NFR-005 to NFR-007)
- No operation should block others
- All operations use async/await pattern
- Connection pooling handles concurrency

---

## Authentication

All tools require valid Flowise API credentials:
- Configured via `FLOWISE_API_URL` environment variable
- Optional `FLOWISE_API_KEY` for secured instances
- Authentication handled transparently by FlowiseClient
- No per-tool authentication

---

## References

- **Feature Spec**: [spec.md](../spec.md) - Functional requirements
- **Data Model**: [data-model.md](../data-model.md) - Entity definitions
- **Clean Code Plan**: [plan_cc.md](../plan_cc.md) - Implementation details
- **MCP Protocol**: https://modelcontextprotocol.io/ - MCP specification

---

**MCP Tools Contract Complete**: ✅

All 8 tools defined with JSON schemas. Ready for implementation.
