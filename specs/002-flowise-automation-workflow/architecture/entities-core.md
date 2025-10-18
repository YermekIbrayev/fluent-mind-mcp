# Key Entities: Core System

**Scope**: Testing, Resilience, Simple Workflow entities

### Key Entities

**Testing & Validation Entities**:

- **TestChecklist**: Structured document mapping user story acceptance scenarios to executable test steps. Contains user_story_id, scenario_list (array of test scenarios), setup_steps (prerequisites, test data), expected_results per scenario, actual_results (filled during execution), pass_fail_status per scenario, test_timestamp, tester_name, notes. Versioned alongside spec. Stored as markdown or JSON. Provides reusable validation framework ensuring all requirements tested systematically. 100% scenario completion required for user story acceptance.

- **AutomatedCriticalPathTests**: Test suite covering critical system paths requiring automated validation. Includes: vector_search_accuracy_test (queries with known relevant results, validates >90% relevance), build_flow_creation_test (template-based and node-list chatflow creation, validates 95%+ success rate), circuit_breaker_state_test (simulates failures, validates state transitions 100% correct). Runs on-demand via test command. Reports pass/fail with error details. Faster than manual testing, catches regressions early.

- **TestDataGenerator**: Utility creating realistic sample data for test execution. Generates sample node descriptions with embeddings, flow templates with various complexity levels, SDD artifacts with semantic variations, failed patterns for warning validation. Ensures consistent, representative test data. Populates vector DB collections for repeatable testing. Parameterized to control data volume and diversity.

- **TestUtilities**: Helper functions supporting test execution. Includes reset_chromadb (clears all collections to clean state), validate_system_health (checks dependencies, circuits, DB accessibility), populate_test_data (loads sample data), verify_test_results (compares actual vs. expected outcomes). Reduces manual test setup effort, ensures test environment consistency.

**System Resilience Entities**:

- **CircuitBreaker**: State machine managing dependency health and request flow for external services (Flowise API, vector DB, embedding model). Tracks three states: closed (normal operation), open (dependency unavailable - blocking requests for 5 minutes), half-open (testing recovery with single request). Maintains failure_count (increments on network/timeout/5xx errors), last_failure_time, circuit_opened_time. Transitions: closed→open after 3 failures, open→half-open after 5min timeout, half-open→closed on success, half-open→open on failure. Separate circuit per dependency. User can manually reset. Prevents cascading failures and resource waste during outages.

**Simple Workflow Entities**:

- **VectorDatabase**: Local ChromaDB instance stored in project folder with separate collections by entity type: `nodes` (node descriptions with embeddings), `templates` (flow templates with embeddings), `sdd_artifacts` (successful SDD artifacts), `failed_artifacts` (failed SDD patterns), `sessions` (session records). Each collection has optimized metadata filters and embeddings tailored to query patterns. Enables semantic search returning relevant results in <500ms. Persists across sessions, updated when Flowise nodes change or artifacts are stored. Separate collections provide faster queries (search only relevant collection), clear data boundaries, and independent schema evolution.

- **NodeDescription**: Rich documentation for Flowise node type including what (capability), why (use case), how (operation), and examples. Vectorized and stored in DB enabling semantic matching. Returned to AI as compact summary (name, one-line description, primary use case) using <30 tokens.

- **FlowTemplate**: Pre-built chatflow pattern with template_id, name, description, required_nodes list, and complete flowData structure. Stored in vector DB with searchable metadata. AI retrieves template_id via semantic search, passes to build_flow without accessing full structure.

- **SearchQuery**: Natural language description from AI used to query vector DB for nodes or templates. Kept minimal (<30 tokens) by focusing on core capability/intent. Vector DB returns top 3-5 relevant results ranked by semantic similarity.

- **SearchResult**: Compact response from vector DB query containing result_id (node name or template_id), name, one-line description, and relevance score. Formatted for AI consumption using <50 tokens per result, enabling informed selection.

- **build_flow Function**: Single entry point for chatflow creation accepting minimal arguments (template_id OR node_list with connections="auto", plus optional parameters). When connections="auto", uses type-compatible chain algorithm: orders nodes by flow pattern heuristics (Input → Processing → Memory → Output), connects consecutive nodes where output baseClass matches input baseClass requirement, validates all required inputs satisfied, returns error if no valid chain found. Generates complete flowData internally, calls Flowise API, returns only chatflow_id and name (<30 tokens). Eliminates need for AI to construct workflows or specify connection details.

- **FlowDataStructure**: Internal chatflow structure (nodes array with position coordinates + edges array) generated by build_flow. Never exposed to AI context, only used for Flowise API calls. Uses left-to-right flow pattern for node positioning: assigns nodes to columns based on connection depth (inputs at column 0, directly connected nodes at column 1, etc.), spaces nodes vertically within each column (200px apart), spaces columns horizontally (300px apart), positions disconnected nodes at bottom. Creates readable flowchart-style layout in Flowise UI. Stored with templates in vector DB but retrieved internally by build_flow, not by AI.

**Dynamic Node Catalog Entities**:

- **NodeCatalogRefresh**: Process of fetching current node list from Flowise server and updating vector DB. Triggered on-demand before build_flow execution when cache staleness exceeds 24-hour threshold. Queries `/api/v1/nodes-list` endpoint, extracts metadata (name, version, baseClasses, category, description, deprecated), compares with cache, performs incremental updates. Completes within 30 seconds for 100-200 nodes (user waits during refresh), logs operation with timestamp and change count. Falls back to cached data with warning if refresh fails.

- **NodeMetadata**: Complete metadata for Flowise node type fetched from live server. Includes unique name (e.g., "chatOpenAI"), display label ("ChatOpenAI"), version number (8.3), category ("Chat Models"), baseClasses array (["ChatOpenAI", "BaseChatModel"]), description (rich text), deprecated status (boolean). Stored in vector DB with embeddings for semantic search, used for node selection and version prioritization.

- **NodeVersionRegistry**: Registry tracking multiple versions of same node type. Enables version comparison, deprecation tracking, and latest version selection. Stores version history with timestamps, identifies breaking changes, prioritizes non-deprecated versions. Supports queries like "get latest ChatOpenAI" or "check if chatOpenAI v7.0 deprecated".

- **CacheMetadata**: Metadata tracking vector DB freshness for node catalog. Includes last refresh timestamp, Flowise server version, total node count, last change detection timestamp. Used to determine when refresh needed (staleness threshold 24 hours), enables offline operation with staleness warning, persists across restarts.

- **DeprecationWarning**: Warning message generated when deprecated node detected during search or flow validation. Includes node name, version, deprecation date, recommended alternative (if available). Formatted for compact display (<50 tokens), helps AI avoid using outdated nodes, logged for template maintenance.

**Spec-Driven Workflow Entities**:

- **ComplexityAnalysis**: Assessment of user request determining workflow path (simple vs. spec-driven). Evaluates node count estimates, complexity keywords (agent, multi-step, conditional), template match confidence from vector search, and integration requirements. Completes in <1 second, returns binary routing decision with confidence score.

- **ChatflowSpecification**: Structured document describing complex chatflow without implementation details. Includes user intent summary, selected nodes with rationale, connection logic and data flow, expected behavior and outputs, edge case handling. Generated in <5 seconds, stored in project folder for reference and potential template creation.

- **ClarificationQuestion**: Structured question resolving ambiguities in chatflow request. Includes context (relevant spec section), specific question, 3-4 answer options with implications, recommended option based on best practices. Formatted as table (<200 tokens per question), max 5 questions per workflow.

- **ImplementationPlan**: Phase-by-phase breakdown of chatflow construction. Defines phases (node selection → connections → configuration → validation), success criteria per phase, dependencies and sequence, estimated complexity per phase. Generated in <10 seconds from approved specification.

- **TaskBreakdown**: Detailed task list for chatflow implementation. Includes specific node configurations (model parameters, prompts, tools), connection mappings (source node → target node + data mappings), validation steps (test inputs, expected outputs), acceptance criteria per task. Generated from implementation plan in <5 seconds.

- **ConsistencyAnalysis**: Validation check ensuring alignment across spec-plan-task artifacts. Identifies mismatches (tasks not covering spec requirements, plan phases missing from tasks, user intent drift), scores alignment percentage, reports specific issues with references. Executes in <3 seconds, blocks implementation if critical issues found.

- **ChatflowDesignSummary**: Human-readable text representation of planned chatflow for approval. Includes ASCII/text diagram of node layout, connection list with data flow annotations, configuration summary (models, parameters, prompts), validation approach (test scenarios). Formatted for readability (<500 tokens), presented before implementation.

- **FeedbackLoop**: Iterative refinement cycle handling user approval or change requests. Tracks iteration count (max 5), captures user feedback (approve, reject with changes, abandon), routes to appropriate phase (clarify for scope changes, plan for implementation changes), terminates with error after max iterations suggesting request rephrase.

- **WorkflowOrchestrator**: State machine managing spec-driven workflow phases. Tracks current phase (specify → clarify → plan → tasks → analyze → approve → implement), handles phase transitions and error recovery, manages user interaction touchpoints (clarification, approval), logs phase timing and outcomes, saves intermediate artifacts on abandonment.

**User Story 8: Core SDD Artifact Learning System Entities** [INVESTIGATE]:
