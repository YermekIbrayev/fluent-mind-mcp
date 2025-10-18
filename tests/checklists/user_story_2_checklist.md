# User Story 2: Template Search and Selection - Test Checklist

**User Story**: As a user, I want to search for curated flow templates using natural language to find starting points for my chatflows.

**Acceptance Criteria**:
- AC1: Semantic search returns relevant templates
- AC2: Tag-based boosting increases precision
- AC3: Results include template metadata (complexity, node count)
- AC4: Search completes within 5 seconds (NFR-020)

---

## Setup Steps

Before testing, ensure:

1. **ChromaDB initialized**
   - [ ] `templates` collection exists
   - [ ] Collection populated with at least 10 templates
   - [ ] Verify: `chromadb_helper.get_collection_count("templates") >= 10`

2. **Templates curated**
   - [ ] Templates have semantic descriptions
   - [ ] Templates have relevant tags
   - [ ] Templates validated for Phase 1:
     - [ ] `simple_chat` (chatbot, conversation, memory)
     - [ ] `rag_flow` (rag, qa, documents, retrieval)
     - [ ] `agent_with_tools` (agent, tools, autonomous)

3. **MCP Server running**
   - [ ] Tool `search_templates` registered
   - [ ] Health check passes

---

## Test Scenarios

### Scenario 1: Search for Simple Chatbot Template

**Query**: `"simple chatbot"`

**Steps**:
1. Execute: `search_templates("simple chatbot", limit=3)`
2. Record results

**Expected Results**:
- [ ] Returns templates (1-3 results)
- [ ] `simple_chat` template appears in results
- [ ] Result fields: `template_id`, `name`, `description`, `tags`, `node_count`, `complexity_level`
- [ ] Does NOT include full `flow_data` (preview only)

**Actual Results**:
- Number of results: ___
- simple_chat found: YES / NO
- simple_chat ranking: ___ / 3
- Fields present: _______________

**Pass/Fail**: ___
**Timestamp**: _______________
**Tester**: _______________
**Notes**: _______________

---

### Scenario 2: Search for Document QA Template

**Query**: `"document question answering"`

**Steps**:
1. Execute: `search_templates("document question answering", limit=3)`

**Expected Results**:
- [ ] `rag_flow` template appears in results
- [ ] Tags include: "rag" or "qa" or "documents"
- [ ] Complexity level indicated (e.g., "intermediate")

**Actual Results**:
- rag_flow found: YES / NO
- Tags: _______________
- Complexity: _______________

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 3: Search for Agent Template

**Query**: `"agent with tools"`

**Steps**:
1. Execute: `search_templates("agent with tools", limit=3)`

**Expected Results**:
- [ ] `agent_with_tools` template appears
- [ ] Tags include: "agent" or "tools"

**Actual Results**:
- agent_with_tools found: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 4: Tag-Based Boosting

**Query**: `"conversational AI"`

**Steps**:
1. Execute: `search_templates("conversational AI", limit=5)`
2. Examine ranking of templates with "conversation" or "chatbot" tags

**Expected Results**:
- [ ] Templates with matching tags rank higher
- [ ] `simple_chat` (tagged "conversation") ranks in top 3
- [ ] Templates without matching tags rank lower

**Actual Results**:
- simple_chat ranking: ___ / 5
- Tag matching observed: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 5: Template Metadata Preview

**Query**: `"simple chatbot"`

**Steps**:
1. Execute: `search_templates("simple chatbot", limit=1)`
2. Examine first result metadata

**Expected Results**:
- [ ] `node_count` present (e.g., 3)
- [ ] `complexity_level` present ("beginner", "intermediate", or "advanced")
- [ ] `estimated_tokens` present
- [ ] Full `flow_data` NOT included (reduces token usage)

**Actual Results**:
- node_count: ___
- complexity_level: ___
- estimated_tokens: ___
- flow_data included: YES / NO (should be NO)

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 6: Performance Validation

**Query**: `"test template"`

**Steps**:
1. Record start time
2. Execute: `search_templates("test template", limit=3)`
3. Record end time

**Expected Results**:
- [ ] Search completes within 5 seconds (NFR-020)

**Actual Results**:
- Duration: ___ seconds
- Within 5s limit: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 7: Empty Query Handling

**Query**: `""` (empty string)

**Steps**:
1. Execute: `search_templates("", limit=3)`

**Expected Results**:
- [ ] Returns ValidationError or empty results
- [ ] Does not crash

**Actual Results**:
- Behavior: _______________
- Error message: _______________

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

## Template Search Accuracy Validation

Using test_data_generator.get_template_queries():

| Query | Expected Template | Found | Ranking | Pass |
|-------|-------------------|-------|---------|------|
| "simple chatbot" | simple_chat | Y/N | ___ / 3 | Y/N |
| "document question answering" | rag_flow | Y/N | ___ / 3 | Y/N |
| "agent with tools" | agent_with_tools | Y/N | ___ / 3 | Y/N |
| "conversational AI" | simple_chat, rag_flow | Y/N | ___ / 3 | Y/N |

**Total Expected**: 5
**Total Found**: ___
**Accuracy**: ___% (Goal: >90%)

---

## Summary

- **Total Scenarios**: 7 + Accuracy Validation
- **Passed**: ___
- **Failed**: ___
- **Pass Rate**: ___%

**Overall Status**: PASS / FAIL
**Sign-off**: _______________
**Date**: _______________

---

## Defects Found

| # | Scenario | Description | Severity | Status |
|---|----------|-------------|----------|--------|
| 1 |          |             |          |        |
| 2 |          |             |          |        |

---

**Next Steps**:
- [ ] Verify template curation quality
- [ ] File defects for failed scenarios
- [ ] Consider adding more diverse templates
