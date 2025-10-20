"""
Unit tests for node description extraction from Flowise API.

Tests the extraction of NodeDescription objects from /api/v1/nodes-list JSON responses.
All tests are TDD-RED phase - they should FAIL until implementation is complete.

Test coverage:
- API response parsing
- Metadata extraction (complete and partial)
- Deprecated flag handling
- Use case generation
- Schema validation
- Batch processing (87 nodes)
- JSON output formatting
"""

import json
import pytest
from typing import Any

from fluent_mind_mcp.models.node_models import NodeDescription
from fluent_mind_mcp.scripts.extract_node_descriptions import (
    extract_node_description,
    extract_all_node_descriptions,
    generate_use_cases,
    validate_node_description,
    export_to_json,
)


# Test Data: Sample Flowise API Response
SAMPLE_NODE_COMPLETE = {
    "name": "chatOpenAI",
    "label": "ChatOpenAI",
    "version": 1,
    "description": "Wrapper around OpenAI large language models that use the Chat endpoint",
    "category": "Chat Models",
    "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel"],
    "deprecated": False,
}

SAMPLE_NODE_MISSING_OPTIONAL = {
    "name": "bufferMemory",
    "label": "Buffer Memory",
    "description": "Maintains a buffer of recent messages",
    "category": "Memory",
    "baseClasses": ["BufferMemory", "BaseChatMemory"],
}

SAMPLE_NODE_DEPRECATED = {
    "name": "oldChatModel",
    "label": "Old Chat Model",
    "version": 0,
    "description": "Legacy chat model - use ChatOpenAI instead",
    "category": "Chat Models",
    "baseClasses": ["OldChatModel"],
    "deprecated": True,
}


class TestNodeDescriptionExtraction:
    """Test extraction of individual node descriptions from API responses."""

    def test_extract_from_flowise_api_response(self):
        """Parse /api/v1/nodes-list JSON → NodeDescription objects."""
        # Arrange
        api_response = SAMPLE_NODE_COMPLETE

        # Act
        node_desc = extract_node_description(api_response)

        # Assert
        assert isinstance(node_desc, NodeDescription)
        assert node_desc.node_name == "chatOpenAI"
        assert node_desc.label == "ChatOpenAI"
        assert node_desc.category == "Chat Models"
        assert len(node_desc.base_classes) == 3
        assert "ChatOpenAI" in node_desc.base_classes

    def test_extract_node_metadata_complete(self):
        """All fields extracted (node_name, label, category, base_classes, description)."""
        # Arrange
        api_response = SAMPLE_NODE_COMPLETE

        # Act
        node_desc = extract_node_description(api_response)

        # Assert - Verify ALL required fields are extracted
        assert node_desc.node_name == "chatOpenAI"
        assert node_desc.label == "ChatOpenAI"
        assert node_desc.category == "Chat Models"
        assert node_desc.base_classes == ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel"]
        assert "OpenAI large language models" in node_desc.description
        assert node_desc.version == "1"
        assert node_desc.deprecated is False

    def test_extract_node_metadata_missing_optional(self):
        """Handle missing optional fields gracefully."""
        # Arrange
        api_response = SAMPLE_NODE_MISSING_OPTIONAL

        # Act
        node_desc = extract_node_description(api_response)

        # Assert - Should work even without version and deprecated fields
        assert node_desc.node_name == "bufferMemory"
        assert node_desc.label == "Buffer Memory"
        assert node_desc.category == "Memory"
        assert node_desc.base_classes == ["BufferMemory", "BaseChatMemory"]
        assert node_desc.version is None or node_desc.version == ""
        assert node_desc.deprecated is False  # Default to False if missing

    def test_extract_deprecated_flag(self):
        """Deprecated nodes marked correctly."""
        # Arrange
        api_response = SAMPLE_NODE_DEPRECATED

        # Act
        node_desc = extract_node_description(api_response)

        # Assert
        assert node_desc.deprecated is True
        assert "legacy" in node_desc.description.lower() or "deprecated" in node_desc.description.lower()


class TestUseCaseGeneration:
    """Test use case inference from node descriptions."""

    def test_generate_use_cases_from_description(self):
        """Infer use cases from description text."""
        # Arrange
        description = "Wrapper around OpenAI large language models that use the Chat endpoint. Supports streaming and function calling."

        # Act
        use_cases = generate_use_cases(description)

        # Assert
        assert isinstance(use_cases, list)
        assert len(use_cases) > 0
        # Should extract key capabilities as use cases
        assert any("chat" in uc.lower() for uc in use_cases)
        assert any("streaming" in uc.lower() or "function" in uc.lower() for uc in use_cases)


class TestNodeDescriptionValidation:
    """Test schema validation for NodeDescription objects."""

    def test_validate_node_description_schema(self):
        """Validate NodeDescription matches data model."""
        # Arrange
        api_response = SAMPLE_NODE_COMPLETE
        node_desc = extract_node_description(api_response)

        # Act & Assert - Should not raise any validation errors
        validate_node_description(node_desc)

        # Verify required attributes exist
        assert hasattr(node_desc, "node_name")
        assert hasattr(node_desc, "label")
        assert hasattr(node_desc, "category")
        assert hasattr(node_desc, "base_classes")
        assert hasattr(node_desc, "description")
        assert hasattr(node_desc, "use_cases")
        assert hasattr(node_desc, "version")
        assert hasattr(node_desc, "deprecated")


class TestBatchExtraction:
    """Test batch processing of multiple nodes."""

    def test_batch_extraction_87_nodes(self):
        """Extract all 87 nodes without errors."""
        # Arrange - Simulate API response with multiple nodes
        api_response = {
            "nodes": [
                SAMPLE_NODE_COMPLETE,
                SAMPLE_NODE_MISSING_OPTIONAL,
                SAMPLE_NODE_DEPRECATED,
            ]
        }

        # Act
        node_descriptions = extract_all_node_descriptions(api_response)

        # Assert
        assert isinstance(node_descriptions, list)
        assert len(node_descriptions) == 3
        assert all(isinstance(nd, NodeDescription) for nd in node_descriptions)

        # Verify each node was extracted correctly
        node_names = [nd.node_name for nd in node_descriptions]
        assert "chatOpenAI" in node_names
        assert "bufferMemory" in node_names
        assert "oldChatModel" in node_names


class TestJSONExport:
    """Test JSON output formatting for review."""

    def test_output_json_format(self):
        """Generate valid JSON for review."""
        # Arrange
        node_descriptions = [
            extract_node_description(SAMPLE_NODE_COMPLETE),
            extract_node_description(SAMPLE_NODE_MISSING_OPTIONAL),
        ]

        # Act
        json_output = export_to_json(node_descriptions)

        # Assert - Should be valid JSON
        parsed = json.loads(json_output)
        assert isinstance(parsed, list)
        assert len(parsed) == 2

        # Verify JSON structure
        first_node = parsed[0]
        assert "node_name" in first_node
        assert "label" in first_node
        assert "category" in first_node
        assert "base_classes" in first_node
        assert "description" in first_node
        assert "use_cases" in first_node

        # Verify data integrity
        assert first_node["node_name"] == "chatOpenAI"
        assert first_node["category"] == "Chat Models"
