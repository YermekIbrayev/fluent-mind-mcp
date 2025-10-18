
**Simple Workflow Dependencies**:
- Existing Flowise MCP Server implementation (specs/001-flowise-mcp-server) providing create_chatflow tool
- Local file system access in project folder for vector database persistence
- ChromaDB for local vector database storage with built-in persistence, HNSW indexing, and multi-collection support (separate collections: nodes, templates, sdd_artifacts, failed_artifacts, sessions) - automatically installed on first run if not present
- sentence-transformers/all-MiniLM-L6-v2 model for generating 384-dimensional embeddings for semantic search - automatically downloaded on first run if not present
- Internet connectivity for initial dependency installation (ChromaDB via pip, embedding model download from Hugging Face)
- Flowise instance with accessible node component library for flowData generation
- Understanding of Flowise node type system, baseClass inheritance, and flowData schema
- Curated node descriptions (what, why, how, use cases) for initial DB population in `nodes` collection
- Access to Flowise examples and documentation for identifying 10-20 common chatflow patterns (RAG chatbot, simple Q&A, customer support, memory-enabled chat, etc.)
- Ability to create and export sample chatflows from Flowise UI for manual template curation into `templates` collection

**Dynamic Node Catalog Dependencies**:
- Flowise API `/api/v1/nodes-list` endpoint for fetching complete node catalog
- Flowise architecture documentation in `docs/flowise_architecture/` (overview, node system, components)
- HTTP client capability for API requests with retry and timeout handling
- JSON parsing capability for node metadata extraction
- Vector embedding generation for new/updated node descriptions
- Timestamp and versioning system for cache metadata tracking
- Existing Flowise MCP Server authentication for API access

**User Story 8: Core SDD Artifact Learning System Dependencies** [INVESTIGATE]:
- sentence-transformers/all-MiniLM-L6-v2 model for generating 384-dimensional embeddings for user request text
- ChromaDB `sdd_artifacts` collection for vector similarity search with cosine distance and HNSW indexing for <500ms performance
- Local vector DB storage for artifact bundles with JSON serialization support in `sdd_artifacts` collection
- Integration with spec-driven workflow completion events to trigger artifact storage
- Access to completed SDD artifacts (user request, spec, plan, tasks, design, chatflow_id)
- Node catalog comparison capability for compatibility validation
- User feedback collection mechanism (rating prompts, storage)
- Timestamp and metadata tracking for artifact management
- Manual cleanup command interface for user-initiated data deletion

**User Story 9: Failed SDD Storage Dependencies** [INVESTIGATE]:
- Failure detection hooks in SDD workflow (catch exceptions, user abandonment events, validation failures)
- Failure categorization logic (classify errors into 4 types: node_compatibility, connectivity, configuration, user_abandonment)
- Pattern clustering algorithm to group similar failed artifacts for threshold tracking
- User interface for presenting failure warnings with proceed/modify/abandon options

**User Story 10: User-Corrected Flow Import Dependencies** [INVESTIGATE]:
- Flowise API `GET /api/v1/chatflows/{id}` endpoint access for fetching chatflow details
- FlowData parsing capability to extract nodes, edges, configurations from Flowise JSON response
- User interface/command for collecting chatflow URL/ID and correction description input
- Validation logic to check corrected flow completeness and compatibility with current node catalog
- Association logic to link corrected flows with original failed artifacts (causality tracking)

**User Story 11: Session Versioning Dependencies** [INVESTIGATE]:
- UUID generation capability for unique session_id creation
- Event capture hooks throughout SDD workflow (clarification, plan generation, design approval, etc.)
- Persistent storage for session records with JSON serialization (5-10KB per session)
- Session query engine supporting filters (date range, outcome status, user_id, similar requests)
- Session analysis engine for cross-session pattern detection (correlation identification)
- Session export functionality in JSON format for external tools

**Spec-Driven Workflow Dependencies**:
- Speckit workflow implementation with commands: `speckit.specify`, `speckit.clarify`, `speckit.plan`, `speckit.tasks`, `speckit.analyze`
- Access to `.specify/commands/*` documentation for workflow step definitions
- Local file system access for storing intermediate artifacts (specs, plans, tasks) in project folder
- AI capability to generate structured specifications from natural language descriptions
- AI capability to generate clarification questions with multiple-choice options
- AI capability to perform consistency analysis across text documents (spec, plan, tasks)
- User interaction capability for presenting questions and collecting feedback
- State management for tracking workflow phase progression and iteration counts

**Error Handling & Resilience Dependencies**:
- Circuit breaker implementation library or pattern (e.g., pybreaker, custom implementation)
- Persistent storage for circuit breaker state (failure counts, timestamps, circuit status per dependency)
- Timer/scheduler capability for 5-minute timeout tracking and automatic half-open transitions
- Timestamp tracking for last_failure_time and circuit_opened_time per dependency
- Error classification logic to distinguish transient (network, timeout, 5xx) from permanent (4xx validation) errors

**Testing & Validation Dependencies**:
- Test checklist templates for each user story (markdown or JSON format) in feature directory
- Test automation framework for critical paths (pytest, unittest, or similar)
- Test data generation scripts for populating ChromaDB with sample nodes, templates, artifacts
- Test utilities for resetting ChromaDB collections to clean state between test runs
- System health validation commands checking dependencies, circuits, DB accessibility
- Test result documentation system (test execution logs, pass/fail tracking, timestamp recording)
- Version control for test checklists alongside specification documents

