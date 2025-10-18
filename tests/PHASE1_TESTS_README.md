# Phase 1 Functional Tests - Complete Test Suite

**Created**: 2025-10-17
**Feature**: 002-flowise-automation-workflow Phase 1
**Deliverable**: Vector search + template-based chatflow creation

---

## Overview

This test suite provides comprehensive coverage for Phase 1 implementation, including:

- **Unit Tests**: Individual component validation (TDD-style)
- **Integration Tests**: End-to-end workflow validation
- **Manual Test Checklists**: Human-executed acceptance testing

All tests follow the **test-driven development (TDD)** approach - they define expected behavior and will guide implementation.

---

## Test Structure

```
tests/
├── utilities/
│   ├── test_data_generator.py          # Sample data generation
│   └── chromadb_helpers.py             # ChromaDB test utilities
├── unit/phase1/
│   ├── test_embedding_client.py        # EmbeddingClient tests (T010)
│   ├── test_vector_db_client.py        # VectorDatabaseClient tests (T011)
│   ├── test_vector_search_service.py   # VectorSearchService tests (US1, US2)
│   └── test_build_flow_service.py      # BuildFlowService tests (US3)
├── integration/phase1/
│   └── test_phase1_end_to_end.py       # Complete Phase 1 workflows
├── checklists/
│   ├── user_story_1_checklist.md       # Manual tests for US1
│   ├── user_story_2_checklist.md       # Manual tests for US2
│   └── user_story_3_checklist.md       # Manual tests for US3
└── conftest.py                          # Shared fixtures
```

---

## Test Categories

### 1. Unit Tests (TDD-Style)

**Purpose**: Define expected behavior for each component to guide implementation.

**Status**: All tests currently skip with `pytest.skip("Implementation pending")` - they will pass once components are implemented.

#### test_embedding_client.py (T010)
- **Coverage**: 20 test cases
- **Key Tests**:
  - Embedding generation (384 dimensions)
  - Batch embedding support
  - Performance validation (<50ms per embedding)
  - Semantic similarity preservation
  - Error handling (empty input, None)
- **Integration Tests**: 2 (with real sentence-transformers model)

#### test_vector_db_client.py (T011)
- **Coverage**: 18 test cases
- **Key Tests**:
  - Collection management (create, get, delete)
  - Document operations (add, update, query)
  - HNSW configuration (cosine similarity, ef=100, M=16)
  - Performance validation (<500ms for 50-1000 entries)
  - Error handling (nonexistent collections, mismatched arrays)
- **Integration Tests**: 2 (with real ChromaDB)

#### test_vector_search_service.py (US1, US2)
- **Coverage**: 16 test cases
- **Key Tests**:
  - Node search with semantic matching
  - Template search with tag boosting
  - Accuracy validation (>90% per NFR-093)
  - Response token budgeting (<50 tokens per result)
  - Category filtering
  - Edge cases (empty query, no results)
- **Integration Tests**: 2 (end-to-end search)

#### test_build_flow_service.py (US3)
- **Coverage**: 10 test cases
- **Key Tests**:
  - Build from template
  - FlowData structure validation
  - Node positioning (left-to-right, 300px spacing)
  - Success rate validation (>95% per NFR-093)
  - Unique node IDs
  - Error handling (nonexistent template)
- **Integration Tests**: 1 (with Flowise API)

**Total Unit Tests**: 64 test cases

---

### 2. Integration Tests

**Purpose**: Validate complete Phase 1 workflows end-to-end.

#### test_phase1_end_to_end.py
- **User Story 1 Tests** (3 scenarios):
  - Search chatbot with memory nodes
  - Search document retrieval nodes
  - Performance validation (<5s)

- **User Story 2 Tests** (2 scenarios):
  - Search simple chatbot template
  - Search RAG template

- **User Story 3 Tests** (3 scenarios):
  - Build simple chat from template
  - Build RAG flow from template
  - Performance validation (<10s)

- **Complete Workflow Tests** (2 scenarios):
  - End-to-end user journey (search → search → build)
  - Full workflow performance (<60s)

**Total Integration Tests**: 10 scenarios

---

### 3. Manual Test Checklists

**Purpose**: Human-executed acceptance testing for Phase 1 deliverable.

#### user_story_1_checklist.md (Vector Search Nodes)
- **Scenarios**: 6 + Accuracy Validation
- **Covers**:
  - Chatbot with memory search
  - Document retrieval search
  - Agent/tool search
  - Performance testing
  - Empty query handling
  - Category filtering
  - Accuracy validation (>90%)

#### user_story_2_checklist.md (Template Search)
- **Scenarios**: 7 + Accuracy Validation
- **Covers**:
  - Simple chatbot template search
  - RAG template search
  - Agent template search
  - Tag-based boosting
  - Metadata preview validation
  - Performance testing
  - Empty query handling

#### user_story_3_checklist.md (Build from Template)
- **Scenarios**: 7 + Success Rate + E2E
- **Covers**:
  - Build simple chat
  - Build RAG flow
  - Build agent with tools
  - Node positioning validation
  - Performance testing
  - Error handling
  - FlowData validation
  - Success rate validation (>95%)
  - Complete Phase 1 workflow

**Total Manual Scenarios**: 20 + validations

---

## Test Utilities

### test_data_generator.py

**Provides**:
- `generate_node_descriptions(count=20)`: Creates diverse node metadata
  - Predefined templates: 14 semantic categories
  - Categories: Chat Models, Memory, Tools, Chains, Agents, Retrievers, etc.

- `generate_flow_templates(count=10)`: Creates flow templates
  - Predefined patterns: simple_chat, rag_flow, agent_with_tools

- `get_test_queries()`: Ground truth for accuracy validation
  - 5 queries with expected node matches

- `get_template_queries()`: Template search validation
  - 4 queries with expected template matches

### chromadb_helpers.py

**Provides**:
- `ChromaDBTestUtilities`: Helper class for ChromaDB testing
  - `reset_all_collections()`: Clean state for tests
  - `create_all_collections()`: Initialize 5 collections
  - `populate_nodes()`: Add node test data
  - `populate_templates()`: Add template test data
  - `check_system_health()`: Pre-test validation (<5s)
  - Context manager support for automatic cleanup

### conftest.py Fixtures

**Shared Fixtures**:
- `chromadb_helper`: ChromaDB test utilities with cleanup
- `test_data_generator`: Test data generation
- `populated_chromadb`: Pre-populated ChromaDB instance
- `test_db_path`: Temporary database path

---

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install -e ".[test]"

# Install Phase 1 dependencies
pip install chromadb sentence-transformers

# Configure Flowise (for integration tests)
export FLOWISE_API_URL=http://localhost:3000
export FLOWISE_API_KEY=your-key-here
```

### Run Unit Tests

```bash
# Run all Phase 1 unit tests
pytest tests/unit/phase1/ -v

# Run specific component tests
pytest tests/unit/phase1/test_embedding_client.py -v
pytest tests/unit/phase1/test_vector_db_client.py -v
pytest tests/unit/phase1/test_vector_search_service.py -v
pytest tests/unit/phase1/test_build_flow_service.py -v

# Run only fast tests (skip integration)
pytest tests/unit/phase1/ -v -m "not slow"
```

### Run Integration Tests

```bash
# Run all Phase 1 integration tests (requires Flowise)
pytest tests/integration/phase1/ -v

# Skip if Flowise not available
pytest tests/integration/phase1/ -v --skipif-not-configured
```

### Run All Phase 1 Tests

```bash
# Complete Phase 1 test suite
pytest tests/unit/phase1/ tests/integration/phase1/ -v
```

### Manual Testing

```bash
# Open checklists and follow step-by-step
open tests/checklists/user_story_1_checklist.md
open tests/checklists/user_story_2_checklist.md
open tests/checklists/user_story_3_checklist.md
```

---

## Test Markers

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.phase1        # Phase 1 specific
@pytest.mark.slow          # Test takes >5 seconds
@pytest.mark.asyncio       # Async test
```

**Usage**:
```bash
# Run only unit tests
pytest -m "unit and phase1" -v

# Run only integration tests
pytest -m "integration and phase1" -v

# Skip slow tests
pytest -m "not slow" -v
```

---

## Success Criteria

### Phase 1 Acceptance

To ACCEPT Phase 1 implementation, all of the following must pass:

**Automated Tests**:
- [ ] All unit tests pass (64/64)
- [ ] All integration tests pass (10/10)

**Manual Validation**:
- [ ] US1 accuracy >90% (14+ out of 14 expected nodes found)
- [ ] US2 accuracy >90% (5+ out of 5 expected templates found)
- [ ] US3 success rate >95% (10+ out of 10 templates build successfully)

**Performance**:
- [ ] Vector search <5s (NFR-020)
- [ ] Template build <10s (NFR-022)
- [ ] Complete workflow <60s

**Quality**:
- [ ] No P0/P1 defects outstanding
- [ ] All manual checklists completed

---

## Next Steps

### For Implementers

1. **Start with Unit Tests**: Implement components to make unit tests pass
   - EmbeddingClient (T010) → test_embedding_client.py
   - VectorDatabaseClient (T011) → test_vector_db_client.py
   - VectorSearchService → test_vector_search_service.py
   - BuildFlowService → test_build_flow_service.py

2. **Run Integration Tests**: Validate end-to-end workflows

3. **Execute Manual Checklists**: Human validation of acceptance criteria

### For Testers

1. **Review Test Cases**: Familiarize with test scenarios
2. **Prepare Test Environment**: ChromaDB, Flowise, test data
3. **Execute Manual Checklists**: Document results
4. **Report Defects**: Use checklist defect tables
5. **Sign-off**: Approve/reject Phase 1 acceptance

---

## Maintenance

### Adding New Tests

1. **Unit Tests**: Add to `tests/unit/phase1/test_<component>.py`
2. **Integration Tests**: Add to `tests/integration/phase1/test_phase1_end_to_end.py`
3. **Manual Tests**: Update checklists in `tests/checklists/`

### Updating Test Data

1. Edit `test_data_generator.py`:
   - Add nodes to `NODE_TEMPLATES`
   - Add templates to `TEMPLATE_PATTERNS`
   - Update `get_test_queries()` for accuracy validation

2. Update expected values in tests

---

## References

- **Feature Spec**: `specs/002-flowise-automation-workflow/spec.md`
- **Implementation Plan**: `specs/002-flowise-automation-workflow/plan_cc.md`
- **Task Breakdown**: `specs/002-flowise-automation-workflow/tasks/01-setup-foundational.md`
- **Testing Strategy**: `specs/002-flowise-automation-workflow/10-testing-manual-checklists.md`

---

**Test Suite Version**: 1.0.0
**Author**: Claude Code
**Date**: 2025-10-17
