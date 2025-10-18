# Edge Cases

**Status**: Comprehensive edge case documentation for all user stories and system components

---

## System Initialization

- What happens when ChromaDB or sentence-transformers installation fails on first run?
- How does system handle network failures during embedding model download?
- What happens when system starts without vector database dependencies installed?
- How does system recover from partial installation (ChromaDB installed but embedding model missing)?

## Data Management & Cleanup

- What happens when user attempts to delete artifacts that are currently referenced by active workflows?
- How does system handle cleanup commands with invalid date filters (e.g., "older than -5 days")?
- What happens when user deletes all artifacts in sdd_artifacts collection (empty corpus)?
- How does system handle concurrent cleanup operations on same collection?
- What happens when inspection commands are run on very large collections (10,000+ entries)?
- How does system validate user confirmation before executing destructive cleanup operations?

## Circuit Breaker & Error Handling

- What happens when circuit opens during critical operation (e.g., mid-chatflow creation)?
- How does system handle user manually resetting circuit while dependency still failing?
- What happens when test request in half-open state times out (neither success nor failure)?
- How does system handle multiple concurrent requests when circuit transitions from half-open to open?
- What happens when different dependencies fail simultaneously (Flowise API + vector DB)?
- How does system distinguish between temporary network glitches (should retry) vs. persistent failures (open circuit)?
- What happens when circuit is open and user explicitly requests operation requiring that dependency?
- How does system handle circuit state persistence across server restarts?

## Testing & Validation

- What happens when automated critical path tests fail during acceptance testing?
- How does system handle test checklist versioning when requirements change mid-development?
- What happens when manual tester marks scenario as "pass" but actual results don't match expected results?
- How does system validate test data generators produce realistic, representative samples?
- What happens when test utilities fail to reset ChromaDB collections (data persists between tests)?
- How does system handle incomplete test checklist execution (some scenarios not tested)?
- What happens when user story has passing tests but user encounters bugs during actual usage?
- How does system ensure test checklists cover all edge cases documented in Edge Cases section?

## Vector Search & Templates

- What happens when vector search returns no results for user query?
- How does system handle ambiguous queries matching multiple unrelated node types?
- What happens when build_flow receives conflicting parameters (e.g., incompatible nodes)?
- How does system handle vector database unavailability during query?
- What happens when template_id references deleted or outdated template?
- How does system handle concurrent build_flow calls creating similar chatflows?
- What happens when Flowise adds new nodes not yet in vector database?
- How does system handle corrupted or malformed template data in vector DB?
- What happens when vector embeddings drift from actual node capabilities?

## Dynamic Node Catalog

- What happens when Flowise server is unreachable during node catalog refresh?
- How does system handle partial node list responses (e.g., network timeout mid-response)?
- What happens when node version changes but description remains unchanged?
- How does system handle nodes with same name but different versions or baseClasses?
- What happens when deprecated node is referenced in existing flow template?
- How does system detect and handle breaking changes in node interfaces (inputs/outputs)?
- What happens when node catalog refresh takes >30 seconds?
- How does system handle Flowise API rate limiting during frequent refreshes?
- What happens when node metadata is incomplete (missing version, description, etc.)?
- How does system prioritize node versions when multiple non-deprecated versions exist?

## Spec-Driven Workflow

- What happens when AI cannot determine if request is complex enough for spec-driven workflow?
- How does system handle user abandoning workflow mid-process (e.g., after spec creation but before approval)?
- What happens when user provides contradictory answers during clarification phase?
- How does system handle spec-plan-task inconsistencies detected during analysis?
- What happens when user rejects design multiple times without clear feedback?
- How does system handle chatflow creation failure after user approval?
- What happens when spec-driven workflow is triggered for simple request that could use template?
- How does system handle infinite feedback loops (user never approves design)?
- What happens when clarification questions cannot resolve fundamental ambiguities?
- How does system handle conflicts between user's stated intent and their clarification answers?

## User Story 8: Core SDD Artifact Learning System [INVESTIGATE]

- What happens when semantic search finds multiple cached designs with similar scores (>70% each)?
- How does system handle cached design that references deprecated nodes discovered during reuse attempt?
- What happens when user request partially matches cached design (70% similar but missing key component)?
- How does system handle user rating manipulation (e.g., all 5-star or all 1-star ratings)?
- What happens when artifact bundle is corrupted or incomplete in vector DB?
- How does system handle semantic drift over time (terminology changes, new patterns emerge)?
- What happens when cached design fails to create chatflow during reuse (Flowise API changes)?
- How does system handle cold start problem (no artifacts in vector DB yet)?
- What happens when similarity threshold is too high (no matches) or too low (false positives)?
- How does system handle privacy when multiple users want similar chatflows (cross-user learning)?
- What happens when user deletes chatflow created from cached design (invalidate artifact)?
- How does system handle vector DB growth to 1000+ artifacts (search performance degradation)?

## User Story 9: Failed SDD Storage [INVESTIGATE]

- What happens when both failed and successful artifacts match user request (which takes priority)?
- How does system handle false negatives (failure was due to temporary issue, not pattern problem)?
- What happens when failure count threshold (3 failures) is reached but user insists on pattern?
- How does system categorize ambiguous failures (multiple possible causes)?
- What happens when failed artifact is successfully recreated after node catalog update?
- How does system handle cascading failures (failure causes more failures in similar patterns)?
- What happens when user provides insufficient failure description (generic "it didn't work")?

## User Story 10: User-Corrected Flow Import [INVESTIGATE]

- What happens when provided Flowise URL/ID is invalid or inaccessible?
- How does system handle corrected flow with deprecated nodes at time of import?
- What happens when user describes correction poorly ("I fixed it" without specifics)?
- How does system handle circular corrections (flow A corrects flow B, flow B corrects flow A)?
- What happens when corrected flow is significantly different from original request (>50% changes)?
- How does system prioritize multiple corrections for same failure pattern?
- What happens when Flowise API rate limits prevent fetching corrected flow?
- How does system handle partial flowData (some nodes/connections missing in Flowise response)?

## User Story 11: Session Versioning [INVESTIGATE]

- What happens when session is interrupted mid-interaction (network loss, app crash)?
- How does system handle session storage growth to 1000+ sessions (storage/search performance)?
- What happens when user requests session history for non-existent session_id?
- How does system handle sensitive data in session history (API keys, credentials accidentally shared)?
- What happens when session spans multiple days/weeks with long user delays?
- How does system detect duplicate sessions (user restarts for same request)?
- What happens when pattern analysis finds no clear success/failure correlation?
- How does system handle sessions with incomplete interaction history (missing events)?
