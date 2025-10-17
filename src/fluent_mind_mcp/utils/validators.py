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


def sanitize_string(value: str, max_length: int | None = None) -> str:
    """Sanitize a single string value to prevent injection attacks.

    WHY: Prevents various injection attacks (XSS, SQL injection, command injection)
         by validating and normalizing string inputs. Does NOT escape HTML/SQL -
         that's the responsibility of the consuming system (Flowise).

    Security measures:
    - Strips leading/trailing whitespace
    - Validates length limits
    - Rejects null bytes (can cause truncation attacks)
    - Rejects control characters except newlines/tabs (for security)

    NOTE: We do NOT reject SQL keywords, HTML tags, or shell metacharacters
          because the MCP server is a pass-through to Flowise. The Flowise
          API is responsible for proper escaping and sanitization for its
          database and UI. We only validate that inputs are well-formed strings.

    Args:
        value: String value to sanitize
        max_length: Optional maximum length (raises ValueError if exceeded)

    Returns:
        Sanitized string value

    Raises:
        ValueError: If input contains forbidden characters or exceeds max_length

    Example:
        >>> sanitize_string("  hello  ")
        'hello'
        >>> sanitize_string("test\\x00injection")  # doctest: +SKIP
        ValueError: String contains null bytes
    """
    if not isinstance(value, str):
        raise ValueError(f"Expected string, got {type(value).__name__}")

    # Strip whitespace
    sanitized = value.strip()

    # Check for null bytes (security: prevents truncation attacks)
    if '\x00' in sanitized:
        raise ValueError("String contains null bytes")

    # Check for control characters (except newlines and tabs which are valid)
    # WHY: Control characters can cause unexpected behavior in logs, UIs, etc.
    for char in sanitized:
        code = ord(char)
        # Allow printable chars (32-126), newline (10), tab (9), carriage return (13)
        # and extended Unicode characters (>127)
        if code < 32 and code not in (9, 10, 13):
            raise ValueError(f"String contains invalid control character: {repr(char)}")

    # Validate length if specified
    if max_length is not None and len(sanitized) > max_length:
        raise ValueError(
            f"String length {len(sanitized)} exceeds maximum {max_length}"
        )

    return sanitized


def sanitize_inputs(**kwargs: Any) -> dict[str, Any]:
    """Sanitize input values by stripping whitespace from strings.

    WHY: Centralizes input sanitization to eliminate duplication of .strip() calls
         across service methods. Ensures consistent handling of whitespace in inputs.

    This is a lightweight sanitization that only strips whitespace. For more
    robust sanitization with injection protection, use sanitize_string() directly.

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


def validate_response_type(response_data: Any, expected_type: type) -> None:
    """Validate API response is of expected type.

    WHY: Protects against malicious or malformed API responses that could
         cause unexpected behavior. Validates response structure before
         processing to prevent type errors and security issues.

    Args:
        response_data: The parsed response data from API
        expected_type: The expected Python type (dict, list, str, etc.)

    Raises:
        ValueError: If response type doesn't match expected type

    Example:
        >>> validate_response_type({"key": "value"}, dict)  # OK
        >>> validate_response_type([1, 2, 3], list)  # OK
        >>> validate_response_type("string", dict)  # doctest: +SKIP
        ValueError: Expected dict response, got str
    """
    if not isinstance(response_data, expected_type):
        actual_type = type(response_data).__name__
        expected_name = expected_type.__name__
        raise ValueError(
            f"Expected {expected_name} response, got {actual_type}. "
            f"This may indicate a malicious or malformed API response."
        )


def validate_response_has_fields(response_data: dict[str, Any], required_fields: list[str]) -> None:
    """Validate API response dict has required fields.

    WHY: Ensures API responses contain expected data structure before processing.
         Prevents KeyError and protects against incomplete or tampered responses.

    Args:
        response_data: The parsed response dictionary from API
        required_fields: List of required field names

    Raises:
        ValueError: If any required field is missing

    Example:
        >>> validate_response_has_fields({"id": "123", "name": "Test"}, ["id", "name"])  # OK
        >>> validate_response_has_fields({"id": "123"}, ["id", "name"])  # doctest: +SKIP
        ValueError: Response missing required field: name
    """
    if not isinstance(response_data, dict):
        raise ValueError("Response must be a dictionary to validate fields")

    missing_fields = [field for field in required_fields if field not in response_data]

    if missing_fields:
        raise ValueError(
            f"Response missing required field(s): {', '.join(missing_fields)}. "
            f"This may indicate an incomplete or malicious API response."
        )
