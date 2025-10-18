"""ChromaDB test utilities for Phase 1 functional tests.

Provides helper functions for:
- Database reset and cleanup
- Test data population
- Health checks
- Collection management

WHY: Enables fast, reliable test execution with consistent state.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import List, Optional

import chromadb
from chromadb.config import Settings
from chromadb.errors import NotFoundError


class ChromaDBTestUtilities:
    """Helper utilities for ChromaDB testing."""

    # Standard collections for Phase 1
    COLLECTIONS = ["nodes", "templates", "sdd_artifacts", "failed_artifacts", "sessions"]

    def __init__(self, test_db_path: Optional[str] = None):
        """Initialize test utilities.

        Args:
            test_db_path: Path to test database (creates temp if None)

        WHY: Isolates test database from production data.
        """
        if test_db_path is None:
            self.test_db_path = tempfile.mkdtemp(prefix="chromadb_test_")
        else:
            self.test_db_path = test_db_path

        self.client = chromadb.PersistentClient(
            path=self.test_db_path,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True  # Enable reset for testing
            )
        )

    def reset_all_collections(self, collections: Optional[List[str]] = None) -> None:
        """Clear all test collections to clean state.

        Args:
            collections: List of collection names (defaults to COLLECTIONS)

        Performance: <10s per NFR-090

        WHY: Provides clean slate for each test run.
        """
        collections = collections or self.COLLECTIONS

        for collection_name in collections:
            try:
                # Delete collection if it exists
                self.client.delete_collection(name=collection_name)
            except (ValueError, NotFoundError):
                # Collection doesn't exist, that's fine
                pass

    def create_all_collections(self, collections: Optional[List[str]] = None) -> None:
        """Create all test collections with proper metadata.

        Args:
            collections: List of collection names (defaults to COLLECTIONS)

        WHY: Ensures consistent collection structure across tests.
        """
        collections = collections or self.COLLECTIONS

        metadata_configs = {
            "nodes": {
                "description": "Node descriptions for vector search",
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 100,
                "hnsw:M": 16
            },
            "templates": {
                "description": "Flow templates for chatflow creation",
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 100,
                "hnsw:M": 16
            },
            "sdd_artifacts": {
                "description": "Spec-driven design artifacts (Phase 2)",
                "hnsw:space": "cosine"
            },
            "failed_artifacts": {
                "description": "Failed generation attempts for learning (Phase 2)",
                "hnsw:space": "cosine"
            },
            "sessions": {
                "description": "User session data for context (Phase 2)",
                "hnsw:space": "cosine"
            }
        }

        for collection_name in collections:
            try:
                self.client.create_collection(
                    name=collection_name,
                    metadata=metadata_configs.get(collection_name, {})
                )
            except ValueError:
                # Collection already exists
                pass

    def get_collection_count(self, collection_name: str) -> int:
        """Get number of documents in a collection.

        Args:
            collection_name: Name of collection to check

        Returns:
            Number of documents in collection

        WHY: Validates data population for tests.
        """
        try:
            collection = self.client.get_collection(name=collection_name)
            return collection.count()
        except ValueError:
            return 0

    def populate_nodes(self, node_data: List[dict]) -> None:
        """Populate nodes collection with test data.

        Args:
            node_data: List of node metadata dictionaries

        WHY: Sets up vector search test data.
        """
        collection = self.client.get_or_create_collection(
            name="nodes",
            metadata={"hnsw:space": "cosine"}
        )

        ids = [node["name"] for node in node_data]
        documents = [node["description"] for node in node_data]
        metadatas = [
            {
                "name": node["name"],
                "label": node["label"],
                "category": node["category"],
                "version": node.get("version", "1.0.0")
            }
            for node in node_data
        ]

        # Add to collection (ChromaDB will generate embeddings if needed)
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def populate_templates(self, template_data: List[dict]) -> None:
        """Populate templates collection with test data.

        Args:
            template_data: List of template metadata dictionaries

        WHY: Sets up template search test data.
        """
        collection = self.client.get_or_create_collection(
            name="templates",
            metadata={"hnsw:space": "cosine"}
        )

        ids = [template["template_id"] for template in template_data]
        documents = [template["description"] for template in template_data]
        metadatas = [
            {
                "template_id": template["template_id"],
                "name": template["name"],
                "tags": ",".join(template.get("tags", []))
            }
            for template in template_data
        ]

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def check_system_health(self) -> dict:
        """Validate system dependencies and database health.

        Returns:
            Health status dictionary

        Performance: <5s per NFR-091

        WHY: Pre-test validation ensures system ready for testing.
        """
        health = {
            "chromadb_accessible": False,
            "collections_created": False,
            "nodes_count": 0,
            "templates_count": 0
        }

        try:
            # Check ChromaDB accessibility
            self.client.heartbeat()
            health["chromadb_accessible"] = True

            # Check collections exist
            collections = [col.name for col in self.client.list_collections()]
            health["collections_created"] = all(
                col in collections for col in ["nodes", "templates"]
            )

            # Check data counts
            health["nodes_count"] = self.get_collection_count("nodes")
            health["templates_count"] = self.get_collection_count("templates")

        except Exception as e:
            health["error"] = str(e)

        return health

    def cleanup(self) -> None:
        """Clean up test database.

        WHY: Removes temporary test data and prevents disk bloat.
        """
        try:
            # Delete all collections
            self.reset_all_collections()
        except Exception:
            pass

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()


# Pytest fixtures for easy test integration
def pytest_chromadb_helper():
    """Pytest fixture for ChromaDB test utilities.

    Usage:
        def test_something(chromadb_helper):
            chromadb_helper.reset_all_collections()
            # ... test code ...

    WHY: Simplifies test setup and ensures cleanup.
    """
    helper = ChromaDBTestUtilities()
    yield helper
    helper.cleanup()
