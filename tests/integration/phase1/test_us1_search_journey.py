"""Integration tests for User Story 1 - Vector Search for Node Selection.

End-to-end scenarios validating complete search journeys from user query to results.

WHY: Validates US1 acceptance criteria with realistic node catalog data.
"""

import pytest
from fluent_mind_mcp.services.vector_search_service import VectorSearchService
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.client.embedding_client import EmbeddingClient


@pytest.fixture
def populated_vector_service(tmp_path):
    """Create VectorSearchService with realistic Flowise node catalog.

    WHY: Simulates real-world usage with comprehensive node descriptions.
    """
    vector_db = VectorDatabaseClient(persist_directory=str(tmp_path / "integration_db"))
    embedder = EmbeddingClient()
    service = VectorSearchService(vector_db, embedder)

    # Populate with realistic Flowise nodes
    realistic_nodes = [
        {
            "id": "chatOpenAI",
            "name": "chatOpenAI",
            "label": "ChatOpenAI",
            "category": "Chat Models",
            "base_classes": ["BaseChatModel", "BaseLanguageModel"],
            "description": "OpenAI's GPT chat models for natural conversations. Supports GPT-3.5 and GPT-4 with streaming, function calling, and vision capabilities.",
            "deprecated": False
        },
        {
            "id": "bufferMemory",
            "name": "bufferMemory",
            "label": "Buffer Memory",
            "category": "Memory",
            "base_classes": ["BaseMemory"],
            "description": "Stores conversation history in a buffer for context-aware chat applications. Maintains message history across turns.",
            "deprecated": False
        },
        {
            "id": "conversationChain",
            "name": "conversationChain",
            "label": "Conversation Chain",
            "category": "Chains",
            "base_classes": ["BaseChain", "LLMChain"],
            "description": "Combines language model with memory to create stateful conversational agents. Ideal for chatbots that remember context.",
            "deprecated": False
        },
        {
            "id": "cheerioWebScraper",
            "name": "cheerioWebScraper",
            "label": "Cheerio Web Scraper",
            "category": "Document Loaders",
            "base_classes": ["BaseDocumentLoader"],
            "description": "Fast and efficient web scraper using Cheerio for HTML parsing. Extracts text content from websites for document processing.",
            "deprecated": False
        },
        {
            "id": "openAIEmbeddings",
            "name": "openAIEmbeddings",
            "label": "OpenAI Embeddings",
            "category": "Embeddings",
            "base_classes": ["Embeddings"],
            "description": "Generate semantic embeddings using OpenAI's text-embedding models. Converts text into vector representations for similarity search.",
            "deprecated": False
        },
        {
            "id": "faiss",
            "name": "faiss",
            "label": "FAISS",
            "category": "Vector Stores",
            "base_classes": ["VectorStore"],
            "description": "Facebook AI Similarity Search - high-performance vector database for semantic document retrieval. Supports billions of vectors with fast similarity search.",
            "deprecated": False
        },
        {
            "id": "conversationalRetrievalQAChain",
            "name": "conversationalRetrievalQAChain",
            "label": "Conversational Retrieval QA",
            "category": "Chains",
            "base_classes": ["BaseChain"],
            "description": "Question-answering chain with document retrieval and conversation memory. Combines vector search with chat for context-aware document Q&A.",
            "deprecated": False
        },
        {
            "id": "csvFile",
            "name": "csvFile",
            "label": "CSV File",
            "category": "Document Loaders",
            "base_classes": ["BaseDocumentLoader"],
            "description": "Load and parse CSV files for data analysis and processing. Supports various delimiters and encoding formats.",
            "deprecated": False
        },
        {
            "id": "reactAgentLLM",
            "name": "reactAgentLLM",
            "label": "ReAct Agent",
            "category": "Agents",
            "base_classes": ["Agent", "BaseSingleActionAgent"],
            "description": "ReAct (Reasoning + Acting) agent that thinks step-by-step and uses tools to solve complex tasks. Combines chain-of-thought reasoning with action execution.",
            "deprecated": False
        },
        {
            "id": "toolAgent",
            "name": "toolAgent",
            "label": "Tool Agent",
            "category": "Agents",
            "base_classes": ["Agent"],
            "description": "Generic agent framework for using multiple tools to accomplish tasks. Autonomously selects and executes appropriate tools based on objectives.",
            "deprecated": False
        },
        {
            "id": "autoGPT",
            "name": "autoGPT",
            "label": "AutoGPT",
            "category": "Agents",
            "base_classes": ["Agent"],
            "description": "Autonomous AI agent inspired by AutoGPT. Self-directs toward goals, creates sub-tasks, and executes multi-step workflows without human intervention.",
            "deprecated": False
        }
    ]

    # Add nodes to vector database
    collection = vector_db.get_or_create_collection("nodes")
    ids = [node["id"] for node in realistic_nodes]
    documents = [node["description"] for node in realistic_nodes]
    embeddings = embedder.batch_embed(documents)
    metadatas = [
        {
            "name": node["name"],
            "label": node["label"],
            "category": node["category"],
            "base_classes": ",".join(node["base_classes"]),
            "deprecated": node["deprecated"]
        }
        for node in realistic_nodes
    ]

    collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    return service


class TestUS1ChatbotMemoryScenario:
    """US1 Acceptance Test 1: Chatbot with conversation memory."""

    @pytest.mark.asyncio
    async def test_chatbot_memory_search(self, populated_vector_service):
        """Query 'chatbot that remembers conversation' returns ChatOpenAI, BufferMemory, ConversationChain.

        User Story 1 - Acceptance Scenario 1:
        GIVEN: User wants to build a chatbot with conversation memory
        WHEN: User queries "chatbot that remembers conversation"
        THEN: Returns ChatOpenAI, BufferMemory, ConversationChain in top 5 results

        WHY: Validates semantic search finds correct nodes for common use case.
        """
        results = await populated_vector_service.search_nodes(
            "chatbot that remembers conversation",
            max_results=5
        )

        # Should return results
        assert len(results) > 0, "Should return results for chatbot memory query"
        assert len(results) <= 5, "Should respect limit of 5"

        # Extract node names from results
        result_names = [r["name"] for r in results]

        # At least 2 of the 3 expected nodes should be in top 5
        expected_nodes = {"chatOpenAI", "bufferMemory", "conversationChain"}
        found_nodes = expected_nodes & set(result_names)

        assert len(found_nodes) >= 2, (
            f"Expected at least 2 of {expected_nodes} in results, "
            f"but only found {found_nodes} in {result_names}"
        )

        # Verify results are relevant (high relevance scores)
        assert all(r["relevance_score"] > 0.6 for r in results), (
            "All results should have relevance >0.6 for this specific query"
        )

        # Verify essential metadata is present
        for result in results:
            assert "name" in result, "Result should have name"
            assert "category" in result, "Result should have category"
            assert "description" in result, "Result should have description"


class TestUS1DocumentRetrievalScenario:
    """US1 Acceptance Test 2: Document search with embeddings."""

    @pytest.mark.asyncio
    async def test_document_retrieval_search(self, populated_vector_service):
        """Query 'search documents using embeddings' returns DocumentLoader, VectorStore, RetrievalQA.

        User Story 1 - Acceptance Scenario 2:
        GIVEN: User wants to implement semantic document search
        WHEN: User queries "search documents using embeddings"
        THEN: Returns relevant nodes (DocumentLoader, Embeddings, VectorStore, RetrievalQA)

        WHY: Validates semantic search for RAG (Retrieval-Augmented Generation) use case.
        """
        results = await populated_vector_service.search_nodes(
            "search documents using embeddings",
            max_results=5
        )

        # Should return results
        assert len(results) > 0, "Should return results for document search query"

        # Extract node names and categories
        result_names = [r["name"] for r in results]
        result_categories = [r["category"] for r in results]

        # Expected components for document search: embeddings, vector store, retrieval
        expected_nodes = {
            "openAIEmbeddings",
            "faiss",
            "conversationalRetrievalQAChain",
            "cheerioWebScraper"
        }
        found_nodes = expected_nodes & set(result_names)

        # Should find at least 2 relevant nodes
        assert len(found_nodes) >= 2, (
            f"Expected at least 2 of {expected_nodes} for document search, "
            f"found {found_nodes} in {result_names}"
        )

        # Verify relevant categories appear
        relevant_categories = {"Embeddings", "Vector Stores", "Chains", "Document Loaders"}
        found_categories = relevant_categories & set(result_categories)

        assert len(found_categories) >= 2, (
            f"Expected categories from {relevant_categories}, "
            f"found {found_categories}"
        )


class TestUS1VagueAgentQuery:
    """US1 Acceptance Test 3: Vague query with multiple valid interpretations."""

    @pytest.mark.asyncio
    async def test_vague_agent_query(self, populated_vector_service):
        """Query 'AI agent' returns 3-5 agent nodes with differentiation.

        User Story 1 - Acceptance Scenario 3:
        GIVEN: User makes vague query about AI agents
        WHEN: User queries "AI agent"
        THEN: Returns 3-5 different agent types with distinct descriptions

        WHY: Validates search handles ambiguous queries and provides variety.
        """
        results = await populated_vector_service.search_nodes(
            "AI agent",
            max_results=5
        )

        # Should return multiple results
        assert 3 <= len(results) <= 5, f"Expected 3-5 results, got {len(results)}"

        # Should include agent category nodes
        agent_results = [r for r in results if r["category"] == "Agents"]
        assert len(agent_results) >= 2, (
            f"Expected at least 2 Agent category nodes, got {len(agent_results)}"
        )

        # Verify agents have different names (diversity)
        agent_names = [r["name"] for r in agent_results]
        assert len(agent_names) == len(set(agent_names)), "Agent results should be unique"

        # Verify descriptions provide differentiation
        for result in agent_results:
            assert len(result["description"]) > 50, (
                "Agent descriptions should be detailed enough to differentiate"
            )

        # Verify relevance scores indicate semantic match
        assert all(r["relevance_score"] > 0.5 for r in results), (
            "Results should have moderate relevance for vague query"
        )


class TestUS1PerformanceAndTokenBudget:
    """US1 Non-Functional Requirements: Performance and token efficiency."""

    @pytest.mark.asyncio
    async def test_search_performance_nfr020(self, populated_vector_service):
        """Search completes within 500ms (NFR-020).

        Non-Functional Requirement NFR-020:
        Vector search operations complete in <500ms for 50+ nodes

        WHY: Ensures responsive user experience.
        """
        import time

        start = time.time()
        results = await populated_vector_service.search_nodes("chat model", max_results=5)
        duration = time.time() - start

        assert duration < 0.5, f"Search took {duration*1000:.0f}ms, expected <500ms"
        assert len(results) > 0, "Should return results"

    @pytest.mark.asyncio
    async def test_token_budget_per_result(self, populated_vector_service):
        """Each result consumes <50 tokens (NFR-002, Success Criterion SC-002).

        Success Criterion SC-002:
        Each search result <50 tokens (name + description + metadata)

        WHY: Ensures token efficiency for AI assistant consumption.
        """
        results = await populated_vector_service.search_nodes("chatbot", max_results=5)

        assert len(results) > 0, "Should have results to validate"

        for result in results:
            # Calculate approximate tokens: ~4 chars per token
            total_chars = (
                len(result.get("name", "")) +
                len(result.get("description", "")) +
                len(result.get("category", "")) +
                len(result.get("label", ""))
            )
            approx_tokens = total_chars / 4

            assert approx_tokens < 50, (
                f"Result for {result.get('name')} uses ~{approx_tokens:.0f} tokens, "
                f"expected <50 tokens"
            )

    @pytest.mark.asyncio
    async def test_total_workflow_token_budget(self, populated_vector_service):
        """Complete search workflow uses <150 tokens (Success Criterion SC-005).

        Success Criterion SC-005:
        Query (30 tokens) + Results (50 tokens) + Response (30 tokens) = <150 total

        WHY: Validates complete workflow token efficiency.
        """
        query = "chatbot with memory"  # ~4 tokens
        results = await populated_vector_service.search_nodes(query, max_results=3)

        # Calculate total tokens
        query_tokens = len(query) / 4

        results_tokens = 0
        for result in results:
            total_chars = (
                len(result.get("name", "")) +
                len(result.get("description", "")) +
                len(result.get("category", ""))
            )
            results_tokens += total_chars / 4

        # Response overhead: status message, result count
        response_tokens = 10  # Approximate

        total_tokens = query_tokens + results_tokens + response_tokens

        assert total_tokens < 150, (
            f"Total workflow uses ~{total_tokens:.0f} tokens, expected <150"
        )
