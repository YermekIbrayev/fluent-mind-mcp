# Functional Requirements: P2 Learning System

**Priority**: P2 (Deferred to Phase 2)

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
- **FR-055**: System MUST support artifact invalidation when referenced chatflow is deleted by user

**User Story 9: Failed SDD Storage (FR-071 to FR-080)** [INVESTIGATE]:
- **FR-071**: System MUST store failed SDD artifacts in ChromaDB `failed_artifacts` collection when workflow fails with failure_reason, error_details, failure_type (node_compatibility, connectivity, configuration, user_abandonment)
- **FR-072**: System MUST search for similar failed SDDs alongside successful artifacts and present failure warnings to user
- **FR-073**: System MUST display failure warning with specific reason when similar failed pattern found (>70% similarity)
- **FR-074**: System MUST allow user to proceed despite failure warning or modify requirements before retrying
- **FR-075**: System MUST update failed artifact to success status when previously failed pattern completes successfully
- **FR-076**: System MUST track failure count per pattern and block automatic suggestion when count exceeds threshold (3 failures)
- **FR-077**: System MUST require explicit user override with justification when blocked pattern selected
- **FR-078**: System MUST categorize failures into types (node_compatibility, connectivity, configuration, user_abandonment) for targeted warnings
- **FR-079**: System MUST demote failed artifacts in search results (reduce similarity score by -0.10) compared to successful artifacts
- **FR-080**: System MUST provide manual command to review failed artifacts and remove those whose patterns now succeed after node catalog updates

**User Story 10: User-Corrected Flow Import (FR-081 to FR-090)** [INVESTIGATE]:
- **FR-081**: System MUST provide user interface/command for importing corrected flows by Flowise URL or chatflow ID
- **FR-082**: System MUST fetch corrected chatflow from Flowise API using `GET /api/v1/chatflows/{id}` endpoint
- **FR-083**: System MUST extract flowData (nodes, edges, configurations) from Flowise API response
- **FR-084**: System MUST prompt user to describe what was corrected (free text explanation)
- **FR-085**: System MUST store corrected flow as artifact with original_request, corrected_design, correction_description, is_user_corrected flag
- **FR-086**: System MUST prioritize user-corrected flows over system-generated designs (boost similarity by +0.15)
- **FR-087**: System MUST validate corrected flow compatibility with current node catalog before storage
- **FR-088**: System MUST associate corrected flow with original failed artifact (if exists) for causality tracking
- **FR-089**: System MUST support batch import of multiple corrected flows for pattern library building
- **FR-090**: System MUST handle Flowise API errors gracefully (invalid ID, access denied, rate limit) with user-friendly messages

**User Story 11: Session Versioning (FR-091 to FR-105)** [INVESTIGATE]:
- **FR-091**: System MUST generate unique session_id (UUID format) when SDD workflow initiated
- **FR-092**: System MUST create session record in ChromaDB `sessions` collection with session_id, timestamp, user_id (if available), initial_user_request
- **FR-093**: System MUST append event to session history for each interaction (clarification Q&A, plan generation, design approval/rejection)
- **FR-094**: System MUST record event with event_type, timestamp, content, user_response for full traceability
- **FR-095**: System MUST store clarification questions with question_text, provided_answer, answer_rationale in session
- **FR-096**: System MUST record final outcome with outcome_status (success, failure, abandoned), final_chatflow_id, user_feedback_rating, lessons_learned
- **FR-097**: System MUST make session accessible by session_id with complete chronological interaction trace
- **FR-098**: System MUST support session query by various filters (date range, outcome status, user_id, similar requests)
- **FR-099**: System MUST present session history in condensed format (<1000 tokens) when user requests "show session X"
- **FR-100**: System MUST analyze patterns across multiple sessions to identify success/failure correlations
- **FR-101**: System MUST flag recurring failure patterns (same pattern fails in >3 sessions) for human review
- **FR-102**: System MUST suggest spec template improvements based on session analysis (e.g., missing clarification questions)
- **FR-103**: System MUST handle interrupted sessions gracefully (save partial history, mark as incomplete)
- **FR-104**: System stores session data as-is without sensitive data detection/masking (personal-use context - user responsible for not including secrets)
- **FR-105**: System MUST support session export in JSON format for external analysis or backup

**Spec-Driven Workflow (FR-056 to FR-070)**:
- **FR-056**: System MUST analyze user request complexity using criteria (node count, keywords, template match confidence) to determine workflow path
- **FR-057**: System MUST trigger spec-driven workflow when request exceeds complexity threshold (>5 nodes OR template confidence <70% OR complexity keywords detected)
- **FR-058**: System MUST generate chatflow specification document including user intent, node selection rationale, connection logic, and expected behavior
- **FR-059**: System MUST identify unclear aspects in chatflow request and generate clarifying questions (max 5) with multiple-choice options
- **FR-060**: System MUST provide context-aware answer options for clarification questions based on best practices and similar flow patterns
- **FR-061**: System MUST update chatflow specification with user's clarification answers, resolving all ambiguities before proceeding
- **FR-062**: System MUST generate implementation plan breaking down chatflow into phases (node selection → connections → configuration → validation)
- **FR-063**: System MUST create task breakdown with specific node configurations, connection mappings, parameter settings, and validation steps
- **FR-064**: System MUST perform consistency analysis validating alignment between user request, spec, plan, and tasks before implementation
- **FR-065**: System MUST generate text-based chatflow design summary including node layout, connections, data flow, and configuration for user review
- **FR-066**: System MUST present chatflow design to user and wait for approval or feedback before creating chatflow
- **FR-067**: System MUST support feedback loop allowing user to request changes, triggering regeneration from clarification phase
- **FR-068**: System MUST limit feedback iterations to prevent infinite loops (max 5 iterations, then request user to rephrase original request)
- **FR-069**: System MUST create chatflow via Flowise API only after user explicitly approves design
- **FR-070**: System MUST report chatflow creation results to user with chatflow_id, summary of implemented design, and validation status

