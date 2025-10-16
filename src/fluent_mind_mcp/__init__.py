"""Fluent Mind MCP Server - Model Context Protocol server for Flowise integration.

WHY: Provides a standardized MCP interface for AI assistants to discover, execute,
     and manage Flowise chatflows programmatically.

This package contains:
- MCP server tools for chatflow operations (server.py)
- Business logic layer for validation and logging (services/)
- HTTP client for Flowise API communication (client/)
- Domain models and validation (models/)
- Structured logging infrastructure (logging/)
"""

from fluent_mind_mcp.models import Chatflow, FlowiseConfig, PredictionResponse

__all__ = ["Chatflow", "FlowiseConfig", "PredictionResponse"]
