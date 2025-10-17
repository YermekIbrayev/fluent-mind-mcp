"""Validation utilities for chatflow operations.

This module provides validation functions and classes for chatflow IDs,
flow data, and chatflow types.
"""

import json
from typing import Any

from fluent_mind_mcp.models.chatflow import ChatflowType


class FlowDataValidator:
    """Reusable validator for flowData structure and constraints.

    WHY: Centralizes flowData validation logic to eliminate duplication
         between service layer validation and Pydantic model validators.
         This ensures consistent validation behavior and maintainability.

    Validates:
    - JSON structure: Must be valid JSON object with 'nodes' and 'edges'
    - Size limit: Must be under 1MB to prevent API payload issues
    - Type safety: Nodes and edges must be arrays

    Example:
        >>> validator = FlowDataValidator()
        >>> validator.validate('{"nodes": [], "edges": []}')
        (True, '', None)
        >>> validator.validate('invalid')
        (False, 'Invalid JSON: ...', None)
    """

    MAX_SIZE_BYTES = 1_048_576  # 1MB

    def __init__(self, max_size: int | None = None):
        """Initialize validator with optional custom size limit.

        WHY: Allows customization of size limit for testing or future requirements.

        Args:
            max_size: Maximum size in bytes (defaults to 1MB)
        """
        self.max_size = max_size or self.MAX_SIZE_BYTES

    def validate(self, flow_data: str) -> tuple[bool, str, dict[str, Any] | None]:
        """Validate flow_data JSON structure and constraints.

        WHY: Single source of truth for flowData validation logic.

        Args:
            flow_data: JSON string of workflow structure

        Returns:
            Tuple of (is_valid: bool, error_message: str, parsed_data: Optional[Dict])
            - is_valid: True if validation passes
            - error_message: Empty string if valid, error description if invalid
            - parsed_data: Parsed JSON dict if valid, None if invalid

        Example:
            >>> validator = FlowDataValidator()
            >>> valid, err, data = validator.validate('{"nodes": [], "edges": []}')
            >>> valid
            True
            >>> data
            {'nodes': [], 'edges': []}
        """
        # Check type and emptiness
        if not flow_data or not isinstance(flow_data, str):
            return (False, "flow_data must be a non-empty string", None)

        # Check size limit
        size = len(flow_data.encode("utf-8"))
        if size > self.max_size:
            return (
                False,
                f"flow_data size ({size} bytes) exceeds {self.max_size} byte limit",
                None
            )

        # Validate JSON structure
        try:
            parsed: dict[str, Any] = json.loads(flow_data)
        except json.JSONDecodeError as e:
            return (False, f"Invalid JSON: {str(e)}", None)

        # Check required structure
        if not isinstance(parsed, dict):
            return (False, "flow_data must be a JSON object, not array or primitive", None)

        if "nodes" not in parsed:
            return (False, "flow_data must contain 'nodes' key", None)

        if "edges" not in parsed:
            return (False, "flow_data must contain 'edges' key", None)

        if not isinstance(parsed["nodes"], list):
            return (False, "'nodes' must be an array", None)

        if not isinstance(parsed["edges"], list):
            return (False, "'edges' must be an array", None)

        return (True, "", parsed)

    def validate_for_pydantic(self, flow_data: str) -> str:
        """Validate flowData for use in Pydantic field validators.

        WHY: Pydantic validators expect to return the value or raise ValueError.
             This adapter method provides the interface Pydantic expects.

        Args:
            flow_data: JSON string to validate

        Returns:
            The original flow_data string if valid

        Raises:
            ValueError: If validation fails with descriptive message

        Example:
            >>> validator = FlowDataValidator()
            >>> validator.validate_for_pydantic('{"nodes": [], "edges": []}')
            '{"nodes": [], "edges": []}'
            >>> validator.validate_for_pydantic('invalid')
            ValueError: Invalid JSON: ...
        """
        is_valid, error_message, _ = self.validate(flow_data)
        if not is_valid:
            raise ValueError(error_message)
        return flow_data


# Singleton instance for convenience
_default_validator = FlowDataValidator()


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

    # Accept non-empty strings
    # WHY: Flowise may use UUID format or other ID formats
    return len(chatflow_id) > 0


def validate_flow_data(flow_data: str) -> tuple[bool, str]:
    """Validate flow data JSON structure.

    Checks that flow_data is valid JSON with required structure:
    - Must be a JSON object
    - Must contain "nodes" array
    - Must contain "edges" array
    - Size must be under 1MB

    WHY: Ensures flow data is well-formed before sending to API.
         This is a convenience wrapper around FlowDataValidator for
         backward compatibility with existing code.

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
    is_valid, error_message, _ = _default_validator.validate(flow_data)
    return (is_valid, error_message)


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


def sanitize_inputs(**kwargs: Any) -> dict[str, Any]:
    """Sanitize input values by stripping whitespace from strings.

    WHY: Centralizes input sanitization to eliminate duplication of .strip() calls
         across service methods. Ensures consistent handling of whitespace in inputs.

    Args:
        **kwargs: Keyword arguments with values to sanitize

    Returns:
        Dictionary with sanitized values (strings stripped, others unchanged)

    Example:
        >>> sanitize_inputs(chatflow_id="  abc  ", count=42, name=None)
        {'chatflow_id': 'abc', 'count': 42, 'name': None}
    """
    result = {}
    for key, value in kwargs.items():
        if isinstance(value, str):
            result[key] = value.strip()
        else:
            result[key] = value
    return result
