# Fluent Mind MCP - Project Overview

## What is it?

Fluent Mind MCP is a Model Context Protocol (MCP) server that provides complete control over Flowise chatflows through MCP tools. It wraps the Flowise REST API to enable AI assistants to create, read, update, delete, and execute Flowise workflows programmatically.

## Why build it?

Existing Flowise MCP implementations (mcp-flowise by matthewhand and andydukes) only support querying existing chatflows. They cannot create new chatflows from scratch (0→1 creation), update flows, or delete them. Fluent Mind MCP provides full lifecycle management with complete control and no external dependencies.

## Core Capabilities

The MCP server exposes 8 tools:

1. **list_chatflows** - List all chatflows
2. **get_chatflow** - Get detailed chatflow by ID
3. **create_chatflow** - Create new chatflow (supports all types: CHATFLOW, AGENTFLOW, MULTIAGENT, ASSISTANT)
4. **update_chatflow** - Update existing chatflow
5. **delete_chatflow** - Remove chatflow
6. **run_prediction** - Execute chatflow with input
7. **deploy_chatflow** - Toggle deployment status
8. **generate_agentflow_v2** - Generate AgentFlow V2 from natural language description

## Technology

Built with Python and FastMCP framework. Uses httpx for HTTP client, Pydantic for data validation.

## Configuration

Requires Flowise instance (local or remote) accessible via REST API. Configurable through environment variables (FLOWISE_API_URL, FLOWISE_API_KEY).

## Use Case

Enables AI assistants (Claude, GPT, etc.) to programmatically manage Flowise workflows. Useful for:
- Automated chatflow creation from templates
- Dynamic workflow generation based on user requirements
- Integration testing of Flowise deployments
- Chatflow lifecycle management in CI/CD pipelines
- Building higher-level abstractions on top of Flowise

## Main View

**Input:** MCP tool calls from AI assistant
**Processing:** HTTP requests to Flowise REST API
**Output:** Structured responses (JSON) back to AI assistant

Simple wrapper layer that translates MCP tool calls into Flowise API operations.
