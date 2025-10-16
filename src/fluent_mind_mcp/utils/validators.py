"""Validation utilities for chatflow operations.

This module provides standalone validation functions for chatflow IDs,
flow data, and chatflow types.
"""

import json
import re
from typing import Any, Dict

from fluent_mind_mcp.models.chatflow import ChatflowType


def validate_chatflow_id(chatflow_id: str) -> bool:
    """Validate chatflow ID format.

    Checks that the chatflow ID is non-empty and optionally
    matches UUID format (Flowise uses UUIDs).

    WHY: Ensures chatflow IDs are valid before making API calls.

    Args:
        chatflow_id: Chatflow identifier to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_chatflow_id("abc-123-def")
        True
        >>> validate_chatflow_id("")
        False
    """
    if not chatflow_id or not isinstance(chatflow_id, str):
        return False

    # Basic validation: non-empty string
    if len(chatflow_id.strip()) == 0:
        return False

    # Optional: Check UUID format (Flowise typically uses UUIDs)
    # Pattern: 8-4-4-4-12 hex digits
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    # Accept both UUID format and other non-empty strings
    # WHY: Flowise may use non-UUID IDs in some cases
    return len(chatflow_id) > 0


def validate_flow_data(flow_data: str) -> tuple[bool, str]:
    """Validate flow data JSON structure.

    Checks that flow_data is valid JSON with required structure:
    - Must be a JSON object
    - Must contain "nodes" array
    - Must contain "edges" array
    - Size must be under 1MB

    WHY: Ensures flow data is well-formed before sending to API.

    Args:
        flow_data: JSON string of workflow structure

    Returns:
        Tuple of (is_valid: bool, error_message: str)
        If valid, error_message is empty string

    Example:
        >>> validate_flow_data('{"nodes": [], "edges": []}')
        (True, '')
        >>> validate_flow_data('invalid json')
        (False, 'Invalid JSON: ...')
    """
    if not flow_data or not isinstance(flow_data, str):
        return (False, "flow_data must be a non-empty string")

    # Check size limit (1MB)
    max_size = 1_048_576  # 1MB in bytes
    size = len(flow_data.encode("utf-8"))
    if size > max_size:
        return (False, f"flow_data size ({size} bytes) exceeds 1MB limit")

    # Validate JSON structure
    try:
        parsed: Dict[str, Any] = json.loads(flow_data)
    except json.JSONDecodeError as e:
        return (False, f"Invalid JSON: {str(e)}")

    # Check required structure
    if not isinstance(parsed, dict):
        return (False, "flow_data must be a JSON object, not array or primitive")

    if "nodes" not in parsed:
        return (False, "flow_data must contain 'nodes' key")

    if "edges" not in parsed:
        return (False, "flow_data must contain 'edges' key")

    if not isinstance(parsed["nodes"], list):
        return (False, "'nodes' must be an array")

    if not isinstance(parsed["edges"], list):
        return (False, "'edges' must be an array")

    return (True, "")


def validate_chatflow_type(chatflow_type: str) -> bool:
    """Validate chatflow type against enum values.

    Checks that the provided type is a valid ChatflowType enum value.

    WHY: Ensures only supported chatflow types are used.

    Args:
        chatflow_type: Chatflow type string to validate

    Returns:
        True if valid enum value, False otherwise

    Example:
        >>> validate_chatflow_type("CHATFLOW")
        True
        >>> validate_chatflow_type("INVALID")
        False
    """
    if not chatflow_type or not isinstance(chatflow_type, str):
        return False

    try:
        ChatflowType(chatflow_type)
        return True
    except ValueError:
        return False
