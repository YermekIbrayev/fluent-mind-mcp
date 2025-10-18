# Layer 2: Vector Search Service

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: VectorSearchService implementation

---

## VectorSearchService (vector_service.py)

```python
class VectorSearchService:
    """
    Service for semantic search of nodes and templates.

    WHY: Separates search logic from MCP interface, enables testing
    DEPENDENCIES: VectorDatabaseClient, EmbeddingClient
    """

    def __init__(self,
                 vector_db_client: VectorDatabaseClient,
                 embedding_client: EmbeddingClient):
        self.vector_db = vector_db_client
        self.embeddings = embedding_client

    async def search_nodes(self,
                          query: str,
                          category: Optional[str] = None,
                          limit: int = 5) -> List[NodeSummary]:
        """
        Search nodes collection with semantic similarity.

        WHY: Returns compact summaries (<30 tokens each) for AI consumption
        ALGORITHM: Generate query embedding, cosine similarity search, filter by category
        PERFORMANCE: <500ms per NFR-010
        """
        # 1. Generate embedding for query
        query_embedding = await self.embeddings.generate_embedding(query)

        # 2. Search vector DB with filters
        filters = {"category": category} if category else None
        results = await self.vector_db.search(
            collection="nodes",
            query_embedding=query_embedding,
            n_results=limit,
            filters=filters
        )

        # 3. Convert to compact NodeSummary format
        return [self._to_node_summary(r) for r in results]

    async def search_templates(self,
                              query: str,
                              limit: int = 3) -> List[TemplateSummary]:
        """
        Search templates collection with semantic similarity.

        WHY: Returns metadata (template_id, name, description) not full flowData
        TOKEN EFFICIENCY: <50 tokens per result
        """
        query_embedding = await self.embeddings.generate_embedding(query)
        results = await self.vector_db.search(
            collection="templates",
            query_embedding=query_embedding,
            n_results=limit
        )
        return [self._to_template_summary(r) for r in results]
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 2 Build Flow Service →](04-layer2-build-flow-service.md)
