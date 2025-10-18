"""Integration tests for User Story 2 - Flow Template Search.

End-to-end scenarios validating complete template discovery journeys.

WHY: Validates US2 acceptance criteria with realistic template catalog data.
"""

import pytest
from fluent_mind_mcp.services.vector_search_service import VectorSearchService
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.client.embedding_client import EmbeddingClient


@pytest.fixture
def populated_template_service(tmp_path):
    """Create VectorSearchService with realistic template catalog.

    WHY: Simulates real-world usage with comprehensive template descriptions.
    """
    vector_db = VectorDatabaseClient(persist_directory=str(tmp_path / "integration_templates_db"))
    embedder = EmbeddingClient()
    service = VectorSearchService(vector_db, embedder)

    # Populate with realistic Flowise templates
    realistic_templates = [
        {
            "id": "tmpl_simple_chat",
            "template_id": "tmpl_simple_chat",
            "name": "Simple Chatbot",
            "description": "Basic conversational chatbot with memory for simple Q&A interactions. Uses ChatOpenAI with buffer memory for maintaining conversation context across turns.",
            "tags": "chatbot,conversation,simple,beginner",
            "node_count": 3,
            "complexity_level": "simple",
            "required_nodes": ["chatOpenAI", "bufferMemory", "conversationChain"]
        },
        {
            "id": "tmpl_rag_chatbot",
            "template_id": "tmpl_rag_chatbot",
            "name": "RAG Chatbot",
            "description": "Retrieval-augmented generation chatbot for knowledge base question answering. Includes document loaders, embeddings, vector store (FAISS), and conversational retrieval chain for context-aware document search.",
            "tags": "chatbot,rag,knowledge,retrieval,support",
            "node_count": 7,
            "complexity_level": "intermediate",
            "required_nodes": ["chatOpenAI", "cheerioWebScraper", "openAIEmbeddings", "faiss", "conversationalRetrievalQAChain", "bufferMemory"]
        },
        {
            "id": "tmpl_support_agent",
            "template_id": "tmpl_support_agent",
            "name": "Customer Support Agent",
            "description": "Intelligent customer support chatbot with knowledge base integration and escalation capabilities. Handles support tickets using document retrieval and provides accurate responses based on knowledge base content.",
            "tags": "support,agent,customer,knowledge,tickets",
            "node_count": 8,
            "complexity_level": "intermediate",
            "required_nodes": ["chatOpenAI", "cheerioWebScraper", "openAIEmbeddings", "faiss", "toolAgent", "bufferMemory"]
        },
        {
            "id": "tmpl_data_agent",
            "template_id": "tmpl_data_agent",
            "name": "Data Analysis Agent",
            "description": "Autonomous agent for data analysis with tools for processing CSV files, performing calculations, and generating visualizations. Integrates with data sources to provide insights and analytics.",
            "tags": "agent,data,analysis,tools,csv,visualization",
            "node_count": 6,
            "complexity_level": "advanced",
            "required_nodes": ["chatOpenAI", "toolAgent", "csvFile", "bufferMemory"]
        },
        {
            "id": "tmpl_research_agent",
            "template_id": "tmpl_research_agent",
            "name": "Research Agent",
            "description": "Advanced research agent with web scraping and summarization capabilities. Uses ReAct reasoning pattern to gather information from multiple sources, analyze content, and provide comprehensive research summaries.",
            "tags": "agent,research,tools,web,scraping,summarization",
            "node_count": 9,
            "complexity_level": "advanced",
            "required_nodes": ["chatOpenAI", "reactAgentLLM", "cheerioWebScraper", "bufferMemory"]
        },
        {
            "id": "tmpl_memory_chat",
            "template_id": "tmpl_memory_chat",
            "name": "Memory-Enhanced Chat",
            "description": "Chatbot with enhanced memory capabilities using buffer window memory for tracking recent conversation history while maintaining context efficiency.",
            "tags": "chatbot,memory,conversation,context",
            "node_count": 4,
            "complexity_level": "simple",
            "required_nodes": ["chatOpenAI", "bufferWindowMemory", "conversationChain"]
        }
    ]

    # Add templates to vector database
    collection = vector_db.get_or_create_collection("templates")
    ids = [tmpl["id"] for tmpl in realistic_templates]
    documents = [tmpl["description"] for tmpl in realistic_templates]
    embeddings = embedder.batch_embed(documents)
    metadatas = [
        {
            "template_id": tmpl["template_id"],
            "name": tmpl["name"],
            "tags": tmpl["tags"],
            "node_count": tmpl["node_count"],
            "complexity_level": tmpl["complexity_level"]
        }
        for tmpl in realistic_templates
    ]

    collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    return service


class TestUS2CustomerSupportScenario:
    """US2 Acceptance Test 1: Customer support with knowledge base."""

    @pytest.mark.asyncio
    async def test_customer_support_search(self, populated_template_service):
        """Query 'chatbot for customer support with knowledge base' returns rag-chatbot, support-agent.

        User Story 2 - Acceptance Scenario 1:
        GIVEN: User wants a customer support chatbot with knowledge base
        WHEN: User queries "chatbot for customer support with knowledge base"
        THEN: Returns rag-chatbot and support-agent templates in top results

        WHY: Validates semantic search finds correct templates for customer support use case.
        """
        results = await populated_template_service.search_templates(
            "chatbot for customer support with knowledge base",
            limit=5
        )

        # Should return results
        assert len(results) > 0, "Should return results for customer support query"
        assert len(results) <= 5, "Should respect limit of 5"

        # Extract template names
        result_names = {r["name"] for r in results}

        # At least one of the expected templates should be in results
        expected_templates = {"RAG Chatbot", "Customer Support Agent"}
        found_templates = expected_templates & result_names

        assert len(found_templates) >= 1, (
            f"Expected at least one of {expected_templates} in results, "
            f"but found {found_templates} in {result_names}"
        )

        # Verify results have required fields
        for result in results:
            assert "template_id" in result, "Result should have template_id"
            assert "name" in result, "Result should have name"
            assert "description" in result, "Result should have description"
            assert "relevance_score" in result, "Result should have relevance_score"


class TestUS2DataAnalysisScenario:
    """US2 Acceptance Test 2: Data analysis agent with tools."""

    @pytest.mark.asyncio
    async def test_data_analysis_search(self, populated_template_service):
        """Query 'data analysis agent with tools' returns agent templates with tool capabilities.

        User Story 2 - Acceptance Scenario 2:
        GIVEN: User wants a data analysis agent
        WHEN: User queries "data analysis agent with tools"
        THEN: Returns data analysis agent template

        WHY: Validates semantic search for specialized agent templates.
        """
        results = await populated_template_service.search_templates(
            "data analysis agent with tools",
            limit=5
        )

        # Should return results
        assert len(results) > 0, "Should return results for data analysis query"

        # Extract template names
        result_names = {r["name"] for r in results}

        # Data Analysis Agent should be in results
        assert "Data Analysis Agent" in result_names, (
            f"Expected 'Data Analysis Agent' in results, found {result_names}"
        )

        # Find data analysis agent result
        data_agent = next(r for r in results if r["name"] == "Data Analysis Agent")

        # Should have high relevance
        assert data_agent["relevance_score"] > 0.6, (
            f"Data analysis agent should have high relevance, got {data_agent['relevance_score']}"
        )


class TestUS2SimpleChatbotScenario:
    """US2 Acceptance Test 3: Simple chatbot query."""

    @pytest.mark.asyncio
    async def test_simple_chatbot_search(self, populated_template_service):
        """Query 'simple chatbot' returns basic chat templates.

        User Story 2 - Acceptance Scenario 3:
        GIVEN: User wants a simple chatbot
        WHEN: User queries "simple chatbot"
        THEN: Returns Simple Chatbot template

        WHY: Validates search finds appropriate simple templates for basic use cases.
        """
        results = await populated_template_service.search_templates(
            "simple chatbot",
            limit=3
        )

        # Should return results
        assert len(results) > 0, "Should return results for simple chatbot query"

        # Extract template names
        result_names = {r["name"] for r in results}

        # Simple Chatbot should be in results
        assert "Simple Chatbot" in result_names, (
            f"Expected 'Simple Chatbot' in results, found {result_names}"
        )

        # Verify it's highly relevant
        simple_chat = next(r for r in results if r["name"] == "Simple Chatbot")
        assert simple_chat["relevance_score"] > 0.6, (
            "Simple Chatbot should be highly relevant for 'simple chatbot' query"
        )


class TestUS2TemplateToBuildFlow:
    """US2 Acceptance Test 4: Template ID for build_flow integration."""

    @pytest.mark.asyncio
    async def test_template_to_build_flow(self, populated_template_service):
        """Selected template_id can be passed to build_flow (<20 tokens).

        User Story 2 - Acceptance Scenario 4:
        GIVEN: User selects a template from search results
        WHEN: User extracts template_id
        THEN: template_id is compact (<20 tokens) and ready for build_flow

        WHY: Validates template_id format is suitable for build_flow integration.
        """
        results = await populated_template_service.search_templates("chatbot", limit=3)

        assert len(results) > 0, "Should have results to validate"

        for result in results:
            # Verify template_id exists and has correct format
            template_id = result["template_id"]
            assert template_id.startswith("tmpl_"), "Template ID should start with 'tmpl_'"

            # Verify template_id is compact (<20 tokens)
            # Approximate: 1 token ≈ 4 characters
            approx_tokens = len(template_id) / 4
            assert approx_tokens < 20, (
                f"Template ID {template_id} should be <20 tokens, got ~{approx_tokens}"
            )

            # Verify essential metadata for build_flow decision
            assert "name" in result, "Should include name for user selection"
            assert "description" in result, "Should include description for user understanding"
