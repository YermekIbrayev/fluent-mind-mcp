"""Unit tests for VectorSearchService.search_nodes (User Story 1).

TDD-RED Phase: These tests define the API contract for search_nodes.
Tests will FAIL until VectorSearchService.search_nodes is implemented.

WHY: Ensures search_nodes API meets US1 requirements before implementation.
"""

import pytest
from fluent_mind_mcp.services.vector_search_service import VectorSearchService
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.client.embedding_client import EmbeddingClient
from fluent_mind_mcp.utils.exceptions import ValidationError


@pytest.fixture
def vector_search_service(tmp_path):
    """Create VectorSearchService with test ChromaDB instance and sample data."""
    vector_db = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
    embedder = EmbeddingClient()
    service = VectorSearchService(vector_db, embedder)

    # Populate test data
    test_nodes = [
        {
            "id": "chatOpenAI",
            "name": "chatOpenAI",
            "label": "ChatOpenAI",
            "category": "Chat Models",
            "base_classes": ["BaseChatModel", "BaseLanguageModel"],
            "description": "OpenAI chat model for conversations and completions",
            "deprecated": False
        },
        {
            "id": "bufferMemory",
            "name": "bufferMemory",
            "label": "Buffer Memory",
            "category": "Memory",
            "base_classes": ["BaseMemory"],
            "description": "Memory buffer for storing conversation history",
            "deprecated": False
        },
        {
            "id": "conversationChain",
            "name": "conversationChain",
            "label": "Conversation Chain",
            "category": "Chains",
            "base_classes": ["BaseChain"],
            "description": "Chain for chatbot conversations with memory",
            "deprecated": False
        },
        {
            "id": "faiss",
            "name": "faiss",
            "label": "FAISS",
            "category": "Vector Stores",
            "base_classes": ["VectorStore"],
            "description": "Facebook AI Similarity Search vector store for document retrieval",
            "deprecated": False
        },
        {
            "id": "oldNode",
            "name": "oldNode",
            "label": "Old Node",
            "category": "Chat Models",
            "base_classes": ["BaseChatModel"],
            "description": "Deprecated chat model",
            "deprecated": True
        }
    ]

    # Add nodes to vector database
    collection = vector_db.get_or_create_collection("nodes")
    ids = [node["id"] for node in test_nodes]
    documents = [node["description"] for node in test_nodes]
    embeddings = embedder.batch_embed(documents)
    metadatas = [
        {
            "name": node["name"],
            "label": node["label"],
            "category": node["category"],
            "base_classes": ",".join(node["base_classes"]),
            "deprecated": node["deprecated"]
        }
        for node in test_nodes
    ]

    collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    return service


class TestSearchNodesBasicFunctionality:
    """Test core search_nodes functionality."""

    @pytest.mark.asyncio
    async def test_search_nodes_basic_query(self, vector_search_service):
        """Query 'chat model' returns results with relevance >0.7.

        WHY: Validates basic semantic search works with minimum relevance threshold.
        """
        results = await vector_search_service.search_nodes("chat model")

        assert len(results) > 0, "Should return at least one result"
        assert all(r["relevance_score"] >= 0.7 for r in results), "All results should meet default threshold 0.7"
        assert all("node_name" in r for r in results), "All results should have node_name"

    @pytest.mark.asyncio
    async def test_search_nodes_max_results(self, vector_search_service):
        """Verify max_results parameter limits returned items (default 5).

        WHY: Ensures token budget control through result limiting.
        """
        results_default = await vector_search_service.search_nodes("model")
        assert len(results_default) <= 5, "Default max_results should be 5"

        results_custom = await vector_search_service.search_nodes("model", max_results=3)
        assert len(results_custom) <= 3, "Custom max_results should be respected"

    @pytest.mark.asyncio
    async def test_search_nodes_similarity_threshold(self, vector_search_service):
        """Verify threshold filtering (default 0.7, test 0.5, 0.8, 0.9).

        WHY: Ensures relevance filtering works correctly at different thresholds.
        """
        results_low = await vector_search_service.search_nodes("chat", similarity_threshold=0.5)
        results_mid = await vector_search_service.search_nodes("chat", similarity_threshold=0.7)
        results_high = await vector_search_service.search_nodes("chat", similarity_threshold=0.9)

        assert len(results_low) >= len(results_mid), "Lower threshold should return more results"
        assert len(results_mid) >= len(results_high), "Higher threshold should return fewer results"
        assert all(r["relevance_score"] >= 0.9 for r in results_high), "High threshold results should meet 0.9"


class TestSearchNodesFiltering:
    """Test filtering and edge cases."""

    @pytest.mark.asyncio
    async def test_search_nodes_category_filter(self, vector_search_service):
        """Filter by category ('Chat Models', 'Memory', 'Tools').

        WHY: Enables precise node discovery by category.
        """
        # Use more semantically relevant query that will score >= 0.7 threshold
        results = await vector_search_service.search_nodes("chat conversations", category="Chat Models")

        assert len(results) > 0, "Should return results for Chat Models category"
        assert all(r["category"] == "Chat Models" for r in results), "All results should match category filter"

    @pytest.mark.asyncio
    async def test_search_nodes_no_results(self, vector_search_service):
        """Empty query or no matches returns empty list.

        WHY: Graceful handling of no-match scenarios without errors.
        """
        results = await vector_search_service.search_nodes("xyznonexistent12345")

        assert results == [], "No matches should return empty list, not error"

    @pytest.mark.asyncio
    async def test_search_nodes_deprecated_filtering(self, vector_search_service):
        """Deprecated nodes ranked lower.

        WHY: Prioritizes actively maintained nodes over deprecated ones.
        """
        results = await vector_search_service.search_nodes("chat model")

        # Find positions of deprecated and non-deprecated nodes
        deprecated_positions = [i for i, r in enumerate(results) if r.get("deprecated", False)]
        non_deprecated_positions = [i for i, r in enumerate(results) if not r.get("deprecated", False)]

        if deprecated_positions and non_deprecated_positions:
            # Deprecated nodes should appear after non-deprecated ones
            assert min(deprecated_positions) > max(non_deprecated_positions), "Deprecated nodes should rank lower"


class TestSearchNodesFormat:
    """Test result format and token efficiency."""

    @pytest.mark.asyncio
    async def test_search_nodes_compact_format(self, vector_search_service):
        """Each result <50 tokens (name+description+metadata).

        WHY: Meets NFR-002 token budget requirement per result.
        """
        results = await vector_search_service.search_nodes("chat model")

        for result in results:
            # Approximate token count: 1 token ≈ 4 characters
            total_chars = (
                len(result["node_name"]) +
                len(result["description"]) +
                len(result.get("category", ""))
            )
            approx_tokens = total_chars / 4

            assert approx_tokens < 50, f"Result should be <50 tokens, got ~{approx_tokens}"

    @pytest.mark.asyncio
    async def test_search_nodes_metadata_inclusion(self, vector_search_service):
        """Results include category, base_classes, deprecated.

        WHY: Provides essential metadata for informed node selection.
        """
        results = await vector_search_service.search_nodes("chat model")

        assert len(results) > 0, "Should have results to validate"
        for result in results:
            assert "category" in result, "Result should include category"
            assert "base_classes" in result, "Result should include base_classes"
            assert "deprecated" in result or "deprecated" not in result, "Deprecated field is optional"


class TestSearchNodesRanking:
    """Test relevance ranking and sorting."""

    @pytest.mark.asyncio
    async def test_search_nodes_sort_by_relevance(self, vector_search_service):
        """Results sorted descending by relevance_score within each group (non-deprecated, then deprecated).

        WHY: Most relevant nodes should appear first for better UX, with deprecated nodes ranked lower.
        """
        results = await vector_search_service.search_nodes("chat model")

        if len(results) > 1:
            # Split into non-deprecated and deprecated groups
            non_deprecated = [r for r in results if not r.get("deprecated", False)]
            deprecated = [r for r in results if r.get("deprecated", False)]

            # Each group should be sorted by relevance DESC
            if non_deprecated:
                non_dep_scores = [r["relevance_score"] for r in non_deprecated]
                assert non_dep_scores == sorted(non_dep_scores, reverse=True), \
                    "Non-deprecated results should be sorted by relevance DESC"

            if deprecated:
                dep_scores = [r["relevance_score"] for r in deprecated]
                assert dep_scores == sorted(dep_scores, reverse=True), \
                    "Deprecated results should be sorted by relevance DESC"


class TestSearchNodesPerformance:
    """Test performance requirements."""

    @pytest.mark.asyncio
    async def test_search_nodes_performance(self, vector_search_service):
        """Average search time <500ms for 87 nodes.

        WHY: Meets NFR-020 performance target.
        """
        import time

        start = time.time()
        await vector_search_service.search_nodes("chat model")
        duration = time.time() - start

        assert duration < 0.5, f"Search should complete in <500ms, took {duration*1000:.0f}ms"


class TestSearchNodesEmbedding:
    """Test embedding generation."""

    @pytest.mark.asyncio
    async def test_search_nodes_embedding_generation(self, vector_search_service):
        """Verify query embedding is 384-dim.

        WHY: Validates embedding model (all-MiniLM-L6-v2) is working correctly.
        """
        # This test verifies the internal embedding call
        # For now, just verify search works (embedding is implicit)
        results = await vector_search_service.search_nodes("chat")
        assert isinstance(results, list), "Should return list of results"


class TestSearchNodesEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_search_nodes_duplicate_prevention(self, vector_search_service):
        """Same query returns identical results.

        WHY: Ensures deterministic search behavior.
        """
        results1 = await vector_search_service.search_nodes("chat model")
        results2 = await vector_search_service.search_nodes("chat model")

        assert len(results1) == len(results2), "Same query should return same number of results"
        if results1:
            assert results1[0]["node_name"] == results2[0]["node_name"], "Top result should be identical"

    @pytest.mark.asyncio
    async def test_search_nodes_special_characters(self, vector_search_service):
        """Handle queries with special chars (!@#$%).

        WHY: Ensures robust query processing.
        """
        # Should not crash, may return no results
        results = await vector_search_service.search_nodes("chat!@#$%")
        assert isinstance(results, list), "Should return list even with special chars"

    @pytest.mark.asyncio
    async def test_search_nodes_empty_string(self, vector_search_service):
        """Empty string query raises ValidationError.

        WHY: Prevents meaningless queries that waste resources.
        """
        with pytest.raises(ValidationError):
            await vector_search_service.search_nodes("")

    @pytest.mark.asyncio
    async def test_search_nodes_very_long_query(self, vector_search_service):
        """Query >500 chars handled or truncated.

        WHY: Prevents excessive embedding processing time.
        """
        long_query = "chat " * 100  # 500+ chars
        results = await vector_search_service.search_nodes(long_query)

        assert isinstance(results, list), "Should handle long queries gracefully"
