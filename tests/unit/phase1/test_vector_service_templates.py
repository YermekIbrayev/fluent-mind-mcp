"""Unit tests for VectorSearchService.search_templates (User Story 2).

TDD-RED Phase: These tests define the API contract for search_templates.
Tests will FAIL until VectorSearchService.search_templates is implemented.

WHY: Ensures search_templates API meets US2 requirements before implementation.
"""

import pytest
from fluent_mind_mcp.services.vector_search_service import VectorSearchService
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.client.embedding_client import EmbeddingClient
from fluent_mind_mcp.utils.exceptions import ValidationError


@pytest.fixture
def vector_search_service_with_templates(tmp_path):
    """Create VectorSearchService with test ChromaDB instance and sample templates."""
    vector_db = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
    embedder = EmbeddingClient()
    service = VectorSearchService(vector_db, embedder)

    # Populate test templates
    test_templates = [
        {
            "id": "tmpl_simple_chat",
            "template_id": "tmpl_simple_chat",
            "name": "Simple Chatbot",
            "description": "Basic conversational chatbot with memory for simple Q&A interactions",
            "tags": "chatbot,conversation,simple",
            "node_count": 3,
            "complexity_level": "simple",
            "required_nodes": ["chatOpenAI", "bufferMemory", "conversationChain"]
        },
        {
            "id": "tmpl_rag_chatbot",
            "template_id": "tmpl_rag_chatbot",
            "name": "RAG Chatbot",
            "description": "Retrieval-augmented generation chatbot for knowledge base Q&A with document search capabilities",
            "tags": "chatbot,rag,knowledge,support",
            "node_count": 7,
            "complexity_level": "intermediate",
            "required_nodes": ["chatOpenAI", "documentLoader", "openAIEmbeddings", "faiss", "conversationalRetrievalQAChain", "bufferMemory"],
            "parameters_schema": {
                "properties": {
                    "chunk_size": {"type": "integer", "default": 1000},
                    "chunk_overlap": {"type": "integer", "default": 200}
                }
            }
        },
        {
            "id": "tmpl_support_agent",
            "template_id": "tmpl_support_agent",
            "name": "Customer Support Agent",
            "description": "Customer support chatbot with knowledge base and escalation capabilities for handling support tickets",
            "tags": "support,agent,customer,knowledge",
            "node_count": 8,
            "complexity_level": "intermediate",
            "required_nodes": ["chatOpenAI", "documentLoader", "openAIEmbeddings", "faiss", "toolAgent", "bufferMemory"]
        },
        {
            "id": "tmpl_data_analysis",
            "template_id": "tmpl_data_analysis",
            "name": "Data Analysis Agent",
            "description": "Agent for data analysis with tools for processing and visualizing data from various sources",
            "tags": "agent,data,analysis,tools",
            "node_count": 6,
            "complexity_level": "advanced",
            "required_nodes": ["chatOpenAI", "toolAgent", "csvFile", "bufferMemory"]
        },
        {
            "id": "tmpl_research_agent",
            "template_id": "tmpl_research_agent",
            "name": "Research Agent",
            "description": "Research agent with web scraping and summarization tools for comprehensive information gathering",
            "tags": "agent,research,tools,web",
            "node_count": 9,
            "complexity_level": "advanced",
            "required_nodes": ["chatOpenAI", "reactAgentLLM", "cheerioWebScraper", "bufferMemory"],
            "parameters_schema": {
                "properties": {
                    "max_iterations": {"type": "integer", "default": 5},
                    "scraper_timeout": {"type": "integer", "default": 30}
                }
            }
        }
    ]

    # Add templates to vector database
    collection = vector_db.get_or_create_collection("templates")
    ids = [tmpl["id"] for tmpl in test_templates]
    documents = [tmpl["description"] for tmpl in test_templates]
    embeddings = embedder.batch_embed(documents)

    # Convert required_nodes list to JSON string for ChromaDB storage
    import json
    metadatas = []
    for tmpl in test_templates:
        metadata = {
            "template_id": tmpl["template_id"],
            "name": tmpl["name"],
            "tags": tmpl["tags"],
            "node_count": tmpl["node_count"],
            "complexity_level": tmpl["complexity_level"],
            "required_nodes": json.dumps(tmpl["required_nodes"])  # Store as JSON string
        }
        # Add parameters_schema if present
        if "parameters_schema" in tmpl:
            metadata["parameters_schema"] = json.dumps(tmpl["parameters_schema"])
        metadatas.append(metadata)

    collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    return service


class TestSearchTemplatesBasicFunctionality:
    """Test core search_templates functionality."""

    @pytest.mark.asyncio
    async def test_search_templates_basic_query(self, vector_search_service_with_templates):
        """Query 'chatbot' returns template results.

        WHY: Validates basic semantic search works for templates.
        """
        results = await vector_search_service_with_templates.search_templates("chatbot")

        assert len(results) > 0, "Should return at least one chatbot template"
        assert all("template_id" in r for r in results), "All results should have template_id"
        assert all(r["template_id"].startswith("tmpl_") for r in results), "All template_ids should start with tmpl_"

    @pytest.mark.asyncio
    async def test_search_templates_max_results(self, vector_search_service_with_templates):
        """Verify max_results parameter (default 3).

        WHY: Ensures result limiting works as expected.
        """
        results_default = await vector_search_service_with_templates.search_templates("chatbot")
        assert len(results_default) <= 3, "Default max_results should be 3"

        results_custom = await vector_search_service_with_templates.search_templates("chatbot", limit=2)
        assert len(results_custom) <= 2, "Custom limit should be respected"

    @pytest.mark.asyncio
    async def test_search_templates_similarity_threshold(self, vector_search_service_with_templates):
        """Verify threshold filtering (default 0.7).

        WHY: Ensures relevance filtering works correctly.
        """
        # TDD-RED: This test will FAIL until threshold filtering is implemented in T027
        results_low = await vector_search_service_with_templates.search_templates("chatbot", threshold=0.5)
        results_high = await vector_search_service_with_templates.search_templates("chatbot", threshold=0.9)

        assert len(results_low) >= len(results_high), "Lower threshold should return more results"

        # All results should meet the threshold
        for result in results_high:
            assert result["relevance_score"] >= 0.9, f"Result should meet threshold 0.9, got {result['relevance_score']}"


class TestSearchTemplatesFormat:
    """Test template result format and content."""

    @pytest.mark.asyncio
    async def test_search_templates_no_flowdata_in_results(self, vector_search_service_with_templates):
        """Results exclude flowData (only metadata).

        WHY: Ensures token efficiency by excluding large flowData from search results.
        """
        results = await vector_search_service_with_templates.search_templates("chatbot")

        assert len(results) > 0, "Should have results to validate"
        for result in results:
            assert "flowData" not in result, "Results should not include flowData"
            assert "template_id" in result, "Results should include template_id"
            assert "name" in result, "Results should include name"
            assert "description" in result, "Results should include description"

    @pytest.mark.asyncio
    async def test_search_templates_compact_format(self, vector_search_service_with_templates):
        """Each result <100 tokens.

        WHY: Meets token budget requirement for template results.
        """
        results = await vector_search_service_with_templates.search_templates("chatbot")

        for result in results:
            # Approximate token count: 1 token ≈ 4 characters
            total_chars = (
                len(result.get("template_id", "")) +
                len(result.get("name", "")) +
                len(result.get("description", ""))
            )
            approx_tokens = total_chars / 4

            assert approx_tokens < 100, f"Template result should be <100 tokens, got ~{approx_tokens}"

    @pytest.mark.asyncio
    async def test_search_templates_required_nodes_included(self, vector_search_service_with_templates):
        """Results include required_nodes list.

        WHY: Provides essential metadata for template selection.
        """
        # TDD-RED: This test will FAIL until required_nodes metadata is added in T026
        results = await vector_search_service_with_templates.search_templates("chatbot")

        assert len(results) > 0, "Should have results to validate"
        for result in results:
            assert "required_nodes" in result, "Result should include required_nodes list"
            assert isinstance(result["required_nodes"], list), "required_nodes should be a list"
            assert len(result["required_nodes"]) > 0, "required_nodes should not be empty"

    @pytest.mark.asyncio
    async def test_search_templates_parameters_schema(self, vector_search_service_with_templates):
        """Results include parameters schema if customizable.

        WHY: Enables template customization by exposing configurable parameters.
        """
        # TDD-RED: This test will FAIL until parameters schema is added in T026
        results = await vector_search_service_with_templates.search_templates("chatbot")

        assert len(results) > 0, "Should have results to validate"

        # At least some templates should have parameters schema
        templates_with_params = [r for r in results if "parameters_schema" in r]
        assert len(templates_with_params) > 0, "At least one template should have parameters_schema"

        # Validate schema structure
        for result in templates_with_params:
            schema = result["parameters_schema"]
            assert isinstance(schema, dict), "parameters_schema should be a dict"
            assert "properties" in schema or "fields" in schema, "Schema should define properties/fields"


class TestSearchTemplatesRanking:
    """Test relevance ranking and sorting."""

    @pytest.mark.asyncio
    async def test_search_templates_sort_by_relevance(self, vector_search_service_with_templates):
        """Results sorted by relevance_score DESC.

        WHY: Most relevant templates should appear first for better UX.
        """
        results = await vector_search_service_with_templates.search_templates("chatbot")

        if len(results) > 1:
            scores = [r["relevance_score"] for r in results]
            assert scores == sorted(scores, reverse=True), "Results should be sorted by relevance DESC"

    @pytest.mark.asyncio
    async def test_search_templates_complexity_tiebreaker(self, vector_search_service_with_templates):
        """Same relevance → fewer nodes ranked higher.

        WHY: Simpler templates are preferred when relevance is equal.
        """
        # TDD-RED: This test will FAIL until complexity tiebreaker is implemented in T027
        results = await vector_search_service_with_templates.search_templates("chatbot")

        # Find templates with similar relevance scores (within 0.05)
        if len(results) > 1:
            for i in range(len(results) - 1):
                curr = results[i]
                next_result = results[i + 1]

                # If relevance scores are within 0.05, check complexity tiebreaker
                if abs(curr["relevance_score"] - next_result["relevance_score"]) < 0.05:
                    curr_complexity = curr.get("node_count", 999)
                    next_complexity = next_result.get("node_count", 999)

                    assert curr_complexity <= next_complexity, (
                        f"When relevance is similar ({curr['relevance_score']:.3f} vs {next_result['relevance_score']:.3f}), "
                        f"simpler template (nodes: {curr_complexity}) should rank before complex (nodes: {next_complexity})"
                    )


class TestSearchTemplatesEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_search_templates_no_results(self, vector_search_service_with_templates):
        """Query with no matches returns empty list.

        WHY: Graceful handling of no-match scenarios without errors.
        """
        results = await vector_search_service_with_templates.search_templates("xyznonexistent12345")

        assert results == [], "No matches should return empty list, not error"

    @pytest.mark.asyncio
    async def test_search_templates_template_id_format(self, vector_search_service_with_templates):
        """All template_ids start with 'tmpl_'.

        WHY: Consistent naming convention for template identification.
        """
        results = await vector_search_service_with_templates.search_templates("chatbot")

        assert len(results) > 0, "Should have results to validate"
        for result in results:
            assert result["template_id"].startswith("tmpl_"), \
                f"Template ID {result['template_id']} should start with 'tmpl_'"


class TestSearchTemplatesPerformance:
    """Test performance requirements."""

    @pytest.mark.asyncio
    async def test_search_templates_performance(self, vector_search_service_with_templates):
        """Average search time <500ms.

        WHY: Meets NFR-020 performance target.
        """
        import time

        start = time.time()
        await vector_search_service_with_templates.search_templates("chatbot")
        duration = time.time() - start

        assert duration < 0.5, f"Search should complete in <500ms, took {duration*1000:.0f}ms"
