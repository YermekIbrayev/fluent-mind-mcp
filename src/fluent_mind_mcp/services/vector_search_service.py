"""Vector search service for nodes and templates.

Provides semantic search functionality for Phase 1 User Stories 1-2.

WHY: Core service layer that orchestrates embedding generation and
     vector database queries for semantic node and template discovery.
"""

from typing import Any, Optional

from fluent_mind_mcp.client.embedding_client import EmbeddingClient
from fluent_mind_mcp.client.vector_db_client import VectorDatabaseClient
from fluent_mind_mcp.utils.exceptions import ValidationError


class VectorSearchService:
    """Service for searching nodes and templates using vector similarity.

    Orchestrates embedding generation and ChromaDB queries.

    WHY: Provides high-level search API with relevance scoring,
         token budgeting, and metadata filtering.
    """

    # Constants
    DEFAULT_TOKEN_BUDGET = 50
    CHARS_PER_TOKEN = 4
    COSINE_DISTANCE_MAX = 2.0
    TAG_BOOST_SCORE = 0.2
    DEFAULT_NODE_LIMIT = 5
    DEFAULT_TEMPLATE_LIMIT = 3
    TEMPLATE_FETCH_MULTIPLIER = 2

    def __init__(
        self,
        vector_db_client: VectorDatabaseClient,
        embedding_client: EmbeddingClient
    ) -> None:
        """Initialize vector search service.

        Args:
            vector_db_client: ChromaDB client for vector queries
            embedding_client: Embedding client for query vectorization

        WHY: Dependency injection enables testing with mocks.
        """
        self.vector_db = vector_db_client
        self.embedder = embedding_client

    def _validate_query(self, query: str) -> None:
        """Validate search query input.

        Args:
            query: Search query to validate

        Raises:
            ValidationError: If query is empty or whitespace-only

        WHY: Centralized validation prevents invalid queries early.
        """
        if not query or not query.strip():
            raise ValidationError("Search query cannot be empty")

    def _calculate_relevance_score(self, distance: float) -> float:
        """Convert cosine distance to relevance score.

        Args:
            distance: Cosine distance from ChromaDB (0-2 range)

        Returns:
            Relevance score (0.0-1.0, where 1.0 is perfect match)

        WHY: Normalizes distance to intuitive relevance metric.
             Cosine distance: 0=identical, 2=opposite
        """
        return max(0.0, 1.0 - (distance / self.COSINE_DISTANCE_MAX))

    def _format_node_result(
        self,
        node_id: str,
        metadata: dict[str, Any],
        distance: float,
        document: str
    ) -> dict[str, Any]:
        """Format single node search result.

        Args:
            node_id: Node identifier
            metadata: Node metadata from ChromaDB
            distance: Cosine distance
            document: Node description

        Returns:
            Formatted result dictionary

        WHY: Separates formatting logic from search orchestration.
        """
        relevance_score = self._calculate_relevance_score(distance)
        truncated_description = self._truncate_to_token_budget(
            document,
            max_tokens=self.DEFAULT_TOKEN_BUDGET
        )

        return {
            "name": metadata["name"],
            "label": metadata["label"],
            "category": metadata["category"],
            "description": truncated_description,
            "relevance_score": round(relevance_score, 3)
        }

    def _format_template_result_with_boost(
        self,
        template_id: str,
        metadata: dict[str, Any],
        distance: float,
        document: str,
        query: str
    ) -> dict[str, Any]:
        """Format template result with tag-based relevance boosting.

        Args:
            template_id: Template identifier
            metadata: Template metadata from ChromaDB
            distance: Cosine distance
            document: Template description
            query: Original search query (for tag matching)

        Returns:
            Formatted result dictionary with boosted relevance

        WHY: Tag boosting improves precision by leveraging explicit metadata.
        """
        base_relevance = self._calculate_relevance_score(distance)

        # Tag boosting: +0.2 relevance if query matches any tag
        tags = metadata.get("tags", "").split(",") if metadata.get("tags") else []
        query_lower = query.lower()
        tag_boost = self.TAG_BOOST_SCORE if any(
            tag.lower() in query_lower for tag in tags
        ) else 0.0

        relevance_score = min(1.0, base_relevance + tag_boost)

        truncated_description = self._truncate_to_token_budget(
            document,
            max_tokens=self.DEFAULT_TOKEN_BUDGET
        )

        return {
            "template_id": metadata["template_id"],
            "name": metadata["name"],
            "description": truncated_description,
            "tags": tags,
            "node_count": metadata.get("node_count", 0),
            "complexity_level": metadata.get("complexity_level", "unknown"),
            "relevance_score": round(relevance_score, 3)
        }

    async def search_nodes(
        self,
        query: str,
        limit: int = DEFAULT_NODE_LIMIT,
        filter_metadata: Optional[dict[str, Any]] = None
    ) -> list[dict[str, Any]]:
        """Search for nodes using semantic similarity (User Story 1).

        Args:
            query: Search query text
            limit: Maximum number of results
            filter_metadata: Optional metadata filters (e.g., {"category": "Chat Models"})

        Returns:
            List of node results with metadata and relevance scores

        Raises:
            ValidationError: If query is empty or invalid

        Performance: <5s per NFR-020
        Accuracy: >90% per NFR-093

        WHY: Core search functionality for discovering relevant nodes
             based on natural language descriptions.
        """
        self._validate_query(query)

        if limit == 0:
            return []

        # Generate query embedding
        query_embedding = self.embedder.generate_embedding(query)

        # Query vector database
        results = self.vector_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=limit,
            where=filter_metadata
        )

        # Format results
        if not results["ids"][0]:  # No results
            return []

        return [
            self._format_node_result(
                node_id=results["ids"][0][i],
                metadata=results["metadatas"][0][i],
                distance=results["distances"][0][i],
                document=results["documents"][0][i]
            )
            for i in range(len(results["ids"][0]))
        ]

    async def search_templates(
        self,
        query: str,
        limit: int = DEFAULT_TEMPLATE_LIMIT
    ) -> list[dict[str, Any]]:
        """Search for templates using semantic similarity with tag boosting (User Story 2).

        Args:
            query: Search query text
            limit: Maximum number of results

        Returns:
            List of template results with metadata and preview info

        Performance: <5s per NFR-020
        Accuracy: >90% per NFR-093

        WHY: Template discovery based on natural language intent with
             tag-based relevance boosting for precision.
        """
        self._validate_query(query)

        if limit == 0:
            return []

        # Generate query embedding
        query_embedding = self.embedder.generate_embedding(query)

        # Query vector database (fetch extra for tag-based re-ranking)
        results = self.vector_db.query(
            collection_name="templates",
            query_embeddings=[query_embedding],
            n_results=limit * self.TEMPLATE_FETCH_MULTIPLIER
        )

        if not results["ids"][0]:  # No results
            return []

        # Format and boost by tag matches
        formatted_results = [
            self._format_template_result_with_boost(
                template_id=results["ids"][0][i],
                metadata=results["metadatas"][0][i],
                distance=results["distances"][0][i],
                document=results["documents"][0][i],
                query=query
            )
            for i in range(len(results["ids"][0]))
        ]

        # Re-rank by boosted relevance and limit
        formatted_results.sort(key=lambda x: x["relevance_score"], reverse=True)

        return formatted_results[:limit]

    def _truncate_to_token_budget(self, text: str, max_tokens: int = DEFAULT_TOKEN_BUDGET) -> str:
        """Truncate text to approximate token budget.

        Args:
            text: Text to truncate
            max_tokens: Maximum tokens

        Returns:
            Truncated text with ellipsis if needed

        WHY: Respects NFR-026 token efficiency by limiting response size.
             Uses ~4 chars per token heuristic (conservative).
        """
        max_chars = max_tokens * self.CHARS_PER_TOKEN

        if len(text) <= max_chars:
            return text

        # Truncate and add ellipsis
        return text[:max_chars - 3] + "..."
