# Quickstart: Fluent Mind MCP Server

**Feature**: Fluent Mind MCP Server
**Branch**: `001-flowise-mcp-server`
**Date**: 2025-10-16

---

## Overview

Get the Fluent Mind MCP Server running with Claude Desktop in 5 minutes.

---

## Prerequisites

✅ **Python 3.12+** installed
✅ **Flowise instance** running (local or remote)
✅ **Claude Desktop** installed
✅ **Git** (to clone repository)

---

## Step 1: Clone and Install

```bash
# Clone repository
cd ~/work/ai
git clone <repository-url> fluent-mind-mcp
cd fluent-mind-mcp

# Install dependencies
pip install -e .
```

---

## Step 2: Configure Environment

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

---

## Step 3: Verify Flowise Connection

```bash
# Test connection to Flowise
python -m fluent_mind_mcp.client.flowise_client --test
```

Expected output:
```
✓ Connected to Flowise at http://localhost:3000
✓ Authentication successful
✓ Found 5 chatflows
```

---

## Step 4: Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

**Note**: Replace `your_api_key_here` with your actual API key (or omit if not using authentication).

---

## Step 5: Restart Claude Desktop

1. **Quit Claude Desktop** completely (⌘Q on Mac)
2. **Relaunch** Claude Desktop
3. Wait for MCP server to initialize (~5 seconds)

---

## Step 6: Test the Integration

In Claude, try these commands:

### List Chatflows
```
List my Flowise chatflows
```

Expected response: List of all chatflows with names, types, and deployment status.

### Get Chatflow Details
```
Get details for chatflow abc-123-def
```

Expected response: Complete chatflow information including flowData structure.

### Execute Chatflow
```
Run chatflow abc-123-def with question "What is AI?"
```

Expected response: Chatflow execution result with answer.

---

## Common Issues

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

---

## Verify Installation

Run all verification checks:

```bash
# 1. Python version
python --version  # Should be 3.12+

# 2. Package installed
python -c "import fluent_mind_mcp; print('✓ Package installed')"

# 3. Dependencies
python -c "import fastmcp, httpx, pydantic; print('✓ Dependencies OK')"

# 4. Flowise connection
python -m fluent_mind_mcp.client.flowise_client --test

# 5. MCP server starts
timeout 5 python -m fluent_mind_mcp.server || echo "✓ Server starts"
```

All checks should pass before proceeding.

---

## Next Steps

### Explore MCP Tools

List all available tools:
```
What MCP tools are available from fluent-mind?
```

Expected: 8 tools listed (list_chatflows, get_chatflow, create_chatflow, update_chatflow, delete_chatflow, run_prediction, deploy_chatflow, generate_agentflow_v2)

### Create a Chatflow

```
Create a new chatflow named "Test Flow" with this structure:
{
  "nodes": [
    {"id": "llm-1", "type": "chatOpenAI", "data": {"model": "gpt-4"}}
  ],
  "edges": []
}
```

### Update a Chatflow

```
Update chatflow abc-123-def to set deployed=true
```

### Generate AgentFlow

```
Generate an AgentFlow V2 for a research agent that searches the web and summarizes findings
```

---

## Performance Verification

Test performance targets:

```bash
# List 100 chatflows (should complete in <5s)
time python -c "
import asyncio
from fluent_mind_mcp.client.flowise_client import FlowiseClient
from fluent_mind_mcp.models.config import FlowiseConfig

async def test():
    config = FlowiseConfig.from_env()
    async with FlowiseClient(config) as client:
        chatflows = await client.list_chatflows()
        print(f'Listed {len(chatflows)} chatflows')

asyncio.run(test())
"

# Create chatflow (should complete in <10s)
# Execute chatflow (should complete in <5s)
```

---

## Development Setup

For development work:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=fluent_mind_mcp tests/

# Run linting
ruff check src/

# Run type checking
mypy src/
```

---

## Logging

View MCP server logs:

```bash
# Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp-server-fluent-mind.log

# Or check all MCP logs
ls -la ~/Library/Logs/Claude/mcp*.log
```

**Log Levels**:
- ERROR: Failures with context
- INFO: Key operations (create, update, delete, execute)
- WARNING: Degraded conditions (slow responses, retries)
- DEBUG: Detailed traces (off by default)

Change log level in `.env`:
```
LOG_LEVEL=DEBUG
```

---

## Uninstall

To remove Fluent Mind MCP:

1. **Remove from Claude Desktop config**:
   Delete the `fluent-mind` entry from `claude_desktop_config.json`

2. **Uninstall package**:
   ```bash
   pip uninstall fluent-mind-mcp
   ```

3. **Remove source**:
   ```bash
   rm -rf ~/work/ai/fluent-mind-mcp
   ```

4. **Restart Claude Desktop**

---

## Support

- **Issues**: Report at repository issues page
- **Documentation**: See [plan_cc.md](plan_cc.md) for implementation details
- **Spec**: See [spec.md](spec.md) for requirements
- **Contracts**: See [contracts/mcp-tools.md](contracts/mcp-tools.md) for API details

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python -m fluent_mind_mcp.server` | Start MCP server |
| `python -m fluent_mind_mcp.client.flowise_client --test` | Test Flowise connection |
| `pytest tests/` | Run all tests |
| `ruff check src/` | Lint code |
| `mypy src/` | Type check |

---

**Quickstart Complete**: ✅

You should now have Fluent Mind MCP Server running with Claude Desktop!
