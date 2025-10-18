# Testing Strategy: Automated Tests & Utilities

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: Automated critical path tests and test utilities

---

## Automated Critical Path Tests (NFR-088, NFR-093)

### test_vector_search_accuracy.py

```python
import pytest
from src.fluent_mind_mcp.services.vector_service import VectorSearchService

@pytest.mark.asyncio
async def test_vector_search_relevance_90_percent():
    """
    Validate >90% relevance for known queries (NFR-093).

    WHY: Ensures vector search meets quality threshold
    """
    service = VectorSearchService(vector_db_client, embedding_client)

    test_cases = [
        ("chat with memory", ["ChatOpenAI", "BufferMemory", "ConversationChain"]),
        ("search documents", ["DocumentLoader", "VectorStore", "RetrievalQA"]),
        ("AI agent", ["Agent", "ToolAgent", "ConversationalAgent"])
    ]

    for query, expected_nodes in test_cases:
        results = await service.search_nodes(query, limit=5)
        relevance = calculate_relevance(results, expected_nodes)
        assert relevance > 0.9, f"Query '{query}': expected >90% relevance, got {relevance*100:.1f}%"
```

---

### test_build_flow_creation.py

```python
@pytest.mark.asyncio
async def test_build_flow_success_rate_95_percent():
    """
    Validate >95% success rate for template-based flows (NFR-093).

    WHY: Ensures build_flow reliability threshold
    """
    service = BuildFlowService(vector_db_client, flowise_client, node_catalog_service)

    templates = await get_all_templates()
    success_count = 0
    failures = []

    for template in templates:
        try:
            result = await service.build_from_template(template.template_id)
            assert result.chatflow_id is not None
            success_count += 1
        except Exception as e:
            failures.append((template.template_id, str(e)))

    success_rate = success_count / len(templates)
    assert success_rate > 0.95, f"Expected >95% success rate, got {success_rate*100:.1f}%"

    if failures:
        print(f"Failed templates: {failures}")
```

---

### test_circuit_breaker_transitions.py

```python
@pytest.mark.asyncio
async def test_circuit_breaker_state_transitions_100_percent():
    """
    Validate 100% correct state transitions (NFR-093).

    WHY: Circuit breaker must be reliable for resilience
    """
    cb = CircuitBreaker("test_dependency", failure_threshold=3, timeout_seconds=5)

    # Test CLOSED → OPEN after 3 failures
    for i in range(3):
        try:
            await cb.call(lambda: raise_error())
        except:
            pass
    assert cb.state == CircuitState.OPEN

    # Test OPEN → HALF_OPEN after timeout
    await asyncio.sleep(6)
    try:
        await cb.call(lambda: "test")
    except:
        pass
    assert cb.state == CircuitState.HALF_OPEN

    # Test HALF_OPEN → CLOSED on success
    result = await cb.call(lambda: "success")
    assert cb.state == CircuitState.CLOSED
```

---

## Test Utilities (NFR-089, NFR-090, NFR-091)

### test_data_generator.py

```python
class TestDataGenerator:
    """Generate realistic sample data for testing (NFR-089)"""

    @staticmethod
    def generate_node_descriptions(count: int = 20) -> List[NodeMetadata]:
        """Generate semantically diverse node descriptions"""
        categories = ["Chat Models", "Memory", "Tools", "Chains", "Agents", "Retrievers"]
        return [
            NodeMetadata(
                name=f"node_{i}",
                label=f"Node {i}",
                version="1.0.0",
                category=random.choice(categories),
                base_classes=[f"Base{random.choice(categories).replace(' ', '')}"],
                description=f"Test node for {random.choice(['chat', 'memory', 'retrieval', 'tools'])}",
                deprecated=False
            )
            for i in range(count)
        ]

    @staticmethod
    def generate_flow_templates(count: int = 10) -> List[FlowTemplate]:
        """Generate flow templates with various complexity levels"""
        return [...]  # Implementation details

    @staticmethod
    def generate_sdd_artifacts(count: int = 15) -> List[ArtifactBundle]:
        """Generate SDD artifacts with semantic variations"""
        return [...]  # Implementation details
```

---

### test_utilities.py

```python
class ChromaDBTestUtilities:
    """Helper functions for test execution"""

    @staticmethod
    async def reset_chromadb(collections: List[str]):
        """
        Clear all collections to clean state (NFR-090: <10s).

        WHY: Enables fast test iteration with consistent starting state
        """
        client = chromadb.PersistentClient(path=TEST_DB_PATH)
        for collection_name in collections:
            collection = client.get_collection(collection_name)
            collection.delete(where={})  # Delete all documents

    @staticmethod
    async def validate_system_health() -> HealthStatus:
        """
        Check dependencies, circuits, DB accessibility (NFR-091: <5s).

        WHY: Pre-test validation ensures system ready for testing
        """
        return HealthStatus(
            chromadb_accessible=await check_chromadb(),
            flowise_accessible=await check_flowise(),
            embedding_model_loaded=await check_embedding_model(),
            circuits_status=await check_all_circuits()
        )

    @staticmethod
    async def populate_test_data():
        """Populate test data using TestDataGenerator"""
        generator = TestDataGenerator()
        nodes = generator.generate_node_descriptions(20)
        templates = generator.generate_flow_templates(10)
        # Store in ChromaDB
        await vector_db_client.add_documents("nodes", nodes)
        await vector_db_client.add_documents("templates", templates)
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Implementation Phases →](12-implementation-phases.md)
