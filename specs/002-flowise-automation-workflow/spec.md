# Feature Specification: Self-Learning Vector-Enhanced Chatflow Automation

**Feature Branch**: `002-flowise-automation-workflow`
**Created**: 2025-10-17
**Updated**: 2025-10-17 (v10)
**Status**: Draft - Clarified & Modularized
**Input**: User description: "create fully automated workflow for creation of flowise thru API call"
**Deployment Context**: Personal-use MCP server (single-user local deployment)
**MVP Scope**: Core Stories (US1, US2, US3, US7) - Essential chatflow automation with vector search, templates, and spec-driven workflow. Post-MVP Phase 1.5: US4, US5, US6 (vector DB population enhancements, error handling polish, dynamic catalog refresh). P2 Stories 8-11 deferred (learning system)

**Updates**:
- v1: Token-friendly script-based approach with minimal parameters
- v2: Vector database for node descriptions and flow templates with semantic search
- v3: Self-learning feedback system, new flow generation, specialized build functions, algorithmic node positioning
- v4: Added spec-driven development workflow for complex chatflows with human-in-the-loop validation
- v5: Added Flowise architecture reference and dynamic node catalog updates from live server
- v6: [INVESTIGATE] Added SDD artifact learning system - storing specs, plans, user inputs in vector DB for reuse without LLM fine-tuning
- v7: [INVESTIGATE] Enhanced learning system with failed SDD storage, user-corrected flow import, and session versioning for complete interaction history
- v8: **Modularization** - Split User Story 8 into 4 independently testable user stories (8, 9, 10, 11) following SDD best practices. Each story delivers independent value and can be prioritized separately.
- v9: **Clarification Session** - Resolved 13 critical ambiguities: dependency initialization (automatic), data retention (manual cleanup), error handling (circuit breaker pattern), testing strategy (manual checklists + critical path automation), MVP scope (P1 stories 1-7 only, P2 deferred). Added 115 new functional requirements, 7 NFR categories, 4 key entities, comprehensive edge cases, testing infrastructure requirements.
- v10: **Constitution Compliance** - Split 1210-line spec into 15 modular files (≤160 lines each, 12 files ≤100 lines). Organized by domain: user stories, requirements, architecture, with navigation index. Follows Principle VIII: Token-Efficient Architecture.

## Clarifications

### Session 2025-10-17

- Q: Vector Database Selection & Embedding Model → A: ChromaDB + sentence-transformers/all-MiniLM-L6-v2
- Q: Node Catalog Refresh Trigger Strategy → A: On-Demand Only (Lazy Loading) - Check staleness before each build_flow call
- Q: Automatic Connection Inference Algorithm → A: Type-Compatible Chain with Validation
- Q: Maximum Clarification Questions → A: Max 5 Questions
- Q: Node Positioning Algorithm → A: Left-to-Right Flow Pattern
- Q: Vector Database Collection Organization → A: Separate Collections by Entity Type
- Q: Initial Template Library Population → A: Manual curation from example chatflows
- Q: Sensitive Data Handling → A: No Special Handling (Personal Usage)
- Q: ChromaDB and Embedding Model Initialization → A: Automatic Installation
- Q: Data Retention and Cleanup Strategy → A: Manual Cleanup Commands
- Q: Cascading Failure Handling → A: Circuit Breaker Pattern
- Q: Acceptance Testing Strategy → A: Manual Testing with Checklists
- Q: MVP Scope Definition → A: P1 Stories Only (Stories 1-7)

---

## 📖 Specification Navigation

### User Stories

- **[P1: Core Automation (Stories 1-7)](user-stories/p1-core-automation.md)** - 159 lines
  - Vector search, flow templates, build_flow function, vector DB setup, error handling, dynamic node catalog, spec-driven workflow
  - **MVP Phase 1** - Complete core chatflow automation functionality

- **[P2: Learning System (Stories 8-11)](user-stories/p2-learning-system.md)** - 136 lines
  - SDD artifact learning, failed pattern storage, user-corrected flow import, session versioning
  - **Deferred to Phase 2** - Advanced learning features after core system validation

### Requirements

- **[Functional Requirements - P1](requirements/functional-p1.md)** - 82 lines
  - FR-000 to FR-070, FR-106-115: System initialization, vector search, templates, data management, circuit breaker, dynamic catalog, spec-driven workflow, testing infrastructure

- **[Functional Requirements - P2](requirements/functional-p2.md)** - 79 lines
  - FR-041 to FR-105: Learning system requirements for artifact storage, failure tracking, corrections, and session management

- **[Non-Functional Requirements - P1](requirements/nfr-p1.md)** - 78 lines
  - Token efficiency, performance, scalability, reliability, observability, testing for core system

- **[Non-Functional Requirements - P2](requirements/nfr-p2.md)** - 61 lines
  - Performance, reliability, observability requirements for learning system features

### Architecture

- **[Entities: Core System](architecture/entities-core.md)** - 69 lines
  - Testing entities (TestChecklist, AutomatedTests, TestDataGenerator, TestUtilities)
  - System resilience (CircuitBreaker)
  - Simple workflow entities (VectorDatabase, NodeDescription, FlowTemplate, SearchQuery, build_flow function, FlowDataStructure)

- **[Entities: Dynamic Catalog & Spec-Driven](architecture/entities-dynamic-sdd.md)** - 37 lines
  - Dynamic node catalog (NodeCatalogRefresh, NodeMetadata, NodeVersionRegistry, CacheMetadata, DeprecationWarning)
  - Spec-driven workflow (ComplexityAnalysis, ChatflowSpecification, ClarificationQuestion, ImplementationPlan, TaskBreakdown, ConsistencyAnalysis, ChatflowDesignSummary, FeedbackLoop, WorkflowOrchestrator)

- **[Entities: P2 Learning System](architecture/entities-p2.md)** - 50 lines
  - Story 8: ArtifactBundle, ArtifactEmbedding, SimilarityScore, CachedDesign, UserFeedbackRating, ReusePath, ArtifactMetadata, CompatibilityValidator, ArtifactCorpus
  - Story 9: FailedArtifact, FailureWarning, FailurePattern
  - Story 10: CorrectedFlowImport, FlowDataExtraction, CorrectionDescription
  - Story 11: SessionRecord, SessionEvent, SessionAnalysis, SessionQuery

### Specification Sections

- **[Edge Cases](edge-cases.md)** - 114 lines
  - Comprehensive edge case documentation covering system initialization, data management, circuit breaker, testing, vector search, dynamic catalog, spec-driven workflow, and all P2 user stories

- **[Success Criteria](success-criteria.md)** - 100 lines
  - 74 measurable outcomes with specific targets across all user stories and system components

- **[Assumptions](assumptions.md)** - 123 lines
  - General system assumptions, MVP scope assumptions, testing assumptions, error handling assumptions, and feature-specific assumptions for all user stories

- **[Dependencies](dependencies.md)** - 80 lines
  - Simple workflow dependencies, dynamic catalog dependencies, error handling dependencies, testing dependencies, and P2 learning system dependencies

- **[Out of Scope](out-of-scope.md)** - 95 lines
  - MVP Phase 1 deferrals (P2 stories), simple workflow exclusions, dynamic catalog exclusions, and P2 learning system out-of-scope items

---

## Constitution Compliance

This modularized specification follows the project constitution:

- **Principle VIII: Token-Efficient Architecture** - All files ≤160 lines (12 files ≤100 lines, 3 files in 100-150 yellow zone)
- **Principle VII: Documentation Excellence** - Clear, navigable, token-optimized structure
- **Vertical Slice Organization** - Grouped by domain (user stories, requirements, architecture)

**File Structure**:
```
specs/002-flowise-automation-workflow/
├── spec.md (this file - 70 lines)
├── user-stories/
│   ├── p1-core-automation.md (159 lines)
│   └── p2-learning-system.md (136 lines)
├── requirements/
│   ├── functional-p1.md (82 lines)
│   ├── functional-p2.md (79 lines)
│   ├── nfr-p1.md (78 lines)
│   └── nfr-p2.md (61 lines)
├── architecture/
│   ├── entities-core.md (69 lines)
│   ├── entities-dynamic-sdd.md (37 lines)
│   └── entities-p2.md (50 lines)
├── edge-cases.md (114 lines)
├── success-criteria.md (100 lines)
├── assumptions.md (123 lines)
├── dependencies.md (80 lines)
└── out-of-scope.md (95 lines)
```

**Total**: 15 files, ~1,240 lines (organized from 1,210-line monolith)

**Constitution Location**: `/Users/yermekibrayev/work/ai/fluent-mind-mcp/.specify/memory/constitution.md`
