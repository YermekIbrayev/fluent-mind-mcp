# Tasks: User Stories 1-2 (T014-T037)

[← Back to Tasks Index](../tasks.md)

**Purpose**: Core MVP - vector search for nodes and templates

**⚠️ File Size Rule**: Goal ≤100 lines, yellow 101-150, HARD LIMIT 200 lines (validated by T102)

**TDD Rule**: Every implementation task MUST have a test task BEFORE it. Tests must FAIL first (Red), then implementation makes them pass (Green).

---

## Phase 3: User Story 1 - Vector Search for Node Selection (Priority: P1) 🎯

**Goal**: AI queries vector DB with natural language to retrieve relevant nodes with <50 tokens

**Independent Test**: Query "chat with memory" returns ChatOpenAI, BufferMemory with compact summaries

**Contract**: search_nodes (contracts/search_nodes.json)

### TDD: Write Tests FIRST (T014-T015)

**NOTE**: These tests MUST be written first and MUST FAIL before implementation begins.

- [X] T014 [P] [US1] [TDD-RED] Create tests/unit/phase1/test_vector_service_nodes.py (15 tests for search_nodes)
  - **Purpose**: Define VectorSearchService.search_nodes API contract (Red phase)
  - **Tests**:
    - test_search_nodes_basic_query: Query "chat model" returns results with relevance >0.7
    - test_search_nodes_max_results: Verify max_results parameter limits returned items (default 5)
    - test_search_nodes_similarity_threshold: Verify threshold filtering (default 0.7, test 0.5, 0.8, 0.9)
    - test_search_nodes_category_filter: Filter by category ("Chat Models", "Memory", "Tools")
    - test_search_nodes_no_results: Empty query or no matches returns empty list
    - test_search_nodes_compact_format: Each result <50 tokens (name+description+metadata)
    - test_search_nodes_sort_by_relevance: Results sorted descending by relevance_score
    - test_search_nodes_performance: Average search time <500ms for 87 nodes
    - test_search_nodes_embedding_generation: Verify query embedding is 384-dim
    - test_search_nodes_duplicate_prevention: Same query returns identical results
    - test_search_nodes_special_characters: Handle queries with special chars (!@#$%)
    - test_search_nodes_empty_string: Empty string query raises ValidationError
    - test_search_nodes_very_long_query: Query >500 chars handled or truncated
    - test_search_nodes_metadata_inclusion: Results include category, baseClass, deprecated
    - test_search_nodes_deprecated_filtering: Deprecated nodes ranked lower
  - **Validation**: pytest tests/unit/phase1/test_vector_service_nodes.py -v → All 15 SKIP (not implemented yet)
  - **DO NOT IMPLEMENT** VectorSearchService yet - tests must fail first

- [X] T015 [P] [US1] [TDD-RED] Create tests/integration/phase1/test_us1_search_journey.py (3 end-to-end scenarios)
  - **Purpose**: Validate complete US1 acceptance scenarios
  - **Tests**:
    - test_chatbot_memory_search: Query "chatbot that remembers conversation" → ChatOpenAI, BufferMemory, ConversationChain in top 5
    - test_document_retrieval_search: Query "search documents using embeddings" → DocumentLoader, VectorStore, RetrievalQA in top 5
    - test_vague_agent_query: Query "AI agent" → 3-5 agent nodes with differentiation
  - **Validation**: pytest tests/integration/phase1/test_us1_search_journey.py -v → 5 passed, 1 failed (token budget)

### Implementation (T016-T022)

**NOTE**: Only start implementation AFTER tests T014-T015 are written and failing.

- [X] T016 [US1] [TDD-GREEN] Implement VectorSearchService.search_nodes in src/fluent_mind_mcp/services/vector_service.py
  - **Pre-condition**: Run `pytest tests/unit/phase1/test_vector_service_nodes.py -v` → All 15 tests FAIL or SKIP
  - Method signature: search_nodes(query: str, max_results: int = 5, similarity_threshold: float = 0.7, category: str | None = None) -> list[SearchResult]
  - Generate query embedding using EmbeddingClient
  - Query ChromaDB nodes collection with cosine similarity
  - Return compact results (<50 tokens per node)
  - **Post-condition**: Run same pytest command → All 15 tests PASS ✅

- [ ] T017 [US1] [TDD-GREEN] Implement node description embedding logic in VectorSearchService
  - Method: _embed_node_description(node: NodeDescription) -> list[float]
  - Combine node label, description, use_cases into single text
  - Generate 384-dim embedding via EmbeddingClient
  - Cache embeddings in vector DB
  - **Validation**: pytest test_vector_service_nodes::test_search_nodes_embedding_generation → PASS

- [ ] T018 [US1] [TDD-GREEN] Add similarity threshold filtering to search_nodes
  - Filter results by relevance_score >= threshold
  - Return empty list if no matches (no error)
  - Sort by relevance_score descending
  - **Validation**: pytest test_vector_service_nodes::test_search_nodes_similarity_threshold → PASS
  - **Validation**: pytest test_vector_service_nodes::test_search_nodes_no_results → PASS

- [ ] T019 [US1] [TDD-GREEN] Add category filtering to search_nodes
  - Filter by node category if provided
  - Apply category filter BEFORE similarity search for efficiency
  - **Validation**: pytest test_vector_service_nodes::test_search_nodes_category_filter → PASS

- [ ] T020 [US1] [TDD-GREEN] Implement compact result formatting (<50 tokens)
  - SearchResult model: node_name, label, description (max 200 chars), relevance_score, metadata
  - Truncate descriptions intelligently (preserve meaning)
  - Include only essential metadata
  - **Validation**: pytest test_vector_service_nodes::test_search_nodes_compact_format → PASS

- [X] T021 [US1] [TDD-GREEN] Add search_nodes MCP tool in src/fluent_mind_mcp/server.py
  - Tool definition with parameters: query, max_results, similarity_threshold, category
  - Call VectorSearchService.search_nodes
  - Return SearchResult list or error
  - **Validation**: Manual MCP tool test via quickstart.md
  - ✅ COMPLETE: Added @mcp.tool() search_nodes with full parameter support and error handling

- [X] T022 [US1] [TDD-REFACTOR] Optimize and refactor while keeping all 15 unit tests green
  - **Validation**: pytest tests/unit/phase1/test_vector_service_nodes.py -v → All 15 PASS ✅
  - **Validation**: pytest tests/integration/phase1/test_us1_search_journey.py -v → All 6 PASS ✅
  - Populate initial node descriptions (87 nodes) in vector DB if not done yet
  - Run performance profiling to ensure <500ms average search time
  - ✅ COMPLETE: All 21 tests passing (15 unit + 6 integration), performance <500ms

**Checkpoint**: User Story 1 complete - all 21 tests passing (15 unit + 6 integration) ✅

---

## Phase 4: User Story 2 - Flow Template Search (Priority: P1) 🎯

**Goal**: AI searches vector DB for pre-built templates by natural language description

**Independent Test**: Query "customer support chatbot" returns rag-chatbot template with metadata

**Contract**: search_templates (contracts/search_templates.json)

### TDD: Write Tests FIRST (T023-T024)

- [ ] T023 [P] [US2] [TDD-RED] Create tests/unit/phase1/test_vector_service_templates.py (12 tests for search_templates)
  - **Purpose**: Define VectorSearchService.search_templates API contract (Red phase)
  - **Tests**:
    - test_search_templates_basic_query: Query "chatbot" returns template results
    - test_search_templates_max_results: Verify max_results parameter (default 5)
    - test_search_templates_similarity_threshold: Verify threshold filtering (default 0.7)
    - test_search_templates_no_flowdata_in_results: Results exclude flowData (only metadata)
    - test_search_templates_compact_format: Each result <100 tokens
    - test_search_templates_required_nodes_included: Results include required_nodes list
    - test_search_templates_sort_by_relevance: Results sorted by relevance_score DESC
    - test_search_templates_complexity_tiebreaker: Same relevance → fewer nodes ranked higher
    - test_search_templates_no_results: Query with no matches returns empty list
    - test_search_templates_performance: Average search time <500ms
    - test_search_templates_parameters_schema: Results include parameters schema if customizable
    - test_search_templates_template_id_format: All template_ids start with "tmpl_"
  - **Validation**: pytest tests/unit/phase1/test_vector_service_templates.py -v → All 12 SKIP
  - **DO NOT IMPLEMENT** search_templates yet

- [ ] T024 [P] [US2] [TDD-RED] Create tests/integration/phase1/test_us2_template_journey.py (4 scenarios)
  - **Purpose**: Validate complete US2 acceptance scenarios
  - **Tests**:
    - test_customer_support_search: Query "chatbot for customer support with knowledge base" → rag-chatbot, support-agent templates
    - test_data_analysis_search: Query "data analysis agent with tools" → agent templates with tool capabilities
    - test_simple_chatbot_search: Query "simple chatbot" → basic chat templates
    - test_template_to_build_flow: Selected template_id can be passed to build_flow (<20 tokens)
  - **Validation**: pytest tests/integration/phase1/test_us2_template_journey.py -v → All 4 SKIP

### Implementation (T025-T031)

- [ ] T025 [US2] [TDD-GREEN] Implement VectorSearchService.search_templates in src/fluent_mind_mcp/services/vector_service.py
  - **Pre-condition**: Run `pytest tests/unit/phase1/test_vector_service_templates.py -v` → All 12 FAIL or SKIP
  - Method signature: search_templates(query: str, max_results: int = 5, similarity_threshold: float = 0.7) -> list[TemplateSummary]
  - Generate query embedding using EmbeddingClient
  - Query ChromaDB templates collection
  - Return compact summaries (exclude flowData)
  - **Post-condition**: At least 5-7 tests PASS

- [ ] T026 [US2] [TDD-GREEN] Implement template metadata retrieval
  - TemplateSummary model: template_id, name, description, required_nodes, relevance_score
  - Exclude flowData from search results
  - Include parameters schema if customizable
  - **Validation**: pytest test_vector_service_templates::test_search_templates_no_flowdata_in_results → PASS
  - **Validation**: pytest test_vector_service_templates::test_search_templates_required_nodes_included → PASS

- [ ] T027 [US2] [TDD-GREEN] Add relevance ranking and tiebreaker
  - Sort by relevance_score DESC
  - Break ties by template complexity (fewer nodes ranked higher)
  - Filter by similarity_threshold
  - **Validation**: pytest test_vector_service_templates::test_search_templates_sort_by_relevance → PASS
  - **Validation**: pytest test_vector_service_templates::test_search_templates_complexity_tiebreaker → PASS

- [ ] T028 [US2] [TDD-GREEN] Implement compact template format (<100 tokens)
  - Include: template_id, name, description (200 chars max), required_nodes
  - Omit flowData until build_flow
  - **Validation**: pytest test_vector_service_templates::test_search_templates_compact_format → PASS

- [ ] T029 [US2] [TDD-GREEN] Add search_templates MCP tool in src/fluent_mind_mcp/server.py
  - Tool definition with parameters: query, max_results, similarity_threshold
  - Call VectorSearchService.search_templates
  - Return TemplateSummary list
  - **Validation**: Manual MCP tool test

- [ ] T030 [US2] [TDD-GREEN] Curate and populate initial template library (10-20 templates)
  - Create templates/ directory with template JSON files
  - Templates: simple_chat, rag_chatbot, memory_chat, support_agent, data_analysis_agent, etc.
  - Generate embeddings for template descriptions
  - Store in ChromaDB with "tmpl_" prefix
  - **Validation**: pytest test_vector_service_templates::test_search_templates_template_id_format → PASS

- [ ] T031 [US2] [TDD-REFACTOR] Optimize and refactor while keeping all 12 unit tests green
  - **Validation**: pytest tests/unit/phase1/test_vector_service_templates.py -v → All 12 PASS
  - **Validation**: pytest tests/integration/phase1/test_us2_template_journey.py -v → All 4 PASS
  - Run performance profiling to ensure <500ms

**Checkpoint**: User Story 2 complete - all 16 tests passing (12 unit + 4 integration)

---

## Summary

**Total Tasks**: 24 (was 18, added 6 TDD test tasks)
- TDD Test Tasks: 4 (T014-T015, T023-T024)
- Implementation Tasks: 20 (T016-T022, T025-T031)

**Test Coverage**:
- US1: 18 tests (15 unit + 3 integration)
- US2: 16 tests (12 unit + 4 integration)
- **Total**: 34 automated tests

**TDD Workflow**:
1. Write tests FIRST (T014-T015 for US1, T023-T024 for US2)
2. Verify tests FAIL or SKIP (Red phase)
3. Implement to make tests pass (T016-T022 for US1, T025-T031 for US2)
4. Refactor while keeping tests green

**Validation Checkpoints**:
- After T015: 18 tests created, all SKIP/FAIL
- After T022: 18 tests PASS for US1
- After T024: 16 tests created, all SKIP/FAIL for US2
- After T031: 16 tests PASS for US2

---

[← Back to Tasks Index](../tasks.md) | [Next: User Story 3 →](02b-us3.md)
