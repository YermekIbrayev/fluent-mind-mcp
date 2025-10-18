# Implementation Phases

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: 6-phase delivery plan (8-10 days total)

---

## Phase 1: Foundation (User Stories 1-3) - 2-3 days

**Goal**: Vector search + template-based chatflow creation working end-to-end

**Tasks**:
1. Setup ChromaDB with 5 collections (nodes, templates, sdd_artifacts, failed_artifacts, sessions)
2. Implement VectorDatabaseClient with persistence in project folder
3. Implement EmbeddingClient with sentence-transformers/all-MiniLM-L6-v2
4. Implement VectorSearchService for nodes and templates
5. Implement BuildFlowService (template-based only)
6. MCP Server tools: vector_search_nodes, search_templates, build_flow (templates)
7. Manual template curation (10-20 common patterns from Flowise examples)
8. Test: Query nodes, search templates, create chatflow from template

**Deliverable**: Vector search + template-based chatflow creation functional

---

## Phase 2: Build Flow Enhancement (User Story 3 completion) - 1-2 days

**Goal**: build_flow supports custom node lists with automatic connections

**Tasks**:
1. Implement connection inference algorithm (type-compatible chain)
   - Order nodes by flow pattern heuristics
   - Match output/input baseClasses
   - Validate all required inputs satisfied
2. Implement node positioning algorithm (left-to-right flow)
   - Calculate connection depth
   - Space vertically (200px) and horizontally (300px)
3. Update BuildFlowService to support node-list with connections="auto"
4. Test: Create chatflow from node list ["chatOpenAI", "bufferMemory"]

**Deliverable**: build_flow supports both templates and custom node lists

---

## Phase 3: Dynamic Node Catalog (User Story 6) - 1 day

**Goal**: Node catalog auto-refreshes from Flowise server

**Tasks**:
1. Implement NodeCatalogService with refresh logic
2. Add on-demand staleness check (>24h threshold)
3. Implement change detection (new, updated, removed, deprecated)
4. Implement incremental updates (<30% changes) vs. full rebuild
5. Add fallback to cached data with warning if refresh fails
6. Integrate staleness check before build_flow execution
7. MCP Server tool: refresh_node_catalog
8. Test: Force refresh, verify new nodes added, check staleness handling

**Deliverable**: Node catalog dynamically syncs with Flowise server

---

## Phase 4: Circuit Breaker & Error Handling (User Story 5 + resilience) - 1 day

**Goal**: System resilient to dependency failures

**Tasks**:
1. Implement CircuitBreakerService with state persistence
2. Create CircuitBreaker class with state machine (CLOSED, OPEN, HALF_OPEN)
3. Integrate circuit breakers for: Flowise API, Vector DB, Embedding Model
4. Add compact error messages (<50 tokens) for all failure modes
5. Implement CredentialMaskingFormatter for logging
6. Add structured logging for all operations (vector search, build_flow, catalog refresh)
7. Test: Simulate Flowise API down, verify circuit opens after 3 failures, verify auto-recovery

**Deliverable**: System handles dependency failures gracefully with transparency

---

## Phase 5: Spec-Driven Workflow (User Story 7) - 2 days

**Goal**: Complex chatflow requests trigger human-validated workflow

**Tasks**:
1. Implement SpecDrivenWorkflowService
2. Implement complexity analysis (node count, keywords, template confidence)
3. Integrate with .specify/commands/* (speckit commands)
4. Implement workflow phases: specify → clarify (max 5 questions) → plan → tasks → analyze
5. Generate text-based chatflow design summary
6. Add feedback loop (max 5 iterations per NFR-031)
7. MCP Server tool: spec_driven_workflow
8. Test: Request "multi-agent system with conditional routing", verify spec generated, answer questions, approve design

**Deliverable**: Complex chatflows go through spec-driven workflow with human validation

---

## Phase 6: Testing & Documentation (User Story 4 + NFRs) - 1-2 days

**Goal**: MVP ready for acceptance testing

**Tasks**:
1. Create manual test checklists for all 7 user stories (tests/checklists/)
2. Implement automated critical path tests:
   - test_vector_search_accuracy.py (>90% relevance)
   - test_build_flow_creation.py (>95% success rate)
   - test_circuit_breaker_transitions.py (100% correct)
3. Implement TestDataGenerator (20+ nodes, 10+ templates, 15+ artifacts)
4. Implement ChromaDBTestUtilities (reset, health check, populate)
5. Write user documentation (README, quickstart)
6. Execute manual test checklists for all 7 user stories
7. Verify all acceptance criteria met (100% pass rate)

**Deliverable**: MVP Phase 1 complete with documented test results

---

[← Back to Plan Index](plan_cc.md) | [Next: Success Criteria & Observability →](13-success-criteria-observability.md)
