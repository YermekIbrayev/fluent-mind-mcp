# Claude Desktop Integration Guide

Complete guide for integrating Fluent Mind MCP Server with Claude Desktop.

---

## Prerequisites

Before integrating, ensure you have:

1. **Claude Desktop** installed
   - Download from: https://claude.ai/download
   - Version: Latest stable release

2. **Python 3.12+** installed
   ```bash
   python3 --version  # Should show 3.12 or higher
   ```

3. **Fluent Mind MCP** installed
   ```bash
   cd /Users/yermekibrayev/work/ai/fluent-mind-mcp
   pip install -e .
   ```

4. **Flowise instance** running
   - Local: http://localhost:3000
   - Remote: Your Flowise URL
   - API key (if secured)

---

## Installation Steps

### 1. Verify MCP Server Works

Test the server runs standalone:

```bash
cd /Users/yermekibrayev/work/ai/fluent-mind-mcp
python -m fluent_mind_mcp.server
```

You should see MCP server output without errors. Press `Ctrl+C` to stop.

### 2. Configure Claude Desktop

Edit Claude Desktop's MCP configuration file:

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```
notepad %APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

### 3. Add MCP Server Configuration

Add the following to `claude_desktop_config.json`:

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

**Configuration Options:**

| Environment Variable | Required | Default | Description |
|---------------------|----------|---------|-------------|
| `FLOWISE_API_URL` | Yes | - | Flowise API base URL (e.g., `http://localhost:3000`) |
| `FLOWISE_API_KEY` | No | - | Flowise API key (if secured) |
| `FLOWISE_TIMEOUT` | No | 60 | Request timeout in seconds |
| `FLOWISE_MAX_CONNECTIONS` | No | 10 | Maximum concurrent connections |
| `LOG_LEVEL` | No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

**Example with all options:**
```json
{
  "mcpServers": {
    "fluent-mind": {
      "command": "python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "http://localhost:3000",
        "FLOWISE_API_KEY": "your_api_key_here",
        "FLOWISE_TIMEOUT": "60",
        "FLOWISE_MAX_CONNECTIONS": "10",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

**Important:** Claude Desktop only loads MCP servers on startup.

**macOS:**
```bash
# Quit Claude completely (⌘Q)
# Then relaunch from Applications
```

**Windows:**
```
Right-click Claude in system tray → Exit
# Then restart from Start Menu
```

**Linux:**
```bash
killall claude-desktop
claude-desktop &
```

---

## Verification

### 1. Check MCP Server Status

In Claude, look for the MCP indicator in the toolbar:
- **Green dot**: Server connected successfully
- **Red dot**: Server failed to start
- **No dot**: Server not configured

### 2. Test Basic Operations

Try these commands in Claude:

#### List Chatflows
```
List my Flowise chatflows
```

**Expected response:** JSON array with chatflow names, types, and IDs.

#### Get Chatflow Details
```
Get details for chatflow <chatflow-id>
```

**Expected response:** Complete chatflow information including flowData.

#### Execute Chatflow
```
Run chatflow <chatflow-id> with question "What is AI?"
```

**Expected response:** Chatflow execution result with answer.

### 3. Check Logs (if issues occur)

**macOS:**
```bash
tail -f ~/Library/Logs/Claude/mcp-server-fluent-mind.log
```

**Windows:**
```
type %APPDATA%\Claude\Logs\mcp-server-fluent-mind.log
```

**Linux:**
```bash
tail -f ~/.config/Claude/logs/mcp-server-fluent-mind.log
```

---

## Troubleshooting

### Issue: "MCP server not found"

**Symptoms:**
- No MCP indicator in Claude toolbar
- Claude doesn't recognize Fluent Mind tools

**Solutions:**

1. **Verify config file path**
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

   # Should show your fluent-mind configuration
   ```

2. **Check JSON syntax**
   - Use https://jsonlint.com/ to validate JSON
   - Common errors: Missing commas, unmatched braces

3. **Restart Claude Desktop completely**
   - Quit Claude (⌘Q on macOS, not just close window)
   - Relaunch from Applications

### Issue: "Connection refused"

**Symptoms:**
- Claude shows "ConnectionError: Cannot connect to Flowise"
- MCP tools fail with network errors

**Solutions:**

1. **Verify Flowise is running**
   ```bash
   curl http://localhost:3000/api/v1/chatflows
   # Should return JSON array
   ```

2. **Check Flowise URL in config**
   - Ensure no trailing slash: `http://localhost:3000` (not `http://localhost:3000/`)
   - For remote Flowise, use full URL: `http://192.168.1.100:3000`

3. **Test network connectivity**
   ```bash
   ping 192.168.1.100  # For remote Flowise
   ```

### Issue: "Authentication failed"

**Symptoms:**
- Claude shows "AuthenticationError: Invalid API key"
- MCP tools fail with 401 errors

**Solutions:**

1. **Verify API key in Flowise**
   - Open Flowise web UI
   - Go to Settings → API Key
   - Copy exact key (no extra spaces)

2. **Update Claude config**
   ```json
   "FLOWISE_API_KEY": "paste_exact_key_here"
   ```

3. **Restart Claude Desktop**

### Issue: "ValidationError: Invalid flowData"

**Symptoms:**
- Create/update operations fail with validation errors
- Error mentions "flowData must contain 'nodes'"

**Solutions:**

1. **Check flowData structure**
   ```json
   {
     "nodes": [
       {"id": "node-1", "type": "chatOpenAI", "data": {}}
     ],
     "edges": []
   }
   ```

2. **Verify flowData size**
   - Maximum: 1MB
   - Check size: `echo "$flowData" | wc -c`

3. **Ensure valid JSON**
   - Test with: `echo "$flowData" | python -m json.tool`

### Issue: Slow performance

**Symptoms:**
- Operations take longer than expected
- Timeout errors

**Solutions:**

1. **Increase timeout**
   ```json
   "FLOWISE_TIMEOUT": "120"
   ```

2. **Check network latency**
   ```bash
   time curl http://localhost:3000/api/v1/chatflows
   ```

3. **Review Flowise logs**
   - Check for slow database queries
   - Look for resource constraints

---

## Advanced Configuration

### Using Python Virtual Environment

If Fluent Mind MCP is installed in a virtualenv:

```json
{
  "mcpServers": {
    "fluent-mind": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "http://localhost:3000"
      }
    }
  }
}
```

**Find venv path:**
```bash
which python  # Copy this path to "command"
```

### Debug Mode

Enable debug logging for troubleshooting:

```json
{
  "mcpServers": {
    "fluent-mind": {
      "command": "python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "http://localhost:3000",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

Then check logs for detailed traces.

### Multiple Flowise Instances

Configure multiple MCP servers for different Flowise instances:

```json
{
  "mcpServers": {
    "fluent-mind-local": {
      "command": "python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "http://localhost:3000"
      }
    },
    "fluent-mind-prod": {
      "command": "python",
      "args": ["-m", "fluent_mind_mcp.server"],
      "env": {
        "FLOWISE_API_URL": "https://flowise.example.com",
        "FLOWISE_API_KEY": "prod_api_key"
      }
    }
  }
}
```

In Claude, specify which server: "List chatflows from fluent-mind-prod"

---

## Available MCP Tools

Once integrated, these tools are available in Claude:

### 1. list_chatflows()
List all available chatflows.

**Example:** "List my Flowise chatflows"

### 2. get_chatflow(chatflow_id)
Get detailed chatflow information.

**Example:** "Get details for chatflow abc-123-def"

### 3. run_prediction(chatflow_id, question)
Execute a deployed chatflow.

**Example:** "Run chatflow abc-123-def with question 'What is AI?'"

### 4. create_chatflow(name, flow_data, type, deployed)
Create a new chatflow.

**Example:** "Create a chatflow named 'Test' with this flowData: {...}"

### 5. update_chatflow(chatflow_id, name, flow_data, deployed)
Update existing chatflow properties.

**Example:** "Update chatflow abc-123-def to set deployed=true"

### 6. delete_chatflow(chatflow_id)
Permanently delete a chatflow.

**Example:** "Delete chatflow abc-123-def"

### 7. deploy_chatflow(chatflow_id, deployed)
Toggle chatflow deployment status.

**Example:** "Deploy chatflow abc-123-def"

### 8. generate_agentflow_v2(description)
Generate AgentFlow V2 from natural language.

**Example:** "Generate an AgentFlow for a research agent that searches the web"

See [README.md](README.md) for detailed API reference.

---

## Usage Tips

### Natural Language Commands

Claude understands natural language for MCP tools:

**Instead of:** "Use list_chatflows tool"

**Try:** "Show me all my Flowise chatflows"

**Instead of:** "Use get_chatflow tool with ID abc-123"

**Try:** "What's in the chatflow named 'Customer Support Bot'?"

### Chaining Operations

Combine multiple operations in one request:

```
Create a new chatflow called "Weather Bot" with this structure: {...}
Then deploy it.
Then test it with the question "What's the weather?"
```

### Error Recovery

If an operation fails, Claude will show the error and suggest fixes:

```
Error: ConnectionError - Cannot connect to Flowise
Suggestion: Check that Flowise is running at http://localhost:3000
```

---

## Security Best Practices

### 1. Protect API Keys

**Don't:**
- Commit `claude_desktop_config.json` to version control
- Share API keys in chat logs

**Do:**
- Use environment-specific API keys
- Rotate keys periodically
- Use Flowise's built-in key management

### 2. Network Security

**For local Flowise:**
- Bind to localhost only (127.0.0.1)
- Don't expose to public internet

**For remote Flowise:**
- Use HTTPS: `https://flowise.example.com`
- Enable Flowise authentication
- Use firewall rules to restrict access

### 3. Resource Limits

Set connection limits to prevent resource exhaustion:

```json
"FLOWISE_MAX_CONNECTIONS": "5",
"FLOWISE_TIMEOUT": "30"
```

---

## Getting Help

### Documentation

- **README.md**: Complete feature documentation
- **specs/001-flowise-mcp-server/**: Design specifications
- **specs/001-flowise-mcp-server/quickstart.md**: Quick setup guide

### Logs

Check MCP server logs for detailed error information:

```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp-server-fluent-mind.log

# Look for:
# - Connection errors: "Cannot connect to Flowise"
# - Authentication errors: "Invalid API key"
# - Validation errors: "Invalid flowData"
```

### Common Issues

See [Troubleshooting](#troubleshooting) section above.

---

## Next Steps

Once integrated:

1. **Explore chatflows**: `"List my Flowise chatflows"`
2. **Test execution**: `"Run chatflow <id> with question '<test question>'"`
3. **Create workflows**: `"Create a chatflow named 'Test' with..."`
4. **Generate agents**: `"Generate an AgentFlow for..."`

For advanced usage, see [README.md](README.md) API Reference.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-16
**Status**: Production Ready
