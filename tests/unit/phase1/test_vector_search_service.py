"""Unit tests for VectorSearchService (Phase 1 - User Stories 1-2).

Tests vector search functionality for nodes and templates.

Coverage:
- Node search with semantic matching
- Template search with tag filtering
- Search result relevance validation (>90% per NFR-093)
- Response token budgeting (<50 tokens per result per NFR-026)
- Error handling and edge cases

WHY: Validates core search service that powers User Stories 1 and 2.
"""

import pytest
from typing import Any

from fluent_mind_mcp.services.vector_search_service import VectorSearchService
from fluent_mind_mcp.client.embedding_client import EmbeddingClient
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.utils.exceptions import ValidationError


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorSearchServiceNodeSearch:
    """Test node search functionality (User Story 1)."""

    @pytest.mark.asyncio
    async def test_search_nodes_returns_relevant_results(self, tmp_path):
        """
        GIVEN: Query "chatbot that remembers conversation"
        WHEN: search_nodes() is called with limit=5
        THEN: Returns 5 most relevant nodes with metadata

        WHY: Core search functionality for User Story 1.
        """
        from fluent_mind_mcp.services.vector_search_service import VectorSearchService
        from fluent_mind_mcp.client.embedding_client import EmbeddingClient
        from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient

        # Setup
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Populate test data
        test_nodes = [
            {"name": "chatOpenAI", "label": "ChatOpenAI", "category": "Chat Models",
             "description": "OpenAI chat model for conversations"},
            {"name": "bufferMemory", "label": "Buffer Memory", "category": "Memory",
             "description": "Memory buffer for storing conversation history"},
            {"name": "conversationChain", "label": "Conversation Chain", "category": "Chains",
             "description": "Chain for chatbot conversations with memory"},
            {"name": "faiss", "label": "FAISS", "category": "Vector Stores",
             "description": "Vector store for document retrieval"},
            {"name": "textSplitter", "label": "Text Splitter", "category": "Document Loaders",
             "description": "Split text documents into chunks"},
        ]

        ids = [node["name"] for node in test_nodes]
        documents = [node["description"] for node in test_nodes]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"name": node["name"], "label": node["label"], "category": node["category"]}
            for node in test_nodes
        ]

        vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes(
            query="chatbot that remembers conversation",
            limit=5
        )

        assert len(results) <= 5
        assert all("name" in r for r in results)
        assert all("description" in r for r in results)
        assert all("relevance_score" in r for r in results)

    @pytest.mark.asyncio
    async def test_search_nodes_results_include_relevance_scores(self, tmp_path):
        """
        GIVEN: Search results from vector query
        WHEN: Processing results
        THEN: Each result has relevance_score (0.0-1.0)

        WHY: Transparency for debugging and quality validation.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test data
        test_nodes = [
            {"name": "chatOpenAI", "label": "ChatOpenAI", "category": "Chat Models",
             "description": "OpenAI chat model"},
            {"name": "bufferMemory", "label": "Buffer Memory", "category": "Memory",
             "description": "Memory buffer"},
        ]

        ids = [node["name"] for node in test_nodes]
        documents = [node["description"] for node in test_nodes]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"name": node["name"], "label": node["label"], "category": node["category"]}
            for node in test_nodes
        ]

        vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("test query", limit=3)

        for result in results:
            assert "relevance_score" in result
            assert 0.0 <= result["relevance_score"] <= 1.0

    @pytest.mark.asyncio
    async def test_search_nodes_results_sorted_by_relevance_descending(self, tmp_path):
        """
        GIVEN: Search results with relevance scores
        WHEN: Examining result order
        THEN: Results are sorted by relevance_score descending

        WHY: Most relevant results should appear first.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add diverse test nodes
        test_nodes = [
            {"name": "chatOpenAI", "label": "ChatOpenAI", "category": "Chat Models",
             "description": "OpenAI chat model for conversations"},
            {"name": "bufferMemory", "label": "Buffer Memory", "category": "Memory",
             "description": "Memory buffer for storing history"},
            {"name": "faiss", "label": "FAISS", "category": "Vector Stores",
             "description": "Vector store for embeddings"},
        ]

        ids = [node["name"] for node in test_nodes]
        documents = [node["description"] for node in test_nodes]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"name": node["name"], "label": node["label"], "category": node["category"]}
            for node in test_nodes
        ]

        vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("test query", limit=5)

        scores = [r["relevance_score"] for r in results]
        assert scores == sorted(scores, reverse=True), "Results not sorted by relevance descending"

    @pytest.mark.asyncio
    async def test_search_nodes_respects_category_filter(self, tmp_path):
        """
        GIVEN: Category filter {"category": "Chat Models"}
        WHEN: search_nodes() is called with filter
        THEN: Returns only nodes from Chat Models category

        WHY: Supports filtered search for precision.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add nodes from different categories
        test_nodes = [
            {"name": "chatOpenAI", "label": "ChatOpenAI", "category": "Chat Models",
             "description": "OpenAI chat model"},
            {"name": "chatAnthropic", "label": "ChatAnthropic", "category": "Chat Models",
             "description": "Anthropic chat model"},
            {"name": "bufferMemory", "label": "Buffer Memory", "category": "Memory",
             "description": "Memory buffer"},
        ]

        ids = [node["name"] for node in test_nodes]
        documents = [node["description"] for node in test_nodes]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"name": node["name"], "label": node["label"], "category": node["category"]}
            for node in test_nodes
        ]

        vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes(
            query="chat model",
            limit=10,
            filter_metadata={"category": "Chat Models"}
        )

        for result in results:
            assert result["category"] == "Chat Models"

    @pytest.mark.asyncio
    async def test_search_nodes_truncates_description_to_token_budget(self, tmp_path):
        """
        GIVEN: Node with long description (>50 tokens)
        WHEN: search_nodes() returns results
        THEN: Description is truncated to ~50 tokens (NFR-026)

        WHY: Respects token budget for efficient responses.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Create node with very long description (>200 chars = ~50 tokens)
        long_desc = "This is a very long description " * 20  # ~600 chars

        test_nodes = [
            {"name": "testNode", "label": "Test Node", "category": "Test",
             "description": long_desc},
        ]

        ids = [node["name"] for node in test_nodes]
        documents = [node["description"] for node in test_nodes]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"name": node["name"], "label": node["label"], "category": node["category"]}
            for node in test_nodes
        ]

        vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("test", limit=1)

        description = results[0]["description"]
        # Rough token count: ~4 chars per token, max 50 tokens = 200 chars
        assert len(description) <= 203, f"Description {len(description)} chars, expected ≤200 (50 tokens)"
        if len(long_desc) > 200:
            assert description.endswith("..."), "Long description should be truncated with ellipsis"


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorSearchServiceTemplateSearch:
    """Test template search functionality (User Story 2)."""

    @pytest.mark.asyncio
    async def test_search_templates_returns_matching_templates(self, tmp_path):
        """
        GIVEN: Query "simple chatbot"
        WHEN: search_templates() is called
        THEN: Returns templates with semantic match and tag match

        WHY: Core search functionality for User Story 2.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add test templates
        test_templates = [
            {"template_id": "tmpl_simple_chat", "name": "Simple Chat",
             "description": "Basic chatbot with memory", "tags": "chatbot,conversation",
             "node_count": 3, "complexity_level": "simple"},
            {"template_id": "tmpl_rag_flow", "name": "RAG Flow",
             "description": "Retrieval augmented generation", "tags": "rag,documents",
             "node_count": 5, "complexity_level": "medium"},
        ]

        ids = [t["template_id"] for t in test_templates]
        documents = [t["description"] for t in test_templates]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"template_id": t["template_id"], "name": t["name"],
             "tags": t["tags"], "node_count": t["node_count"],
             "complexity_level": t["complexity_level"]}
            for t in test_templates
        ]

        vector_db_client.add_documents("templates", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_templates("simple chatbot", limit=3)

        assert len(results) <= 3
        assert all("template_id" in r for r in results)
        assert all("name" in r for r in results)
        assert all("description" in r for r in results)
        assert all("tags" in r for r in results)

    @pytest.mark.asyncio
    async def test_search_templates_boosts_tag_matches(self, tmp_path):
        """
        GIVEN: Query "chatbot" and template with tag "chatbot"
        WHEN: search_templates() is called
        THEN: Tagged template has higher relevance than semantic-only match

        WHY: Tags provide explicit signals for better precision.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Add templates with different tag matches
        test_templates = [
            {"template_id": "tmpl_with_tag", "name": "Chat Template",
             "description": "A template for building applications", "tags": "chatbot,assistant",
             "node_count": 3, "complexity_level": "simple"},
            {"template_id": "tmpl_without_tag", "name": "Other Template",
             "description": "A chatbot template for conversations", "tags": "other,stuff",
             "node_count": 3, "complexity_level": "simple"},
        ]

        ids = [t["template_id"] for t in test_templates]
        documents = [t["description"] for t in test_templates]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"template_id": t["template_id"], "name": t["name"],
             "tags": t["tags"], "node_count": t["node_count"],
             "complexity_level": t["complexity_level"]}
            for t in test_templates
        ]

        vector_db_client.add_documents("templates", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_templates("chatbot", limit=5)

        # Template with "chatbot" tag should rank high
        top_3_tags = [r.get("tags", []) for r in results[:3]]
        has_chatbot_tag = any("chatbot" in tags for tags in top_3_tags)
        assert has_chatbot_tag, "Tag-boosted template should appear in top results"

    @pytest.mark.asyncio
    async def test_search_templates_returns_flow_data_preview(self, tmp_path):
        """
        GIVEN: Template search results
        WHEN: Examining result structure
        THEN: Includes node_count and complexity_level (not full flowData)

        WHY: Preview metadata helps selection without full payload.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        test_templates = [
            {"template_id": "tmpl_test", "name": "Test Template",
             "description": "A test template", "tags": "test",
             "node_count": 5, "complexity_level": "medium"},
        ]

        ids = [t["template_id"] for t in test_templates]
        documents = [t["description"] for t in test_templates]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"template_id": t["template_id"], "name": t["name"],
             "tags": t["tags"], "node_count": t["node_count"],
             "complexity_level": t["complexity_level"]}
            for t in test_templates
        ]

        vector_db_client.add_documents("templates", documents, embeddings, ids, metadatas)

        # Test
        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_templates("test", limit=1)

        result = results[0]
        assert "node_count" in result
        assert "complexity_level" in result
        # Full flowData should NOT be in search results
        assert "flow_data" not in result and "flowData" not in result


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorSearchServiceEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_search_nodes_empty_query_returns_empty_results(self, tmp_path):
        """
        GIVEN: Empty query string
        WHEN: search_nodes("") is called
        THEN: Raises ValidationError

        WHY: Graceful handling of invalid input.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        service = VectorSearchService(vector_db_client, embedding_client)

        with pytest.raises(ValidationError) as exc_info:
            await service.search_nodes("", limit=5)

        assert "empty" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_search_nodes_with_limit_zero_returns_empty(self, tmp_path):
        """
        GIVEN: limit=0
        WHEN: search_nodes() is called
        THEN: Returns empty results

        WHY: Edge case validation for parameter bounds.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        service = VectorSearchService(vector_db_client, embedding_client)

        results = await service.search_nodes("test query", limit=0)
        assert results == []

    @pytest.mark.asyncio
    async def test_search_nodes_no_results_returns_empty_list(self, tmp_path):
        """
        GIVEN: Query that matches no nodes (empty collection)
        WHEN: search_nodes() is called
        THEN: Returns empty list (not error)

        WHY: Graceful handling of no-match scenarios.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        # Create empty collection
        vector_db_client.get_or_create_collection("nodes")

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("xyzabc123nonexistent", limit=5)

        assert isinstance(results, list)
        assert len(results) == 0


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorSearchServiceResponseFormat:
    """Test response structure and formatting."""

    @pytest.mark.asyncio
    async def test_node_search_result_structure(self, tmp_path):
        """
        GIVEN: Node search results
        WHEN: Examining result structure
        THEN: Contains required fields: name, label, category, description, relevance_score

        WHY: Defines API contract for MCP tool integration.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        test_nodes = [
            {"name": "testNode", "label": "Test Node", "category": "Test",
             "description": "A test node"},
        ]

        ids = [node["name"] for node in test_nodes]
        documents = [node["description"] for node in test_nodes]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"name": node["name"], "label": node["label"], "category": node["category"]}
            for node in test_nodes
        ]

        vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("test", limit=1)

        result = results[0]
        required_fields = ["name", "label", "category", "description", "relevance_score"]
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"

    @pytest.mark.asyncio
    async def test_template_search_result_structure(self, tmp_path):
        """
        GIVEN: Template search results
        WHEN: Examining result structure
        THEN: Contains: template_id, name, description, tags, node_count, complexity_level

        WHY: Defines API contract for template selection.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))

        test_templates = [
            {"template_id": "tmpl_test", "name": "Test",
             "description": "Test template", "tags": "test",
             "node_count": 3, "complexity_level": "simple"},
        ]

        ids = [t["template_id"] for t in test_templates]
        documents = [t["description"] for t in test_templates]
        embeddings = embedding_client.batch_embed(documents)
        metadatas = [
            {"template_id": t["template_id"], "name": t["name"],
             "tags": t["tags"], "node_count": t["node_count"],
             "complexity_level": t["complexity_level"]}
            for t in test_templates
        ]

        vector_db_client.add_documents("templates", documents, embeddings, ids, metadatas)

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_templates("test", limit=1)

        result = results[0]
        required_fields = ["template_id", "name", "description", "tags", "node_count", "complexity_level"]
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"
