# Tasks: Chatflow Automation System

**Input**: Design documents from `/specs/002-flowise-automation-workflow/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, contracts/
**Tests**: Manual checklists + critical path automation only (per constitution)
**MVP Scope**: P1 Stories 1-7 (P2 Stories 8-11 deferred)

---

## 🚨 MANDATORY RULES

### File Size Limits

**Every Python file MUST adhere to these limits**:
- 🎯 **Goal**: ≤100 lines (ideal, maintainable)
- ⚠️ **Yellow Zone**: 101-150 lines (needs justification)
- 🚫 **HARD LIMIT**: 200 lines (MUST NOT EXCEED)

**Enforcement**:
- Task T102 validates all files ≤200 lines
- Files >200 lines MUST be refactored before completion
- Files in yellow zone (150-200) require justification

### TDD Rule (STRICTLY ENFORCED)

**Red-Green-Refactor Cycle**:
1. **RED**: Write test FIRST - test MUST fail (or skip with pytest.mark.skip)
2. **GREEN**: Implement just enough to make test pass
3. **REFACTOR**: Improve code while keeping tests green

**A test CANNOT be counted as green/passing if it**:
- ❌ Wasn't actually executed (skipped without @pytest.mark.skip)
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

**Every implementation task now has**:
- ✅ Corresponding test task(s) BEFORE implementation
- ✅ Clear Pre-condition: Run pytest command → tests FAIL/SKIP
- ✅ Clear Post-condition: Run pytest command → tests PASS
- ✅ Specific test file and test function names

**See [05b-testing-polish.md](tasks/05b-testing-polish.md) for full testing requirements.**

**Organization**: Tasks split into modular files for token efficiency (≤150 lines per file)

---

## 📖 Task Navigation

### Core Phases
- **[Setup & Foundational](tasks/01-setup-foundational.md)** - 14 tasks (T001-T013 + T003a-k) **TDD READY**
  - Project structure, models, clients, ChromaDB setup
  - **TDD Infrastructure**: 74 tests created (64 unit + 10 integration) - all skip until implementation
  - **CRITICAL**: Phase 2 (Foundational) BLOCKS all user story work

- **[User Stories 1-2 (Vector Search)](tasks/02a-us1-us2.md)** - 24 tasks (T014-T037) **TDD ENFORCED**
  - US1: Vector node search (12 tasks: 2 test + 10 impl)
  - US2: Template search (12 tasks: 2 test + 10 impl)
  - **TDD Coverage**: 34 automated tests (27 unit + 7 integration)
  - **MVP Phase 1**: Core search functionality

- **[User Story 3 (Flow Building)](tasks/02b-us3.md)** - 22 tasks (T032-T053) **TDD ENFORCED**
  - US3: build_flow function (22 tasks: 3 test + 19 impl)
  - **TDD Coverage**: 35 automated tests (30 unit + 5 integration)
  - **MVP Phase 1**: Chatflow creation

- **[User Stories 4-5 (Support)](tasks/03-us4-us5.md)** - 14 tasks (T044-T057)
  - US4: Vector DB setup (7 tasks)
  - US5: Error handling (7 tasks)

- **[User Story 6 (Dynamic Catalog)](tasks/04a-us6.md)** - 11 tasks (T058-T068)
  - US6: Dynamic catalog refresh (11 tasks)
  - **MVP Phase 1**: Included in MVP

- **[User Story 7 (Spec-Driven Workflow)](tasks/04b-us7.md)** - 14 tasks (T069-T082)
  - US7: Spec-driven workflow (14 tasks)
  - **MVP Phase 1**: Complex chatflows

- **[Circuit Breaker & Resilience](tasks/05a-circuit.md)** - 8 tasks (T083-T090)
  - Circuit breaker system with persistence (8 tasks)

- **[Testing & Polish](tasks/05b-testing-polish.md)** - 28 tasks (T091-T110, including T093a)
  - Testing & validation (9 tasks including T093a)
  - Documentation (3 tasks)
  - Code quality (4 tasks)
  - Data management & cleanup (5 tasks T106-T110)

---

## Quick Reference

### Task Format
```
- [ ] [ID] [P?] [Story?] Description with file path
```

**Components**:
- `[P]`: Parallelizable (different files, no dependencies)
- `[US#]`: User story label (US1-US7)
- File path: Exact location for implementation

### Phase Dependencies

```
Phase 1 (Setup)
     ↓
Phase 2 (Foundational) ← CRITICAL: Blocks all user stories
     ↓
┌────┴────┬────────┬────────┐
US1      US2      US3      US7 (can run in parallel after Phase 2)
  ↓       ↓        ↓        ↓
Phase 10 (Circuit Breaker)
     ↓
Phase 11 (Testing)
     ↓
Phase 12 (Polish)
```

### MVP Scope (8-10 days)

**Included**:
- Phases 1-2: Setup + Foundational (2-3 days)
- Phase 3: US1 - Vector node search (1 day)
- Phase 4: US2 - Template search (1 day)
- Phase 5: US3 - build_flow function (2 days)
- Phase 9: US7 - Spec-driven workflow (2 days)
- Phase 10: Circuit breaker resilience (1 day)
- Phase 11: Testing validation (1 day)
- Phase 12: Documentation polish (0.5 days)

**Deferred to P2**:
- US4: Vector DB setup enhancements
- US5: Enhanced error handling
- US6: Dynamic catalog refresh
- US8-US11: Learning system features

---

## Summary Statistics

**Total Tasks**: 120+ (MVP Phase 1: P1 Stories 1-7) **+10-15 TDD test tasks added**

**Task Breakdown by Phase**:
- Setup & Foundational: 14 tasks (T001-T013 + T003a-k TDD infrastructure)
- User Stories 1-2: 24 tasks (T014-T037) **+6 TDD test tasks**
- User Story 3: 22 tasks (T032-T053) **+10 TDD test tasks**
- User Stories 4-5: 14 tasks (T044-T057)
- User Story 6: 11 tasks (T058-T068)
- User Story 7: 14 tasks (T069-T082)
- Circuit Breaker: 8 tasks (T083-T090)
- Testing: 9 tasks (T091-T098, T093a)
- Documentation: 3 tasks (T099-T101)
- Code Quality: 4 tasks (T102-T105)
- Data Management: 5 tasks (T106-T110)

**TDD Test Coverage (NEW)**:
- Setup Phase: 74 tests created (64 unit + 10 integration)
- US1 (Vector Search): 18 automated tests (15 unit + 3 integration)
- US2 (Template Search): 16 automated tests (12 unit + 4 integration)
- US3 (build_flow): 35 automated tests (30 unit + 5 integration)
- Critical Paths: 4 performance/regression tests
- **Total Automated Tests**: 143+ tests (US1-3: 69 tests, Setup: 74 tests)

**TDD Workflow Tasks**:
- Test-First Tasks: 7 tasks (T014-T015, T023-T024, T032-T034)
- Test-Driven Implementation: 46 tasks with [TDD-GREEN] label
- Refactor Tasks: 3 tasks with [TDD-REFACTOR] label

**Parallel Opportunities**: 30+ tasks marked [P] (25%+ can run in parallel)

**User Story Tasks**: 69 tasks with [US#] labels (58% directly mapped to user stories)

---

## Implementation Strategy

### MVP First (Recommended)

1. **Foundation** (Phases 1-2): Setup + Foundational → Foundation ready
2. **Core Search** (Phases 3-4): US1 + US2 → Test independently
3. **Flow Building** (Phase 5): US3 → Test independently
4. **Complex Workflows** (Phase 9): US7 → Test independently
5. **Resilience** (Phase 10): Circuit breaker → System hardened
6. **Validation** (Phase 11): Testing → All criteria met
7. **Launch** (Phase 12): Documentation → **MVP READY**

### Incremental Delivery (Post-MVP)

- After MVP: Add US6 (dynamic catalog) → Deploy
- After US6: Add US4 (vector DB enhancements) → Deploy
- After US4: Add US5 (enhanced errors) → Deploy
- After US5: P2 Stories 8-11 (learning system) → Future release

### Parallel Team Strategy

With 3+ developers after Foundational phase:
- **Dev A**: US1 → US4 → Testing
- **Dev B**: US2 → US5 → Documentation
- **Dev C**: US3 → US6 → Circuit Breaker
- **Dev D**: US7 → Integration

---

## File Structure

```
specs/002-flowise-automation-workflow/
├── tasks.md (this file - navigation hub)
└── tasks/
    ├── 01-setup-foundational.md (Setup + Foundational: T001-T013, T003a)
    ├── 02a-us1-us2.md (User Stories 1-2: T014-T031)
    ├── 02b-us3.md (User Story 3: T032-T043)
    ├── 03-us4-us5.md (User Stories 4-5: T044-T057)
    ├── 04a-us6.md (User Story 6: T058-T068)
    ├── 04b-us7.md (User Story 7: T069-T082)
    ├── 05a-circuit.md (Circuit Breaker: T083-T090)
    └── 05b-testing-polish.md (Testing & Polish: T091-T110)
```

**Constitution Compliance**: Principle VIII - All files ≤250 lines max (target ≤100, yellow 150-200, red >200), modular organization

**File Sizes (Updated with TDD)**:
- 01: 199 lines ⚠️ YELLOW (was 139, +60 for TDD infrastructure docs)
- 02a: 221 lines ⚠️ YELLOW (was 133, +88 for comprehensive TDD workflow)
- 02b: 228 lines ⚠️ YELLOW (was 102, +126 for comprehensive TDD workflow)
- 03: ~127 lines ✅ GREEN
- 04a: 102 lines ✅ GREEN
- 04b: 133 lines ✅ GREEN
- 05a: 83 lines ✅ GREEN
- 05b: 236 lines ⚠️ YELLOW (comprehensive testing polish)

**Justification for Yellow Zone Files**:
- 01: TDD infrastructure setup (74 tests) requires detailed documentation
- 02a, 02b: Comprehensive TDD workflow with test specifications (27+35 tests) requires detailed pre/post-conditions
- 05b: Complete testing validation framework requires comprehensive test scenarios

---

**Next**: Load specific task file for implementation
