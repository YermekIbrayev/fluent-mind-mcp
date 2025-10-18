"""Unit tests for VectorDatabaseClient (Phase 1 - T011).

Tests ChromaDB client wrapper functionality.

Coverage:
- Collection creation and management
- Document addition with embeddings
- Vector similarity queries
- Update and delete operations
- HNSW indexing configuration
- Performance validation (<500ms for 50-1000 entries)

WHY: Validates core vector database operations for semantic search.
"""

import time
from pathlib import Path

import pytest

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient


@pytest.fixture
def test_db_path(tmp_path):
    """Create temporary database path for testing."""
    db_path = tmp_path / "test_chroma"
    return str(db_path)


@pytest.fixture
def client(test_db_path):
    """Create VectorDatabaseClient instance for testing."""
    return VectorDatabaseClient(persist_directory=test_db_path)


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorDatabaseClientCollectionManagement:
    """Test collection creation and management operations."""

    def test_get_or_create_collection_creates_new_collection(self, client):
        """Verify new collection is created with HNSW config."""
        collection = client.get_or_create_collection("nodes")

        assert collection is not None
        assert collection.name == "nodes"
        assert "nodes" in client.list_collections()

    def test_get_or_create_collection_returns_existing_collection(self, client):
        """Verify get_or_create is idempotent."""
        collection1 = client.get_or_create_collection("nodes")
        collection2 = client.get_or_create_collection("nodes")

        assert collection1.name == collection2.name

    def test_delete_collection_removes_collection(self, client):
        """Verify collection deletion works."""
        client.get_or_create_collection("test_collection")
        assert "test_collection" in client.list_collections()

        client.delete_collection("test_collection")

        assert "test_collection" not in client.list_collections()

    def test_list_collections_returns_all_names(self, client):
        """Verify list_collections returns all collection names."""
        client.get_or_create_collection("col1")
        client.get_or_create_collection("col2")

        collections = client.list_collections()

        assert "col1" in collections
        assert "col2" in collections


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorDatabaseClientDocumentOperations:
    """Test document addition, update, and deletion."""

    def test_add_documents_stores_with_embeddings(self, client):
        """Verify documents are stored correctly."""
        client.add_documents(
            collection_name="nodes",
            documents=["chatbot with memory", "document search"],
            embeddings=[[0.1] * 384, [0.2] * 384],
            ids=["node1", "node2"],
            metadatas=[{"type": "chat"}, {"type": "retrieval"}],
        )

        collection = client.get_collection("nodes")
        assert collection.count() == 2

    def test_add_documents_validates_length_mismatch(self, client):
        """Verify length mismatch raises error."""
        with pytest.raises(ValueError, match="Array length mismatch"):
            client.add_documents(
                collection_name="nodes",
                documents=["doc1", "doc2"],
                embeddings=[[0.1] * 384],  # Wrong length
                ids=["id1", "id2"],
            )

    def test_add_documents_validates_metadata_length(self, client):
        """Verify metadata length validation."""
        with pytest.raises(ValueError, match="Metadata length"):
            client.add_documents(
                collection_name="nodes",
                documents=["doc1", "doc2"],
                embeddings=[[0.1] * 384, [0.2] * 384],
                ids=["id1", "id2"],
                metadatas=[{"type": "test"}],  # Wrong length
            )

    def test_update_document_changes_metadata(self, client):
        """Verify document update works."""
        # Add initial document
        client.add_documents(
            collection_name="nodes",
            documents=["test"],
            embeddings=[[0.1] * 384],
            ids=["node1"],
            metadatas=[{"version": "1.0"}],
        )

        # Update metadata
        client.update_document(
            collection_name="nodes",
            document_id="node1",
            metadata={"version": "2.0"},
        )

        # Verify update
        collection = client.get_collection("nodes")
        result = collection.get(ids=["node1"], include=["metadatas"])
        assert result["metadatas"][0]["version"] == "2.0"


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorDatabaseClientQueryOperations:
    """Test vector similarity query functionality."""

    def test_query_returns_top_k_results(self, client):
        """Verify query returns correct number of results."""
        # Add 10 documents
        docs = [f"document {i}" for i in range(10)]
        embeddings = [[i / 10.0] * 384 for i in range(10)]
        ids = [f"doc{i}" for i in range(10)]

        client.add_documents("nodes", docs, embeddings, ids)

        # Query for top 5
        results = client.query(
            collection_name="nodes",
            query_embeddings=[[0.5] * 384],
            n_results=5,
        )

        assert len(results["ids"][0]) == 5
        assert len(results["documents"][0]) == 5
        assert len(results["distances"][0]) == 5

    def test_query_with_metadata_filter(self, client):
        """Verify metadata filtering works."""
        client.add_documents(
            collection_name="nodes",
            documents=["chat node", "memory node", "retrieval node"],
            embeddings=[[0.1] * 384, [0.2] * 384, [0.3] * 384],
            ids=["node1", "node2", "node3"],
            metadatas=[
                {"category": "Chat"},
                {"category": "Memory"},
                {"category": "Chat"},
            ],
        )

        results = client.query(
            collection_name="nodes",
            query_embeddings=[[0.1] * 384],
            n_results=10,
            where={"category": "Chat"},
        )

        # Should only return Chat nodes
        assert len(results["ids"][0]) == 2
        for metadata in results["metadatas"][0]:
            assert metadata["category"] == "Chat"

    def test_query_returns_results_sorted_by_distance(self, client):
        """Verify results are sorted by similarity."""
        client.add_documents(
            collection_name="nodes",
            documents=["doc1", "doc2", "doc3"],
            embeddings=[[0.1] * 384, [0.5] * 384, [0.3] * 384],
            ids=["id1", "id2", "id3"],
        )

        results = client.query(
            collection_name="nodes",
            query_embeddings=[[0.2] * 384],
            n_results=3,
        )

        distances = results["distances"][0]
        assert distances == sorted(distances), "Results not sorted by distance"


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorDatabaseClientPerformance:
    """Test performance requirements (NFR-093)."""

    def test_query_50_entries_completes_within_500ms(self, client):
        """Verify query performance with 50 documents."""
        # Add 50 documents
        docs = [f"document {i}" for i in range(50)]
        embeddings = [[i / 50.0] * 384 for i in range(50)]
        ids = [f"doc{i}" for i in range(50)]
        client.add_documents("nodes", docs, embeddings, ids)

        # Measure query performance
        start = time.time()
        client.query("nodes", [[0.5] * 384], n_results=5)
        duration = (time.time() - start) * 1000

        assert duration < 500, f"Query took {duration:.2f}ms, expected <500ms"

    def test_query_1000_entries_completes_within_500ms(self, client):
        """Verify HNSW performance at scale."""
        # Add 1000 documents
        docs = [f"document {i}" for i in range(1000)]
        embeddings = [[i / 1000.0] * 384 for i in range(1000)]
        ids = [f"doc{i}" for i in range(1000)]
        client.add_documents("nodes", docs, embeddings, ids)

        # Measure query performance
        start = time.time()
        client.query("nodes", [[0.5] * 384], n_results=5)
        duration = (time.time() - start) * 1000

        assert duration < 500, f"Query took {duration:.2f}ms, expected <500ms"


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorDatabaseClientHNSWConfiguration:
    """Test HNSW indexing configuration."""

    def test_collection_uses_cosine_similarity(self, client):
        """Verify HNSW space is set to cosine."""
        collection = client.get_or_create_collection("nodes")

        # Check metadata (ChromaDB stores HNSW config in metadata)
        assert collection.metadata.get("hnsw:space") == "cosine"

    def test_hnsw_construction_ef_configured(self, client):
        """Verify construction_ef parameter is set."""
        collection = client.get_or_create_collection("nodes")

        assert collection.metadata.get("hnsw:construction_ef") == 100


@pytest.mark.unit
@pytest.mark.phase1
class TestVectorDatabaseClientErrorHandling:
    """Test error handling and edge cases."""

    def test_query_nonexistent_collection_raises_error(self, client):
        """Verify querying nonexistent collection raises error."""
        with pytest.raises(ValueError, match="does not exist"):
            client.query("nonexistent", [[0.1] * 384])

    def test_get_nonexistent_collection_raises_error(self, client):
        """Verify getting nonexistent collection raises error."""
        with pytest.raises(ValueError, match="does not exist"):
            client.get_collection("nonexistent")


@pytest.mark.integration
@pytest.mark.phase1
class TestVectorDatabaseClientPersistence:
    """Integration tests for persistence."""

    def test_persistence_across_client_instances(self, test_db_path):
        """Verify data persists across client instances."""
        # Write data
        client1 = VectorDatabaseClient(persist_directory=test_db_path)
        client1.add_documents(
            "nodes",
            ["test data"],
            [[0.1] * 384],
            ["node1"],
        )

        # Read from new instance
        client2 = VectorDatabaseClient(persist_directory=test_db_path)
        collection = client2.get_collection("nodes")

        assert collection.count() == 1
