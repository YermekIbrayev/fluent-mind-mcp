# Tasks: Circuit Breaker & Resilience (T083-T090)

[← Back to Tasks Index](../tasks.md)

**Purpose**: System resilience to dependency failures

**⚠️ File Size Rule**: Goal ≤100 lines, yellow 101-150, HARD LIMIT 200 lines (validated by T102)

---

## Phase 10: Circuit Breaker & Resilience

**Purpose**: System resilient to dependency failures (Flowise API, Vector DB, Embedding Model)

**Contract**: get_system_health (contracts/get_system_health.json)

### Implementation (T083-T090)

- [ ] T083 [P] Implement CircuitBreaker class with state machine in src/fluent_mind_mcp/services/circuit_breaker_service.py
  - Class: CircuitBreaker with states (CLOSED, OPEN, HALF_OPEN)
  - Properties: failure_count, failure_threshold (default 3), timeout_seconds (default 300), last_failure_time, opened_time
  - Methods: call(operation), record_success(), record_failure(), _transition_state(), persist_state(), restore_state()
  - State transitions: CLOSED→OPEN (3 failures), OPEN→HALF_OPEN (5min timeout), HALF_OPEN→CLOSED (success), HALF_OPEN→OPEN (failure)
  - **Persistence**: State persisted to disk (circuit_breaker_state.json) on each transition
  - **Restoration**: State restored from disk on service initialization (survives server restarts)
  - **File location**: chroma_db/circuit_breaker_state.json (co-located with vector DB)

- [ ] T084 [P] Implement circuit breaker for Flowise API (3 failures, 5min timeout, CLOSED→OPEN→HALF_OPEN)
  - CircuitBreakerService.get_flowise_breaker() → CircuitBreaker instance
  - Wrap all FlowiseApiClient calls in circuit breaker
  - Record success/failure for each API call
  - Raise CircuitOpenError when circuit OPEN
  - Log state transitions

- [ ] T085 [P] Implement circuit breaker for Vector DB (3 failures, 5min timeout)
  - CircuitBreakerService.get_vector_db_breaker() → CircuitBreaker instance
  - Wrap all VectorDatabaseClient calls in circuit breaker
  - Record success/failure for each query/add/update operation
  - Raise CircuitOpenError when circuit OPEN
  - Log state transitions

- [ ] T086 [P] Implement circuit breaker for Embedding Model (3 failures, 5min timeout)
  - CircuitBreakerService.get_embedding_breaker() → CircuitBreaker instance
  - Wrap all EmbeddingClient calls in circuit breaker
  - Record success/failure for each embedding generation
  - Raise CircuitOpenError when circuit OPEN
  - Log state transitions

- [ ] T087 Integrate circuit breakers into FlowiseApiClient, VectorDatabaseClient, EmbeddingClient
  - Update each client to inject CircuitBreakerService in constructor
  - Wrap external calls with circuit breaker: breaker.call(lambda: actual_operation())
  - Handle CircuitOpenError gracefully (don't retry, return error to caller)
  - Log circuit state for observability

- [ ] T088 Add CIRCUIT_OPEN error messages (<30 tokens) to all MCP tools
  - Error code: CIRCUIT_OPEN
  - Message template: "{dependency} circuit open. Retry in {time_remaining}s."
  - Examples:
    - "Flowise API circuit open. Retry in 180s."
    - "Vector DB circuit open. Retry in 240s."
  - Token budget: 30 tokens
  - Include time_remaining calculated from opened_time + timeout_seconds

- [ ] T089 Add get_system_health MCP tool in src/fluent_mind_mcp/server.py (reports circuit states)
  - Tool definition: no parameters
  - Return SystemHealth model: status, vector_db_status, embedding_model_status, flowise_api_status, circuit_states, node_catalog_status
  - Circuit states: {dependency_name: {state, failure_count, opened_time, time_until_half_open}}
  - Status values: "HEALTHY", "DEGRADED", "UNHEALTHY"
  - Overall status: HEALTHY if all circuits CLOSED, DEGRADED if any OPEN, UNHEALTHY if multiple OPEN

- [ ] T090 Implement structured logging for all operations (vector search, build_flow, catalog refresh)
  - Update VectorSearchService, BuildFlowService, NodeCatalogService to use utils/logging.py
  - Log operation start: log_operation_start(operation_name, parameters)
  - Log operation end: log_operation_end(operation_name, duration, result_summary)
  - Log errors: log_error(operation_name, error, context)
  - Apply credential masking via CredentialMaskingFormatter
  - Include operation timing for performance monitoring

**Checkpoint**: Circuit breaker system operational, all dependencies protected

---

[← Back to Tasks Index](../tasks.md) | [Next: Testing & Polish →](05b-testing-polish.md)
