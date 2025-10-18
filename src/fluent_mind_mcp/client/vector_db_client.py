"""ChromaDB client for vector database operations.

Provides vector storage and similarity search functionality.

WHY: Core component for semantic search - stores embeddings and performs
     fast similarity queries using HNSW indexing.
"""

from pathlib import Path
from typing import Any, Optional

import chromadb
from chromadb.config import Settings
from chromadb.errors import NotFoundError
from chromadb.utils import embedding_functions


class VectorDatabaseClient:
    """Client for ChromaDB vector database operations.

    Uses persistent storage with HNSW indexing for fast similarity search.

    WHY: Provides reliable vector storage and <500ms query performance
         for 50-1000 document collections.
    """

    def __init__(self, persist_directory: str = "chroma_db") -> None:
        """Initialize ChromaDB client with persistent storage.

        Args:
            persist_directory: Directory for ChromaDB persistence (relative to project root)

        WHY: Local persistence ensures data survives restarts and provides
             predictable performance for MCP server use cases.
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize persistent ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False),
        )
        self.circuit_breaker: Optional[object] = None  # Placeholder for Phase 4

    def get_or_create_collection(
        self,
        name: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> chromadb.Collection:
        """Get existing collection or create new one with HNSW indexing.

        Args:
            name: Collection name
            metadata: Optional collection metadata

        Returns:
            ChromaDB Collection instance

        WHY: HNSW (Hierarchical Navigable Small World) provides optimal
             balance of speed and accuracy for similarity search.
        """
        return self.client.get_or_create_collection(
            name=name,
            metadata={
                **(metadata or {}),
                "hnsw:space": "cosine",  # Cosine similarity for normalized embeddings
                "hnsw:construction_ef": 100,  # Build-time accuracy parameter
                "hnsw:M": 16,  # Graph connectivity (higher = more accurate, slower)
            },
        )

    def add_documents(
        self,
        collection_name: str,
        documents: list[str],
        embeddings: list[list[float]],
        ids: list[str],
        metadatas: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        """Add documents to collection with embeddings.

        Args:
            collection_name: Target collection
            documents: Document texts
            embeddings: Pre-computed embeddings (384-dimensional)
            ids: Unique document IDs
            metadatas: Optional metadata for each document

        Raises:
            ValueError: If array lengths don't match

        WHY: Batch insertion is more efficient than individual adds and
             ensures atomicity for related documents.
        """
        if not (len(documents) == len(embeddings) == len(ids)):
            raise ValueError(
                f"Array length mismatch: documents={len(documents)}, "
                f"embeddings={len(embeddings)}, ids={len(ids)}"
            )

        if metadatas is not None and len(metadatas) != len(documents):
            raise ValueError(
                f"Metadata length ({len(metadatas)}) doesn't match documents ({len(documents)})"
            )

        collection = self.get_or_create_collection(collection_name)
        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    def query(
        self,
        collection_name: str,
        query_embeddings: list[list[float]],
        n_results: int = 5,
        where: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Query collection for similar documents.

        Args:
            collection_name: Collection to search
            query_embeddings: Query embedding vectors
            n_results: Number of results to return
            where: Optional metadata filters

        Returns:
            Query results with ids, documents, distances, metadatas

        WHY: Optimized for <500ms queries on 50-1000 doc collections
             using HNSW approximate nearest neighbor search.
        """
        try:
            collection = self.client.get_collection(collection_name)
        except (ValueError, NotFoundError) as e:
            raise ValueError(f"Collection '{collection_name}' does not exist") from e

        return collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where,
        )

    def update_document(
        self,
        collection_name: str,
        document_id: str,
        document: Optional[str] = None,
        embedding: Optional[list[float]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Update existing document in collection.

        Args:
            collection_name: Target collection
            document_id: Document ID to update
            document: Updated document text (optional)
            embedding: Updated embedding (optional)
            metadata: Updated metadata (optional)

        WHY: Allows incremental updates without full re-indexing.
        """
        collection = self.get_or_create_collection(collection_name)
        collection.update(
            ids=[document_id],
            documents=[document] if document else None,
            embeddings=[embedding] if embedding else None,
            metadatas=[metadata] if metadata else None,
        )

    def delete_collection(self, name: str) -> None:
        """Delete collection and all its documents.

        Args:
            name: Collection name to delete

        WHY: Cleanup operation for testing and maintenance.
        """
        self.client.delete_collection(name)

    def get_collection(self, name: str) -> chromadb.Collection:
        """Get existing collection.

        Args:
            name: Collection name

        Returns:
            ChromaDB Collection instance

        Raises:
            ValueError: If collection doesn't exist

        WHY: Direct collection access for advanced operations.
        """
        try:
            return self.client.get_collection(name)
        except (ValueError, NotFoundError) as e:
            raise ValueError(f"Collection '{name}' does not exist") from e

    def list_collections(self) -> list[str]:
        """List all collection names.

        Returns:
            List of collection names

        WHY: Useful for health checks and debugging.
        """
        collections = self.client.list_collections()
        return [c.name for c in collections]
