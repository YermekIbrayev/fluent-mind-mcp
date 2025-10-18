## Requirements *(mandatory)*

### Functional Requirements

**System Initialization (FR-000)**:
- **FR-000**: System MUST automatically install ChromaDB and download sentence-transformers/all-MiniLM-L6-v2 embedding model on first run if dependencies not present, displaying installation progress to user and falling back to descriptive error message if installation fails while allowing core MCP functionality to continue

**Vector Search & Templates (FR-001 to FR-015)**:
- **FR-001**: System MUST maintain local ChromaDB vector database in project folder with separate collections by entity type: `nodes` collection for node descriptions, `templates` collection for flow templates, `sdd_artifacts` collection for successful SDD artifacts, `failed_artifacts` collection for failed SDDs, `sessions` collection for session records
- **FR-002**: System MUST enable semantic search of vector DB for nodes using natural language queries returning results in <50 tokens
- **FR-003**: System MUST enable semantic search of vector DB for flow templates returning template_id and metadata in <50 tokens per result
- **FR-004**: System MUST store node descriptions including what (capability), why (use case), how (operation), and examples
- **FR-005**: System MUST store flow templates with template_id, name, description, required_nodes list, and full flowData structure
- **FR-006**: System MUST provide build_flow function accepting template_id as primary argument (<20 tokens per call)
- **FR-007**: System MUST provide build_flow function accepting node list with automatic connection inference using type-compatible chain algorithm: order nodes by flow pattern heuristics (Input → Processing → Memory → Output), connect consecutive nodes where output baseClass matches input baseClass requirement, validate all required inputs satisfied, return error if no valid chain found (<50 tokens per call)
- **FR-008**: System MUST support build_flow optional parameters (model, temperature, memory_type) for template customization
- **FR-009**: System MUST generate complete flowData structures within build_flow without exposing to AI context, including node positioning using left-to-right flow pattern algorithm (assign nodes to columns by connection depth, space vertically 200px apart within columns, space columns 300px apart horizontally)
- **FR-010**: System MUST create chatflows via Flowise API and return only chatflow_id and name (<30 tokens response)
- **FR-011**: System MUST return top 3-5 most relevant results from vector searches ranked by semantic similarity
- **FR-012**: System MUST support vector DB refresh/update when new Flowise nodes added
- **FR-013**: System MUST validate build_flow parameters and return compact errors (<50 tokens) on failure
- **FR-014**: System MUST handle vector DB queries with similarity threshold to filter low-relevance results
- **FR-015**: System MUST support querying vector DB for specific node categories (Chat Models, Memory, Tools, etc.)

**Data Management (FR-026 to FR-030)**:
- **FR-026**: System MUST provide manual cleanup commands for deleting artifacts older than specified age (e.g., "delete artifacts older than 6 months")
- **FR-027**: System MUST provide manual cleanup commands for removing failed patterns from failed_artifacts collection
- **FR-028**: System MUST provide manual cleanup commands for clearing sessions older than specified age or by outcome status
- **FR-029**: System MUST provide inspection commands showing storage statistics per collection (count, total size, oldest/newest entry dates)
- **FR-030**: System MUST never perform automatic deletion of any data from ChromaDB collections - all cleanup requires explicit user command

**Error Handling & Resilience (FR-031 to FR-040)**:
- **FR-031**: System MUST implement circuit breaker pattern for Flowise API calls with failure threshold of 3 consecutive failures
- **FR-032**: System MUST open circuit for 5 minutes after threshold reached, blocking further API calls to failing dependency
- **FR-033**: System MUST provide clear circuit status to user (open, closed, half-open) with reason and time until auto-retry
- **FR-034**: System MUST automatically retry (close circuit) after 5-minute timeout with single test request (half-open state)
- **FR-035**: System MUST allow user to manually reset circuit breaker at any time via command
- **FR-036**: System MUST track circuit breaker state per dependency (separate circuits for Flowise API, vector DB, embedding model)
- **FR-037**: System MUST provide compact error message (<50 tokens) when circuit is open explaining dependency unavailable and retry timing
- **FR-038**: System MUST log all circuit breaker state transitions (closed→open, open→half-open, half-open→closed, half-open→open) with timestamps
- **FR-039**: System MUST increment failure count only for dependency-level failures (network, timeout, 5xx errors), not for validation errors (4xx)
- **FR-040**: System MUST reset failure count to zero after successful operation when circuit is closed or half-open

**Dynamic Node Catalog (FR-016 to FR-025)**:
- **FR-016**: System MUST check node catalog cache staleness (24-hour threshold) before build_flow execution and query Flowise API `/api/v1/nodes-list` endpoint to refresh if stale
- **FR-017**: System MUST extract node metadata from API response including name, label, version, category, baseClasses, description, deprecated status
- **FR-018**: System MUST compare fetched node list with vector DB cache to identify new, updated, removed, or deprecated nodes
- **FR-019**: System MUST add new nodes to vector DB with full metadata including version and embeddings for semantic search
- **FR-020**: System MUST update existing nodes in vector DB when version or description changes
- **FR-021**: System MUST mark nodes as deprecated in vector DB when Flowise API indicates deprecation status
- **FR-022**: System MUST exclude deprecated nodes from vector search results or rank them lower with deprecation warnings
- **FR-023**: System MUST prioritize latest non-deprecated node version when multiple versions exist unless specific version requested
- **FR-024**: System MUST record timestamp and version metadata for cache validation after each node catalog refresh
- **FR-025**: System MUST fall back to cached vector DB with staleness warning when Flowise server unreachable during refresh

**User Story 8: Core SDD Artifact Learning System (FR-041 to FR-055)** [INVESTIGATE]:
- **FR-041**: System MUST store completed SDD artifact bundles (user request, spec, plan, tasks, design, chatflow_id) in ChromaDB `sdd_artifacts` collection after successful chatflow creation
- **FR-042**: System MUST generate vector embeddings for user request text to enable semantic search of historical artifacts
- **FR-043**: System MUST store artifact metadata (creation date, success status, user rating, chatflow_id, node versions used) with each bundle
- **FR-044**: System MUST search vector DB for similar historical requests before initiating full SDD workflow
- **FR-045**: System MUST retrieve cached design when semantic similarity >70% and present reuse option to user
- **FR-046**: System MUST present cached design in condensed format (<500 tokens): node list, connections, key configurations
- **FR-047**: System MUST support user approval/rejection workflow for cached designs with reason capture
- **FR-048**: System MUST create chatflow from cached design using <600 tokens total when user approves reuse
- **FR-049**: System MUST proceed with full SDD workflow when user rejects cached design or no match found
- **FR-050**: System MUST collect user feedback rating (1-5 stars) after cached design reuse
- **FR-051**: System MUST boost vector search relevance for high-rated artifacts (4-5 stars) and demote low-rated (1-2 stars)
- **FR-052**: System MUST present top 3 cached designs when multiple matches have similar scores (within 5%)
- **FR-053**: System MUST validate cached design compatibility with current node catalog before presenting to user
- **FR-054**: System MUST maintain vector search performance (<500ms) as artifact corpus grows to 50+ entries
**Testing & Validation (FR-106 to FR-115)**:
- **FR-106**: System MUST provide documented test checklists for each user story mapping to all acceptance scenarios with pass/fail checkboxes
- **FR-107**: Test checklists MUST include setup steps, test data requirements, expected results, and actual results fields for documentation
- **FR-108**: System MUST provide automated tests for critical paths: vector search accuracy (>90% relevance), build_flow chatflow creation (95%+ success), circuit breaker state transitions (100% correct)
- **FR-109**: Automated critical path tests MUST run on demand via test command and report pass/fail results with error details
- **FR-110**: Manual test execution MUST document test results with timestamp, tester name, pass/fail status, and notes per scenario
- **FR-111**: User story completion MUST require all acceptance scenarios pass (100% checklist completion) with documented evidence
- **FR-112**: Test checklists MUST be versioned alongside feature specification to maintain alignment with requirements
- **FR-113**: System MUST provide test data generators for populating vector DB with sample nodes and templates for testing
- **FR-114**: System MUST provide test utilities for resetting ChromaDB collections to clean state between test runs
- **FR-115**: System MUST provide validation commands to verify system health (all dependencies available, vector DB accessible, circuit breakers closed)

