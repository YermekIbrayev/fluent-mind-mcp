"""Shared fixtures for Phase 1 integration tests.

Provides common fixtures for integration testing of Phase 1 features.

WHY: pytest's conftest.py provides auto-discovered fixtures available to all
integration tests in the directory, following DRY principle.
"""

import pytest


@pytest.fixture
def mock_vector_db_client():
    """Create mock VectorDatabaseClient for testing.

    WHY: Integration tests need isolated vector DB without actual ChromaDB.
    """
    from unittest.mock import AsyncMock, MagicMock

    mock_client = MagicMock()
    mock_client.search_nodes = AsyncMock(return_value=[])
    mock_client.search_templates = AsyncMock(return_value=[])

    # Mock get_collection().get() chain for template retrieval
    mock_collection = MagicMock()
    mock_collection.get.return_value = {
        "ids": ["tmpl_simple_chat"],
        "metadatas": [{"name": "Simple Chat"}],
        "documents": []
    }
    mock_client.get_collection.return_value = mock_collection

    return mock_client


@pytest.fixture
def mock_flowise_client():
    """Create mock Flowise client for testing.

    WHY: Integration tests need isolated Flowise client without actual instance.
    """
    from unittest.mock import AsyncMock, MagicMock

    mock_client = MagicMock()
    mock_client.create_chatflow = AsyncMock(return_value={"id": "test-id", "name": "Test"})
    mock_client.get_chatflow = AsyncMock(return_value=None)
    mock_client.update_chatflow = AsyncMock(return_value=True)
    return mock_client
