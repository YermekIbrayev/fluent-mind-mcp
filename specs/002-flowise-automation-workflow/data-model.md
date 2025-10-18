# Data Model: Core Entities

**Feature**: Chatflow Automation | **Date**: 2025-10-17 | **Scope**: P1 Stories 1-7 (MVP)

---

## 1. SearchQuery
Natural language query for vector search.
- `query_text`: str (3-100 chars) - Natural language description
- `query_type`: enum ["node", "template"] - Search target
- `max_results`: int (1-10, default 5) - Results limit
- `similarity_threshold`: float (0.0-1.0, default 0.7) - Min relevance

---

## 2. SearchResult
Compact search result (<50 tokens).
- `result_id`: str - Node name or template_id
- `name`: str - Display name
- `description`: str (max 200 chars) - One-line summary
- `relevance_score`: float (0.0-1.0) - Similarity score
- `metadata`: dict - Category, baseClass, deprecated status

---

## 3. NodeDescription
Flowise node documentation for semantic search.
- `node_name`: str (unique) - Node identifier
- `label`: str - Display label
- `category`: str - Node category
- `base_classes`: list[str] - Type hierarchy
- `description`: str - What/why/how documentation
- `use_cases`: list[str] - Example scenarios
- `version`: str - Node version
- `deprecated`: bool - Deprecation status
- `embedding`: list[float] (384 dims) - Vector representation
**Storage**: ChromaDB `nodes` collection

---

## 4. FlowTemplate
Pre-built chatflow pattern.
- `template_id`: str (unique, prefix "tmpl_") - Template identifier
- `name`: str - Template name
- `description`: str - Rich template documentation
- `required_nodes`: list[str] - Node names required
- `flow_data`: dict - Complete Flowise flowData structure
- `parameters`: dict - Customizable parameters
- `embedding`: list[float] (384 dims) - Vector representation
**Storage**: ChromaDB `templates` collection

---

## 5. BuildFlowRequest
Input to build_flow function.
- `template_id`: str | None - Template to instantiate
- `nodes`: list[str] | None - Custom node list
- `connections`: str | None - "auto" or manual edges
- `parameters`: dict - Optional customizations
**Validation**: Exactly one of template_id or nodes required

---

## 6. BuildFlowResponse
Output from build_flow (<30 tokens success).
- `chatflow_id`: str - Created chatflow ID
- `name`: str - Chatflow name
- `status`: enum ["success", "error"] - Operation status
- `error`: str | None - Error message if failed (<50 tokens)

---

## 7. NodeMetadata
Live node catalog metadata from Flowise `/api/v1/nodes-list`.
- `node_name`: str - Unique identifier
- `label`: str - Display label
- `version`: str - Version number
- `category`: str - Node category
- `base_classes`: list[str] - Type hierarchy
- `description`: str - Node documentation
- `deprecated`: bool - Deprecation status
- `fetch_timestamp`: datetime - When fetched

---

## 8. CacheMetadata
Vector DB cache freshness tracking.
- `last_refresh_timestamp`: datetime - Last successful refresh
- `total_node_count`: int - Nodes in cache
- `flowise_version`: str | None - Server version
- `staleness_threshold_hours`: int (default 24) - Refresh trigger
**Validation**: is_stale() returns true if age > threshold

---

## 9. CircuitBreakerState
Circuit breaker state per dependency.
- `dependency_name`: enum ["flowise_api", "vector_db", "embedding_model"]
- `state`: enum ["CLOSED", "OPEN", "HALF_OPEN"]
- `failure_count`: int (0-3) - Consecutive failures
- `last_failure_time`: datetime | None
- `opened_time`: datetime | None
- `failure_threshold`: int (default 3)
- `timeout_seconds`: int (default 300) - 5 minutes
**Transitions**: CLOSED→OPEN (3 failures), OPEN→HALF_OPEN (5min), HALF_OPEN→CLOSED (success), HALF_OPEN→OPEN (failure)

---

## 10. TestChecklist
Manual test validation framework.
- `user_story_id`: str - User story identifier
- `scenarios`: list[TestScenario] - Acceptance scenarios
- `setup_steps`: list[str] - Test prerequisites
- `test_timestamp`: datetime | None - Execution time
- `tester_name`: str | None - Who executed
- `overall_status`: enum ["not_started", "in_progress", "passed", "failed"]

---

**File Size**: 97 lines | **Status**: ✅ GREEN ZONE
