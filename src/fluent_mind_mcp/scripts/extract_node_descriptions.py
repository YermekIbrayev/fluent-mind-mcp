"""
Node description extraction from Flowise API responses.

This module extracts NodeDescription objects from /api/v1/nodes-list JSON data.
Implements T054a (TDD-GREEN phase) following Clean Code principles.

WHY: Node descriptions are stored in ChromaDB for semantic search
WHY: Separates API parsing from storage concerns
WHY: Enables automated extraction from Flowise metadata

Design decisions:
- Extract all required fields from API response (node_name, label, category, etc.)
- Default missing optional fields (version, deprecated) to safe values
- Generate use cases from description text using simple keyword extraction
- Validate against Pydantic model for type safety
- Export to JSON for manual review before vector storage
"""

import json
import re
from typing import Any

from fluent_mind_mcp.models.node_models import NodeDescription


# Constants for use case extraction
# WHY: Named constants improve readability and maintainability
MAX_USE_CASES = 5
SUPPORTS_PATTERN = r"supports?\s+([^.]+)"
ENABLE_PATTERN = r"(?:enable|allow)s?\s+([^.]+)"


def extract_node_description(api_response: dict[str, Any]) -> NodeDescription:
    """
    Extract NodeDescription from Flowise API node data.

    WHY: Transforms raw API JSON into strongly-typed NodeDescription model
    WHY: Handles missing optional fields with sensible defaults
    WHY: Separates parsing logic from storage logic

    Args:
        api_response: Single node object from /api/v1/nodes-list

    Returns:
        NodeDescription: Validated node description with all fields

    Example:
        >>> node_data = {"name": "chatOpenAI", "label": "ChatOpenAI", ...}
        >>> desc = extract_node_description(node_data)
        >>> print(desc.node_name)  # "chatOpenAI"
    """
    # Extract required fields
    node_name = api_response["name"]
    label = api_response["label"]
    category = api_response["category"]
    description = api_response["description"]
    base_classes = api_response.get("baseClasses", [])

    # Extract optional fields with defaults
    # WHY: version may be missing in some nodes (e.g., custom nodes)
    # WHY: Use 'or' operator for cleaner None/empty handling
    version = str(api_response.get("version") or "")

    # WHY: deprecated defaults to False for safety (assume nodes are active unless marked)
    deprecated = api_response.get("deprecated", False)

    # Generate use cases from description
    # WHY: Use cases improve semantic search accuracy by capturing intent
    use_cases = generate_use_cases(description)

    # Create and return NodeDescription
    return NodeDescription(
        node_name=node_name,
        label=label,
        category=category,
        base_classes=base_classes,
        description=description,
        use_cases=use_cases,
        version=version,
        deprecated=deprecated,
    )


def extract_all_node_descriptions(api_response: dict[str, Any]) -> list[NodeDescription]:
    """
    Extract all NodeDescription objects from /api/v1/nodes-list response.

    WHY: Batch processing for efficient extraction of all 87 nodes
    WHY: Handles API response format with "nodes" array

    Args:
        api_response: Full API response with "nodes" array

    Returns:
        list[NodeDescription]: All extracted node descriptions

    Example:
        >>> api_data = {"nodes": [node1, node2, ...]}
        >>> descriptions = extract_all_node_descriptions(api_data)
        >>> len(descriptions)  # 87
    """
    nodes = api_response.get("nodes", [])
    return [extract_node_description(node) for node in nodes]


def _extract_first_sentence(description: str) -> str:
    """
    Extract first sentence from description text.

    WHY: First sentence typically captures the main purpose of a node
    WHY: Provides a fallback use case when no patterns match

    Args:
        description: Full description text

    Returns:
        str: First sentence (text before first period)
    """
    return description.split(".")[0].strip()


def _extract_pattern_matches(
    desc_lower: str, pattern: str, split_on_connectors: bool = True
) -> list[str]:
    """
    Extract and process regex pattern matches from description.

    WHY: Reusable pattern extraction logic
    WHY: Handles splitting on 'and', 'or', commas for capability lists
    WHY: Single responsibility - one pattern extraction strategy

    Args:
        desc_lower: Lowercase description text for case-insensitive matching
        pattern: Regex pattern to match
        split_on_connectors: If True, split matches on 'and', 'or', commas

    Returns:
        list[str]: Extracted and processed matches
    """
    matches = re.findall(pattern, desc_lower)
    result = []

    for match in matches:
        if split_on_connectors:
            # WHY: "Supports X and Y" → ["X", "Y"]
            items = re.split(r"\s+and\s+|\s+or\s+|,\s*", match)
            result.extend([item.strip() for item in items if item.strip()])
        else:
            result.append(match.strip())

    return result


def _deduplicate_preserving_order(items: list[str], max_items: int) -> list[str]:
    """
    Remove duplicates while preserving order and limiting results.

    WHY: Avoid redundant use cases in embeddings
    WHY: Case-insensitive deduplication (treat "Chat" and "chat" as same)
    WHY: Preserve original order for relevance (first mention often most important)

    Args:
        items: List of items to deduplicate
        max_items: Maximum items to return

    Returns:
        list[str]: Deduplicated items limited to max_items
    """
    seen = set()
    unique = []

    for item in items:
        item_lower = item.lower()
        if item_lower not in seen:
            seen.add(item_lower)
            unique.append(item)

    return unique[:max_items]


def generate_use_cases(description: str) -> list[str]:
    """
    Infer use cases from node description text.

    WHY: Use cases improve embedding quality for semantic search
    WHY: Extracts key capabilities mentioned in description
    WHY: Simple keyword-based extraction (no LLM needed)
    WHY: Orchestrates helper functions for clean separation of concerns

    Strategy:
    - Extract first sentence as primary use case (captures main purpose)
    - Look for capability keywords: "support", "enable", "allow"
    - Extract phrases around these keywords
    - Handle common patterns like "Supports X and Y"
    - Deduplicate and limit to MAX_USE_CASES

    Args:
        description: Node description text

    Returns:
        list[str]: Inferred use cases (at least one, max MAX_USE_CASES)

    Example:
        >>> desc = "Wrapper around OpenAI models. Supports streaming and function calling."
        >>> use_cases = generate_use_cases(desc)
        >>> len(use_cases) > 0  # True
    """
    use_cases = []

    # WHY: Convert to lowercase for case-insensitive matching
    desc_lower = description.lower()

    # Pattern 0: Extract first sentence as primary use case
    # WHY: First sentence usually describes main purpose (e.g., "chat endpoint")
    first_sentence = _extract_first_sentence(description)
    if first_sentence:
        use_cases.append(first_sentence)

    # Pattern 1: "Supports X and Y" or "Supports X, Y, Z"
    # WHY: Common documentation pattern in Flowise
    use_cases.extend(
        _extract_pattern_matches(desc_lower, SUPPORTS_PATTERN, split_on_connectors=True)
    )

    # Pattern 2: "Enable X" or "Allow Y"
    # WHY: Another common capability pattern
    use_cases.extend(
        _extract_pattern_matches(desc_lower, ENABLE_PATTERN, split_on_connectors=False)
    )

    # WHY: Remove duplicates and limit to MAX_USE_CASES
    return _deduplicate_preserving_order(use_cases, MAX_USE_CASES)


def validate_node_description(node_desc: NodeDescription) -> None:
    """
    Validate NodeDescription against data model schema.

    WHY: Ensures extracted data conforms to Pydantic model
    WHY: Catches extraction errors early before storage
    WHY: Validates required attributes exist

    Args:
        node_desc: NodeDescription to validate

    Raises:
        AttributeError: If required attribute is missing
        ValueError: If Pydantic validation fails

    Example:
        >>> desc = extract_node_description(api_data)
        >>> validate_node_description(desc)  # Raises if invalid
    """
    # WHY: Check required attributes exist
    # WHY: These are core fields needed for semantic search
    required_attrs = [
        "node_name",
        "label",
        "category",
        "base_classes",
        "description",
        "use_cases",
        "version",
        "deprecated",
    ]

    for attr in required_attrs:
        if not hasattr(node_desc, attr):
            raise AttributeError(f"NodeDescription missing required attribute: {attr}")

    # WHY: Pydantic already validates during creation, but explicit check for clarity
    # WHY: This validation helps catch issues in tests
    if not isinstance(node_desc, NodeDescription):
        raise ValueError(f"Expected NodeDescription, got {type(node_desc)}")


def export_to_json(node_descriptions: list[NodeDescription]) -> str:
    """
    Export NodeDescription list to JSON format for review.

    WHY: Enables manual review of extracted nodes before vector storage
    WHY: JSON format is easy to inspect and version control
    WHY: Uses Pydantic's built-in serialization for consistency

    Args:
        node_descriptions: List of NodeDescription objects

    Returns:
        str: Pretty-printed JSON string

    Example:
        >>> descriptions = [desc1, desc2]
        >>> json_output = export_to_json(descriptions)
        >>> json.loads(json_output)  # Valid JSON
    """
    # WHY: Use model_dump() instead of dict() for Pydantic v2 compatibility
    # WHY: exclude_none=True removes None values for cleaner JSON
    data = [nd.model_dump(exclude_none=True, exclude={"embedding"}) for nd in node_descriptions]

    # WHY: indent=2 for human-readable format
    # WHY: sort_keys=True for consistent ordering
    return json.dumps(data, indent=2, sort_keys=True)
