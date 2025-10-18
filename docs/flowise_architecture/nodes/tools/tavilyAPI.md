# Tavily API

**Category**: Tools | **Type**: TavilyAPI | **Version**: 1.2

---

## Overview

Wrapper around TavilyAPI - A specialized search engine designed for LLMs and AI agents.
Provides real-time web search capabilities for AI applications.

---

## Credentials

**Required**: Yes

**API Field**: `data.credential`

**Credential Types**:
- `tavilyApi` - Tavily API key

---

## API Required Fields

| Field | API Path | Type | Description | Default |
|-------|----------|------|-------------|---------|
| Node ID | `id` | string | Unique identifier: `tavilyAPI_{index}` | - |
| Data ID | `data.id` | string | Must match outer `id` | - |
| Node Name | `data.name` | string | Must be: `tavilyAPI` | - |
| Node Type | `data.type` | string | Must be: `TavilyAPI` | - |
| Topic | `data.inputs.topic` | string | Search topic filter | - |

**Topic Options**: `general`, `news`

---

## API Optional Fields

| Field | API Path | Type | Description | Default |
|-------|----------|------|-------------|---------|
| Search Depth | `data.inputs.searchDepth` | string | Search thoroughness | `basic` |
| Max Results | `data.inputs.maxResults` | number | Maximum search results | 5 |

**Search Depth Options**: `basic`, `advanced`

---

## Connections

**No Input Connections Required**

**Outputs**: `TavilyAPI`, `Tool`, `StructuredTool`

---

## API Template

See: [templates/tavily-api.json](../templates/tavily-api.json)

```json
{
  "id": "tavilyAPI_0",
  "data": {
    "name": "tavilyAPI",
    "credential": "tavilyApi_cred_id",
    "inputs": {
      "topic": "general",
      "searchDepth": "basic",
      "maxResults": 5
    }
  }
}
```

---

## Common Use Cases

1. **Web search agent**: Provide real-time web search to AI agents
2. **News monitoring**: Use `topic: "news"` for current events
3. **Research assistant**: Use `searchDepth: "advanced"` for thorough research

---

**Source**: `packages/components/nodes/tools/TavilyAPI/TavilyAPI.ts`