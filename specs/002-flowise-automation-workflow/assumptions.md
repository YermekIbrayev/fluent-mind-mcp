## Assumptions

**General System Assumptions**:
- System designed for personal-use MCP server deployment (single-user local operation)
- User controls their own data and is responsible for not including sensitive information (API keys, credentials) in requests
- No multi-tenant features or cross-user data isolation required
- User has direct access to local file system and vector database for debugging/inspection

**MVP Scope & Delivery Assumptions**:
- MVP Phase 1 delivers User Stories 1-7 (P1 priority) providing complete end-to-end chatflow automation capability
- P1 stories (vector search, templates, build_flow, spec-driven workflow, dynamic catalog, circuit breaker, data management) represent fully functional system ready for real-world validation
- P2 stories (8: artifact learning, 9: failed storage, 10: corrected imports, 11: sessions) are valuable enhancements but not essential for core automation functionality
- Core system must be validated with real usage before investing in advanced learning infrastructure (P2 stories)
- Phased delivery follows lean/agile principles: deliver working system first, validate with usage, then enhance based on observed needs
- User can begin productive chatflow automation immediately after MVP Phase 1 completion without waiting for P2 features
- P2 features can be prioritized and developed independently based on actual usage patterns observed during Phase 1

**Testing & Validation Assumptions**:
- Manual testing with documented checklists provides sufficient quality assurance for personal-use MCP server
- Developer/user has time and discipline to execute test checklists systematically for each user story
- Critical path automation (vector search, build_flow, circuit breaker) catches most regressions without full automation
- Human validation is essential for AI interaction scenarios (clarification questions, design approval) that are difficult to automate
- Test checklist documentation creates reusable validation framework for future changes and debugging
- 100% acceptance scenario pass rate is achievable and necessary for user story completion
- Test data generators can produce sufficiently realistic samples to validate system behavior
- Personal-use context allows for iterative testing and bug fixes without formal QA process
- User can identify and document bugs encountered during natural usage after acceptance testing

**Error Handling & Resilience Assumptions**:
- 3 consecutive failures are sufficient indicator of persistent dependency issue requiring circuit opening
- 5-minute circuit open duration provides reasonable balance between avoiding overload and testing recovery
- Transient errors (network, timeout, 5xx) justify circuit breaker activation while validation errors (4xx) do not
- User can recognize circuit breaker status messages and understand when to manually reset vs. wait for auto-recovery
- Circuit breaker state persistence across restarts is important for avoiding immediate retry storms after server restart
- Separate circuits per dependency prevent one failing service from blocking all operations

**Simple Workflow Assumptions**:
- Vector database stored locally in project folder is accessible for read/write operations
- Initial node descriptions will be curated and uploaded to `nodes` collection during system setup
- Flowise examples and documentation provide sufficient common patterns for manual template curation (10-20 templates covering RAG chatbot, simple Q&A, customer support, memory-enabled chat, etc.)
- Manual template curation effort (creating, exporting, annotating 10-20 templates) is acceptable one-time setup cost for high-quality template library
- Vector embeddings adequately capture semantic meaning of node capabilities and use cases
- Semantic search can accurately match user queries to relevant nodes/templates with >90% accuracy
- build_flow function has access to Flowise node type definitions and baseClass information for flowData generation and connection inference
- Flowise baseClass type system is consistent and reliable for automatic connection matching (output baseClass matches input requirements)
- Flowise instance is accessible with credentials configured for chatflow creation
- AI assistants can formulate effective natural language queries (<30 tokens) for vector search
- Template library will start with 10-20 common patterns and grow based on usage
- Token cost is primary optimization metric (prioritized over search accuracy within reason)
- System will leverage existing MCP server capabilities (create_chatflow) for Flowise API communication
- Vector DB updates (new nodes, templates) will be infrequent (weekly/monthly, not per-request)
- Left-to-right flow pattern positioning algorithm produces readable layouts for 90%+ of typical chatflows (linear and tree-shaped flows)

**Dynamic Node Catalog Assumptions**:
- Flowise server exposes `/api/v1/nodes-list` endpoint returning complete node catalog as JSON
- Node metadata from Flowise API includes sufficient detail for semantic search (description, category, baseClasses)
- Flowise server is accessible with authentication during catalog refresh (uses same credentials as chatflow creation)
- Node version numbers follow semantic versioning or comparable numbering scheme enabling comparison
- Deprecated status is clearly indicated in node metadata (boolean flag or status field)
- Node catalog changes occur at reasonable frequency (daily/weekly, not hourly) enabling 24-hour cache staleness threshold with on-demand refresh
- Incremental updates are more efficient than full rebuilds when <30% of nodes changed
- all-MiniLM-L6-v2 embeddings (384 dimensions) adequately capture semantic meaning for node descriptions with no external API dependency
- 24-hour staleness threshold is acceptable for most use cases (not real-time critical)
- Flowise node system is stable enough that breaking interface changes are rare and documented
- Complete Flowise architecture documentation available in `docs/flowise_architecture/` for reference

**User Story 8: Core SDD Artifact Learning System Assumptions** [INVESTIGATE]:
- all-MiniLM-L6-v2 embeddings (384 dimensions) adequately capture semantic meaning of user requests for pattern matching
- Semantic similarity threshold of 70% balances precision (avoiding false positives) and recall (finding relevant matches)
- Users will provide honest feedback ratings (1-5 stars) after reusing cached designs
- Chatflow patterns are reusable across users (e.g., "customer support bot" has consistent requirements)
- Cold start problem (need 5-10 initial artifacts) is acceptable - system demonstrates value after 2-3 weeks
- Artifact bundle storage (2-5KB per artifact) is acceptable for local vector DB (50 artifacts = 100-250KB)
- Node compatibility validation can detect deprecation and breaking changes from node catalog comparison
- Users will manually clean up low-rated artifacts (1-2 stars) or old data when desired using cleanup commands
- Semantic drift (terminology changes) is gradual enough to allow manual threshold adjustments
- Privacy concerns addressed by single-user artifact storage (no cross-user learning by default)
- Token savings (85-95% for reuse path) justify development effort and storage overhead
- No LLM fine-tuning required - vector similarity search sufficient for pattern matching

**User Story 9: Failed SDD Storage Assumptions** [INVESTIGATE]:
- Failed SDDs provide valuable learning signal (not just noise to be discarded)
- Failure patterns are reproducible (similar requests will fail for similar reasons)
- Failure categorization (4 types) covers 90%+ of failure scenarios
- 3-failure threshold before blocking is reasonable trade-off (allow retries without excessive waste)
- Users will provide meaningful failure descriptions when abandoning workflows
- Failed patterns can be resolved through node catalog updates or requirement modifications
- False negatives (temporary failures) are rare enough (<10%) not to undermine system value

**User Story 10: User-Corrected Flow Import Assumptions** [INVESTIGATE]:
- Users who manually fix flows in Flowise are willing to share corrections back to learning system
- User-provided correction descriptions are sufficiently detailed for future users (1-3 sentences acceptable)
- Manually corrected flows are generally superior to AI-generated designs (justify +0.15 priority boost)
- Flowise API provides complete flowData in `GET /api/v1/chatflows/{id}` response for extraction
- Corrected flows remain valid/compatible long enough to be useful (not immediately deprecated)
- Users can provide Flowise chatflow URL or ID accurately (no frequent typos/errors)
- Batch import of 5-10 flows at once is sufficient for pattern library bootstrapping

**User Story 11: Session Versioning Assumptions** [INVESTIGATE]:
- Complete interaction history provides debugging and learning value justifying storage overhead
- Session storage (5-10KB per session) is acceptable for 1000+ sessions (~5-10MB total)
- Users understand session_id concept and can reference sessions for debugging/review
- Personal-use context: User is responsible for not including sensitive data (API keys, credentials) in requests - no automated detection/masking needed
- Pattern analysis across 20+ sessions provides statistically significant correlations
- Recurring failure patterns flagged for human review will actually receive human attention
- Session export in JSON format meets external analysis needs (no custom formats required)
- Interrupted sessions are recoverable despite network loss or app crashes (persistent storage)

**Spec-Driven Workflow Assumptions**:
- AI can accurately assess request complexity to determine workflow routing within 1 second
- Users will engage with clarification questions and provide meaningful answers (not "I don't know" repeatedly)
- Users can understand and evaluate text-based chatflow designs without visual diagrams
- Speckit workflow commands (`.specify/commands/*`) are available and functional in AI environment
- Users will approve or reject designs with actionable feedback enabling workflow progression
- Max 5 clarification questions are sufficient to resolve ambiguities in 80%+ of complex requests
- Max 5 feedback iterations are sufficient to achieve user approval or indicate fundamental misalignment
- Intermediate artifacts (spec, plan, tasks) storage in project folder is reliable and accessible
- Consistency analysis can detect critical misalignments with reasonable accuracy (95%+)
- Users prefer high-confidence complex chatflows over fast but potentially incorrect simple workflows
- Spec-driven approach reduces overall token cost vs. trial-and-error for complex chatflows (>5 nodes)
- Generated chatflow specifications can be reused as templates for future similar requests

## Dependencies
