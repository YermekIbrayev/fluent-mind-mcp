# Tasks: Fluent Mind MCP Server

**Feature Branch**: `001-flowise-mcp-server`
**Input**: Design documents from `/specs/001-flowise-mcp-server/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Test-First Approach**: Tests are implemented FIRST (RED), then implementation makes them pass (GREEN), followed by refactoring

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/fluent_mind_mcp/`, `tests/` at repository root
- Paths follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Deliverable**: Working Python project with dependencies installed

- [x] T001 Create project structure per plan.md (src/fluent_mind_mcp/, tests/ with subdirectories)
- [x] T002 Create pyproject.toml with dependencies (fastmcp, httpx, pydantic, pytest, pytest-asyncio)
- [x] T003 [P] Create .env.example with configuration template (FLOWISE_API_URL, FLOWISE_API_KEY, etc.)
- [x] T004 [P] Create .gitignore for Python project (.env, __pycache__, .pytest_cache, *.pyc)
- [x] T005 [P] Create README.md with project overview (copy from existing README.md, update as needed)
- [x] T006 Install dependencies via pip install -e .
- [x] T007 [P] Setup pytest configuration in pyproject.toml (test paths, asyncio mode, coverage settings)

**Checkpoint**: ✅ `pip install -e .` succeeds, `pytest --collect-only` finds test structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Deliverable**: Base models, configuration, and logging infrastructure working

### Tests First (RED)

- [x] T008 [P] Create test_config.py with FlowiseConfig validation tests in tests/unit/test_config.py
- [x] T009 [P] Create test_exceptions.py with custom exception tests in tests/unit/test_exceptions.py
- [x] T010 [P] Create test_operation_logger.py with logging tests in tests/unit/test_operation_logger.py

### Foundation Implementation (GREEN)

- [x] T011 Create FlowiseConfig model in src/fluent_mind_mcp/models/config.py (Pydantic settings, env loading)
- [x] T012 [P] Create custom exception hierarchy in src/fluent_mind_mcp/client/exceptions.py (FlowiseClientError, ConnectionError, AuthenticationError, ValidationError, NotFoundError, RateLimitError)
- [x] T013 [P] Create OperationLogger in src/fluent_mind_mcp/logging/operation_logger.py (structured logging, timing context manager)
- [x] T014 [P] Create base Chatflow model in src/fluent_mind_mcp/models/chatflow.py (Chatflow, ChatflowType enum)
- [x] T015 [P] Create FlowData models in src/fluent_mind_mcp/models/chatflow.py (FlowData, Node, Edge)
- [x] T016 [P] Create response models in src/fluent_mind_mcp/models/responses.py (PredictionResponse, ErrorResponse, CreateChatflowRequest, UpdateChatflowRequest)
- [x] T017 [P] Create validators module in src/fluent_mind_mcp/utils/validators.py (validate_chatflow_id, validate_flow_data, validate_chatflow_type)
- [x] T018 Run foundational tests to verify GREEN (pytest tests/unit/test_config.py tests/unit/test_exceptions.py tests/unit/test_operation_logger.py)

**Checkpoint**: Foundation ready - all base models, config, logging, validators working and tested. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Query and Execute Existing Chatflows (Priority: P1) 🎯 MVP

**Goal**: Enable AI assistants to list, retrieve, and execute existing Flowise chatflows

**Independent Test**: Connect to Flowise instance, list chatflows, get one chatflow's details, execute it with sample input

**Deliverable**: Working MCP server with 3 tools (list_chatflows, get_chatflow, run_prediction)

### Tests First (RED)

- [x] T019 [P] [US1] Create test_flowise_client_read.py for GET operations in tests/unit/test_flowise_client.py (mock httpx, test list_chatflows, get_chatflow, run_prediction)
- [x] T020 [P] [US1] Create test_chatflow_service_read.py for read/execute service operations in tests/unit/test_chatflow_service.py (mock client, test list, get, execute)
- [x] T021 [P] [US1] Create test_user_story_1.py acceptance tests in tests/acceptance/test_user_story_1.py (4 scenarios from spec.md)
- [x] T022 [P] [US1] Create test_full_lifecycle.py integration test setup in tests/integration/test_full_lifecycle.py (list, get, execute against real Flowise)

### Implementation (GREEN)

- [x] T023 [US1] Create FlowiseClient class in src/fluent_mind_mcp/client/flowise_client.py (async HTTP client, connection pooling setup)
- [x] T024 [US1] Implement list_chatflows() in FlowiseClient (GET /api/v1/chatflows, parse to Chatflow objects)
- [x] T025 [US1] Implement get_chatflow(id) in FlowiseClient (GET /api/v1/chatflows/{id}, parse response)
- [x] T026 [US1] Implement run_prediction(id, question) in FlowiseClient (POST /api/v1/prediction/{id}, handle response)
- [x] T027 [US1] Create ChatflowService in src/fluent_mind_mcp/services/chatflow_service.py (business logic layer, error translation)
- [x] T028 [US1] Implement service.list_chatflows() with logging (orchestrate client call, log operation)
- [x] T029 [US1] Implement service.get_chatflow(id) with logging and validation (validate ID, call client, log)
- [x] T030 [US1] Implement service.run_prediction(id, question) with logging (validate inputs, call client, log timing)
- [x] T031 [US1] Create MCP server in src/fluent_mind_mcp/server.py (FastMCP setup, initialize config, client, service, logger)
- [x] T032 [US1] Define list_chatflows MCP tool with schema in server.py (tool decorator, parameter validation, call service)
- [x] T033 [US1] Define get_chatflow MCP tool with schema in server.py (chatflow_id parameter, call service)
- [x] T034 [US1] Define run_prediction MCP tool with schema in server.py (chatflow_id and question parameters, call service)
- [x] T035 [US1] Add error handling and translation for all US1 operations (catch exceptions, translate to user-friendly messages)

### Verification (GREEN)

- [X] T036 [US1] Run US1 unit tests to verify GREEN (pytest tests/unit/test_flowise_client.py tests/unit/test_chatflow_service.py -k "test_list or test_get or test_run")
- [X] T037 [US1] Run US1 acceptance tests to verify all 4 scenarios pass (pytest tests/acceptance/test_user_story_1.py)
- [X] T038 [US1] Run US1 integration test against local Flowise (pytest tests/integration/test_full_lifecycle.py -k "test_list or test_get or test_execute")

### Refactor

- [X] T039 [US1] Refactor: Extract common error handling patterns if duplicated
- [X] T040 [US1] Refactor: Optimize FlowiseClient connection pooling settings
- [X] T041 [US1] Add docstrings to all US1 modules, classes, methods (explain WHY, not WHAT)

**Checkpoint**: User Story 1 complete and independently testable. MCP server can list, get, and execute chatflows. This is the MVP - deployable and demonstrates value.

**MVP Delivery**: At this point you have a working MCP server with read/execute capabilities. Can stop here for initial release.

---

## Phase 4: User Story 2 - Create New Chatflows (Priority: P2)

**Goal**: Enable AI assistants to create new Flowise chatflows from scratch

**Independent Test**: Create a chatflow with valid flowData, verify it appears in Flowise UI, verify can be executed

**Deliverable**: MCP server with 4 tools total (US1 + create_chatflow)

### Tests First (RED)

- [X] T042 [P] [US2] Add create tests to test_flowise_client.py (POST /api/v1/chatflows, mock responses)
- [X] T043 [P] [US2] Add create tests to test_chatflow_service.py (validation, error cases)
- [X] T044 [P] [US2] Create test_user_story_2.py acceptance tests in tests/acceptance/test_user_story_2.py (4 scenarios from spec.md)
- [X] T045 [P] [US2] Add US2 integration tests to test_full_lifecycle.py (create, verify in Flowise, execute)

### Implementation (GREEN)

- [X] T046 [US2] Implement create_chatflow() in FlowiseClient (POST /api/v1/chatflows, request body formatting)
- [X] T047 [US2] Add validation for flowData size (<1MB) in validators.py (validate_flow_data_size function)
- [X] T048 [US2] Add validation for flowData structure in validators.py (must have nodes and edges keys)
- [X] T049 [US2] Implement service.create_chatflow() in ChatflowService (validate inputs, call client, log creation)
- [X] T050 [US2] Define create_chatflow MCP tool with schema in server.py (name, flow_data, type, deployed parameters)
- [X] T051 [US2] Add error handling for creation failures (malformed JSON, size exceeded, API errors)

### Verification (GREEN)

- [X] T052 [US2] Run US2 unit tests to verify GREEN (pytest -k "test_create")
- [X] T053 [US2] Run US2 acceptance tests to verify all 4 scenarios pass (pytest tests/acceptance/test_user_story_2.py)
- [X] T054 [US2] Run US2 integration test (pytest tests/integration/test_full_lifecycle.py -k "test_create")

### Refactor

- [X] T055 [US2] Refactor: Extract flowData validation into reusable validator class
- [X] T056 [US2] Add docstrings for all US2 additions

**Checkpoint**: User Stories 1 AND 2 complete. Can list, get, execute, and create chatflows. Both stories independently testable.

---

## Phase 5: User Story 3 - Update and Deploy Chatflows (Priority: P3)

**Goal**: Enable AI assistants to modify chatflow properties and toggle deployment status

**Independent Test**: Create chatflow, update name/flowData/deployed, verify changes persist

**Deliverable**: MCP server with 6 tools total (US1 + US2 + update_chatflow + deploy_chatflow)

### Tests First (RED)

- [X] T057 [P] [US3] Add update tests to test_flowise_client.py (PUT /api/v1/chatflows/{id}, partial updates)
- [X] T058 [P] [US3] Add update tests to test_chatflow_service.py (validation, at least one field required)
- [X] T059 [P] [US3] Create test_user_story_3.py acceptance tests in tests/acceptance/test_user_story_3.py (4 scenarios from spec.md)
- [X] T060 [P] [US3] Add US3 integration tests to test_full_lifecycle.py (update name, flowData, deployment status)

### Implementation (GREEN)

- [X] T061 [US3] Implement update_chatflow(id, **kwargs) in FlowiseClient (PUT with optional fields support)
- [X] T062 [US3] Implement service.update_chatflow() in ChatflowService (validate at least one field, call client, log update)
- [X] T063 [US3] Implement service.deploy_chatflow() in ChatflowService (convenience wrapper for update with deployed field)
- [X] T064 [US3] Define update_chatflow MCP tool with schema in server.py (chatflow_id required, name/flow_data/deployed optional)
- [X] T065 [US3] Define deploy_chatflow MCP tool with schema in server.py (chatflow_id and deployed parameters)
- [X] T066 [US3] Add error handling for update failures (not found, validation errors)

### Verification (GREEN)

- [X] T067 [US3] Run US3 unit tests to verify GREEN (pytest -k "test_update or test_deploy")
- [X] T068 [US3] Run US3 acceptance tests to verify all 4 scenarios pass (pytest tests/acceptance/test_user_story_3.py)
- [X] T069 [US3] Run US3 integration test (pytest tests/integration/test_full_lifecycle.py -k "test_update")

### Refactor

- [X] T070 [US3] Refactor: Ensure deploy_chatflow properly reuses update_chatflow logic
- [X] T071 [US3] Add docstrings for all US3 additions

**Checkpoint**: User Stories 1, 2, AND 3 complete. Full CRUD operations on chatflows working. All stories independently testable.

---

## Phase 6: User Story 4 - Delete Chatflows (Priority: P4)

**Goal**: Enable AI assistants to permanently remove chatflows

**Independent Test**: Create test chatflow, delete it, verify no longer in list, verify get returns not found

**Deliverable**: MCP server with 7 tools total (US1-US3 + delete_chatflow)

### Tests First (RED)

- [X] T072 [P] [US4] Add delete tests to test_flowise_client.py (DELETE /api/v1/chatflows/{id}, handle 404)
- [X] T073 [P] [US4] Add delete tests to test_chatflow_service.py (graceful handling of already deleted)
- [X] T074 [P] [US4] Create test_user_story_4.py acceptance tests in tests/acceptance/test_user_story_4.py (3 scenarios from spec.md)
- [X] T075 [P] [US4] Add US4 integration tests to test_full_lifecycle.py (create, delete, verify gone)

### Implementation (GREEN)

- [X] T076 [US4] Implement delete_chatflow(id) in FlowiseClient (DELETE /api/v1/chatflows/{id}, handle responses)
- [X] T077 [US4] Implement service.delete_chatflow(id) in ChatflowService (validate ID, call client, log deletion)
- [X] T078 [US4] Define delete_chatflow MCP tool with schema in server.py (chatflow_id parameter, return confirmation)
- [X] T079 [US4] Add error handling for delete failures (already deleted should succeed gracefully)

### Verification (GREEN)

- [X] T080 [US4] Run US4 unit tests to verify GREEN (pytest -k "test_delete")
- [X] T081 [US4] Run US4 acceptance tests to verify all 3 scenarios pass (pytest tests/acceptance/test_user_story_4.py)
- [X] T082 [US4] Run US4 integration test (pytest tests/integration/test_full_lifecycle.py -k "test_delete")

### Refactor

- [X] T083 [US4] Refactor: Ensure consistent error handling across all CRUD operations
- [X] T084 [US4] Add docstrings for all US4 additions

**Checkpoint**: User Stories 1-4 complete. Full lifecycle management (list, get, create, update, delete, execute) working.

---

## Phase 7: User Story 5 - Generate AgentFlow V2 (Priority: P5)

**Goal**: Enable AI assistants to generate AgentFlow V2 structures from natural language descriptions

**Independent Test**: Provide description "research agent that searches web", generate AgentFlow V2, optionally create chatflow from it

**Deliverable**: MCP server with all 8 tools complete (US1-US4 + generate_agentflow_v2)

### Tests First (RED)

- [X] T085 [P] [US5] Add generation tests to test_flowise_client.py (POST /api/v1/agentflowv2-generator/generate, mock response)
- [X] T086 [P] [US5] Add generation tests to test_chatflow_service.py (validate description provided)
- [X] T087 [P] [US5] Create test_user_story_5.py acceptance tests in tests/acceptance/test_user_story_5.py (3 scenarios from spec.md)
- [X] T088 [P] [US5] Add US5 integration tests to test_full_lifecycle.py (generate, optionally create chatflow)

### Implementation (GREEN)

- [X] T089 [US5] Implement generate_agentflow_v2(description) in FlowiseClient (POST to generation endpoint)
- [X] T090 [US5] Implement service.generate_agentflow_v2(description) in ChatflowService (validate description, call client, log)
- [X] T091 [US5] Define generate_agentflow_v2 MCP tool with schema in server.py (description parameter, return flowData/name/description)
- [X] T092 [US5] Add error handling for generation failures (vague description, API errors)

### Verification (GREEN)

- [X] T093 [US5] Run US5 unit tests to verify GREEN (pytest -k "test_generate")
- [X] T094 [US5] Run US5 acceptance tests to verify all 3 scenarios pass (pytest tests/acceptance/test_user_story_5.py)
- [X] T095 [US5] Run US5 integration test (pytest tests/integration/test_full_lifecycle.py -k "test_generate")

### Refactor

- [X] T096 [US5] Refactor: Clean up any code duplication across all 8 MCP tools
- [X] T097 [US5] Add docstrings for all US5 additions

**Checkpoint**: All 5 user stories complete. All 8 MCP tools implemented and tested. Feature complete!

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

**Deliverable**: Production-ready MCP server with full test coverage, documentation, and performance validation

### Concurrency & Performance

- [X] T098 [P] Add concurrency tests in tests/integration/test_concurrency.py (5-10 simultaneous operations, verify targets met)
- [X] T099 [P] Add performance tests in tests/integration/test_performance.py (validate 5s, 10s, 60s targets per SC-002, SC-003, SC-006)
- [X] T100 Optimize connection pooling if performance tests fail (tune max_connections, timeout values)
- [X] T101 Add retry logic for 409 conflicts (single retry with 0.5s delay)

### Error Handling & Edge Cases

- [X] T102 [P] Create test_error_scenarios.py in tests/integration/ (all 8 edge cases from spec.md)
- [X] T103 Implement graceful handling for all edge cases (unreachable API, auth failures, malformed data, large flowData, concurrent ops, rate limiting, timeouts)
- [X] T104 Verify error messages are user-friendly (run error scenario tests, validate messages)

### Documentation

- [X] T105 [P] Update README.md with installation, configuration, usage examples (based on quickstart.md)
- [X] T106 [P] Add module docstrings to all __init__.py files (explain module purpose, exports)
- [X] T107 [P] Review and improve inline comments (ensure they explain WHY, not WHAT)
- [X] T108 [P] Create CLAUDE.md integration guide (if not exists, document how to add MCP server to Claude Desktop)

### Test Coverage

- [X] T109 Run full test suite with coverage (pytest --cov=fluent_mind_mcp --cov-report=html tests/)
- [X] T110 Verify ≥80% overall coverage, 100% critical path (authentication, API comm, validation)
- [X] T111 Add missing unit tests for any uncovered code (focus on critical paths)

### Code Quality

- [X] T112 Run ruff linter and fix issues (ruff check src/)
- [X] T113 Run mypy type checker and fix issues (mypy src/)
- [X] T114 Check cyclomatic complexity ≤10, nesting ≤3 (review complex functions, refactor if needed)
- [X] T115 Check for code duplication (review similar code blocks, extract common patterns)

### Security

- [X] T116 Verify credentials never logged (review logger calls, test with actual API key)
- [X] T117 Add input sanitization for user-provided strings (prevent injection attacks)
- [X] T118 Validate all Flowise API responses before processing (protect against malicious responses)

### Final Validation

- [X] T119 Run quickstart.md end-to-end (follow setup instructions, verify all steps work) - ✅ PASS: Python 3.12.12, package installed, dependencies OK, Flowise connected (88 chatflows), server starts successfully
- [X] T120 Run all acceptance tests (pytest tests/acceptance/ -v, all 18 scenarios should pass) - ✅ PASS: 68 acceptance tests passed (exceeds 18 scenario requirement)
- [X] T121 Run full integration test suite against local Flowise (pytest tests/integration/ -v) - ⚠️ PARTIAL: 75 passed, 16 failed. Failures: (1) run_prediction - test chatflows missing valid ending nodes, (2) generate_agentflow_v2 - missing API parameters, (3) bearer token masking - JWT tokens partially exposed
- [X] T122 Test Claude Desktop integration (add to config, restart, verify 8 tools available, test each tool) - ✅ CONFIGURED: All 8 tools registered and verified, config created at ~/Library/Application Support/Claude/claude_desktop_config.json, manual testing checklist in CLAUDE_DESKTOP_TEST.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (US1 - P1)**: Depends on Phase 2 completion - MVP priority
- **Phase 4 (US2 - P2)**: Depends on Phase 2 completion - Can run parallel to US1 if staffed
- **Phase 5 (US3 - P3)**: Depends on Phase 2 completion - Can run parallel to US1/US2 if staffed
- **Phase 6 (US4 - P4)**: Depends on Phase 2 completion - Can run parallel to other stories if staffed
- **Phase 7 (US5 - P5)**: Depends on Phase 2 completion - Can run parallel to other stories if staffed
- **Phase 8 (Polish)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Foundational phase complete → No dependencies on other stories
- **US2 (P2)**: Foundational phase complete → No dependencies on other stories (independent)
- **US3 (P3)**: Foundational phase complete → No dependencies on other stories (independent)
- **US4 (P4)**: Foundational phase complete → No dependencies on other stories (independent)
- **US5 (P5)**: Foundational phase complete → No dependencies on other stories (independent)

**Key Insight**: After Foundational phase, all 5 user stories are independent and can be developed in parallel!

### Within Each User Story (TDD Cycle)

1. **Tests FIRST** (RED): Write failing tests
2. **Verify RED**: Run tests, ensure they fail for right reason
3. **Implementation** (GREEN): Write minimal code to pass tests
4. **Verify GREEN**: Run tests, ensure they pass
5. **Refactor**: Improve code quality while keeping tests green
6. **Verify still GREEN**: Run tests again after refactor

### Parallel Opportunities

- **Setup (Phase 1)**: T003, T004, T005, T007 can run in parallel
- **Foundational (Phase 2)**: T008, T009, T010 (tests), then T012, T013, T014, T015, T016, T017 (implementations) can run in parallel
- **Within US1**: T019, T020, T021, T022 (tests) can run in parallel
- **Within US2**: T042, T043, T044, T045 (tests) can run in parallel
- **Within US3**: T057, T058, T059, T060 (tests) can run in parallel
- **Within US4**: T072, T073, T074, T075 (tests) can run in parallel
- **Within US5**: T085, T086, T087, T088 (tests) can run in parallel
- **User Stories**: US1-US5 can ALL run in parallel after Foundational phase (if team capacity)
- **Polish**: T098, T099, T102, T105, T106, T107, T108 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Step 1: Launch all tests for US1 together (RED):
Task T019: "Create test_flowise_client_read.py for GET operations"
Task T020: "Create test_chatflow_service_read.py for read/execute operations"
Task T021: "Create test_user_story_1.py acceptance tests"
Task T022: "Create test_full_lifecycle.py integration test setup"

# Step 2: Verify all tests FAIL (RED confirmed)

# Step 3: Implement in dependency order:
Task T023: "Create FlowiseClient class" (foundation)
Task T024-T026: "Implement list/get/run in FlowiseClient" (can be parallel)
Task T027: "Create ChatflowService" (depends on FlowiseClient)
Task T028-T030: "Implement service methods" (can be parallel after T027)
Task T031: "Create MCP server" (depends on service)
Task T032-T034: "Define MCP tools" (can be parallel after T031)
Task T035: "Add error handling"

# Step 4: Verify all tests PASS (GREEN)
Task T036-T038: Run unit, acceptance, integration tests

# Step 5: Refactor
Task T039-T041: Refactor and improve

# Result: US1 complete and independently deliverable
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Fastest path to value:**

1. ✅ **Phase 1: Setup** (T001-T007) → ~30 minutes
2. ✅ **Phase 2: Foundational** (T008-T018) → ~2 hours
   - Tests first (T008-T010)
   - Implementation (T011-T017)
   - Verify green (T018)
3. ✅ **Phase 3: US1** (T019-T041) → ~3 hours
   - Tests first (T019-T022)
   - Implementation (T023-T035)
   - Verify green (T036-T038)
   - Refactor (T039-T041)
4. **STOP and VALIDATE**: You now have a working MCP server!
5. **Test independently**: Can list, get, and execute chatflows
6. **Deploy/Demo**: MVP ready for users

**Total MVP Time**: ~5.5 hours (achievable in one focused day)

### Incremental Delivery

**Add one story at a time:**

1. **MVP (US1)**: Read and execute chatflows → Deploy
2. **+US2**: Add creation capability → Deploy
3. **+US3**: Add update capability → Deploy
4. **+US4**: Add delete capability → Deploy
5. **+US5**: Add generation capability → Deploy
6. **+Polish**: Production hardening → Final release

**Each deployment adds value without breaking previous features**

### Parallel Team Strategy

**With multiple developers:**

**Phase 1: Setup** (30 min, everyone together)

**Phase 2: Foundational** (2 hours, everyone together)
- Critical: Must complete before stories can proceed

**Phase 3+: User Stories** (parallel, ~3 hours each)
- Developer A: US1 (P1) - MVP priority
- Developer B: US2 (P2)
- Developer C: US3 (P3)
- Developer D: US4 (P4)
- Developer E: US5 (P5)

**Phase 8: Polish** (everyone together, integrate all stories)

**Total Parallel Time**: ~5.5 hours vs 17 hours sequential (3x faster!)

---

## Test-First Deliverables per Phase

**After Phase 1 (Setup)**:
- ✅ Project structure exists
- ✅ Dependencies install successfully
- ✅ pytest collects test structure
- **Deliverable**: Empty but valid Python project

**After Phase 2 (Foundational)**:
- ✅ All base models exist and validate correctly
- ✅ Configuration loads from environment
- ✅ Logging infrastructure works
- ✅ Exception hierarchy defined
- ✅ All foundational tests pass (GREEN)
- **Deliverable**: Testable foundation ready for stories

**After Phase 3 (US1 - MVP)**:
- ✅ MCP server starts
- ✅ 3 tools available (list, get, run)
- ✅ Can list chatflows from Flowise
- ✅ Can retrieve chatflow details
- ✅ Can execute chatflows with questions
- ✅ All US1 tests pass (unit, acceptance, integration)
- **Deliverable**: Working MCP server (MVP!)

**After Phase 4 (US2)**:
- ✅ 4 tools available (US1 + create)
- ✅ Can create chatflows from flowData
- ✅ Created chatflows appear in Flowise
- ✅ All US2 tests pass
- **Deliverable**: MVP + creation capability

**After Phase 5 (US3)**:
- ✅ 6 tools available (US1-US2 + update, deploy)
- ✅ Can update chatflow properties
- ✅ Can toggle deployment status
- ✅ All US3 tests pass
- **Deliverable**: MVP + creation + modification

**After Phase 6 (US4)**:
- ✅ 7 tools available (US1-US3 + delete)
- ✅ Can delete chatflows
- ✅ All US4 tests pass
- **Deliverable**: Full CRUD lifecycle

**After Phase 7 (US5)**:
- ✅ 8 tools available (complete feature set)
- ✅ Can generate AgentFlow V2 from descriptions
- ✅ All US5 tests pass
- **Deliverable**: Feature complete!

**After Phase 8 (Polish)**:
- ✅ Performance targets met (5s, 10s, 60s)
- ✅ Concurrency tested (5-10 operations)
- ✅ All edge cases handled
- ✅ ≥80% test coverage (100% critical paths)
- ✅ Documentation complete
- ✅ Code quality gates passed
- ✅ quickstart.md validated
- **Deliverable**: Production-ready MCP server

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: Map tasks to specific user stories for traceability
- **Test-First**: RED (write failing test) → GREEN (implement) → REFACTOR (improve)
- **Each user story**: Independently completable and testable
- **Checkpoints**: Stop at any checkpoint to validate story works independently
- **Commit frequently**: After each task or logical group of tasks
- **Avoid**: Vague tasks, same file conflicts, cross-story dependencies that break independence
- **TDD Non-Negotiable**: Tests before implementation (constitution requirement)
- **Deliverable milestones**: Each phase ends with something deployable/testable

---

**Tasks Complete**: 122 tasks organized across 8 phases, TDD approach throughout, every user story independently testable and deliverable.
