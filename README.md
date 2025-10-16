# Fluent Mind MCP

> Fine! I'll go build my own theme park! With blackjack! And hookers!

A comprehensive Model Context Protocol (MCP) server for [Flowise](https://github.com/FlowiseAI/Flowise) - the open-source LLM orchestration platform. Provides complete control over Flowise chatflows via MCP tools.

## Why Fluent Mind MCP?

Existing Flowise MCP wrappers only support **querying** existing chatflows. Fluent Mind MCP gives you **full lifecycle management**:

- ✅ Create chatflows from scratch (0→1)
- ✅ Update and modify existing flows
- ✅ Delete chatflows
- ✅ Deploy/undeploy flows
- ✅ Execute predictions
- ✅ Generate AgentFlow V2 from descriptions

**Built from scratch with full control. No dependencies on other MCP implementations. MIT-free.**

## Features

### 8 Comprehensive MCP Tools

1. **list_chatflows** - List all chatflows with metadata
2. **get_chatflow** - Get detailed chatflow by ID
3. **create_chatflow** - Create new chatflow (CHATFLOW, AGENTFLOW, MULTIAGENT, ASSISTANT)
4. **update_chatflow** - Update existing chatflow
5. **delete_chatflow** - Remove chatflow
6. **run_prediction** - Execute chatflow with input
7. **deploy_chatflow** - Toggle deployment status
8. **generate_agentflow_v2** - Generate AgentFlow V2 from natural language

### Architecture

- **FastMCP** - Modern Python MCP framework
- **httpx** - Async HTTP client for Flowise API
- **Pydantic** - Type-safe data validation
- **Clean separation** - Client layer, MCP tools, models

## Installation

### Prerequisites

- Python 3.12+
- Flowise instance running (local or remote)

### Install

```bash
cd ~/work/ai/fluent-mind-mcp
pip install -e .
```

### Configuration

Create `.env` file:

```bash
FLOWISE_API_URL=http://localhost:3000
FLOWISE_API_KEY=optional_api_key_if_secured
```

## Usage

### Run the MCP Server

```bash
# Using FastMCP
python -m fluent_mind_mcp.server
```

### Use with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fluent-mind": {
      "command": "python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "http://localhost:3000",
        "FLOWISE_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Example: Create a Chatflow

```python
# Via MCP tool
create_chatflow(
    name="My RAG Assistant",
    type="CHATFLOW",
    flowData='{"nodes": [...], "edges": [...]}'
)
```

### Example: Generate AgentFlow V2

```python
# Natural language to AgentFlow
generate_agentflow_v2(
    description="Create a research agent that searches the web and summarizes findings"
)
```

## API Reference

### list_chatflows()

Returns array of all chatflows.

**Response:**
```json
[
  {
    "id": "abc123",
    "name": "My Chatflow",
    "type": "CHATFLOW",
    "deployed": true,
    "createdDate": "2025-10-16T..."
  }
]
```

### get_chatflow(chatflow_id: str)

Get detailed chatflow including flowData.

**Parameters:**
- `chatflow_id` (str): Chatflow UUID

**Response:**
```json
{
  "id": "abc123",
  "name": "My Chatflow",
  "flowData": "{\"nodes\": [...], \"edges\": [...]}",
  "type": "CHATFLOW",
  "deployed": true
}
```

### create_chatflow(name: str, type: str, flowData: str, deployed: bool = False)

Create new chatflow.

**Parameters:**
- `name` (str): Chatflow name
- `type` (str): CHATFLOW | AGENTFLOW | MULTIAGENT | ASSISTANT
- `flowData` (str): JSON string with nodes and edges
- `deployed` (bool): Initial deployment status

**Response:** Created chatflow object with id

### update_chatflow(chatflow_id: str, name: str = None, flowData: str = None, deployed: bool = None)

Update existing chatflow (partial updates supported).

**Parameters:**
- `chatflow_id` (str): Chatflow UUID
- `name` (str, optional): New name
- `flowData` (str, optional): New flow structure
- `deployed` (bool, optional): New deployment status

**Response:** Updated chatflow object

### delete_chatflow(chatflow_id: str)

Delete chatflow permanently.

**Parameters:**
- `chatflow_id` (str): Chatflow UUID

**Response:** Success confirmation

### run_prediction(chatflow_id: str, question: str)

Execute chatflow with input.

**Parameters:**
- `chatflow_id` (str): Chatflow UUID
- `question` (str): Input text

**Response:** Chatflow execution result

### deploy_chatflow(chatflow_id: str, deployed: bool)

Toggle deployment status.

**Parameters:**
- `chatflow_id` (str): Chatflow UUID
- `deployed` (bool): Deployment state

**Response:** Updated chatflow

### generate_agentflow_v2(description: str)

Generate AgentFlow V2 from natural language description.

**Parameters:**
- `description` (str): Natural language description of desired agent

**Response:** Generated AgentFlow V2 structure

## Development

### Project Structure

```
fluent-mind-mcp/
├── src/fluent_mind_mcp/
│   ├── __init__.py
│   ├── server.py                    # MCP server entry point, tool definitions
│   ├── services/
│   │   ├── __init__.py
│   │   └── chatflow_service.py      # Business logic orchestration
│   ├── client/
│   │   ├── __init__.py
│   │   ├── flowise_client.py        # HTTP client implementation
│   │   └── exceptions.py            # Custom exception hierarchy
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chatflow.py              # Chatflow, FlowData domain models
│   │   ├── config.py                # Configuration model
│   │   └── responses.py             # API response models
│   ├── logging/
│   │   ├── __init__.py
│   │   └── operation_logger.py      # Structured logging
│   └── utils/
│       ├── __init__.py
│       └── validators.py            # Input validation helpers
├── tests/
│   ├── unit/
│   ├── integration/
│   └── acceptance/
├── README.md
├── pyproject.toml
└── .env.example
```

### Run Tests

```bash
pytest tests/
```

## License

This project is **fully open source** and built from scratch. No MIT license requirements from forked code because there is no forked code. Do whatever you want with it.

## Why "Fluent Mind"?

Because interacting with Flowise should be fluid, intuitive, and intelligent. Plus it sounds cool.

## Credits

Built with frustration after discovering existing mcp-flowise tools couldn't actually create chatflows. Sometimes you just gotta build your own theme park.

---

**Status:** 🚧 In Development

**Estimated completion:** 2-4 hours from now
