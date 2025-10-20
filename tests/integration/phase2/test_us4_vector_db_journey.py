"""
Integration tests for User Story 4: Vector DB Setup end-to-end scenarios.

Tests the complete pipeline from extraction → embedding → storage → query.
All tests are TDD-RED phase - they should FAIL until implementation is complete.

Test coverage:
- Full extraction → embed → store pipeline
- Query accuracy for memory nodes
- Query accuracy for chat model nodes
- Incremental update workflow
- Vector search precision validation (>90% on top 3)
- End-to-end performance (<10s for 87 nodes)
"""

import time
import pytest
import json
from pathlib import Path

from fluent_mind_mcp.scripts.extract_node_descriptions import extract_all_node_descriptions
from fluent_mind_mcp.client.embedding_client import EmbeddingClient
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.models.node_models import NodeDescription


def combine_node_text(node: NodeDescription) -> str:
    """Combine node fields into text for embedding generation.

    WHY: Helper function to create consistent text representation
         for embedding generation across integration tests.
    """
    return f"{node.label}. {node.description}. Use cases: {', '.join(node.use_cases)}"


@pytest.fixture(scope="module")
def integration_db_client(tmp_path_factory):
    """Provide VectorDatabaseClient for integration tests."""
    # Create temporary directory for integration tests
    persist_dir = tmp_path_factory.mktemp("integration_test_db")
    client = VectorDatabaseClient(persist_directory=str(persist_dir))

    # Ensure clean state - delete collection if it exists
    try:
        client.delete_collection("integration_test_nodes")
    except Exception:
        pass

    yield client

    # Cleanup after all tests
    try:
        client.delete_collection("integration_test_nodes")
    except Exception:
        pass


@pytest.fixture(scope="module")
def embedding_client():
    """Provide EmbeddingClient for integration tests."""
    return EmbeddingClient()


@pytest.fixture(scope="module")
def sample_flowise_api_response():
    """Simulate Flowise /api/v1/nodes-list API response with key nodes."""
    return {
        "nodes": [
            {
                "name": "bufferMemory",
                "label": "Buffer Memory",
                "category": "Memory",
                "baseClasses": ["BufferMemory", "BaseChatMemory", "BaseMemory"],
                "description": "Buffer memory stores all conversation messages in a buffer",
                "deprecated": False,
            },
            {
                "name": "bufferWindowMemory",
                "label": "Buffer Window Memory",
                "category": "Memory",
                "baseClasses": ["BufferWindowMemory", "BaseChatMemory", "BaseMemory"],
                "description": "Buffer window memory stores the last K conversation messages",
                "deprecated": False,
            },
            {
                "name": "conversationSummaryMemory",
                "label": "Conversation Summary Memory",
                "category": "Memory",
                "baseClasses": ["ConversationSummaryMemory", "BaseChatMemory", "BaseMemory"],
                "description": "Conversation summary memory summarizes conversation over time",
                "deprecated": False,
            },
            {
                "name": "chatOpenAI",
                "label": "ChatOpenAI",
                "category": "Chat Models",
                "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel"],
                "description": "Wrapper around OpenAI large language models using Chat endpoint",
                "deprecated": False,
            },
            {
                "name": "chatAnthropic",
                "label": "ChatAnthropic",
                "category": "Chat Models",
                "baseClasses": ["ChatAnthropic", "BaseChatModel", "BaseLanguageModel"],
                "description": "Wrapper around Anthropic Claude models for conversational AI",
                "deprecated": False,
            },
        ]
    }


class TestExtractProcessStorePipeline:
    """Test complete extraction → embedding → storage pipeline."""

    def test_extract_process_store_pipeline(
        self, integration_db_client, embedding_client, sample_flowise_api_response
    ):
        """Extract nodes → generate embeddings → store in ChromaDB."""
        # ARRANGE: Prepare API response
        api_response = sample_flowise_api_response

        # ACT 1: Extract node descriptions
        node_descriptions = extract_all_node_descriptions(api_response)
        assert len(node_descriptions) == 5

        # ACT 2: Generate embeddings for each node
        for node in node_descriptions:
            combined_text = combine_node_text(node)
            embedding = embedding_client.generate_embedding(combined_text)
            node.embedding = embedding

        # ACT 3: Store in ChromaDB
        integration_db_client.add_documents(
            collection_name="integration_test_nodes",
            documents=[node.description for node in node_descriptions],
            embeddings=[node.embedding for node in node_descriptions],
            ids=[node.node_name for node in node_descriptions],
            metadatas=[
                {
                    "label": node.label,
                    "category": node.category,
                    "base_classes": ",".join(node.base_classes),
                    "deprecated": node.deprecated,
                }
                for node in node_descriptions
            ],
        )

        # ASSERT: Verify all nodes stored (health check via collection.get())
        collection = integration_db_client.get_collection("integration_test_nodes")
        all_docs = collection.get()
        assert len(all_docs["ids"]) == 5, "Should have 5 documents"
        assert all_docs["ids"] == [node.node_name for node in node_descriptions]


class TestQueryAccuracy:
    """Test vector search accuracy for specific queries."""

    def test_query_memory_nodes(self, integration_db_client, embedding_client, sample_flowise_api_response):
        """Query "memory" → BufferMemory, BufferWindowMemory, ConversationMemory in results."""
        # ARRANGE: Ensure nodes are loaded (from previous test)
        # Generate query embedding
        query_text = "memory for storing conversation history"
        query_embedding = embedding_client.generate_embedding(query_text)

        # ACT: Query vector database
        results = integration_db_client.query(
            collection_name="integration_test_nodes",
            query_embeddings=[query_embedding],
            n_results=5,
        )

        # ASSERT: Memory nodes should be in top results
        result_ids = results["ids"][0]
        distances = results["distances"][0]

        assert "bufferMemory" in result_ids, "BufferMemory not found in results"
        assert "bufferWindowMemory" in result_ids, "BufferWindowMemory not found in results"
        assert "conversationSummaryMemory" in result_ids, "ConversationSummaryMemory not found in results"

        # Verify relevance scores (ChromaDB uses cosine distance: distance = 1 - similarity)
        similarity_scores = [1 - d for d in distances]
        for score in similarity_scores[:3]:  # Top 3 should be memory nodes
            assert score > 0.5, f"Low similarity score: {score}"

    def test_query_chat_model_nodes(self, integration_db_client, embedding_client):
        """Query "chat model" → ChatOpenAI, ChatAnthropic in top 5."""
        # ARRANGE: Generate query embedding
        query_text = "chat model for conversational AI"
        query_embedding = embedding_client.generate_embedding(query_text)

        # ACT: Query vector database
        results = integration_db_client.query(
            collection_name="integration_test_nodes",
            query_embeddings=[query_embedding],
            n_results=5,
        )

        # ASSERT: Chat model nodes should be in results
        result_ids = results["ids"][0]
        assert "chatOpenAI" in result_ids, "ChatOpenAI not found in results"
        assert "chatAnthropic" in result_ids, "ChatAnthropic not found in results"


class TestIncrementalUpdateWorkflow:
    """Test incremental update workflow."""

    def test_incremental_update_workflow(self, integration_db_client, embedding_client):
        """Add new node → query returns it."""
        # ARRANGE: Create new node
        new_node = NodeDescription(
            node_name="entityMemory",
            label="Entity Memory",
            category="Memory",
            base_classes=["EntityMemory", "BaseChatMemory"],
            description="Entity memory stores information about entities in conversation",
            use_cases=["Entity tracking"],
            version="1",
            deprecated=False,
            embedding=None,
        )

        # ACT 1: Generate embedding and store (using add_documents for single doc)
        combined_text = combine_node_text(new_node)
        embedding = embedding_client.generate_embedding(combined_text)
        integration_db_client.add_documents(
            collection_name="integration_test_nodes",
            documents=[new_node.description],
            embeddings=[embedding],
            ids=[new_node.node_name],
            metadatas=[
                {
                    "label": new_node.label,
                    "category": new_node.category,
                    "base_classes": ",".join(new_node.base_classes),
                    "deprecated": new_node.deprecated,
                }
            ],
        )

        # ACT 2: Query for memory nodes
        query_text = "memory for conversation"
        query_embedding = embedding_client.generate_embedding(query_text)
        results = integration_db_client.query(
            collection_name="integration_test_nodes",
            query_embeddings=[query_embedding],
            n_results=10,
        )

        # ASSERT: New node should be in results
        result_ids = results["ids"][0]
        assert "entityMemory" in result_ids, "Newly added node not found in search results"


class TestVectorSearchPrecision:
    """Test vector search precision with multiple test queries."""

    def test_full_vector_search_accuracy(self, integration_db_client, embedding_client):
        """10 test queries → >90% precision on top 3 results."""
        # ARRANGE: Define test queries with expected results
        test_queries = [
            {
                "query": "memory for storing messages",
                "expected_in_top_3": ["bufferMemory", "bufferWindowMemory", "conversationSummaryMemory"],
            },
            {
                "query": "chat model for OpenAI",
                "expected_in_top_3": ["chatOpenAI"],
            },
            {
                "query": "conversation history tracking",
                "expected_in_top_3": ["bufferMemory", "bufferWindowMemory", "conversationSummaryMemory"],
            },
            {
                "query": "recent conversation messages",
                "expected_in_top_3": ["bufferWindowMemory", "bufferMemory"],
            },
            {
                "query": "Claude chat model",
                "expected_in_top_3": ["chatAnthropic"],
            },
        ]

        # ACT & ASSERT: Test each query
        total_queries = len(test_queries)
        successful_queries = 0

        for test_case in test_queries:
            query_text = test_case["query"]
            expected_nodes = test_case["expected_in_top_3"]

            # Generate query embedding
            query_embedding = embedding_client.generate_embedding(query_text)

            # Query database
            results = integration_db_client.query(
                collection_name="integration_test_nodes",
                query_embeddings=[query_embedding],
                n_results=3,
            )

            # Check if at least one expected node in top 3
            result_ids = results["ids"][0]
            found = any(expected_id in result_ids for expected_id in expected_nodes)

            if found:
                successful_queries += 1

        # Calculate precision
        precision = successful_queries / total_queries
        assert precision >= 0.90, f"Precision {precision:.2%} below 90% threshold"


class TestEndToEndPerformance:
    """Test complete pipeline performance."""

    def test_end_to_end_performance(self, sample_flowise_api_response, tmp_path):
        """Full pipeline (extract → embed → store → query) <10s for 87 nodes."""
        # ARRANGE: Create temporary DB client
        persist_dir = str(tmp_path / "perf_test_db")
        temp_client = VectorDatabaseClient(persist_directory=persist_dir)
        embedding_client = EmbeddingClient()

        # Ensure clean state
        try:
            temp_client.delete_collection("perf_test")
        except Exception:
            pass

        # Expand to 87 nodes (duplicate the 5 sample nodes)
        expanded_response = {"nodes": []}
        for i in range(18):  # 18 * 5 = 90 (close to 87)
            for node in sample_flowise_api_response["nodes"][:5]:
                expanded_node = node.copy()
                expanded_node["name"] = f"{node['name']}_{i}"
                expanded_response["nodes"].append(expanded_node)

        # Take exactly 87 nodes
        expanded_response["nodes"] = expanded_response["nodes"][:87]

        try:
            # ACT: Measure end-to-end time
            start_time = time.time()

            # Step 1: Extract
            node_descriptions = extract_all_node_descriptions(expanded_response)

            # Step 2: Generate embeddings (batch)
            texts = [combine_node_text(node) for node in node_descriptions]
            embeddings = embedding_client.batch_embed(texts)

            # Step 3: Store (batch add)
            temp_client.add_documents(
                collection_name="perf_test",
                documents=[node.description for node in node_descriptions],
                embeddings=embeddings,
                ids=[node.node_name for node in node_descriptions],
                metadatas=[{"category": node.category} for node in node_descriptions],
            )

            # Step 4: Query
            query_embedding = embedding_client.generate_embedding("memory")
            results = temp_client.query(
                collection_name="perf_test",
                query_embeddings=[query_embedding],
                n_results=5,
            )

            elapsed_time = time.time() - start_time

            # ASSERT
            assert elapsed_time < 10.0, f"End-to-end pipeline took {elapsed_time:.2f}s, expected <10s"
            assert len(node_descriptions) == 87
            assert len(results["ids"][0]) > 0

        finally:
            # Cleanup
            try:
                temp_client.delete_collection("perf_test")
            except Exception:
                pass
