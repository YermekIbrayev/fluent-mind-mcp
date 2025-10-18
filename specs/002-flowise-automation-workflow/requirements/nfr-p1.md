### Non-Functional Requirements

**Token Efficiency**:
- **NFR-001**: Vector search queries MUST use <30 tokens for natural language input
- **NFR-002**: Vector search results MUST return node/template summaries using <50 tokens per result
- **NFR-003**: build_flow template invocation MUST use <20 tokens (template_id only)
- **NFR-004**: build_flow custom node invocation MUST use <50 tokens (node list + connections="auto")
- **NFR-005**: build_flow responses MUST contain only chatflow_id and name using <30 tokens
- **NFR-006**: Error messages MUST be compact (<50 tokens) while remaining actionable
- **NFR-007**: Complete simple workflow (search → build → result) MUST average <150 tokens total
- **NFR-008**: Clarification questions MUST be concise (<200 tokens per question including options)
- **NFR-009**: Chatflow design summary MUST be comprehensive yet readable (<500 tokens total)

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
- **NFR-061**: Session history presentation MUST use <1000 tokens for complete interaction trace (condensed format)

**Security (Personal Use Context)**:
- **NFR-080**: System assumes single-user personal deployment where user controls their own data and is responsible for not including secrets in requests (no automated sensitive data detection/masking required)

**Performance & Scalability**:
- **NFR-010**: Vector search MUST complete within 500ms for typical queries
- **NFR-011**: build_flow execution MUST complete within 10 seconds for template-based creation
- **NFR-012**: build_flow execution MUST complete within 15 seconds for custom node combinations
- **NFR-013**: Vector DB MUST support 10-20 concurrent queries without performance degradation
- **NFR-014**: System MUST handle vector DB with 100-200 node descriptions and 20-50 flow templates
- **NFR-015**: Node catalog refresh from Flowise API MUST complete within 30 seconds for 100-200 nodes (user waits during on-demand refresh before build_flow proceeds)
- **NFR-016**: Node catalog comparison and vector DB update MUST complete within 10 seconds for typical change set (10-20 nodes)
- **NFR-017**: System MUST support incremental vector DB updates without full rebuild when <30% of nodes changed
- **NFR-018**: Complexity analysis MUST complete within 1 second for request routing decision
- **NFR-019**: Spec generation MUST complete within 5 seconds for typical complex request
- **NFR-020**: Plan generation MUST complete within 10 seconds for typical chatflow
- **NFR-021**: Complete spec-driven workflow (without user wait time) MUST complete within 2 minutes

**User Story 8: Core SDD Artifact Learning System** [INVESTIGATE]:
- **NFR-046**: SDD artifact search MUST complete within 500ms for vector DB with 50+ artifacts
- **NFR-047**: Cached design validation (node compatibility check) MUST complete within 2 seconds
- **NFR-048**: Artifact bundle storage (embedding generation + DB insertion) MUST complete within 5 seconds
- **NFR-049**: System MUST support artifact corpus growth to 100+ entries without search degradation (>10% latency increase)

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

