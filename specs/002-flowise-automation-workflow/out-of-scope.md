## Out of Scope

**MVP Phase 1 (Deferred to Future Phases)**:

The Minimum Viable Product (MVP) scope includes only P1 priority user stories (Stories 1-7). The following P2 priority stories are explicitly deferred to future phases:

- **User Story 8: Core SDD Artifact Learning System** [INVESTIGATE] - Deferred to Phase 2. While valuable for learning from past designs, not essential for core chatflow automation functionality. Core system must be validated with real usage before investing in learning infrastructure.

- **User Story 9: Failed SDD Storage** [INVESTIGATE] - Deferred to Phase 2. Failure pattern detection is an enhancement; basic error handling in P1 stories sufficient for MVP.

- **User Story 10: User-Corrected Flow Import** [INVESTIGATE] - Deferred to Phase 2. Manual flow import adds convenience but not core automation capability.

- **User Story 11: Session Versioning** [INVESTIGATE] - Deferred to Phase 3. Session analytics and history tracking are useful for long-term optimization but not critical for initial delivery.

**Rationale**: P1 stories (1-7) deliver complete end-to-end chatflow automation: vector search, template-based flows, build_flow with node lists, spec-driven workflow for complex requests, dynamic node catalog refresh, circuit breaker resilience, and data management. This represents fully functional system ready for real-world validation. P2 stories enhance learning and analytics capabilities but are not blockers for core use cases. Following lean/agile principles: deliver working system first, validate with usage, then enhance based on observed needs.

**Simple Workflow Out of Scope**:
- AI-generated flowData structures in conversation context (handled by build_flow internally)
- Dynamic node discovery at runtime (nodes pre-populated in vector DB)
- Real-time vector DB updates (manual/scheduled refresh only)
- Visual workflow editor UI (automation via build_flow function)
- Custom workflow generation beyond templates and node lists (use templates + parameters)
- Workflow optimization and performance tuning post-creation
- Custom node type creation or modification
- Vector DB hosting/sync across multiple instances (local only)
- Automated vector embedding quality assessment

**Dynamic Node Catalog Out of Scope**:
- Automatic node compatibility checking across versions (manual template validation required)
- Predictive analysis of which nodes will be deprecated (reactive approach only)
- Automatic migration of flow templates when nodes deprecated (manual template updates required)
- Real-time node catalog updates (scheduled refresh or on-demand only, not streaming)
- Custom node type creation or modification through automation system
- Integration with Flowise development/staging environments (production only)
- Automatic detection and alerting for Flowise API breaking changes (manual monitoring)
- Historical tracking of all node version changes (only current and immediately previous version)
- Custom node description enrichment beyond what Flowise provides (use official descriptions)
- Multi-tenant node catalog management (single Flowise instance only)

**User Story 8: Core SDD Artifact Learning System Out of Scope** [INVESTIGATE]:
- Automatic design modification based on partial matches (user must accept as-is or run full SDD)
- Cross-user artifact sharing and learning (privacy - single-user storage only by default)
- Real-time collaborative filtering or recommendation systems (offline batch processing only)
- Machine learning-based similarity scoring (cosine distance from embeddings only, no ML training)
- Automatic semantic drift detection and threshold adjustment (manual tuning required)
- Predictive analytics on which artifacts will be popular (reactive rating system only)
- Natural language explanation of why cached design matches user request (similarity score only)
- Automatic artifact versioning and historical tracking (current version only)
- Integration with external knowledge bases or documentation (Flowise-specific only)
- Multi-modal artifact storage (images, videos - text and JSON only)
- Real-time artifact synchronization across multiple instances (single local DB only)
- Automatic chatflow testing to validate cached design before reuse (compatibility check only)
- Cost-benefit analysis comparing reuse savings to SDD cost (token counting only)
- A/B testing different similarity thresholds or relevance scoring methods (fixed 70% threshold)

**User Story 9: Failed SDD Storage Out of Scope** [INVESTIGATE]:
- Automatic failure resolution or self-healing (failures must be addressed by user or node updates)
- Predictive failure analysis (e.g., "this request is likely to fail") before attempting SDD
- Machine learning for failure categorization (rule-based classification only)
- Automated ticket creation or escalation for recurring failures (manual human review only)
- Cross-session failure correlation beyond simple pattern matching (no deep causal analysis)

**User Story 10: User-Corrected Flow Import Out of Scope** [INVESTIGATE]:
- Automatic diff/comparison between failed design and corrected flow (user describes correction manually)
- Integration with Flowise version control or history for tracking flow evolution
- Automatic correction propagation to similar failed artifacts (one-to-one association only)
- Visual flow diagram rendering for corrected flows (text-based structure representation only)
- Automated validation that correction actually fixes the issue (user confirmation assumed)
- Support for importing flows from external systems besides Flowise (Flowise API only)

**User Story 11: Session Versioning Out of Scope** [INVESTIGATE]:
- Real-time session collaboration or shared viewing (single-user session access only)
- Advanced statistical analysis or machine learning for correlation detection (basic pattern matching only)
- Automatic rollback or replay of sessions for debugging (read-only history access)
- Integration with external analytics platforms (JSON export only for manual import)
- Session compression or archiving for long-term storage optimization (full sessions stored)
- Multi-user session aggregation or anonymized cross-user analysis (single-user privacy only)
- Automated A/B testing of different spec templates based on session outcomes (manual template updates)

**Spec-Driven Workflow Out of Scope**:
- Visual diagram generation for chatflow designs (text-based representations only)
- Real-time collaboration between multiple users on same chatflow specification
- Automated testing and validation of generated chatflows (manual user validation required)
- Machine learning for complexity detection (rule-based heuristics only)
- Workflow versioning and rollback for chatflow specifications
- Integration with external specification tools or formats
- Automated clarification question generation beyond template-based patterns
- Natural language understanding of user feedback (structured feedback expected)
- Chatflow performance optimization suggestions during spec phase
- Cost estimation for chatflow execution (Flowise token usage, API costs)
- Security and compliance validation for chatflow specifications
- Automated template extraction from successful spec-driven chatflows (manual curation)
- Multi-language support for specifications and clarification questions (English only)
- AgentFlow V2 generation via spec-driven workflow (focus on traditional ChatFlow)
- Advanced workflow patterns beyond linear node chains (conditional routing, loops, complex multi-agent requires manual implementation)
