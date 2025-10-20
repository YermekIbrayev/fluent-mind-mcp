"""
Unit tests for ChromaDB storage and retrieval operations.

Tests the VectorDatabaseClient for storing node embeddings and performing
vector similarity searches. All tests are TDD-RED phase - they should FAIL
until the implementation (T056a) is complete.

Test coverage:
- Store nodes with embeddings and metadata
- Retrieve nodes by ID
- Update vs. add logic (incremental updates)
- Vector similarity search with relevance scoring
- Top-k result limiting
- Performance validation (<2s for 87 nodes)
- Error handling for edge cases

WHY: These tests define the contract for how nodes are stored in ChromaDB,
     ensuring that vector search results are accurate and performant.
"""

import time
import pytest
import numpy as np
from typing import Any

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.client.embedding_client import EmbeddingClient


class TestNodeStorage:
    """Test storing nodes with embeddings and metadata."""

    @pytest.fixture
    def db_client(self, tmp_path):
        """Provide VectorDatabaseClient with temporary storage."""
        persist_dir = str(tmp_path / "test_chroma_db")
        client = VectorDatabaseClient(persist_directory=persist_dir)
        yield client
        # Cleanup: Delete test collection after test
        try:
            client.delete_collection("nodes")
        except Exception:
            pass

    @pytest.fixture
    def embedding_client(self):
        """Provide EmbeddingClient for generating embeddings."""
        return EmbeddingClient()

    def test_store_node_with_embedding(self, db_client, embedding_client):
        """Add document to nodes collection with embedding and metadata.

        WHY: Validates that nodes can be stored with complete metadata
             (label, category, base_classes, deprecated) for later retrieval.
        """
        # Arrange
        node_name = "chatOpenAI"
        label = "ChatOpenAI"
        description = "Wrapper around OpenAI large language models for chat applications"
        category = "Chat Models"
        base_classes = ["BaseChatModel", "BaseLanguageModel"]
        deprecated = False

        # Generate embedding for the node description
        embedding = embedding_client.generate_embedding(description)

        # Act - Store node using add_documents (existing method)
        db_client.add_documents(
            collection_name="nodes",
            documents=[description],
            embeddings=[embedding],
            ids=[node_name],
            metadatas=[{
                "label": label,
                "category": category,
                "base_classes": ",".join(base_classes),  # Store as comma-separated string
                "deprecated": deprecated
            }]
        )

        # Assert - Verify node was stored by querying it back
        collection = db_client.get_collection("nodes")
        result = collection.get(ids=[node_name])

        assert len(result["ids"]) == 1
        assert result["ids"][0] == node_name
        assert result["documents"][0] == description
        assert result["metadatas"][0]["label"] == label
        assert result["metadatas"][0]["category"] == category
        assert result["metadatas"][0]["base_classes"] == ",".join(base_classes)
        assert result["metadatas"][0]["deprecated"] == deprecated

    def test_store_node_metadata_complete(self, db_client, embedding_client):
        """Metadata includes label, category, base_classes, deprecated.

        WHY: Ensures all required metadata fields are stored correctly
             for filtering and display purposes.
        """
        # Arrange
        nodes_data = [
            {
                "node_name": "bufferMemory",
                "label": "Buffer Memory",
                "description": "Maintains a buffer of recent conversation messages",
                "category": "Memory",
                "base_classes": ["BaseMemory", "Runnable"],
                "deprecated": False
            },
            {
                "node_name": "conversationChain",
                "label": "Conversation Chain",
                "description": "Chain for having a conversation with memory",
                "category": "Chains",
                "base_classes": ["LLMChain", "Chain"],
                "deprecated": True  # Test deprecated flag
            }
        ]

        # Generate embeddings for all nodes
        embeddings = [
            embedding_client.generate_embedding(node["description"])
            for node in nodes_data
        ]

        # Act - Store multiple nodes
        db_client.add_documents(
            collection_name="nodes",
            documents=[node["description"] for node in nodes_data],
            embeddings=embeddings,
            ids=[node["node_name"] for node in nodes_data],
            metadatas=[
                {
                    "label": node["label"],
                    "category": node["category"],
                    "base_classes": ",".join(node["base_classes"]),
                    "deprecated": node["deprecated"]
                }
                for node in nodes_data
            ]
        )

        # Assert - Verify all metadata fields are stored correctly
        collection = db_client.get_collection("nodes")
        for node in nodes_data:
            result = collection.get(ids=[node["node_name"]])
            metadata = result["metadatas"][0]

            assert metadata["label"] == node["label"]
            assert metadata["category"] == node["category"]
            assert metadata["base_classes"] == ",".join(node["base_classes"])
            assert metadata["deprecated"] == node["deprecated"]


class TestNodeRetrieval:
    """Test retrieving nodes by ID and updating existing nodes."""

    @pytest.fixture
    def db_client(self, tmp_path):
        """Provide VectorDatabaseClient with temporary storage."""
        persist_dir = str(tmp_path / "test_chroma_db")
        client = VectorDatabaseClient(persist_directory=persist_dir)
        yield client
        try:
            client.delete_collection("nodes")
        except Exception:
            pass

    @pytest.fixture
    def embedding_client(self):
        """Provide EmbeddingClient."""
        return EmbeddingClient()

    def test_retrieve_node_by_id(self, db_client, embedding_client):
        """Query by node_name returns correct document.

        WHY: Validates that nodes can be retrieved by their unique ID
             for exact lookups.
        """
        # Arrange - Store a node first
        node_name = "chatOpenAI"
        description = "OpenAI chat model wrapper"
        embedding = embedding_client.generate_embedding(description)

        db_client.add_documents(
            collection_name="nodes",
            documents=[description],
            embeddings=[embedding],
            ids=[node_name],
            metadatas=[{"label": "ChatOpenAI"}]
        )

        # Act - Retrieve node by ID
        collection = db_client.get_collection("nodes")
        result = collection.get(ids=[node_name])

        # Assert
        assert len(result["ids"]) == 1
        assert result["ids"][0] == node_name
        assert result["documents"][0] == description
        assert result["metadatas"][0]["label"] == "ChatOpenAI"

    def test_update_existing_node(self, db_client, embedding_client):
        """update_document updates existing entry without creating duplicate.

        WHY: Validates that incremental updates work correctly - updating
             a node's description or metadata doesn't create duplicates.
        """
        # Arrange - Store initial node
        node_name = "chatOpenAI"
        original_description = "OpenAI chat model"
        original_embedding = embedding_client.generate_embedding(original_description)

        db_client.add_documents(
            collection_name="nodes",
            documents=[original_description],
            embeddings=[original_embedding],
            ids=[node_name],
            metadatas=[{"label": "ChatOpenAI", "version": "1.0"}]
        )

        # Act - Update the node with new description
        updated_description = "Advanced OpenAI chat model with streaming"
        updated_embedding = embedding_client.generate_embedding(updated_description)

        db_client.update_document(
            collection_name="nodes",
            document_id=node_name,
            document=updated_description,
            embedding=updated_embedding,
            metadata={"label": "ChatOpenAI", "version": "2.0"}
        )

        # Assert - Verify only one document exists (no duplicates)
        collection = db_client.get_collection("nodes")
        result = collection.get(ids=[node_name])

        assert len(result["ids"]) == 1, "Should have exactly one document (no duplicates)"
        assert result["documents"][0] == updated_description
        assert result["metadatas"][0]["version"] == "2.0"

    def test_add_new_node(self, db_client, embedding_client):
        """Adding a new node (not updating) creates new entry.

        WHY: Validates that add_documents correctly adds new nodes
             when they don't already exist.
        """
        # Arrange
        nodes = [
            ("chatOpenAI", "OpenAI chat model"),
            ("bufferMemory", "Buffer memory for conversations"),
        ]

        # Act - Add both nodes
        for node_name, description in nodes:
            embedding = embedding_client.generate_embedding(description)
            db_client.add_documents(
                collection_name="nodes",
                documents=[description],
                embeddings=[embedding],
                ids=[node_name],
                metadatas=[{"label": node_name}]
            )

        # Assert - Verify both nodes exist
        collection = db_client.get_collection("nodes")
        all_results = collection.get()

        assert len(all_results["ids"]) == 2
        assert "chatOpenAI" in all_results["ids"]
        assert "bufferMemory" in all_results["ids"]

    def test_incremental_update_preserves_others(self, db_client, embedding_client):
        """Updating one node doesn't affect other nodes.

        WHY: Ensures that incremental updates are isolated and don't
             corrupt or delete unrelated nodes.
        """
        # Arrange - Store multiple nodes
        nodes = [
            ("chatOpenAI", "OpenAI chat model"),
            ("bufferMemory", "Buffer memory"),
            ("conversationChain", "Conversation chain"),
        ]

        for node_name, description in nodes:
            embedding = embedding_client.generate_embedding(description)
            db_client.add_documents(
                collection_name="nodes",
                documents=[description],
                embeddings=[embedding],
                ids=[node_name],
                metadatas=[{"label": node_name, "version": "1.0"}]
            )

        # Act - Update only the middle node
        updated_description = "Advanced buffer memory with windowing"
        updated_embedding = embedding_client.generate_embedding(updated_description)
        db_client.update_document(
            collection_name="nodes",
            document_id="bufferMemory",
            document=updated_description,
            embedding=updated_embedding,
            metadata={"label": "bufferMemory", "version": "2.0"}
        )

        # Assert - Verify other nodes unchanged
        collection = db_client.get_collection("nodes")

        # Check that we still have 3 nodes
        all_results = collection.get()
        assert len(all_results["ids"]) == 3

        # Check that bufferMemory was updated
        buffer_result = collection.get(ids=["bufferMemory"])
        assert buffer_result["documents"][0] == updated_description
        assert buffer_result["metadatas"][0]["version"] == "2.0"

        # Check that other nodes are unchanged
        chat_result = collection.get(ids=["chatOpenAI"])
        assert chat_result["metadatas"][0]["version"] == "1.0"

        conv_result = collection.get(ids=["conversationChain"])
        assert conv_result["metadatas"][0]["version"] == "1.0"


class TestVectorSearch:
    """Test vector similarity search with relevance scoring."""

    @pytest.fixture
    def db_client(self, tmp_path):
        """Provide VectorDatabaseClient with temporary storage."""
        persist_dir = str(tmp_path / "test_chroma_db")
        client = VectorDatabaseClient(persist_directory=persist_dir)
        yield client
        try:
            client.delete_collection("nodes")
        except Exception:
            pass

    @pytest.fixture
    def embedding_client(self):
        """Provide EmbeddingClient."""
        return EmbeddingClient()

    @pytest.fixture
    def populated_db(self, db_client, embedding_client):
        """Populate database with test nodes for search."""
        nodes = [
            {
                "node_name": "bufferMemory",
                "label": "Buffer Memory",
                "description": "Maintains a buffer of recent conversation messages in memory",
                "category": "Memory"
            },
            {
                "node_name": "bufferWindowMemory",
                "label": "Buffer Window Memory",
                "description": "Keeps last K conversation messages in a sliding window memory buffer",
                "category": "Memory"
            },
            {
                "node_name": "conversationMemory",
                "label": "Conversation Memory",
                "description": "Stores entire conversation history in memory for context",
                "category": "Memory"
            },
            {
                "node_name": "chatOpenAI",
                "label": "ChatOpenAI",
                "description": "OpenAI chat model for conversational AI applications",
                "category": "Chat Models"
            },
            {
                "node_name": "conversationChain",
                "label": "Conversation Chain",
                "description": "Chain for managing conversations with language models",
                "category": "Chains"
            },
        ]

        # Store all nodes
        for node in nodes:
            embedding = embedding_client.generate_embedding(node["description"])
            db_client.add_documents(
                collection_name="nodes",
                documents=[node["description"]],
                embeddings=[embedding],
                ids=[node["node_name"]],
                metadatas=[{
                    "label": node["label"],
                    "category": node["category"]
                }]
            )

        return db_client

    def test_vector_search_relevance(self, populated_db, embedding_client):
        """Query 'memory' returns relevant nodes (score >0.7).

        WHY: Validates that vector search returns semantically relevant
             results with high similarity scores.
        """
        # Arrange
        query = "memory for storing conversation history"
        query_embedding = embedding_client.generate_embedding(query)

        # Act - Search for memory-related nodes
        results = populated_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=5
        )

        # Assert - Verify relevant nodes are returned
        returned_ids = results["ids"][0]
        distances = results["distances"][0]

        # Convert distances to similarity scores (ChromaDB uses cosine distance: distance = 1 - similarity)
        similarity_scores = [1 - d for d in distances]

        # Check that we got results
        assert len(returned_ids) > 0, "Should return at least one result"

        # Check that memory-related nodes are in top results
        assert any("memory" in node_id.lower() for node_id in returned_ids[:3]), \
            "Top 3 results should include memory-related nodes"

        # Check that top results have high similarity (>0.7)
        assert similarity_scores[0] > 0.7, \
            f"Top result should have similarity >0.7, got {similarity_scores[0]:.3f}"

    def test_vector_search_ranking(self, populated_db, embedding_client):
        """Results ordered by similarity score (descending).

        WHY: Ensures that search results are properly ranked by relevance,
             with most similar results first.
        """
        # Arrange
        query = "buffer memory window"
        query_embedding = embedding_client.generate_embedding(query)

        # Act
        results = populated_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=5
        )

        # Assert - Verify results are ordered by distance (ascending = similarity descending)
        distances = results["distances"][0]

        # Distances should be in ascending order (lower distance = higher similarity)
        for i in range(len(distances) - 1):
            assert distances[i] <= distances[i + 1], \
                f"Results not properly ranked: distance[{i}]={distances[i]:.3f} > distance[{i+1}]={distances[i+1]:.3f}"

    def test_vector_search_top_k(self, populated_db, embedding_client):
        """max_results parameter limits results correctly.

        WHY: Validates that the n_results parameter correctly limits
             the number of returned results.
        """
        # Arrange
        query = "conversation memory"
        query_embedding = embedding_client.generate_embedding(query)

        # Act - Request only top 3 results
        results = populated_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=3
        )

        # Assert
        assert len(results["ids"][0]) == 3, "Should return exactly 3 results"
        assert len(results["distances"][0]) == 3

        # Act - Request top 2 results
        results_2 = populated_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=2
        )

        # Assert
        assert len(results_2["ids"][0]) == 2, "Should return exactly 2 results"

    def test_vector_search_no_results(self, db_client, embedding_client):
        """Query with no matches returns empty list.

        WHY: Validates error handling when searching an empty collection
             or when no documents match the query.
        """
        # Arrange - Create empty collection
        db_client.get_or_create_collection("nodes")
        query = "nonexistent query"
        query_embedding = embedding_client.generate_embedding(query)

        # Act - Search empty collection
        results = db_client.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=5
        )

        # Assert - Should return empty results
        assert len(results["ids"][0]) == 0, "Empty collection should return no results"
        assert len(results["distances"][0]) == 0


class TestHealthAndPerformance:
    """Test health checks and performance validation."""

    @pytest.fixture
    def db_client(self, tmp_path):
        """Provide VectorDatabaseClient with temporary storage."""
        persist_dir = str(tmp_path / "test_chroma_db")
        client = VectorDatabaseClient(persist_directory=persist_dir)
        yield client
        try:
            client.delete_collection("nodes")
        except Exception:
            pass

    @pytest.fixture
    def embedding_client(self):
        """Provide EmbeddingClient."""
        return EmbeddingClient()

    def test_health_check_query(self, db_client, embedding_client):
        """Verify collection accessible and contains documents.

        WHY: Health check ensures the database is operational and
             contains expected data.
        """
        # Arrange - Store test documents
        nodes = [
            ("node1", "Test node 1"),
            ("node2", "Test node 2"),
            ("node3", "Test node 3"),
        ]

        for node_name, description in nodes:
            embedding = embedding_client.generate_embedding(description)
            db_client.add_documents(
                collection_name="nodes",
                documents=[description],
                embeddings=[embedding],
                ids=[node_name],
                metadatas=[{"label": node_name}]
            )

        # Act - Perform health check by getting collection and counting documents
        collection = db_client.get_collection("nodes")
        all_docs = collection.get()

        # Assert
        assert collection is not None, "Collection should exist"
        assert len(all_docs["ids"]) == 3, "Should have 3 documents"
        assert len(all_docs["ids"]) == len(all_docs["documents"])
        assert len(all_docs["ids"]) == len(all_docs["metadatas"])

    def test_storage_performance(self, db_client, embedding_client):
        """Store 87 nodes in <2s.

        WHY: Validates that batch storage is performant enough for
             initial DB population and incremental updates.
        """
        # Arrange - Generate 87 test nodes
        nodes = []
        for i in range(87):
            nodes.append({
                "node_name": f"node_{i}",
                "description": f"Test node {i} with unique description for embedding generation variety",
            })

        # Generate embeddings for all nodes (batch)
        descriptions = [node["description"] for node in nodes]
        embeddings = embedding_client.batch_embed(descriptions)

        # Act - Store all 87 nodes and measure time
        start_time = time.time()
        db_client.add_documents(
            collection_name="nodes",
            documents=descriptions,
            embeddings=embeddings,
            ids=[node["node_name"] for node in nodes],
            metadatas=[{"label": node["node_name"]} for node in nodes]
        )
        elapsed_time = time.time() - start_time

        # Assert
        assert elapsed_time < 2.0, \
            f"Storage took {elapsed_time:.2f}s, expected <2s"

        # Verify all nodes were stored
        collection = db_client.get_collection("nodes")
        all_docs = collection.get()
        assert len(all_docs["ids"]) == 87, "Should have stored all 87 nodes"
