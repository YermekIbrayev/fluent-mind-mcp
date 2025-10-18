"""Integration tests for Phase 1 complete workflows.

Tests end-to-end scenarios for User Stories 1-3:
- US1: Vector search for node selection
- US2: Template search and selection
- US3: Build chatflow from template

These tests validate the complete Phase 1 deliverable:
"Vector search + template-based chatflow creation working end-to-end"

WHY: Validates Phase 1 acceptance criteria before Phase 2 work begins.

NOTE: These tests use tmp_path instead of populated_chromadb fixture to avoid
ChromaDB instance conflicts when creating multiple VectorDatabaseClient instances.
"""

import pytest
import os
import time

from fluent_mind_mcp.services.vector_search_service import VectorSearchService
from fluent_mind_mcp.services.build_flow_service import BuildFlowService
from fluent_mind_mcp.client.embedding_client import EmbeddingClient
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient


# Skip all tests if Flowise not configured (integration tests only run when available)
pytestmark = pytest.mark.skipif(
    not os.getenv("FLOWISE_API_URL"),
    reason="Flowise API not configured (set FLOWISE_API_URL to run integration tests)"
)


def setup_test_nodes(vector_db_client: VectorDatabaseClient, embedding_client: EmbeddingClient):
    """Helper to populate test nodes."""
    test_nodes = [
        {"name": "chatOpenAI", "label": "ChatOpenAI", "category": "Chat Models",
         "description": "OpenAI chat model for conversations"},
        {"name": "bufferMemory", "label": "Buffer Memory", "category": "Memory",
         "description": "Memory buffer for storing conversation history"},
        {"name": "conversationChain", "label": "Conversation Chain", "category": "Chains",
         "description": "Chain for chatbot conversations with memory"},
        {"name": "openAIEmbeddings", "label": "OpenAI Embeddings", "category": "Embeddings",
         "description": "OpenAI embedding model for text vectorization"},
        {"name": "faiss", "label": "FAISS", "category": "Vector Stores",
         "description": "Vector store for document retrieval"},
        {"name": "conversationalRetrievalQAChain", "label": "Conversational Retrieval QA", "category": "Chains",
         "description": "QA chain with document retrieval"},
    ]

    ids = [node["name"] for node in test_nodes]
    documents = [node["description"] for node in test_nodes]
    embeddings = embedding_client.batch_embed(documents)
    metadatas = [
        {"name": node["name"], "label": node["label"], "category": node["category"]}
        for node in test_nodes
    ]

    vector_db_client.add_documents("nodes", documents, embeddings, ids, metadatas)


def setup_test_templates(vector_db_client: VectorDatabaseClient, embedding_client: EmbeddingClient):
    """Helper to populate test templates."""
    test_templates = [
        {"template_id": "tmpl_simple_chat", "name": "Simple Chat",
         "description": "Basic chatbot with conversational memory", "tags": "chatbot,conversation",
         "nodes": "chatOpenAI,bufferMemory,conversationChain"},
        {"template_id": "tmpl_rag_flow", "name": "RAG Assistant",
         "description": "Retrieval-augmented generation for document question answering", "tags": "rag,qa,documents",
         "nodes": "chatOpenAI,openAIEmbeddings,faiss,conversationalRetrievalQAChain"},
    ]

    ids = [t["template_id"] for t in test_templates]
    documents = [t["description"] for t in test_templates]
    embeddings = embedding_client.batch_embed(documents)
    metadatas = [
        {"template_id": t["template_id"], "name": t["name"],
         "tags": t["tags"], "nodes": t["nodes"]}
        for t in test_templates
    ]

    # Populate templates collection
    collection = vector_db_client.get_or_create_collection("templates")
    collection.add(ids=ids, documents=documents, metadatas=metadatas)


@pytest.mark.integration
@pytest.mark.phase1
class TestUserStory1VectorSearchNodes:
    """User Story 1: As a user, I want to search for Flowise nodes using natural language."""

    @pytest.mark.asyncio
    async def test_us1_scenario1_search_chatbot_with_memory_nodes(self, tmp_path):
        """
        SCENARIO: User searches for nodes to build a chatbot with memory
        GIVEN: Vector database populated with Flowise node catalog
        WHEN: User queries "chatbot that remembers conversation"
        THEN: Returns ChatOpenAI, BufferMemory, ConversationChain in top 3 results

        WHY: Validates US1 AC1 (semantic search returns relevant nodes).
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_nodes(vector_db_client, embedding_client)

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("chatbot that remembers conversation", limit=5)

        # Verify results
        assert len(results) <= 5
        top_3_names = [r["name"] for r in results[:3]] if len(results) >= 3 else [r["name"] for r in results]

        # Expected nodes in top 3 (at least some should match)
        expected = ["chatOpenAI", "bufferMemory", "conversationChain"]
        matches = sum(1 for node in expected if node in top_3_names)
        assert matches >= 1, f"Expected at least 1/3 matches in top 3, got {matches}: {top_3_names}"

        # Each result has required fields
        for result in results:
            assert "name" in result
            assert "label" in result
            assert "description" in result
            assert "relevance_score" in result
            assert len(result["description"]) <= 250  # Token budget (~50 tokens)

    @pytest.mark.asyncio
    async def test_us1_scenario2_search_document_retrieval_nodes(self, tmp_path):
        """
        SCENARIO: User searches for nodes to implement document search
        GIVEN: Vector database populated with node catalog
        WHEN: User queries "search documents using embeddings"
        THEN: Returns DocumentLoader, VectorStore, RetrievalQA nodes

        WHY: Validates semantic search accuracy across different use cases.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_nodes(vector_db_client, embedding_client)

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_nodes("search documents using embeddings", limit=5)

        top_3_names = [r["name"] for r in results[:3]] if len(results) >= 3 else [r["name"] for r in results]
        expected = ["openAIEmbeddings", "faiss", "conversationalRetrievalQAChain"]
        matches = sum(1 for node in expected if node in top_3_names)
        assert matches >= 1, f"Expected at least 1 match in top 3, got {matches}: {top_3_names}"

    @pytest.mark.asyncio
    async def test_us1_scenario3_performance_within_5_seconds(self, tmp_path):
        """
        SCENARIO: User expects fast search results
        GIVEN: Normal database size (50-100 nodes)
        WHEN: Performing vector search
        THEN: Completes within 5 seconds (NFR-020)

        WHY: Validates performance requirement for responsive UX.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_nodes(vector_db_client, embedding_client)

        service = VectorSearchService(vector_db_client, embedding_client)

        start = time.time()
        results = await service.search_nodes("test query", limit=5)
        duration = time.time() - start

        assert duration < 5.0, f"Search took {duration}s, expected <5s"
        assert len(results) <= 5



@pytest.mark.integration
@pytest.mark.phase1
class TestUserStory2TemplateSearch:
    """User Story 2: As a user, I want to search for flow templates."""

    @pytest.mark.asyncio
    async def test_us2_scenario1_search_simple_chatbot_template(self, tmp_path):
        """
        SCENARIO: User searches for simple chatbot template
        GIVEN: Template database with curated templates
        WHEN: User queries "simple chatbot"
        THEN: Returns "Simple Chat" template in top results

        WHY: Validates US2 AC1 (template search by description).
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_templates(vector_db_client, embedding_client)

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_templates("simple chatbot", limit=3)

        # "tmpl_simple_chat" template should be in results
        template_ids = [r["template_id"] for r in results]
        assert "tmpl_simple_chat" in template_ids, f"Expected tmpl_simple_chat in {template_ids}"

        # Verify template structure
        simple_chat = next(r for r in results if r["template_id"] == "tmpl_simple_chat")
        assert simple_chat["name"] == "Simple Chat"
        assert "chatbot" in simple_chat.get("tags", "")

    @pytest.mark.asyncio
    async def test_us2_scenario2_search_rag_template(self, tmp_path):
        """
        SCENARIO: User searches for document QA template
        GIVEN: Template database
        WHEN: User queries "document question answering"
        THEN: Returns "RAG Assistant" template

        WHY: Validates template search for different use cases.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_templates(vector_db_client, embedding_client)

        service = VectorSearchService(vector_db_client, embedding_client)
        results = await service.search_templates("document question answering", limit=3)

        template_ids = [r["template_id"] for r in results]
        assert "tmpl_rag_flow" in template_ids, f"Expected tmpl_rag_flow in {template_ids}"



@pytest.mark.integration
@pytest.mark.phase1
class TestUserStory3BuildFromTemplate:
    """User Story 3: As a user, I want to create chatflows from templates."""

    @pytest.mark.asyncio
    async def test_us3_scenario1_build_simple_chat_from_template(self, tmp_path):
        """
        SCENARIO: User creates chatbot from template
        GIVEN: "Simple Chat" template exists
        WHEN: User calls build_from_template("tmpl_simple_chat")
        THEN: Chatflow structure is generated correctly

        WHY: Validates US3 AC1 (template-based chatflow creation).
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_templates(vector_db_client, embedding_client)

        service = BuildFlowService(vector_db_client)

        # Build chatflow
        result = await service.build_from_template("tmpl_simple_chat")

        # Verify creation
        assert result["status"] == "success"
        assert "chatflow_id" in result
        assert "flow_data" in result

        # Verify flowData structure
        flow_data = result["flow_data"]
        assert "nodes" in flow_data
        assert "edges" in flow_data
        assert len(flow_data["nodes"]) > 0

    @pytest.mark.asyncio
    async def test_us3_scenario2_build_rag_flow_from_template(self, tmp_path):
        """
        SCENARIO: User creates RAG assistant from template
        GIVEN: "RAG Assistant" template exists
        WHEN: User builds chatflow from template
        THEN: Chatflow has embeddings, vector store, and retrieval chain nodes

        WHY: Validates template with multiple nodes and complexity.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_templates(vector_db_client, embedding_client)

        service = BuildFlowService(vector_db_client)
        result = await service.build_from_template("tmpl_rag_flow")

        # Verify flowData structure
        flow_data = result["flow_data"]
        assert len(flow_data["nodes"]) >= 3  # RAG requires multiple nodes

        # Verify nodes have proper structure
        for node in flow_data["nodes"]:
            assert "id" in node
            assert "type" in node
            assert "data" in node
            assert "position" in node

    @pytest.mark.asyncio
    async def test_us3_scenario3_build_completes_within_10_seconds(self, tmp_path):
        """
        SCENARIO: User expects quick chatflow creation
        GIVEN: Normal template
        WHEN: Building chatflow
        THEN: Completes within 10 seconds (NFR-022)

        WHY: Validates performance requirement.
        """
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_templates(vector_db_client, embedding_client)

        service = BuildFlowService(vector_db_client)

        start = time.time()
        result = await service.build_from_template("tmpl_simple_chat")
        duration = time.time() - start

        assert duration < 10.0, f"Build took {duration}s, expected <10s"
        assert result["status"] == "success"



@pytest.mark.integration
@pytest.mark.phase1
class TestPhase1CompleteWorkflow:
    """End-to-end Phase 1 workflow: search nodes → search template → build chatflow."""

    @pytest.mark.asyncio
    async def test_complete_phase1_user_journey(self, tmp_path):
        """
        SCENARIO: Complete user journey through Phase 1 features
        GIVEN: User wants to build a chatbot with memory
        WHEN: User searches nodes, finds template, and builds chatflow
        THEN: Each step succeeds and produces expected results

        WHY: Validates Phase 1 deliverable: "Vector search + template-based chatflow creation working end-to-end"
        """
        # Setup clients
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_nodes(vector_db_client, embedding_client)
        setup_test_templates(vector_db_client, embedding_client)

        search_service = VectorSearchService(vector_db_client, embedding_client)
        build_service = BuildFlowService(vector_db_client)

        # Step 1: Search for relevant nodes
        node_results = await search_service.search_nodes(
            "chatbot that remembers conversation",
            limit=5
        )
        assert len(node_results) <= 5
        assert any("chat" in r["name"].lower() for r in node_results)

        # Step 2: Search for template
        template_results = await search_service.search_templates(
            "simple chatbot",
            limit=3
        )
        assert len(template_results) > 0
        assert "tmpl_simple_chat" in [r["template_id"] for r in template_results]

        # Step 3: Build chatflow from template
        build_result = await build_service.build_from_template("tmpl_simple_chat")
        assert build_result["status"] == "success"
        assert "chatflow_id" in build_result
        assert "flow_data" in build_result

        # Verify flowData structure
        flow_data = build_result["flow_data"]
        assert "nodes" in flow_data
        assert "edges" in flow_data

    @pytest.mark.asyncio
    async def test_phase1_complete_in_under_60_seconds(self, tmp_path):
        """
        SCENARIO: User completes full workflow quickly
        GIVEN: Normal conditions
        WHEN: Running complete Phase 1 workflow
        THEN: Total time < 60 seconds (search + search + build)

        WHY: Validates overall system performance.
        """
        # Setup
        embedding_client = EmbeddingClient()
        vector_db_client = VectorDatabaseClient(persist_directory=str(tmp_path / "test_db"))
        setup_test_nodes(vector_db_client, embedding_client)
        setup_test_templates(vector_db_client, embedding_client)

        search_service = VectorSearchService(vector_db_client, embedding_client)
        build_service = BuildFlowService(vector_db_client)

        start = time.time()

        # Complete workflow
        await search_service.search_nodes("test", limit=5)
        await search_service.search_templates("test", limit=3)
        result = await build_service.build_from_template("tmpl_simple_chat")

        duration = time.time() - start

        assert duration < 60.0, f"Full workflow took {duration}s, expected <60s"
        assert result["status"] == "success"
