# Layer 2: Node Catalog Service

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: NodeCatalogService with dynamic node catalog refresh

---

## NodeCatalogService (node_catalog_service.py)

```python
class NodeCatalogService:
    """
    Service for managing Flowise node catalog with caching.

    WHY: Ensures AI always works with latest node versions and deprecation status
    TRIGGER: On-demand lazy loading (checks staleness >24h before build_flow)
    DEPENDENCIES: FlowiseApiClient, VectorDatabaseClient, EmbeddingClient
    """

    async def ensure_fresh_catalog(self) -> RefreshResult:
        """
        Check staleness and refresh if needed.

        WHY: On-demand approach per spec (user waits ~30s if refresh needed)
        STALENESS THRESHOLD: 24 hours
        FALLBACK: Uses cached data with warning if refresh fails
        """
        cache_metadata = await self._get_cache_metadata()

        if self._is_stale(cache_metadata):
            return await self.refresh_catalog()

        return RefreshResult(refreshed=False, reason="cache_fresh")

    async def refresh_catalog(self) -> RefreshResult:
        """
        Fetch latest nodes from Flowise and update vector DB.

        WHY: Detects new/updated/removed/deprecated nodes
        ALGORITHM:
        1. Query Flowise API /api/v1/nodes-list
        2. Compare with cached nodes (detect changes)
        3. Generate embeddings for new/updated nodes
        4. Update vector DB (incremental if <30% changed, else full rebuild per NFR-017)
        5. Update cache metadata
        PERFORMANCE: <30s for 100-200 nodes per NFR-015
        """
        try:
            # 1. Query Flowise API
            nodes = await self.flowise.list_nodes()

            # 2. Detect changes
            changes = await self._detect_changes(nodes)

            # 3. Generate embeddings for new/updated nodes
            if changes.new_nodes or changes.updated_nodes:
                docs = changes.new_nodes + changes.updated_nodes
                embeddings = await self.embeddings.generate_batch_embeddings(
                    [n.description for n in docs]
                )

            # 4. Apply changes to vector DB
            await self._apply_changes(changes, embeddings)

            # 5. Update cache metadata
            await self._update_cache_metadata(timestamp=datetime.now())

            return RefreshResult(refreshed=True, changes=changes)

        except Exception as e:
            # Fallback to cached data with staleness warning
            return RefreshResult(
                refreshed=False,
                error=str(e),
                fallback=True,
                warning="Using stale cache - Flowise server unreachable"
            )
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Layer 2 Circuit Breaker & Workflow Services →](06-layer2-circuit-workflow-services.md)
