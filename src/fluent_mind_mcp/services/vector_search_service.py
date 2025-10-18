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
    CATEGORY_FILTER_THRESHOLD_REDUCTION = 0.8  # Reduce threshold by 20% when category filter provides precision
    FILTER_FETCH_MULTIPLIER = 2  # Fetch extra results to account for threshold filtering

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

        # Parse base_classes from comma-separated string
        base_classes_str = metadata.get("base_classes", "")
        base_classes = [cls.strip() for cls in base_classes_str.split(",")] if base_classes_str else []

        return {
            "node_name": metadata["name"],
            "name": metadata["name"],
            "label": metadata["label"],
            "category": metadata["category"],
            "description": truncated_description,
            "base_classes": base_classes,
            "deprecated": metadata.get("deprecated", False),
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
        max_results: int = DEFAULT_NODE_LIMIT,
        similarity_threshold: float = 0.7,
        category: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """Search for nodes using semantic similarity (User Story 1).

        Args:
            query: Search query text
            max_results: Maximum number of results (default 5)
            similarity_threshold: Minimum relevance score (default 0.7)
            category: Optional category filter (e.g., "Chat Models")

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

        if max_results == 0:
            return []

        # Generate query embedding
        query_embedding = self.embedder.generate_embedding(query)

        # Calculate fetch count and effective threshold
        has_category = category is not None
        fetch_count = self._calculate_fetch_count(max_results, similarity_threshold, has_category)
        effective_threshold = self._calculate_effective_threshold(similarity_threshold, has_category)

        # Query vector database
        filter_metadata = {"category": category} if has_category else None
        raw_results = self.vector_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=fetch_count,
            where=filter_metadata
        )

        # Filter, format, sort, and limit results
        formatted_results = self._filter_and_format_results(raw_results, effective_threshold)
        sorted_results = self._sort_by_deprecated_and_relevance(formatted_results)
        return sorted_results[:max_results]

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

    def _calculate_fetch_count(self, max_results: int, similarity_threshold: float, has_category: bool) -> int:
        """Calculate how many results to fetch from vector DB.

        Args:
            max_results: Maximum results requested by caller
            similarity_threshold: Similarity threshold for filtering
            has_category: Whether category filter is applied

        Returns:
            Number of results to fetch (may be higher than max_results to account for filtering)

        WHY: Fetches extra results when filtering is applied to ensure we have enough
             results after threshold and deprecated node filtering.
        """
        if similarity_threshold > 0.0 or has_category:
            return max_results * self.FILTER_FETCH_MULTIPLIER
        return max_results

    def _calculate_effective_threshold(self, similarity_threshold: float, has_category: bool) -> float:
        """Calculate effective similarity threshold based on whether category filter is applied.

        Args:
            similarity_threshold: Base similarity threshold
            has_category: Whether category filter is applied

        Returns:
            Effective threshold (possibly reduced if category filter provides precision)

        WHY: Category filtering already provides precision, so we can be more lenient
             with relevance threshold to avoid filtering out good matches.
        """
        if has_category:
            return similarity_threshold * self.CATEGORY_FILTER_THRESHOLD_REDUCTION
        return similarity_threshold

    def _filter_and_format_results(
        self,
        raw_results: dict[str, Any],
        effective_threshold: float
    ) -> list[dict[str, Any]]:
        """Filter and format raw vector DB results by relevance threshold.

        Args:
            raw_results: Raw results from ChromaDB query
            effective_threshold: Minimum relevance score to include

        Returns:
            List of formatted results that meet threshold

        WHY: Separates result formatting and filtering logic for clarity and testability.
        """
        if not raw_results["ids"][0]:
            return []

        formatted_results = []
        for i in range(len(raw_results["ids"][0])):
            result = self._format_node_result(
                node_id=raw_results["ids"][0][i],
                metadata=raw_results["metadatas"][0][i],
                distance=raw_results["distances"][0][i],
                document=raw_results["documents"][0][i]
            )

            if result["relevance_score"] >= effective_threshold:
                formatted_results.append(result)

        return formatted_results

    def _sort_by_deprecated_and_relevance(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Sort results with deprecated nodes last, then by relevance within each group.

        Args:
            results: List of formatted search results

        Returns:
            Sorted list (non-deprecated first, each group sorted by relevance DESC)

        WHY: Prioritizes actively maintained nodes over deprecated ones while
             maintaining relevance ordering within each group.
        """
        results.sort(key=lambda x: (x.get("deprecated", False), -x["relevance_score"]))
        return results

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
