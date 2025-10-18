# Layer 3: Client Layer

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: FlowiseApiClient, VectorDatabaseClient, EmbeddingClient

---

## FlowiseApiClient (flowise_client.py)

```python
class FlowiseApiClient:
    """
    HTTP client for Flowise API operations.

    WHY: Reuses existing implementation from 001-flowise-mcp-server
    ADDITIONS: GET /api/v1/nodes-list for node catalog refresh
    CONNECTION POOLING: max_connections=20, max_keepalive=10
    """

    async def list_nodes(self) -> List[NodeMetadata]:
        """
        Fetch complete node catalog from Flowise server.

        WHY: Enables dynamic node catalog refresh
        ENDPOINT: GET /api/v1/nodes-list
        RESPONSE: Array of node metadata (name, version, baseClasses, category, description, deprecated)
        """
        response = await self.client.get(f"{self.base_url}/api/v1/nodes-list")
        response.raise_for_status()
        return [NodeMetadata(**node) for node in response.json()]
```

---

## VectorDatabaseClient (vector_db_client.py)

```python
class VectorDatabaseClient:
    """
    Client for ChromaDB vector database operations.

    WHY: Encapsulates vector DB logic, enables testing with mock
    STORAGE: Persistent in project folder
    COLLECTIONS: nodes, templates, sdd_artifacts, failed_artifacts, sessions
    """

    def __init__(self, persistence_path: str):
        self.client = chromadb.PersistentClient(path=persistence_path)
        self._ensure_collections()

    def _ensure_collections(self):
        """
        Create required collections if not exist.

        WHY: Separate collections per entity type (faster queries, clear boundaries per spec)
        """
        for collection_name in ["nodes", "templates", "sdd_artifacts", "failed_artifacts", "sessions"]:
            self.client.get_or_create_collection(collection_name)

    async def search(self,
                    collection: str,
                    query_embedding: List[float],
                    n_results: int,
                    filters: Optional[Dict] = None) -> List[SearchResult]:
        """
        Perform semantic similarity search.

        WHY: Core vector search operation for all use cases
        ALGORITHM: Cosine distance similarity
        PERFORMANCE: <500ms per NFR-010
        """
        collection_obj = self.client.get_collection(collection)
        results = collection_obj.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filters
        )
        return self._parse_results(results)
```

---

## EmbeddingClient (embedding_client.py)

```python
class EmbeddingClient:
    """
    Wrapper for sentence-transformers embedding model.

    WHY: Encapsulates model loading, caching, batch operations
    MODEL: sentence-transformers/all-MiniLM-L6-v2 (384-dimensional embeddings)
    INITIALIZATION: Automatic download on first use per FR-000
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None  # Lazy load

    def _load_model(self):
        """
        Load embedding model (lazy initialization).

        WHY: Automatic download on first use, cache to avoid reloading
        FALLBACK: Clear error message if download fails
        """
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
        except Exception as e:
            raise EmbeddingModelError(
                f"Failed to load embedding model {self.model_name}. "
                f"Ensure internet connection and sentence-transformers installed. Error: {e}"
            )

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate 384-dimensional embedding for single text"""
        if not self.model:
            self._load_model()
        return self.model.encode(text).tolist()

    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts (more efficient)"""
        if not self.model:
            self._load_model()
        return self.model.encode(texts).tolist()
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 4 Models →](08-layer4-models.md)
