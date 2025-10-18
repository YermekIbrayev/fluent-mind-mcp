# User Stories: P2 Learning System (Stories 8-11)

**Priority**: P2 (Future Enhancements - Deferred)
**Status**: [INVESTIGATE] - Advanced learning features for Phase 2+

**Note**: These stories are deferred to Phase 2. The MVP (Phase 1) focuses on P1 stories 1-7 which deliver complete core chatflow automation functionality. P2 stories enhance the system with advanced learning capabilities after core system validation.

---

## User Story 8 - Core SDD Artifact Learning System for Pattern Reuse (Priority: P2) [INVESTIGATE]

AI assistants need to store completed spec-driven development (SDD) artifacts (user requests, specifications, plans, tasks, chatflow designs, user feedback) in vector database, enabling semantic search to recognize similar future requests and propose reusing previously successful implementations without requiring LLM fine-tuning.

**Why this priority**: Many users request similar chatflows (e.g., "customer support bot", "RAG chatbot"). Storing successful SDD artifacts enables token-efficient pattern matching - when new request semantically matches previous request, system can propose reusing proven design instead of running full SDD workflow. Leverages vector similarity search (no LLM retraining needed), dramatically reducing tokens and time for repeated patterns. **This is the MVP for artifact learning** - delivers core value independently.

**Token Efficiency Analysis**:
- **Without learning**: Each similar request runs full SDD workflow (specify → clarify → plan → tasks → analyze) = ~2,000-5,000 tokens
- **With learning**: Semantic search finds match (~30 tokens query) + retrieve cached design (~200-500 tokens) + user approval (~50 tokens) = ~300-600 tokens total
- **Savings**: 85-95% token reduction for recognized patterns
- **Feasibility**: Works with vector DB only - no LLM fine-tuning required. Uses embedding similarity (cosine distance) to match user intent with historical requests.

**Independent Test**: Can be fully tested by completing SDD workflow for chatflow A, storing artifacts in vector DB, submitting similar request B, and verifying system proposes reusing A's design with >70% semantic similarity. Delivers value through intelligent reuse of proven patterns.

**Acceptance Scenarios**:

1. **Given** SDD workflow completes successfully, **When** chatflow created and validated, **Then** system stores artifact bundle (user request, spec, plan, tasks, design, chatflow_id, user feedback) in vector DB with embeddings
2. **Given** stored artifact bundle, **When** indexed in vector DB, **Then** user request text embedded for semantic search with metadata (creation date, success status, user rating, chatflow_id)
3. **Given** new user request received, **When** complexity analysis determines spec-driven workflow needed, **Then** system first searches vector DB for similar historical requests (semantic similarity >70%)
4. **Given** vector search finds matching historical request, **When** similarity score >70%, **Then** system retrieves cached design and presents to user: "Found similar chatflow: [name]. Would you like to reuse this design or create new?"
5. **Given** user approves reusing cached design, **When** confirmation received, **Then** system creates chatflow from cached design using <600 tokens total (vs. 2,000-5,000 for full SDD)
6. **Given** user rejects cached design, **When** rejection received, **Then** system proceeds with full SDD workflow and logs rejection reason for pattern refinement
7. **Given** cached design reused, **When** chatflow created, **Then** system asks user for feedback rating (1-5 stars) and stores rating with artifact for future relevance scoring
8. **Given** artifact with user feedback ratings, **When** calculating vector search relevance, **Then** system boosts results with high ratings (4-5 stars) and demotes low ratings (1-2 stars)
9. **Given** multiple cached designs match user request, **When** similarity scores similar (within 5%), **Then** system prioritizes higher-rated designs and presents top 3 options
10. **Given** artifact learning system operational, **When** vector DB grows to 50+ stored artifacts, **Then** semantic search still completes within 500ms maintaining token efficiency

**Token Efficiency Constraints**:
- User request embedding: <30 tokens
- Cached design retrieval: <500 tokens (condensed format: node list, connections, key configs)
- User approval flow: <100 tokens
- Total for reuse path: <600 tokens (vs. 2,000-5,000 for full SDD)

**Feasibility Without LLM Fine-Tuning**:
- **✅ Works with vector DB only**: Semantic similarity via embeddings (cosine distance)
- **✅ No model retraining required**: Standard sentence transformers handle text embedding
- **✅ Incremental learning**: Each successful SDD adds artifact to searchable corpus
- **✅ User feedback loop**: Ratings improve relevance without model updates
- **⚠️ Cold start problem**: Requires 5-10 initial artifacts to demonstrate value (first few weeks of usage)
- **⚠️ Similarity threshold tuning**: May need adjustment (70% default, could be 60-80% depending on domain)

**Core Learning Scope**:
- **In scope**: Storing specs, plans, tasks, chatflow designs, user requests, feedback ratings
- **In scope**: Semantic search for similar requests using vector embeddings
- **In scope**: User approval/rejection workflow for cached designs
- **In scope**: Compatibility validation (check nodes exist and not deprecated)
- **Out of scope**: Automatic design modification based on differences (user must accept as-is or run full SDD)
- **Out of scope**: Cross-user learning (privacy - only store artifacts for consenting users)
- **Out of scope**: Real-time collaborative filtering (offline batch similarity updates)
- **Out of scope**: Failed SDD storage (see User Story 9)
- **Out of scope**: User-corrected flow import (see User Story 10)
- **Out of scope**: Session versioning (see User Story 11)

---

## User Story 9 - Failed SDD Storage to Avoid Repeating Unsuccessful Patterns (Priority: P3) [INVESTIGATE]

AI assistants need to store failed spec-driven development (SDD) workflows with failure context (reason, error details, failure type) in vector database, enabling semantic search to warn users when similar requests previously failed, preventing wasted effort on patterns likely to fail again.

**Why this priority**: Not all chatflow requests are viable - some fail due to node incompatibilities, connectivity issues, or fundamental design problems. Storing failed SDDs prevents users from repeatedly attempting the same failing patterns. **This builds on User Story 8** by adding negative pattern detection. P3 priority because it's an enhancement - system provides value without it, but reduces user frustration when available.

**Independent Test**: Can be fully tested by creating failed SDD for pattern A, storing failure context in vector DB, submitting similar request B, and verifying system warns user about previous failure with specific reason. Delivers value through intelligent failure avoidance.

**Acceptance Scenarios**:

1. **Given** SDD workflow fails (chatflow creation error, user abandonment, validation failure), **When** failure detected, **Then** system stores failed artifact with failure_reason, error_details, and negative_pattern flag
2. **Given** new user request received, **When** semantic search finds similar failed SDD (>70% similarity), **Then** system warns user: "Similar request failed previously: [reason]. Proceed with caution or modify requirements?"
3. **Given** user proceeds after failure warning, **When** SDD workflow completes successfully, **Then** system updates failed artifact to success status and marks pattern as resolved
4. **Given** multiple failures for similar pattern, **When** failure count >3 for pattern, **Then** system blocks automatic suggestion and requires explicit user override with justification
5. **Given** failed artifact with specific error, **When** system analyzes failure, **Then** failure categorized (node_compatibility, connectivity, configuration, user_abandonment) for targeted warnings

**Failure Types**:
- **node_compatibility**: Selected nodes cannot work together (baseClass mismatches, missing required connections)
- **connectivity**: Connection logic fails (invalid edge configurations, data flow incompatibility)
- **configuration**: Node parameters invalid or incompatible (model not available, missing credentials)
- **user_abandonment**: User terminates workflow before completion (ambiguity unresolved, requirements unclear)

---

## User Story 10 - User-Corrected Flow Import from Flowise for Pattern Library (Priority: P3) [INVESTIGATE]

AI assistants need to import user-corrected chatflows from Flowise (by URL/ID), extract flowData structure, and store as high-priority artifacts, enabling system to learn from manually fixed designs and prioritize proven corrections over system-generated designs.

**Why this priority**: When AI-generated chatflows fail, users often fix them manually in Flowise. Capturing these corrections creates a library of proven designs that represent real-world solutions to edge cases. **This builds on User Stories 8 and 9** by enabling human expertise to directly improve the learning corpus. P3 priority because it's an enhancement - system learns from successful SDDs without it, but incorporating user corrections accelerates learning quality.

**Independent Test**: Can be fully tested by providing Flowise chatflow ID for corrected flow, verifying system fetches via API, extracts structure, prompts user for correction description, stores as artifact with priority boost, and reuses for similar requests. Delivers value through human-in-the-loop learning.

**Acceptance Scenarios**:

1. **Given** user provides Flowise chatflow URL/ID for corrected flow, **When** system receives import request, **Then** system fetches chatflow via Flowise API (`GET /api/v1/chatflows/{id}`)
2. **Given** chatflow fetched from Flowise, **When** system processes flowData, **Then** system extracts node list, connections, configurations, and metadata for artifact storage
3. **Given** extracted chatflow data, **When** user describes what was corrected, **Then** system stores correction as artifact with original_request, corrected_design, correction_description, and high priority flag
4. **Given** corrected flow artifact stored, **When** future similar request occurs (>70% similarity), **Then** system prioritizes corrected flow over original failed attempt (boost similarity by +0.15)
5. **Given** user-corrected flow imported, **When** system validates compatibility, **Then** system checks all nodes exist in current catalog and flags any deprecated nodes for user awareness

**Correction Description Prompt**:
After importing corrected flow, system prompts user: "Please describe what was corrected (1-3 sentences):" to capture human insights for future users (e.g., "Changed from GPT-4 to GPT-3.5 for cost", "Fixed connection between retriever and chat model").

---

## User Story 11 - Session Versioning for Complete Interaction Traceability (Priority: P3) [INVESTIGATE]

AI assistants need to record complete interaction history for each spec-driven development (SDD) workflow execution in session records with unique session_id, capturing all events (clarifications, plan generation, design approval/rejection), enabling debugging, pattern analysis, and identification of success/failure correlations across multiple sessions.

**Why this priority**: SDD workflows involve multiple interactions (clarifications, plan reviews, design approvals). Capturing complete session history enables debugging ("what went wrong in session X?"), pattern analysis ("which clarification answers correlate with success?"), and continuous system improvement. **This builds on User Stories 8-10** by adding comprehensive audit trail for learning system optimization. P3 priority because it's observability enhancement - system functions without it, but session history enables data-driven improvements.

**Independent Test**: Can be fully tested by initiating SDD workflow, capturing all interaction events in session record, storing with unique session_id, querying by session_id or filters, and analyzing patterns across multiple sessions. Delivers value through traceability and insight discovery.

**Acceptance Scenarios**:

1. **Given** SDD workflow initiated, **When** session starts, **Then** system generates unique session_id and creates session record with timestamp, user_id (if available), initial_request
2. **Given** active SDD session, **When** each interaction occurs (clarification Q&A, plan generation, design approval/rejection), **Then** system appends event to session history with event_type, timestamp, content, user_response
3. **Given** session includes clarification questions, **When** user provides answers, **Then** system records question_text, provided_answer, answer_rationale in session history
4. **Given** SDD workflow completes (success or failure), **When** final outcome determined, **Then** system records outcome_status (success, failure, abandoned), final_chatflow_id, user_feedback_rating, lessons_learned
5. **Given** completed session, **When** stored in vector DB, **Then** session accessible by session_id with complete interaction trace for debugging and pattern analysis
6. **Given** multiple sessions for similar requests, **When** analyzing patterns, **Then** system compares interaction paths to identify which clarifications/decisions lead to success vs. failure
7. **Given** session history available, **When** user requests "show me what happened in session X", **Then** system presents chronological interaction log with decisions and outcomes (<1000 tokens)
8. **Given** session versioning active, **When** system detects recurring failure pattern across sessions, **Then** system flags pattern for human review and suggests spec template improvements

**Session Event Types**:
- **clarification_question**: System asks question to resolve ambiguity
- **clarification_answer**: User provides answer with rationale
- **plan_generated**: Implementation plan created
- **design_presented**: Chatflow design shown for approval
- **user_approval**: User approves design
- **user_rejection**: User rejects design with feedback
- **error_occurred**: Workflow error or failure
