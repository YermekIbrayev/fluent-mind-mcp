# Non-Functional Requirements: P2 Learning System

**Priority**: P2 (Deferred to Phase 2)

**User Story 8: Core SDD Artifact Learning System** [INVESTIGATE]:
- **NFR-042**: SDD artifact search query MUST use <30 tokens for user request embedding
- **NFR-043**: Cached design retrieval MUST present condensed format using <500 tokens (node list, connections, configs)
- **NFR-044**: User approval/rejection workflow for cached designs MUST use <100 tokens total
- **NFR-045**: Complete reuse workflow (search → retrieve → approve → create) MUST average <600 tokens (vs. 2,000-5,000 for full SDD)

**User Story 9: Failed SDD Storage** [INVESTIGATE]:
- **NFR-060**: Failure warning presentation MUST use <100 tokens (failure type, reason, proceed/modify options)

**User Story 10: User-Corrected Flow Import** [INVESTIGATE]:
- **NFR-062**: Corrected flow import user prompt (describe correction) MUST use <200 tokens total

**User Story 11: Session Versioning** [INVESTIGATE]:
**User Story 9: Failed SDD Storage** [INVESTIGATE]:
- **NFR-063**: Failed artifact search and warning presentation MUST complete within 1 second

**User Story 10: User-Corrected Flow Import** [INVESTIGATE]:
- **NFR-064**: Corrected flow fetch from Flowise API MUST complete within 10 seconds (network dependent)

**User Story 11: Session Versioning** [INVESTIGATE]:
- **NFR-065**: Session history retrieval by session_id MUST complete within 500ms
- **NFR-066**: Session pattern analysis across 50+ sessions MUST complete within 30 seconds
- **NFR-067**: System MUST support 1000+ sessions without storage/search performance degradation

**Reliability**:
- **NFR-022**: Vector DB MUST persist locally in project folder surviving process restarts
- **NFR-023**: build_flow MUST validate parameters before flowData generation
- **NFR-024**: Vector search MUST gracefully handle DB unavailability with clear error message
- **NFR-025**: System MUST provide actionable error messages for 100% of failures
- **NFR-026**: Circuit breaker MUST open within 5 seconds of detecting 3rd consecutive failure to prevent prolonged retry attempts
- **NFR-027**: System MUST cache node catalog for offline operation when Flowise server unreachable (circuit open)
- **NFR-028**: Node catalog cache MUST include staleness metadata (last refresh timestamp, version)
- **NFR-029**: System MUST validate node metadata completeness (name, version, category) before vector DB insertion
- **NFR-030**: Spec-driven workflow MUST handle user abandonment gracefully (save intermediate artifacts)
- **NFR-031**: Feedback loop MUST enforce max iteration limit (5 attempts) to prevent infinite loops
- **NFR-032**: Consistency analysis MUST detect and report spec-plan-task misalignments with specific issues
- **NFR-081**: Circuit breaker state transitions MUST complete within 100ms to avoid blocking user operations
- **NFR-082**: System MUST provide circuit status check command completing within 50ms for all dependencies
- **NFR-083**: Circuit breaker failure count MUST persist across server restarts to maintain failure history

**User Story 8: Core SDD Artifact Learning System** [INVESTIGATE]:
- **NFR-050**: Artifact bundles MUST persist in vector DB surviving process restarts
- **NFR-051**: System MUST validate artifact bundle completeness (all required fields present) before storage
- **NFR-052**: Cached design reuse MUST validate node compatibility with current catalog before chatflow creation
- **NFR-053**: System MUST handle corrupted artifact bundles gracefully (log error, exclude from search, continue operation)
- **NFR-054**: Artifact invalidation MUST remove all associated data (embeddings, metadata) when chatflow deleted

**User Story 9: Failed SDD Storage** [INVESTIGATE]:
- **NFR-068**: Failed artifact storage MUST include all failure context (reason, error details, failure type) for accurate warnings

**User Story 10: User-Corrected Flow Import** [INVESTIGATE]:
- **NFR-069**: System MUST handle Flowise API failures during corrected flow import gracefully (retry 3x, timeout 10s per attempt)
- **NFR-072**: System MUST validate corrected flow completeness (all nodes/edges present) before accepting import

**User Story 11: Session Versioning** [INVESTIGATE]:
- **NFR-070**: Session storage MUST handle interrupted sessions (save partial history, mark incomplete, allow resumption)

