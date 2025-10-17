"""Logging utilities for Fluent Mind MCP.

WHY: Provides structured logging infrastructure with operation timing, credential masking,
     and context management for monitoring and debugging.

This package contains:
- OperationLogger: Structured logger with timing context manager

Exports:
- OperationLogger: Logger for tracking operations with timing and context

Features:
- Automatic credential masking (API keys, passwords)
- Operation timing with context manager
- Structured log output for parsing and analysis
- Configurable log levels (DEBUG, INFO, WARNING, ERROR)
"""

from fluent_mind_mcp.logging.operation_logger import OperationLogger

__all__ = ["OperationLogger"]
