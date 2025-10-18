"""Initialize ChromaDB with required collections for chatflow automation.

Creates and configures all vector database collections with proper schemas.

WHY: Ensures consistent database structure across all environments and provides
     a single source of truth for collection configuration.
"""

from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient


# Collection configurations from data-model.md
COLLECTION_CONFIGS = {
    "nodes": {
        "description": "Flowise node descriptions with semantic search support",
        "schema": {
            "node_id": "str - Unique identifier (e.g., 'chatOpenAI', 'bufferMemory')",
            "name": "str - Human-readable name",
            "description": "str - Rich documentation (what, why, how, use cases)",
            "category": "str - Node category (Agents, Memory, etc.)",
            "version": "str - Node version",
        },
    },
    "templates": {
        "description": "Pre-built chatflow templates with semantic search support",
        "schema": {
            "template_id": "str - Unique template identifier",
            "name": "str - Template name",
            "description": "str - Template purpose and use cases",
            "category": "str - Template category (Simple, RAG, etc.)",
            "node_count": "int - Number of nodes in template",
            "flowData": "JSON - Complete flowData structure (never sent to AI)",
        },
    },
    "sdd_artifacts": {
        "description": "Spec-Driven Development artifacts (P2 - Phase 2)",
        "schema": {
            "artifact_id": "str - Unique artifact ID",
            "chatflow_name": "str - Associated chatflow name",
            "spec_content": "str - Specification content",
            "timestamp": "datetime - Creation timestamp",
        },
    },
    "failed_artifacts": {
        "description": "Failed chatflow attempts for learning system (P2 - Phase 2)",
        "schema": {
            "attempt_id": "str - Unique attempt ID",
            "chatflow_name": "str - Attempted chatflow name",
            "error_message": "str - Failure reason",
            "timestamp": "datetime - Failure timestamp",
        },
    },
    "sessions": {
        "description": "Workflow session state for complex chatflows (P2 - Phase 2)",
        "schema": {
            "session_id": "str - Unique session ID",
            "user_request": "str - Original user request",
            "state": "str - Current workflow state",
            "timestamp": "datetime - Session start time",
        },
    },
}


def initialize_collections(persist_directory: str = "chroma_db") -> list[str]:
    """Initialize all ChromaDB collections with proper configuration.

    Args:
        persist_directory: Directory for ChromaDB persistence

    Returns:
        List of created collection names

    WHY: Single entry point for database initialization ensures consistency
         across development, testing, and production environments.
    """
    client = VectorDatabaseClient(persist_directory=persist_directory)
    created_collections = []

    for collection_name, config in COLLECTION_CONFIGS.items():
        # Create collection with metadata
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": config["description"],
                "schema": str(config["schema"]),
            },
        )
        created_collections.append(collection_name)
        print(f"✓ Collection '{collection_name}' initialized")
        print(f"  Description: {config['description']}")

    return created_collections


def health_check(persist_directory: str = "chroma_db") -> dict[str, bool]:
    """Verify all collections exist and are accessible.

    Args:
        persist_directory: Directory for ChromaDB persistence

    Returns:
        Dictionary of collection names to health status

    WHY: Quick verification that database is properly initialized and
         all required collections are accessible.
    """
    client = VectorDatabaseClient(persist_directory=persist_directory)
    health_status = {}

    existing_collections = client.list_collections()

    for collection_name in COLLECTION_CONFIGS.keys():
        health_status[collection_name] = collection_name in existing_collections

    return health_status


def main() -> None:
    """Main entry point for database initialization.

    WHY: Allows script to be run standalone for initial setup or testing.
    """
    print("Initializing ChromaDB collections...")
    created = initialize_collections()
    print(f"\n✓ Successfully initialized {len(created)} collections")

    print("\nRunning health check...")
    status = health_check()
    all_healthy = all(status.values())

    print("\nCollection Health Status:")
    for collection, is_healthy in status.items():
        status_icon = "✓" if is_healthy else "✗"
        print(f"  {status_icon} {collection}: {'OK' if is_healthy else 'MISSING'}")

    if all_healthy:
        print("\n✓ All collections are healthy and ready to use!")
    else:
        print("\n✗ Some collections are missing or inaccessible")
        exit(1)


if __name__ == "__main__":
    main()
