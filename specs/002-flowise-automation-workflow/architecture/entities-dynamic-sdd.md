# Key Entities: Dynamic Catalog & Spec-Driven Workflow

**Scope**: Dynamic node catalog and spec-driven workflow entities

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
