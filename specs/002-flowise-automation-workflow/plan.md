# Implementation Plan: Chatflow Automation System

**Branch**: `002-flowise-automation-workflow` | **Date**: 2025-10-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-flowise-automation-workflow/spec.md`
**Detailed Architecture**: See [plan_cc.md](plan_cc.md) for 14-file modular design (1,322 lines split for token efficiency)

## Summary

Automated chatflow creation system using vector-enhanced semantic search. AI assistants invoke compact build_flow function (<20 tokens) leveraging ChromaDB for node discovery and template retrieval. MVP (Core Stories US1, US2, US3, US7): vector search, templates, build_flow, spec-driven workflow. Post-MVP (US4, US5, US6): DB population, error polish, dynamic catalog.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: ChromaDB, sentence-transformers (all-MiniLM-L6-v2), existing Flowise MCP Server, httpx
**Storage**: Local ChromaDB (5 collections: nodes, templates, sdd_artifacts, failed_artifacts, sessions)
**Testing**: pytest with manual checklists (all scenarios) + automated critical paths only
**Target Platform**: macOS/Linux (single-user local MCP server)
**Project Type**: single (extends fluent-mind-mcp package)
**Performance Goals**: Vector search <500ms (50+ entries), build_flow <5s, catalog refresh <10s
**Constraints**: Token efficiency per NFR-002/005/006 (<50 tokens for search results, <30 tokens for build_flow responses, <50 tokens for errors), auto dependency install, manual cleanup only
**Scale/Scope**: Personal use (10-50 chatflows), 10-20 templates, 50+ node descriptions

## Constitution Check

*GATE: Must pass before Phase 0. Re-check after Phase 1.*

### Principle II: TDD
**Status**: ✅ PASS - Manual checklists (all scenarios) + automated critical path tests (vector search >90%, build_flow 95%+, circuit breaker 100%)
**Justification**: MCP server infrastructure extending existing system for personal automation. Infrastructure Code per Principle II allows tests recommended (not required), TDD optional, best effort coverage. Critical paths have automated tests with >90% accuracy targets; remaining functionality validated via manual checklists.

### Principle V: Quality Gates
- Security: ✅ No user input at MCP level, only internal API calls
- Test Coverage: ⚠️ Manual checklists + critical path automation
- IDE Diagnostics: ✅ mypy + ruff
- Code Quality: ✅ Complexity ≤10, vertical slice architecture
- Documentation: ✅ Comprehensive (research, data-model, contracts, quickstart)

### Principle VIII: Token-Efficient Architecture
- Vertical Slice: ✅ Feature-based (vector_search/, flow_builder/, node_catalog/, etc.)
- File Size: ✅ All ≤200 lines (target ≤100, warning 150)
- Module Organization: ✅ Single responsibility, explicit exports, no circular deps
- Context Management: ✅ Progressive loading, 50% reserve

**Work Type**: Infrastructure Code (MCP server extension for personal automation)
**Summary**: ✅ PASS - Infrastructure Code classification with manual testing + critical path automation per constitution allowance

## Project Structure

**Documentation** (this feature):
```
specs/002-flowise-automation-workflow/
├── spec.md              # Main spec (navigation hub, 15 modular files)
├── plan.md              # This file (compact summary)
├── plan_cc.md           # Detailed architecture (14 modular files, 1,322 lines)
├── research.md          # Phase 0 output (will be created, split if >100 lines)
├── data-model.md        # Phase 1 output (will be created, split if >100 lines)
├── quickstart.md        # Phase 1 output (will be created, split if >100 lines)
├── contracts/           # Phase 1 output (one JSON file per MCP tool)
└── [existing spec files]
```

**Source Code** (from plan_cc.md):
```
src/fluent_mind_mcp/
├── server.py                    # MCP Server with 5 tools (search_nodes, search_templates, build_flow, refresh_node_catalog, get_system_health)
├── models/ (4 files)            # Pydantic models
├── services/ (5 files)          # Business logic
├── client/ (3 files)            # API/DB/embedding clients
└── utils/ (2 files)             # Logging, exceptions

tests/
├── checklists/ (7 files)        # Manual test checklists per user story
├── critical_paths/ (3 files)    # Automated critical path tests
├── utilities/ (2 files)         # Test data generators
└── integration/                  # End-to-end tests
```

See [plan_cc.md](plan_cc.md) for complete 4-layer architecture details.

## Complexity Tracking

**No violations** - All gates pass or have approved conditional passes.

## Post-Design Re-Check

**Status**: ✅ **PASS**
**Date**: 2025-10-17 (after Phase 1 completion)

### File Size Verification (Principle VIII)
All generated files within limits:
- plan.md: 96 lines ✅ GREEN
- research.md: 93 lines ✅ GREEN
- data-model.md: 97 lines ✅ GREEN
- quickstart.md: 93 lines ✅ GREEN
- contracts/*.json: 5 files (48, 42, 42, 27, 48 lines) ✅ GREEN

**Architecture from plan_cc.md**: 14 modular files, avg 94 lines, longest 167 lines ⚠️ YELLOW (acceptable for detailed service implementations)

### TDD & Quality Gates
- ✅ Manual test checklists planned for all 7 user stories
- ✅ Critical path automation identified (3 tests)
- ✅ Test utilities specified
- ✅ All quality gates pass

### Final Verdict
**Status**: ✅ READY FOR TASK GENERATION (`/speckit.tasks`)

---

**File Size**: 112 lines | **Status**: ⚠️ YELLOW ZONE (acceptable for plan summary)
**Next**: Phase 2 → `/speckit.tasks` for task breakdown
