# Key Entities: P2 Learning System

**Priority**: P2 (Deferred to Phase 2)

**User Story 8: Core SDD Artifact Learning System Entities** [INVESTIGATE]:

- **ArtifactBundle**: Complete package of SDD workflow outputs stored in vector DB for reuse. Contains user request text (original prompt), specification document, implementation plan, task breakdown, chatflow design, chatflow_id (Flowise reference), node versions used, creation timestamp, success status. Indexed with vector embeddings of user request enabling semantic search. Average size ~2-5KB per bundle, stored as JSON with metadata.

- **ArtifactEmbedding**: Vector representation of user request text enabling semantic similarity search. Generated using sentence transformers (384-768 dimensions), stored alongside artifact bundle. Supports cosine similarity calculations for matching new requests to historical patterns. Embeddings generated once during artifact storage, reused for all future searches.

- **SimilarityScore**: Numeric measure (0.0-1.0) of semantic similarity between new user request and historical artifact. Calculated via cosine distance between embeddings. Threshold of 0.70 (70%) used to determine match relevance. Adjusted by user feedback ratings - high-rated artifacts boosted by +0.05, low-rated demoted by -0.05. Multiple matches ranked by adjusted score.

- **CachedDesign**: Condensed representation of historical chatflow design retrieved for reuse. Extracted from artifact bundle, formatted for token efficiency (<500 tokens). Includes node list with types and versions, connection mappings (source→target with data flow), key configuration parameters (model names, prompts, temperatures), validation approach. Presented to user for approval before chatflow creation.

- **UserFeedbackRating**: 1-5 star rating collected after cached design reuse. Stored with artifact_id, timestamp, optional text comment. Used to adjust artifact relevance in future searches (4-5 stars boost by +0.05, 1-2 stars demote by -0.05). Enables continuous quality improvement without LLM retraining. Aggregated ratings visible in artifact metadata.

- **ReusePath**: Fast workflow for creating chatflows from cached designs bypassing full SDD. Steps: 1) Embed new user request (~30 tokens), 2) Search vector DB for matches >70% similarity (~500ms), 3) Retrieve and present cached design (~500 tokens), 4) User approval (~50 tokens), 5) Create chatflow from cached design (~20 tokens). Total ~600 tokens vs. 2,000-5,000 for full SDD (85-95% savings).

- **ArtifactMetadata**: Descriptive data stored with each artifact bundle. Includes creation_date (timestamp), success_status (boolean - chatflow created successfully), user_rating (1-5 stars, null if not rated), chatflow_id (Flowise reference), node_versions (array of node names+versions used), reuse_count (how many times design reused), last_reuse_date (most recent reuse timestamp). Enables filtering, sorting, and analytics.

- **CompatibilityValidator**: Component checking cached design compatibility with current node catalog before presenting to user. Validates: 1) All referenced nodes exist in current catalog, 2) Node versions are not deprecated, 3) Breaking changes haven't invalidated connections. Returns compatibility_status (compatible, deprecated_nodes, incompatible) with specific issues. Prevents presenting outdated designs that would fail.

- **ArtifactCorpus**: Complete collection of stored artifact bundles in vector DB. Grows incrementally as users complete SDD workflows. Expected growth: 5-10 artifacts per week (active usage), 100+ artifacts after 3-6 months. Search performance target <500ms maintained through vector indexing (HNSW or similar). User can manually clean up low-rated (1-2 stars) or old artifacts via cleanup commands when desired.

**User Story 9: Failed SDD Storage Entities** [INVESTIGATE]:

- **FailedArtifact**: Artifact bundle for unsuccessful SDD workflow stored to prevent repeating failures. Contains user_request, spec (if generated), failure_reason (descriptive text), error_details (technical error), failure_type (node_compatibility, connectivity, configuration, user_abandonment), failure_timestamp, failure_count (for pattern tracking). Embedded similarly to successful artifacts but demoted in search results (similarity score -0.10). Linked to successful retry if pattern resolves.

- **FailureWarning**: Message presented to user when similar failed pattern detected (>70% similarity). Includes failure_type, failure_reason (user-friendly description), failure_count (how many times pattern failed), recommended_action (proceed with caution, modify requirements, or blocked if count >3). Formatted for token efficiency (<100 tokens). User can proceed despite warning or modify request.

- **FailurePattern**: Clustered grouping of similar failed artifacts sharing common characteristics (similar user requests, same failure_type, overlapping node selections). Tracked with pattern_id, failure_count (total failures in pattern), first_failure_date, last_failure_date, is_blocked (true if count >3). Used to identify systemic issues requiring human review or spec template improvements.

**User Story 10: User-Corrected Flow Import Entities** [INVESTIGATE]:

- **CorrectedFlowImport**: User-provided Flowise chatflow (by URL/ID) representing manually fixed version of failed SDD attempt. Fetched via Flowise API (`GET /api/v1/chatflows/{id}`), extracts flowData (nodes, edges, configurations). Stored with chatflow_id (Flowise reference), corrected_design (extracted structure), correction_description (user explanation of fixes), original_failed_artifact_id (causality link if exists), is_user_corrected (true), import_timestamp. Prioritized in searches (+0.15 similarity boost).

- **FlowDataExtraction**: Process of parsing Flowise API response to extract reusable chatflow structure. Extracts node_list (types, names, versions), connection_mappings (source→target edges with data flow), node_configurations (model parameters, prompts, tools), metadata (chatflow name, description, category). Validates completeness (all nodes/edges present) and compatibility (nodes exist in current catalog). Formatted for artifact storage (~2-3KB per flow).

- **CorrectionDescription**: User-provided explanation of what was corrected in manually fixed flow. Free text input prompted after chatflow import. Guides future users on what changes were needed (e.g., "Changed from GPT-4 to GPT-3.5 for cost", "Fixed connection between retriever and chat model"). Stored with artifact, displayed when corrected flow suggested. Target length: 1-3 sentences (50-200 chars).

**User Story 11: Session Versioning Entities** [INVESTIGATE]:

- **SessionRecord**: Complete interaction history for single SDD workflow execution. Contains session_id (UUID), timestamp (session start), user_id (optional), initial_user_request, event_history (array of SessionEvents), outcome_status (success, failure, abandoned), final_chatflow_id (if success), user_feedback_rating (1-5 stars if provided), lessons_learned (analysis insights). Persisted in vector DB, queryable by session_id or filters (date range, outcome, user). Average size ~5-10KB per session.

- **SessionEvent**: Individual interaction within SDD session. Contains event_type (clarification_question, clarification_answer, plan_generated, design_presented, user_approval, user_rejection, error_occurred), timestamp, content (event-specific data: question text, answer, plan summary, error message), user_response (for interactive events). Chronologically ordered in session history. Enables detailed traceability and pattern analysis.

- **SessionAnalysis**: Comparative analysis across multiple sessions to identify success/failure correlations. Analyzes which clarification questions, answer patterns, node selections correlate with successful vs. failed outcomes. Outputs correlation_insights (e.g., "Sessions where user answered Q3 with option A had 80% success rate"), recurring_failure_patterns (patterns failing in >3 sessions), suggested_improvements (spec template enhancements, additional clarification questions). Runs periodically (weekly) or on-demand for corpus of 20+ sessions.

- **SessionQuery**: Filtering and retrieval mechanism for session records. Supports filters: date_range (start/end timestamps), outcome_status (success, failure, abandoned), user_id, similar_request (semantic similarity to user request text). Returns matching session_ids with summary metadata (timestamp, initial_request, outcome). Used for debugging, pattern analysis, and user "show me session X" requests.

