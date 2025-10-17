# Fluent Mind MCP

> Fine! I'll go build my own theme park! With blackjack! And hookers!

A comprehensive Model Context Protocol (MCP) server for [Flowise](https://github.com/FlowiseAI/Flowise) - the open-source LLM orchestration platform. Provides complete lifecycle management of Flowise chatflows via MCP tools.

## Why Fluent Mind MCP?

Existing Flowise MCP wrappers only support **querying** existing chatflows. Fluent Mind MCP gives you **full lifecycle management**:

- ✅ Create chatflows from scratch (0→1)
- ✅ Update and modify existing flows
- ✅ Delete chatflows
- ✅ Deploy/undeploy flows
- ✅ Execute predictions
- ✅ Generate AgentFlow V2 from natural language descriptions

**Built from scratch with full control. No dependencies on other MCP implementations. MIT-free.**

## Features

### 8 Comprehensive MCP Tools

1. **list_chatflows** - List all chatflows with metadata
2. **get_chatflow** - Get detailed chatflow information by ID
3. **create_chatflow** - Create new chatflow (CHATFLOW, AGENTFLOW, MULTIAGENT, ASSISTANT)
4. **update_chatflow** - Update existing chatflow properties
5. **delete_chatflow** - Remove chatflow permanently
6. **run_prediction** - Execute chatflow with user input
7. **deploy_chatflow** - Toggle deployment status
8. **generate_agentflow_v2** - Generate AgentFlow V2 from natural language

### Architecture

- **FastMCP** - Modern Python MCP framework
- **httpx** - Async HTTP client with connection pooling
- **Pydantic** - Type-safe data validation
- **Clean separation** - 4-layer architecture (MCP Server, Service Logic, Flowise Client, Domain Models)
- **Production-ready** - Comprehensive error handling, logging, and testing

## Documentation

**Start here**: [Documentation Hub](docs/README.md) - Central navigation for all documentation

### Quick Navigation

| I want to... | Go to |
|--------------|-------|
| **Create a working chatflow** | [Node Templates](examples/node_templates/) |
| **Understand API field names** | [API Field Comparison](docs/API_FIELD_COMPARISON.md) |
| **Learn chatflow creation** | [Working Chatflows Guide](examples/WORKING_CHATFLOWS_GUIDE.md) |
| **Use MCP tools** | [API Reference](#api-reference) (this README) |
| **Understand the data model** | [Data Model](specs/001-flowise-mcp-server/data-model.md) |
| **View implementation plan** | [Implementation Plan](specs/001-flowise-mcp-server/plan.md) |

### Key Resources

- **[docs/README.md](docs/README.md)** - Complete documentation index and navigation hub
- **[examples/node_templates/](examples/node_templates/)** - 39 production-ready node templates
- **[examples/WORKING_CHATFLOWS_GUIDE.md](examples/WORKING_CHATFLOWS_GUIDE.md)** - How to create functional chatflows
- **[docs/API_FIELD_COMPARISON.md](docs/API_FIELD_COMPARISON.md)** - Critical API field reference (camelCase vs snake_case)
- **[specs/001-flowise-mcp-server/](specs/001-flowise-mcp-server/)** - Complete specification and design docs

### Learning Path

**Beginner**: Start here
1. [README.md](#) (this file) - Project overview
2. [examples/node_templates/QUICK_REFERENCE.md](examples/node_templates/QUICK_REFERENCE.md) - Quick start
3. [examples/WORKING_CHATFLOWS_GUIDE.md](examples/WORKING_CHATFLOWS_GUIDE.md) - Learn the patterns

**Intermediate**: Building chatflows
1. [examples/node_templates/](examples/node_templates/) - Browse 39 templates
2. [examples/node_templates/node_builder.py](examples/node_templates/node_builder.py) - Use helper utilities
3. [docs/API_FIELD_COMPARISON.md](docs/API_FIELD_COMPARISON.md) - Understand API structure

**Advanced**: Contributing
1. [specs/001-flowise-mcp-server/spec.md](specs/001-flowise-mcp-server/spec.md) - Full specification
2. [specs/001-flowise-mcp-server/data-model.md](specs/001-flowise-mcp-server/data-model.md) - Data model
3. [.specify/memory/constitution.md](.specify/memory/constitution.md) - Development principles

## Installation

### Prerequisites

- **Python 3.12+** installed
- **Flowise instance** running (local or remote)
- **Claude Desktop** (for MCP integration)
- **Git** (to clone repository)

### Quick Install

```bash
# Clone repository
cd ~/work/ai
git clone <repository-url> fluent-mind-mcp
cd fluent-mind-mcp

# Install dependencies
pip install -e .
```

### Configuration

Create `.env` file in project root:

```bash
# Required
FLOWISE_API_URL=http://localhost:3000

# Optional (if Flowise is secured)
FLOWISE_API_KEY=your_api_key_here

# Optional (defaults shown)
FLOWISE_TIMEOUT=60
FLOWISE_MAX_CONNECTIONS=10
LOG_LEVEL=INFO
```

## Usage

### 1. Standalone Mode

Run the MCP server directly:

```bash
python -m fluent_mind_mcp.server
```

### 2. Claude Desktop Integration

Configure Claude Desktop to use Fluent Mind MCP:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "fluent-mind": {
      "command": "python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "http://localhost:3000",
        "FLOWISE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Restart Claude Desktop** (⌘Q then relaunch) for changes to take effect.

### 3. Test the Integration

In Claude, try these commands:

#### List Chatflows
```
List my Flowise chatflows
```

Expected response: List of all chatflows with names, types, and deployment status.

#### Get Chatflow Details
```
Get details for chatflow abc-123-def
```

Expected response: Complete chatflow information including flowData structure.

#### Execute Chatflow
```
Run chatflow abc-123-def with question "What is AI?"
```

Expected response: Chatflow execution result with answer.

#### Create Chatflow
```
Create a new chatflow named "Test Flow" with this structure:
{
  "nodes": [
    {"id": "llm-1", "type": "chatOpenAI", "data": {"model": "gpt-4"}}
  ],
  "edges": []
}
```

#### Update Chatflow
```
Update chatflow abc-123-def to set deployed=true
```

#### Generate AgentFlow
```
Generate an AgentFlow V2 for a research agent that searches the web and summarizes findings
```

## API Reference

### list_chatflows()

List all available Flowise chatflows.

**Returns:**
```json
{
  "chatflows": [
    {
      "id": "abc-123-def",
      "name": "My Chatflow",
      "type": "CHATFLOW",
      "deployed": true,
      "createdDate": "2025-10-16T12:00:00Z"
    }
  ]
}
```

**Performance**: ≤5 seconds

---

### get_chatflow(chatflow_id: str)

Get detailed chatflow information including workflow structure.

**Parameters:**
- `chatflow_id` (str, required): Unique chatflow identifier

**Returns:**
```json
{
  "id": "abc-123-def",
  "name": "My Chatflow",
  "type": "CHATFLOW",
  "deployed": true,
  "flowData": "{\"nodes\": [...], \"edges\": [...]}",
  "createdDate": "2025-10-16T12:00:00Z"
}
```

**Performance**: ≤5 seconds

---

### create_chatflow(name: str, flow_data: str, type: str = "CHATFLOW", deployed: bool = False)

Create a new Flowise chatflow from flowData structure.

**Parameters:**
- `name` (str, required): Chatflow display name (1-255 characters)
- `flow_data` (str, required): JSON string containing workflow nodes and edges
- `type` (str, optional): Chatflow type - CHATFLOW | AGENTFLOW | MULTIAGENT | ASSISTANT (default: "CHATFLOW")
- `deployed` (bool, optional): Whether to deploy immediately (default: False)

**Returns:** Created chatflow object with assigned ID

**Performance**: ≤10 seconds

**Example:**
```python
flow_data = json.dumps({
  "nodes": [
    {"id": "node-1", "type": "chatOpenAI", "data": {"model": "gpt-4"}}
  ],
  "edges": []
})

result = await create_chatflow(
  name="My Assistant",
  flow_data=flow_data,
  type="CHATFLOW",
  deployed=False
)
```

---

### update_chatflow(chatflow_id: str, name: str = None, flow_data: str = None, deployed: bool = None)

Update existing chatflow properties (partial updates supported).

**Parameters:**
- `chatflow_id` (str, required): Unique chatflow identifier
- `name` (str, optional): New display name
- `flow_data` (str, optional): New workflow structure (JSON string)
- `deployed` (bool, optional): New deployment status

**Returns:** Updated chatflow object

**Performance**: ≤10 seconds

**Note**: At least one optional parameter must be provided.

---

### delete_chatflow(chatflow_id: str)

Delete chatflow permanently from Flowise.

**Parameters:**
- `chatflow_id` (str, required): Unique chatflow identifier

**Returns:**
```json
{
  "success": true,
  "message": "Chatflow abc-123-def deleted successfully",
  "chatflow_id": "abc-123-def"
}
```

**Performance**: ≤5 seconds

**Warning**: This operation cannot be undone.

---

### run_prediction(chatflow_id: str, question: str)

Execute a deployed chatflow with user input.

**Parameters:**
- `chatflow_id` (str, required): Chatflow to execute
- `question` (str, required): User input or question

**Returns:**
```json
{
  "text": "Response from chatflow",
  "questionMessageId": "msg-123",
  "chatMessageId": "msg-456",
  "sessionId": "session-789"
}
```

**Performance**: ≤5 seconds

**Note**: Chatflow must be deployed to execute.

---

### deploy_chatflow(chatflow_id: str, deployed: bool)

Toggle chatflow deployment status.

**Parameters:**
- `chatflow_id` (str, required): Unique chatflow identifier
- `deployed` (bool, required): True to deploy, False to undeploy

**Returns:** Updated chatflow object

**Performance**: ≤10 seconds

---

### generate_agentflow_v2(description: str)

Generate AgentFlow V2 structure from natural language description.

**Parameters:**
- `description` (str, required): Natural language description of desired agent (minimum 10 characters)

**Returns:**
```json
{
  "flowData": "{\"nodes\": [...], \"edges\": [...]}",
  "name": "Generated Agent Name",
  "description": "Generated description"
}
```

**Performance**: ≤10 seconds

**Example:**
```
description = "Create a research agent that searches the web and summarizes findings"
result = await generate_agentflow_v2(description)

# Optionally create chatflow from generated structure
chatflow = await create_chatflow(
  name=result["name"],
  flow_data=result["flowData"],
  type="AGENTFLOW",
  deployed=True
)
```

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
│   ├── unit/                        # Unit tests (mocked)
│   ├── integration/                 # Integration tests (real API)
│   └── acceptance/                  # Acceptance tests (user stories)
├── specs/001-flowise-mcp-server/    # Design documentation
│   ├── spec.md                      # Feature specification
│   ├── plan.md                      # Implementation plan
│   ├── tasks.md                     # Task breakdown
│   ├── data-model.md                # Data models
│   ├── research.md                  # Technical research
│   ├── quickstart.md                # Quick setup guide
│   └── contracts/                   # API contracts
├── README.md                        # This file
├── pyproject.toml                   # Python project configuration
└── .env.example                     # Environment template
```

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=fluent_mind_mcp --cov-report=html tests/

# Run specific test suites
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests only
pytest tests/acceptance/        # Acceptance tests only

# Run linting
ruff check src/

# Run type checking
mypy src/
```

### Code Quality

The project maintains high code quality standards:

- **Test Coverage**: ≥80% overall, 100% critical paths
- **Type Safety**: Full type hints with mypy validation
- **Code Style**: Formatted with ruff
- **Complexity**: Cyclomatic complexity ≤10, nesting ≤3
- **Documentation**: Comprehensive docstrings explaining WHY, not WHAT

## Troubleshooting

### Issue: "Connection refused"

**Cause**: Flowise not running or URL incorrect

**Solution**:
```bash
# Check Flowise is running
curl http://localhost:3000/api/v1/chatflows

# If not running, start Flowise
cd path/to/flowise
npm start
```

### Issue: "Authentication failed"

**Cause**: Invalid or missing API key

**Solution**:
1. Verify API key in Flowise settings
2. Update `FLOWISE_API_KEY` in `.env` and Claude config
3. Restart Claude Desktop

### Issue: "MCP server not found"

**Cause**: Claude Desktop config incorrect or server not installed

**Solution**:
1. Verify `claude_desktop_config.json` path is correct
2. Check `python -m fluent_mind_mcp.server` runs without errors
3. Review Claude Desktop logs: `~/Library/Logs/Claude/mcp*.log`

### Issue: "Import error: fluent_mind_mcp"

**Cause**: Package not installed correctly

**Solution**:
```bash
# Reinstall package
cd ~/work/ai/fluent-mind-mcp
pip install -e . --force-reinstall
```

### View Logs

```bash
# Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp-server-fluent-mind.log

# Or check all MCP logs
ls -la ~/Library/Logs/Claude/mcp*.log
```

**Log Levels**:
- `ERROR`: Failures with context
- `INFO`: Key operations (create, update, delete, execute)
- `WARNING`: Degraded conditions (slow responses, retries)
- `DEBUG`: Detailed traces (off by default)

Change log level in `.env`:
```bash
LOG_LEVEL=DEBUG
```

## Performance

The MCP server meets the following performance targets:

- **List/Get/Execute**: ≤5 seconds per operation
- **Create/Update/Deploy**: ≤10 seconds per operation
- **Full Lifecycle**: ≤60 seconds (create + update + execute + deploy + delete)
- **Concurrency**: Supports 5-10 simultaneous AI assistant connections
- **Scalability**: Efficiently handles up to 100 chatflows

## Security

- **Authentication**: Supports Flowise API key authentication
- **No Credential Exposure**: API keys never logged or exposed in error messages
- **Input Validation**: All user inputs validated before processing
- **Size Limits**: flowData size limited to 1MB to prevent resource exhaustion
- **Error Handling**: Graceful handling of all failure scenarios

## License

This project is **fully open source** and built from scratch. No MIT license requirements from forked code because there is no forked code. Do whatever you want with it.

## Why "Fluent Mind"?

Because interacting with Flowise should be fluid, intuitive, and intelligent. Plus it sounds cool.

## Credits

Built with frustration after discovering existing mcp-flowise tools couldn't actually create chatflows. Sometimes you just gotta build your own theme park.

## Support

- **Issues**: Report at repository issues page
- **Documentation**: See [docs/README.md](docs/README.md) for complete documentation hub
- **Quick Start**: See [specs/001-flowise-mcp-server/quickstart.md](specs/001-flowise-mcp-server/quickstart.md) for fast setup
- **Node Templates**: See [examples/node_templates/](examples/node_templates/) for 39 production-ready templates
- **Working Chatflows**: See [examples/WORKING_CHATFLOWS_GUIDE.md](examples/WORKING_CHATFLOWS_GUIDE.md) for how to create functional chatflows

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m fluent_mind_mcp.server` | Start MCP server |
| `pytest tests/` | Run all tests |
| `pytest --cov=fluent_mind_mcp tests/` | Run tests with coverage |
| `ruff check src/` | Lint code |
| `mypy src/` | Type check |

---

**Status:** ✅ Production Ready

**Version:** 1.0.0

Built with ❤️ and a healthy dose of frustration.
