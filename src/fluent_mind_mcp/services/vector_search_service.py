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

    # Constants with WHY explanations
    DEFAULT_TOKEN_BUDGET = 50
    # WHY: Each result should use ~50 tokens to meet NFR-002 token efficiency.
    # Allows ~20 results within 1000-token context budget.

    CHARS_PER_TOKEN = 4
    # WHY: Conservative estimate (OpenAI uses ~4 chars/token for English).
    # Ensures we don't exceed token budget when truncating text.

    COSINE_DISTANCE_MAX = 2.0
    # WHY: ChromaDB uses cosine distance where 0=identical, 2=opposite vectors.
    # This is the mathematical maximum for normalized embeddings.

    TAG_BOOST_SCORE = 0.2
    # WHY: +0.2 relevance boost for tag matches provides meaningful signal
    # without overwhelming base semantic similarity. Tested empirically.

    DEFAULT_NODE_LIMIT = 5
    # WHY: Balances discovery (enough options) with token efficiency.
    # 5 nodes × 50 tokens = 250 tokens, leaving room for context.

    DEFAULT_TEMPLATE_LIMIT = 3
    # WHY: Templates are more token-heavy than nodes (~100 tokens each).
    # 3 templates × 100 tokens = 300 tokens, similar to node budget.

    TEMPLATE_FETCH_MULTIPLIER = 2
    # WHY: Tag boosting re-ranks results, so we fetch 2x to ensure
    # best tag-matched templates appear in final top-N after sorting.

    FILTER_FETCH_MULTIPLIER = 2
    # WHY: When filtering is applied (category or threshold), we fetch 2x results
    # to ensure we have enough matches after post-processing filters.

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

    def _parse_base_classes(self, base_classes_str: str) -> list[str]:
        """Parse comma-separated base classes string.

        Args:
            base_classes_str: Comma-separated base classes (e.g., "BaseChain,LLMChain")

        Returns:
            List of trimmed base class names, empty list if input is empty

        WHY: Centralizes parsing logic for consistency and reusability.
             Handles empty strings and whitespace trimming uniformly.
        """
        if not base_classes_str:
            return []
        return [cls.strip() for cls in base_classes_str.split(",")]

    def _parse_tags(self, tags_str: str) -> list[str]:
        """Parse comma-separated tags string.

        Args:
            tags_str: Comma-separated tags (e.g., "chatbot,rag,memory")

        Returns:
            List of trimmed tag names, empty list if input is empty

        WHY: Centralizes tag parsing for consistency with base_classes parsing.
        """
        if not tags_str:
            return []
        return [tag.strip() for tag in tags_str.split(",")]

    def _parse_required_nodes(self, required_nodes_raw: Any) -> list[str]:
        """Parse required_nodes from various formats.

        Args:
            required_nodes_raw: Required nodes as list, JSON string, or CSV

        Returns:
            List of node names, empty list if input is empty

        WHY: Handles flexible storage formats (JSON array, comma-separated).
             Tries JSON first (structured), falls back to CSV parsing.
        """
        if isinstance(required_nodes_raw, list):
            return required_nodes_raw
        elif isinstance(required_nodes_raw, str) and required_nodes_raw:
            # Try JSON parsing first, fallback to comma-separated
            try:
                import json
                return json.loads(required_nodes_raw)
            except (json.JSONDecodeError, ValueError):
                return [n.strip() for n in required_nodes_raw.split(",") if n.strip()]
        return []

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
        # Calculate derived fields
        relevance_score = self._calculate_relevance_score(distance)
        truncated_description = self._truncate_to_token_budget(
            document,
            max_tokens=self.DEFAULT_TOKEN_BUDGET
        )
        base_classes = self._parse_base_classes(metadata.get("base_classes", ""))

        # WHY: Return both top-level fields (for backward compatibility with tests)
        # and metadata dict (for SearchResult model compliance). Duplication is
        # intentional to support both direct field access and structured metadata.
        return {
            "result_id": metadata["name"],  # Unique node identifier (e.g., "chatOpenAI")
            "name": metadata["label"],      # Display name (e.g., "ChatOpenAI")
            "label": metadata["label"],     # Backward compatibility
            "category": metadata["category"],
            "description": truncated_description,
            "base_classes": base_classes,
            "deprecated": metadata.get("deprecated", False),
            "relevance_score": round(relevance_score, 3),
            "metadata": {
                "category": metadata["category"],
                "base_classes": base_classes,
                "deprecated": metadata.get("deprecated", False)
            }
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
        # Calculate derived fields
        base_relevance = self._calculate_relevance_score(distance)
        tags = self._parse_tags(metadata.get("tags", ""))
        truncated_description = self._truncate_to_token_budget(
            document,
            max_tokens=self.DEFAULT_TOKEN_BUDGET
        )

        # Apply tag-based relevance boost
        query_lower = query.lower()
        tag_boost = self.TAG_BOOST_SCORE if any(
            tag.lower() in query_lower for tag in tags
        ) else 0.0
        relevance_score = min(1.0, base_relevance + tag_boost)

        # Parse required_nodes (handles JSON string, list, or comma-separated)
        required_nodes = self._parse_required_nodes(metadata.get("required_nodes", ""))

        result = {
            "result_id": metadata["template_id"],  # WHY: SearchResult expects result_id
            "template_id": metadata["template_id"],
            "name": metadata["name"],
            "description": truncated_description,
            "tags": tags,
            "node_count": metadata.get("node_count", 0),
            "complexity_level": metadata.get("complexity_level", "unknown"),
            "required_nodes": required_nodes,
            "relevance_score": round(relevance_score, 3),
            "metadata": {
                "tags": tags,
                "node_count": metadata.get("node_count", 0),
                "complexity_level": metadata.get("complexity_level", "unknown")
            }
        }

        # Add parameters_schema if present (T026 - optional field)
        if "parameters_schema" in metadata and metadata["parameters_schema"]:
            params_raw = metadata["parameters_schema"]
            if isinstance(params_raw, dict):
                result["parameters_schema"] = params_raw
            elif isinstance(params_raw, str):
                # Parse JSON string
                try:
                    import json
                    result["parameters_schema"] = json.loads(params_raw)
                except (json.JSONDecodeError, ValueError):
                    pass  # Skip invalid JSON

        return result

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

        # Calculate fetch count (fetch extra when filtering to ensure enough results)
        has_category = category is not None
        fetch_count = self._calculate_fetch_count(max_results, similarity_threshold, has_category)

        # Query vector database
        filter_metadata = {"category": category} if has_category else None
        raw_results = self.vector_db.query(
            collection_name="nodes",
            query_embeddings=[query_embedding],
            n_results=fetch_count,
            where=filter_metadata
        )

        # Filter, format, sort, and limit results
        formatted_results = self._filter_and_format_results(raw_results, similarity_threshold)
        sorted_results = self._sort_by_deprecated_and_relevance(formatted_results)
        return sorted_results[:max_results]

    async def search_templates(
        self,
        query: str,
        limit: int = DEFAULT_TEMPLATE_LIMIT,
        threshold: float = 0.7
    ) -> list[dict[str, Any]]:
        """Search for templates using semantic similarity with tag boosting (User Story 2).

        Args:
            query: Search query text
            limit: Maximum number of results
            threshold: Minimum relevance score (default 0.7)

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

        # Query vector database (fetch extra for threshold filtering and tag-based re-ranking)
        fetch_count = limit * self.TEMPLATE_FETCH_MULTIPLIER if threshold > 0.0 else limit
        results = self.vector_db.query(
            collection_name="templates",
            query_embeddings=[query_embedding],
            n_results=fetch_count
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

        # Filter by threshold
        if threshold > 0.0:
            formatted_results = [r for r in formatted_results if r["relevance_score"] >= threshold]

        # Re-rank by boosted relevance, then by complexity (fewer nodes = simpler)
        formatted_results.sort(
            key=lambda x: (-x["relevance_score"], x.get("node_count", 999))
        )

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

    def _filter_and_format_results(
        self,
        raw_results: dict[str, Any],
        similarity_threshold: float
    ) -> list[dict[str, Any]]:
        """Filter and format raw vector DB results by relevance threshold.

        Args:
            raw_results: Raw results from ChromaDB query
            similarity_threshold: Minimum relevance score to include (applied strictly)

        Returns:
            List of formatted results that meet threshold

        WHY: Separates result formatting and filtering logic for clarity and testability.
             Enforces threshold strictly to honor API contract - if user specifies 0.7,
             ALL results will be >= 0.7 (Principle of Least Surprise).
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

            # Strict threshold enforcement: honor user's expectation
            if result["relevance_score"] >= similarity_threshold:
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
