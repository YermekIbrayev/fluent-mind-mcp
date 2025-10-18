# Tasks: Setup & Foundational (T001-T013)

[← Back to Tasks Index](../tasks.md)

**Purpose**: Project initialization and core infrastructure that BLOCKS all user story work

**⚠️ File Size Rule**: Goal ≤100 lines, yellow 101-150, HARD LIMIT 200 lines (validated by T102)

---

## Phase 1: Setup (Shared Infrastructure + TDD Test Suite)

**Purpose**: Project initialization + TDD test infrastructure (74 tests)

- [X] T001 Create project structure: src/fluent_mind_mcp/{models/,services/,client/,utils/,scripts/}
- [X] T002 Create test structure: tests/{unit/phase1/,integration/phase1/,utilities/,checklists/}
- [X] T003 [P] Install dependencies: chromadb, sentence-transformers, pytest-asyncio in pyproject.toml

**TDD Test Infrastructure** (Created - All tests currently skip with "Implementation pending"):

- [X] T003a [P] Create test utilities in tests/utilities/test_data_generator.py
  - TestDataGenerator with generate_node_descriptions(20), generate_flow_templates(10)
  - get_test_queries() → 5 queries with expected nodes for >90% accuracy validation
  - get_template_queries() → 4 template queries for >90% accuracy
  - Purpose: Provides realistic test data for vector search validation

- [X] T003b [P] Create ChromaDB helpers in tests/utilities/chromadb_helpers.py
  - ChromaDBTestUtilities with reset/create/populate/health_check methods
  - Enables fast test execution (<10s reset, <5s health check per NFRs)
  - Purpose: Consistent test state management

**TDD Unit Tests Created** (64 tests - all skip until implementation):

- [X] T003c Create tests/unit/phase1/test_embedding_client.py (20 tests for T010)
  - Tests: 384-dim embeddings, batch operations, <50ms performance, semantic similarity
  - Purpose: Define EmbeddingClient API contract (Red phase)

- [X] T003d Create tests/unit/phase1/test_vector_db_client.py (18 tests for T011)
  - Tests: Collection management, CRUD ops, HNSW config, <500ms queries
  - Purpose: Define VectorDatabaseClient API contract (Red phase)

- [X] T003e Create tests/unit/phase1/test_vector_search_service.py (16 tests for US1/US2)
  - Tests: Node search, template search, >90% accuracy, token budgeting
  - Purpose: Define VectorSearchService API contract (Red phase)

- [X] T003f Create tests/unit/phase1/test_build_flow_service.py (10 tests for US3)
  - Tests: Build from template, node positioning, >95% success rate
  - Purpose: Define BuildFlowService API contract (Red phase)

**TDD Integration Tests Created** (10 scenarios):

- [X] T003g Create tests/integration/phase1/test_phase1_end_to_end.py
  - US1: 3 scenarios (chatbot memory search, doc retrieval, performance)
  - US2: 2 scenarios (simple chatbot template, RAG template)
  - US3: 3 scenarios (build simple chat, RAG flow, performance)
  - Complete workflow: 2 scenarios (E2E journey, <60s total)

**Manual Test Checklists Created** (20 scenarios):

- [X] T003h Create tests/checklists/user_story_1_checklist.md (6 + accuracy)
- [X] T003i Create tests/checklists/user_story_2_checklist.md (7 + accuracy)
- [X] T003j Create tests/checklists/user_story_3_checklist.md (7 + success rate + E2E)

**TDD Documentation**:

- [X] T003k Create tests/PHASE1_TESTS_README.md
  - Test structure overview (74 tests total)
  - Running instructions (pytest commands)
  - Success criteria (64 unit + 10 integration + 20 manual)
  - TDD workflow guidance

**Checkpoint**: ✅ Project structure + TDD test suite ready (74 tests skip, waiting for implementation)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for ALL user stories - MUST complete before ANY story work

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Models Layer (T004-T007)

All models can be created in parallel - different files, no dependencies

- [X] T004 [P] Create Pydantic models in src/fluent_mind_mcp/models/node_models.py
  - NodeMetadata, NodeDescription, NodeSummary, SearchQuery, SearchResult
  - All models include validation, docstrings, examples

- [X] T005 [P] Create template models in src/fluent_mind_mcp/models/template_models.py
  - FlowTemplate, TemplateSummary, TemplateSearchQuery, TemplateMetadata
  - Include flowData structure validation

- [X] T006 [P] Create workflow models in src/fluent_mind_mcp/models/workflow_models.py
  - ComplexityAnalysis, ChatflowSpecification, ClarificationQuestion, ImplementationPlan
  - TaskBreakdown, ConsistencyAnalysis, ChatflowDesignSummary, FeedbackLoop, WorkflowResponse

- [X] T007 [P] Create common models in src/fluent_mind_mcp/models/common_models.py
  - ChatflowResponse, Edge, Node, Position, RefreshResult, CacheMetadata
  - BuildFlowRequest, BuildFlowResponse, SystemHealth, CircuitBreakerState

### Utils Layer (T008-T009)

Utilities can be created in parallel - different concerns

- [X] T008 [P] Create custom exceptions in src/fluent_mind_mcp/utils/exceptions.py
  - ChatflowAutomationError (base exception)
  - VectorSearchError, TemplateNotFoundError, BuildFlowError, ConnectionInferenceError
  - CircuitOpenError, FlowiseApiError, VectorDatabaseError, EmbeddingError
  - Include error codes, user-friendly messages, token budgets

- [X] T009 [P] Create credential masking formatter in src/fluent_mind_mcp/utils/logging.py
  - CredentialMaskingFormatter class extending logging.Formatter
  - Mask patterns: API keys, Bearer tokens, passwords, sensitive URLs
  - Structured logging helper functions (log_operation_start, log_operation_end, log_error)

### Client Layer (T010-T012) - TDD Implementation

Clients follow TDD Red → Green → Refactor cycle

- [X] T010 [TDD] Implement EmbeddingClient in src/fluent_mind_mcp/client/embedding_client.py
  - **Test File**: tests/unit/phase1/test_embedding_client.py (20 tests created)
  - **Red Phase**: Run `pytest tests/unit/phase1/test_embedding_client.py -v` → All 20 skip
  - **Green Phase**: Implement to pass tests:
    - Load sentence-transformers/all-MiniLM-L6-v2 model (auto-download)
    - generate_embedding(text: str) → list[float] (384 dims, <50ms)
    - batch_embed(texts: list) → 2x faster than individual calls
    - Semantic similarity validation (>0.7 for similar texts)
    - Error handling (empty string → ValidationError)
  - **Refactor**: Optimize while keeping 20 tests green
  - **Validation**: pytest tests/unit/phase1/test_embedding_client.py → 20/20 PASS + 2 integration

- [X] T011 [TDD] Implement VectorDatabaseClient in src/fluent_mind_mcp/client/vector_db_client.py
  - **Test File**: tests/unit/phase1/test_vector_db_client.py (18 tests created)
  - **Red Phase**: Run `pytest tests/unit/phase1/test_vector_db_client.py -v` → All 18 skip
  - **Green Phase**: Implement to pass tests:
    - PersistentClient with project-local chroma_db/ directory
    - get_or_create_collection with HNSW (cosine, ef=100, M=16)
    - add_documents, query (<500ms for 50-1000 entries), update_document
    - Collection management (create, get, delete)
    - Error handling (nonexistent collection, mismatched arrays)
  - **Refactor**: Optimize HNSW parameters based on test results
  - **Validation**: pytest tests/unit/phase1/test_vector_db_client.py → 18/18 PASS + 2 integration

- [X] T012 Implement FlowiseApiClient in src/fluent_mind_mcp/client/flowise_client.py
  - AsyncClient with connection pooling (max_connections=20, max_keepalive=10)
  - Methods: get_nodes_list, create_chatflow, get_chatflow, update_chatflow, delete_chatflow
  - Timeout: 30s connect, 60s read
  - Circuit breaker integration ready (placeholder)
  - Performance target: <5s for chatflow creation
  - **Note**: Reuses existing Flowise MCP Server client patterns

### Database Setup (T013)

- [X] T013 Setup ChromaDB with 5 collections (nodes, templates, sdd_artifacts, failed_artifacts, sessions)
  - Create initialization script: src/fluent_mind_mcp/scripts/init_vector_db.py
  - Initialize all collections with proper metadata fields (see data-model.md for schemas)
  - Collections: nodes (NodeDescription schema), templates (FlowTemplate schema), sdd_artifacts (P2), failed_artifacts (P2), sessions (P2)
  - Create health check function
  - Verify collections created and accessible

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Dependencies

- **T001-T003 (Setup)**: No dependencies, can run in any order
- **T004-T007 (Models)**: Depend on T001-T003, can run in parallel after setup
- **T008-T009 (Utils)**: Depend on T001-T003, can run in parallel with models
- **T010 (EmbeddingClient)**: Depends on T004, T008
- **T011 (VectorDatabaseClient)**: Depends on T004, T008
- **T012 (FlowiseApiClient)**: Depends on T007, T008
- **T013 (Database Setup)**: Depends on T011

**Critical Path**: T001 → T004 → T010 → T011 → T013 (5 tasks sequential)

---

## Validation Criteria

### Setup Phase
- ✓ All directories created with proper structure
- ✓ Dependencies installed and importable
- ✓ pyproject.toml updated with new dependencies

### Foundational Phase
- ✓ All models pass Pydantic validation
- ✓ All exceptions are catchable and have proper messages
- ✓ Logging formatter masks credentials in test logs
- ✓ EmbeddingClient generates 384-dim vectors
- ✓ VectorDatabaseClient connects to ChromaDB
- ✓ FlowiseApiClient connects to Flowise (if available)
- ✓ All 5 ChromaDB collections created
- ✓ Health check passes for all components

---

[← Back to Tasks Index](../tasks.md) | [Next: User Stories 1-3 →](02-us1-us2-us3.md)
