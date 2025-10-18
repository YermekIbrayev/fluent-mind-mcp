# Tasks: Testing & Polish (T091-T110)

[← Back to Tasks Index](../tasks.md)

**Purpose**: Validation, documentation, and production readiness

---

## 🚨 MANDATORY RULES

### File Size Limits

**Every Python file MUST adhere to these limits**:
- 🎯 **Goal**: ≤100 lines (ideal, green zone)
- ⚠️ **Yellow Zone**: 101-150 lines (needs justification)
- 🚫 **HARD LIMIT**: 200 lines (MUST NOT EXCEED)

**Validated by T102**: Files >200 lines MUST be refactored before completion.

### TDD Rule

**A test CANNOT be counted as green/passing if it**:
- ❌ Wasn't actually executed (skipped)
- ❌ Wasn't implemented (placeholder/stub)
- ❌ Has placeholder assertions (e.g., `assert True`)
- ❌ Doesn't do actual work (mocked without verification)
- ❌ Tests nothing meaningful (empty test body)

**Only count tests as passing if they**:
- ✅ Were executed and completed
- ✅ Are fully implemented with real logic
- ✅ Have meaningful assertions that verify behavior
- ✅ Test actual functionality (not just mocks)
- ✅ Can catch real defects

**This applies to ALL test tasks**: T091-T098, including automated and manual tests.

---

## Phase 11: Testing & Validation

**Purpose**: Manual checklists + critical path automation for MVP acceptance

### Critical Path Automation (T091-T093a)

All automated tests can run in parallel - different files, independent validations

- [ ] T091 [P] Implement test_vector_search_accuracy.py in tests/critical_paths/ (>90% relevance target)
  - Test: Query 20 predefined descriptions, verify top result is expected node
  - Acceptance: ≥18/20 correct (90% accuracy)
  - Assertions: relevance_score ≥0.7, expected node in top 3 results
  - **Performance assertion**: Average search time <500ms per query (per NFR-003)
  - Test data: Generate via TestDataGenerator

- [ ] T092 [P] Implement test_build_flow_creation.py in tests/critical_paths/ (>95% success rate target)
  - Test: Create 20 chatflows (10 from templates, 10 from node lists)
  - Acceptance: ≥19/20 succeed (95% success rate)
  - Assertions: chatflow_id returned, chatflow exists in Flowise, flowData valid
  - **Performance assertion**: Average build_flow time <10s for templates, <15s for custom nodes (per NFR-004)
  - Test data: Use curated templates and common node combinations

- [ ] T093 [P] Implement test_circuit_breaker_transitions.py in tests/critical_paths/ (100% correct target)
  - Test: Simulate 3 failures → verify OPEN, wait 5min → verify HALF_OPEN, succeed → verify CLOSED
  - Acceptance: 100% correct state transitions
  - Assertions: state matches expected at each step, failure_count accurate, timeout enforced
  - Mock external dependencies to force failures

- [ ] T093a [P] Implement test_performance_regression.py in tests/critical_paths/ (baseline tracking)
  - Test: Measure and track performance baselines for all critical operations
  - Operations: vector_search (target <500ms), build_flow_template (target <10s), build_flow_nodes (target <15s), catalog_refresh (target <30s per NFR-008)
  - Assertions: No operation exceeds 120% of baseline time
  - Store baselines in tests/performance_baselines.json
  - Fail test if performance degrades >20% from baseline

### Test Utilities (T094-T095)

- [ ] T094 [P] Implement TestDataGenerator in tests/utilities/test_data_generator.py (20+ nodes, 10+ templates, 15+ artifacts)
  - Method: generate_node_descriptions(count: int = 20) → list[NodeDescription]
  - Method: generate_flow_templates(count: int = 10) → list[FlowTemplate]
  - Method: generate_search_queries(count: int = 15) → list[str]
  - Include realistic data: varied categories, descriptions, use cases
  - Ensure deterministic generation (seed for reproducibility)

- [ ] T095 [P] Implement ChromaDBTestUtilities in tests/utilities/test_utilities.py (reset, health check, populate)
  - Method: reset_test_database() → None (delete all collections, recreate)
  - Method: health_check() → bool (verify all collections exist and queryable)
  - Method: populate_with_test_data(nodes, templates) → None (bulk add test data)
  - Method: clear_collection(collection_name: str) → None
  - Use separate test database path: chroma_db_test/

### Manual Testing Execution (T096-T098)

- [ ] T096 Execute all 7 manual test checklists and document results
  - Run checklists for US1, US2, US3, US4, US5, US6, US7
  - Mark each scenario as PASS or FAIL
  - Document any failures with notes
  - Calculate pass rate per user story
  - Target: 100% pass rate for MVP acceptance

- [ ] T097 Run automated critical path tests and verify targets met
  - Execute: pytest tests/critical_paths/ -v
  - Verify test_vector_search_accuracy: ≥90% accuracy, <500ms avg
  - Verify test_build_flow_creation: ≥95% success rate, <10-15s avg
  - Verify test_circuit_breaker_transitions: 100% correct
  - Verify test_performance_regression: No degradation >20%
  - Document results in test report
  - **TDD Rule**: Only count tests as passing if fully implemented and executed (no skipped/placeholder tests)

- [ ] T098 Validate quickstart.md scenarios (5 steps, <5 minutes total)
  - Follow quickstart.md step-by-step from clean environment
  - Time each step (install, init, test search, test template, test build_flow)
  - Verify all steps complete successfully
  - Total time should be <5 minutes
  - Document any deviations or issues

**Checkpoint**: All acceptance criteria met, MVP ready for deployment

---

## Phase 12: Documentation & Polish

**Purpose**: Production-ready documentation and final refinements

### Documentation (T099-T101)

All documentation tasks can run in parallel - different files

- [ ] T099 [P] Create README.md with installation, usage, examples
  - Sections: Overview, Features, Installation, Quick Start, Usage, MCP Tools, Architecture, Contributing
  - Include code examples for each MCP tool
  - Link to quickstart.md for 5-minute setup
  - Badge: constitution compliance, test coverage
  - Keep concise: ≤150 lines

- [ ] T100 [P] Update quickstart.md with actual paths and commands
  - Verify all paths are correct (post-implementation)
  - Test all commands work from clean environment
  - Update expected outputs to match actual output
  - Add troubleshooting section with common issues
  - Keep concise: ≤100 lines

- [ ] T101 [P] Document all 5 MCP tools in docs/tools.md (or server.py docstrings)
  - For each tool: name, description, parameters, returns, errors, examples
  - Tools: search_nodes, search_templates, build_flow, refresh_node_catalog, get_system_health
  - Include token budgets for responses
  - Link to contracts/*.json for detailed schemas
  - Provide usage examples with expected outputs
  - Keep concise: ≤150 lines total or comprehensive docstrings

### Code Quality (T102-T105)

- [ ] T102 Validate all file sizes ≤200 lines (HARD LIMIT: goal ≤100, yellow 101-150, red >150)
  - Run: find src/ -name "*.py" -exec wc -l {} \; | awk '$1 > 200'
  - Identify any files >200 lines → **MUST refactor immediately (HARD LIMIT violation)**
  - Identify files 151-200 lines → Refactor or provide strong justification
  - Identify files 101-150 lines → Yellow zone, document justification
  - Goal: All files ≤100 lines (green zone)
  - Generate report: green/yellow/red breakdown per file

- [ ] T103 Run mypy type checking and fix any issues
  - Execute: mypy src/fluent_mind_mcp/ --strict
  - Fix type errors, add type hints where missing
  - Target: 0 type errors
  - Document any type: ignore with justification

- [ ] T104 Run ruff linting and fix any issues
  - Execute: ruff check src/ tests/
  - Fix linting errors (unused imports, formatting, etc.)
  - Apply auto-fixes: ruff check --fix
  - Target: 0 linting errors

- [ ] T105 Verify code complexity ≤10 for all functions (radon cc)
  - Execute: radon cc src/fluent_mind_mcp/ -a -nb
  - Identify functions with cyclomatic complexity >10
  - Refactor complex functions into smaller helper methods
  - Target: all functions ≤10 complexity

### Data Management (T106-T110)

- [ ] T106 Implement clear_all_collections command in src/fluent_mind_mcp/scripts/cleanup.py
  - Command: python -m fluent_mind_mcp.scripts.cleanup --all
  - Clears all 5 ChromaDB collections (nodes, templates, sdd_artifacts, failed_artifacts, sessions)
  - Prompts for confirmation before deletion
  - Logs: "Cleared X collections. Vector DB reset complete."

- [ ] T107 Implement clear_collection command for specific collection
  - Command: python -m fluent_mind_mcp.scripts.cleanup --collection <name>
  - Clears specified collection only
  - Options: nodes, templates, sdd_artifacts, failed_artifacts, sessions
  - Validates collection name before deletion

- [ ] T108 Implement clear_old_sessions command with age threshold
  - Command: python -m fluent_mind_mcp.scripts.cleanup --sessions --older-than <days>
  - Clears session records older than specified days
  - Default: 30 days
  - Example: --sessions --older-than 7 (clears sessions >7 days old)

- [ ] T109 Implement clear_failed_artifacts command
  - Command: python -m fluent_mind_mcp.scripts.cleanup --failed-artifacts
  - Clears all failed SDD artifact entries
  - Option: --keep-recent <count> (keep N most recent failures for learning)
  - Default: keeps 10 most recent failures

- [ ] T110 Add cleanup documentation to README.md
  - Section: Data Management & Cleanup
  - Document all cleanup commands with examples
  - Include warnings about data loss
  - Provide backup recommendations
  - Note: Manual cleanup only per FR-011

**Checkpoint**: MVP Phase 1 complete - production-ready, documented, tested

---

## Summary

**Total Tasks**: 28
- Testing: 9 tasks (T091-T098, T093a)
- Documentation: 3 tasks (T099-T101)
- Code Quality: 4 tasks (T102-T105)
- Data Management: 5 tasks (T106-T110)

**Parallel Opportunities**: 7 tasks marked [P] (25%)
- T091-T095 (automated tests and utilities, T093a)
- T099-T101 (documentation files)

**Critical Path**: T091 → T097 (critical path tests → execution validation)

**Estimated Time**:
- Testing: 1.5 days
- Documentation & Polish: 0.5 days
- Data Management: 0.5 days

---

[← Back to Tasks Index](../tasks.md)
