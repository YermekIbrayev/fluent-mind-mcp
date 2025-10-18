"""Shared fixtures for Phase 1 unit tests.

Centralizes common test fixtures to eliminate duplication.

WHY: pytest's conftest.py provides auto-discovered fixtures available to all
tests in the directory, following DRY principle and improving maintainability.
"""

import pytest

from tests.unit.phase1.test_builders import NodeBuilder


@pytest.fixture
async def build_flow_service(mock_vector_db_client):
    """Create BuildFlowService instance for testing.

    WHY: Provides isolated service instance with test dependencies.
    Shared across all Phase 1 tests to ensure consistency.
    """
    from fluent_mind_mcp.services.build_flow_service import BuildFlowService

    service = BuildFlowService(vector_db_client=mock_vector_db_client)
    return service


@pytest.fixture
def mock_vector_db_client():
    """Create mock VectorDatabaseClient for testing.

    WHY: BuildFlowService requires vector_db_client dependency.
    Mock enables testing without actual ChromaDB instance.
    """
    from unittest.mock import AsyncMock, MagicMock

    mock_client = MagicMock()
    # Add async methods that will be called
    mock_client.search_nodes = AsyncMock(return_value=[])
    mock_client.search_templates = AsyncMock(return_value=[])

    # Mock get_collection().get() chain for template retrieval
    mock_collection = MagicMock()

    def mock_get_side_effect(ids=None, where=None):
        """Smart mock that returns data for valid IDs, empty for invalid ones."""
        if ids:
            # Template lookup by ID
            if ids[0] in ["tmpl_simple_chat", "tmpl_chat", "tmpl_123"]:
                return {
                    "ids": [ids[0]],
                    "metadatas": [{"name": "Simple Chat Template"}],
                    "documents": []
                }
            else:
                # Invalid template ID
                return {"ids": [], "metadatas": [], "documents": []}
        elif where:
            # Node lookup by name
            node_name = where.get("name") if isinstance(where, dict) else None
            if node_name in ["chatOpenAI", "bufferMemory", "documentLoader", "conversationChain"]:
                return {
                    "ids": [f"node_{node_name}"],
                    "metadatas": [{"name": node_name}],
                    "documents": []
                }
            else:
                # Invalid node name
                return {"ids": [], "metadatas": [], "documents": []}
        return {"ids": [], "metadatas": [], "documents": []}

    mock_collection.get.side_effect = mock_get_side_effect
    mock_client.get_collection.return_value = mock_collection

    return mock_client


@pytest.fixture
def mock_flowise_client():
    """Create mock Flowise client for testing.

    WHY: BuildFlowService may use flowise_client for chatflow operations.
    Mock enables testing without actual Flowise instance.
    """
    from unittest.mock import AsyncMock, MagicMock

    mock_client = MagicMock()
    # Add async methods that might be called
    mock_client.create_chatflow = AsyncMock(return_value={"id": "test-id", "name": "Test"})
    mock_client.get_chatflow = AsyncMock(return_value=None)
    mock_client.update_chatflow = AsyncMock(return_value=True)
    return mock_client


@pytest.fixture
def chat_openai_node():
    """Create a standard ChatOpenAI node for testing.

    WHY: Commonly used in tests, eliminates duplicate node definitions.
    """
    return (NodeBuilder()
            .with_id("1")
            .with_name("chatOpenAI")
            .with_base_classes(["BaseChatModel", "BaseLanguageModel"])
            .with_outputs(["BaseChatModel"])
            .build())


@pytest.fixture
def buffer_memory_node():
    """Create a standard BufferMemory node for testing.

    WHY: Memory nodes frequently used in connection inference tests.
    """
    return (NodeBuilder()
            .with_id("2")
            .with_name("bufferMemory")
            .with_base_classes(["BaseMemory"])
            .build())


@pytest.fixture
def document_loader_node():
    """Create a standard DocumentLoader node for testing.

    WHY: Input nodes frequently used in flow construction tests.
    """
    return (NodeBuilder()
            .with_id("doc_loader_1")
            .with_name("documentLoader")
            .with_base_classes(["BaseLoader", "Document"])
            .build())


@pytest.fixture
def conversation_chain_node():
    """Create a standard ConversationChain node for testing.

    WHY: Output nodes frequently used in connection inference tests.
    """
    return (NodeBuilder()
            .with_id("conv_chain_1")
            .with_name("conversationChain")
            .with_base_classes(["BaseChain"])
            .with_inputs(["BaseChatModel"])
            .build())


@pytest.fixture
def agent_node():
    """Create a standard Agent node for testing validation.

    WHY: Agents have strict input requirements, useful for validation tests.
    """
    return (NodeBuilder()
            .with_id("1")
            .with_name("agent")
            .with_base_classes(["BaseAgent"])
            .with_inputs(["BaseChatModel"])
            .with_required_inputs(["BaseChatModel"])
            .build())
