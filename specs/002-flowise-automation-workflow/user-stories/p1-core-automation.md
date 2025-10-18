# User Stories: P1 Core Automation (Stories 1-7)

**Priority**: P1 (MVP Phase 1)
**Status**: Defines core chatflow automation functionality

---

## User Story 1 - Vector Search for Node Selection with Semantic Matching (Priority: P1)

AI assistants need to query vector database with user's natural language description to retrieve relevant node types and use cases, enabling informed flow design decisions without loading full node catalog into conversation context.

**Why this priority**: Semantic search eliminates need for AI to know all node types upfront. Vector database stores node descriptions (what, why, how, use cases) enabling sub-second retrieval of only relevant nodes using <50 tokens per query.

**Independent Test**: Can be fully tested by querying vector DB with descriptions like "chat with memory" and verifying relevant nodes (ChatOpenAI, BufferMemory) are returned with compact summaries. Delivers value through intelligent node discovery at minimal token cost.

**Acceptance Scenarios**:

1. **Given** user description "chatbot that remembers conversation", **When** AI queries vector DB, **Then** relevant nodes (ChatOpenAI, BufferMemory, ConversationChain) returned with use cases using <50 tokens
2. **Given** query "search documents using embeddings", **When** AI searches vector DB, **Then** RAG-related nodes (DocumentLoader, VectorStore, RetrievalQA) returned
3. **Given** vague description "AI agent", **When** AI queries vector DB with similarity threshold, **Then** top 3-5 most relevant agent nodes returned with differentiation
4. **Given** vector DB query result, **When** AI receives node summaries, **Then** compact format includes node name, one-line description, primary use case

---

## User Story 2 - Flow Template Retrieval via Semantic Search (Priority: P1)

AI assistants need to search vector database for pre-built flow templates matching user's description, retrieving template metadata (not full flowData) that identifies the best starting point for workflow construction.

**Why this priority**: Template search eliminates guesswork. Vector DB stores flow templates with rich descriptions enabling AI to find proven patterns through semantic matching, then reference them by ID for build_flow function.

**Independent Test**: Can be fully tested by searching templates with descriptions like "customer support chatbot" and verifying relevant templates are returned with metadata. Delivers value through pattern discovery without token overhead.

**Acceptance Scenarios**:

1. **Given** user description "chatbot for customer support with knowledge base", **When** AI searches flow templates, **Then** relevant templates (rag-chatbot, support-agent) returned with template_id and summary
2. **Given** query "data analysis agent with tools", **When** AI searches vector DB, **Then** agent templates with tool capabilities returned ranked by relevance
3. **Given** template search results, **When** AI receives template metadata, **Then** compact format includes template_id, name, description, required_nodes list (not full flowData)
4. **Given** selected template_id, **When** AI invokes build_flow function, **Then** only template_id passed as argument (<20 tokens) to generate chatflow

---

## User Story 3 - Compact build_flow Function with Minimal Arguments (Priority: P1)

AI assistants need to invoke build_flow function with minimal arguments (template_id or node_list + optional parameters) to create chatflows, keeping token usage minimal by referencing stored templates rather than specifying full structures.

**Why this priority**: Single function interface with compact arguments is the ultimate token efficiency goal. AI provides only high-level intent, build_flow handles all flowData generation internally.

**Independent Test**: Can be fully tested by calling build_flow with various argument combinations and verifying chatflows are created correctly. Delivers core value through minimal token interface.

**Acceptance Scenarios**:

1. **Given** template_id from search, **When** AI calls build_flow(template_id="tmpl_123"), **Then** chatflow created from template using <20 tokens for invocation
2. **Given** custom node selection from vector search, **When** AI calls build_flow(nodes=["chatOpenAI", "bufferMemory"], connections="auto"), **Then** chatflow with specified nodes created using type-compatible chain algorithm (order by flow pattern, connect where baseClass matches, validate required inputs) using <50 tokens
3. **Given** template with parameters, **When** AI calls build_flow(template_id="tmpl_123", model="gpt-4", temperature=0.7), **Then** template instantiated with custom parameters
4. **Given** build_flow execution, **When** chatflow created successfully, **Then** response contains only chatflow_id and name using <30 tokens

---

## User Story 4 - Vector Database Setup and Maintenance (Priority: P2)

System needs to populate vector database with node descriptions (what, why, how, use cases) and flow templates, enabling semantic search without requiring manual curation for each query.

**Why this priority**: Database is foundation for semantic search. One-time setup enables unlimited token-efficient queries. Must handle updates as Flowise adds new nodes.

**Independent Test**: Can be fully tested by populating DB with sample nodes/templates, querying with various descriptions, and verifying relevant results returned. Delivers value through searchable knowledge base.

**Acceptance Scenarios**:

1. **Given** Flowise node type definitions, **When** system processes node metadata, **Then** vector embeddings created for each node with description covering what, why, how, use cases
2. **Given** manually curated flow templates (10-20 common patterns created from Flowise examples: RAG chatbot, simple Q&A, customer support, memory-enabled chat), **When** system populates initial template library during setup, **Then** templates stored in ChromaDB `templates` collection with rich descriptions, flowData structure, and assigned template_id
3. **Given** node description update, **When** system refreshes vectors, **Then** existing embeddings updated without requiring full rebuild
4. **Given** vector DB query for "memory", **When** search executes, **Then** relevant nodes (BufferMemory, BufferWindowMemory, ConversationMemory) returned ranked by relevance

---

## User Story 5 - Compact Error Handling and Validation (Priority: P3)

AI assistants need compact error messages (<50 tokens) when vector search finds no results or build_flow fails, maintaining token efficiency even in error scenarios while providing actionable guidance.

**Why this priority**: Error handling must maintain token efficiency. Clear, concise errors enable AI to recover or inform user without verbose diagnostics.

**Independent Test**: Can be fully tested by triggering various error conditions and verifying messages are actionable within token budget. Delivers value through reliable error handling.

**Acceptance Scenarios**:

1. **Given** vector search with no matches, **When** AI receives empty result, **Then** message suggests query refinement using <30 tokens
2. **Given** invalid template_id, **When** AI calls build_flow, **Then** error indicates template not found and suggests searching templates using <40 tokens
3. **Given** missing required parameter, **When** build_flow validates inputs, **Then** error specifies which parameter needed using <50 tokens
4. **Given** build_flow failure during execution, **When** error occurs, **Then** response includes error type and recovery suggestion using <50 tokens

---

## User Story 6 - Dynamic Node Catalog Refresh from Flowise Server (Priority: P2)

AI assistants and system need to fetch latest node catalog from Flowise server before creating flows, ensuring vector database contains current node types, versions, and deprecation status for accurate flow construction.

**Why this priority**: Flowise regularly adds/updates/deprecates nodes. Querying live server ensures AI always works with latest node capabilities, preventing outdated node selection and flow creation failures. Essential for build_flow accuracy but not blocking for vector search MVP.

**Independent Test**: Can be fully tested by calling Flowise API to list nodes, comparing with vector DB cache, and updating DB with new/changed nodes. Delivers value through accurate, up-to-date node recommendations.

**Acceptance Scenarios**:

1. **Given** build_flow function invoked, **When** system checks cache staleness (>24h threshold), **Then** system queries Flowise API `/api/v1/nodes-list` endpoint for current node list before proceeding with flow creation
2. **Given** Flowise API returns node list, **When** system processes response, **Then** each node's version, baseClass, category, deprecated status, and description extracted
3. **Given** fetched node list, **When** system compares with vector DB cache, **Then** new nodes added, updated nodes refreshed, removed nodes marked as deprecated
4. **Given** node marked as deprecated in Flowise, **When** AI searches vector DB, **Then** deprecated nodes excluded from search results or ranked lower with deprecation warning
5. **Given** multiple versions of same node exist, **When** AI queries vector DB, **Then** system returns latest non-deprecated version unless specific version requested
6. **Given** node catalog refresh completes, **When** vector DB updated, **Then** timestamp and version metadata recorded for cache validation
7. **Given** Flowise server unreachable during refresh, **When** refresh fails, **Then** system falls back to cached vector DB with staleness warning (<50 tokens)
8. **Given** node catalog refresh scheduled, **When** system detects no changes since last refresh, **Then** refresh skips DB update and logs "no changes" (<30 tokens)

**Flowise API Reference**:
- Endpoint: `GET /api/v1/nodes-list` (returns full node catalog)
- Response: Array of node metadata including `name`, `label`, `version`, `category`, `baseClasses`, `description`, `deprecated`
- Architecture docs: `docs/flowise_architecture/components/01-node-system.md`

---

## User Story 7 - Spec-Driven Development Workflow for Complex Chatflows (Priority: P1)

AI assistants need to detect when user request is complex or novel (not in flow template database), triggering a spec-driven development workflow that creates a chatflow specification, gathers user feedback through clarification questions, generates an implementation plan, and produces the chatflow only after user approval.

**Why this priority**: Complex or novel chatflows require human validation before implementation to ensure they meet user intent. Using the speckit workflow (`.specify/commands/*`) provides structured phases (specify → clarify → plan → tasks → analyze → implement) with built-in quality gates, preventing token-heavy trial-and-error cycles.

**Independent Test**: Can be fully tested by requesting complex chatflows (e.g., "multi-agent system with conditional routing and 5 specialized tools"), verifying system generates spec, asks clarifying questions, creates plan, presents design for approval, and only creates chatflow after user confirms. Delivers value through high-confidence complex workflow generation.

**Acceptance Scenarios**:

1. **Given** user request for complex chatflow not in template DB, **When** AI analyzes request complexity, **Then** system triggers spec-driven workflow instead of immediate build_flow call
2. **Given** spec-driven workflow initiated, **When** AI creates chatflow specification, **Then** spec document includes user intent, node selection rationale, connection logic, and expected behavior
3. **Given** chatflow specification created, **When** AI identifies unclear aspects, **Then** system presents clarifying questions with options based on best practices and context
4. **Given** user provides answers to clarification questions, **When** AI updates specification, **Then** spec incorporates user feedback and resolves ambiguities
5. **Given** updated specification, **When** AI creates implementation plan, **Then** plan breaks down chatflow into phases (node selection → connections → configuration → validation)
6. **Given** implementation plan created, **When** AI generates task breakdown, **Then** tasks include specific node configurations, connection mappings, and validation steps
7. **Given** spec, plan, and tasks completed, **When** AI performs consistency analysis, **Then** system validates alignment between user request, spec, plan, and tasks
8. **Given** consistency validation passed, **When** AI presents chatflow design as text, **Then** design includes node layout, connections, data flow, and configuration summary
9. **Given** chatflow design presented, **When** user reviews and approves, **Then** system proceeds to create chatflow via build_flow or Flowise API
10. **Given** chatflow design presented, **When** user provides feedback/changes, **Then** system loops back to clarification phase (step 3) and regenerates design
11. **Given** chatflow created after approval, **When** creation succeeds, **Then** system returns chatflow_id and summary of implemented design
12. **Given** chatflow creation fails, **When** error occurs, **Then** system reports issue to user and offers to retry with adjusted parameters

**Complexity Detection Criteria**:
- Request requires >5 nodes or >3 node types
- Request mentions "agent", "multi-step", "conditional", "routing", "decision"
- Request describes novel use case not matching any template (semantic search confidence <70%)
- Request includes multiple integrations or external tools
- User explicitly asks for "complex", "advanced", or "custom" workflow

**Human-in-the-Loop Touchpoints**:
1. **Clarification phase**: User answers questions to resolve ambiguities (max 5 questions)
2. **Design approval**: User reviews text-based chatflow design before creation
3. **Feedback loop**: User can request changes, triggering regeneration from clarification phase

**Speckit Workflow Integration**:
- Uses `.specify/commands/speckit.specify` for initial spec generation
- Uses `.specify/commands/speckit.clarify` for clarification questions
- Uses `.specify/commands/speckit.plan` for implementation planning
- Uses `.specify/commands/speckit.tasks` for task breakdown
- Uses `.specify/commands/speckit.analyze` for consistency validation
