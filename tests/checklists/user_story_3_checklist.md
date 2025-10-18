# User Story 3: Build Chatflow from Template - Test Checklist

**User Story**: As a user, I want to create chatflows from curated templates to quickly start with proven patterns.

**Acceptance Criteria**:
- AC1: Build chatflow from template_id
- AC2: Generated flowData has valid structure (nodes, edges, positions)
- AC3: Chatflow created in Flowise and accessible
- AC4: Build completes within 10 seconds (NFR-022)
- AC5: Success rate >95% for curated templates (NFR-093)

---

## Setup Steps

Before testing, ensure:

1. **Flowise API accessible**
   - [ ] FLOWISE_API_URL configured: _______________
   - [ ] FLOWISE_API_KEY configured (if required)
   - [ ] Can connect: `curl $FLOWISE_API_URL/api/v1/chatflows`
   - [ ] API responds successfully

2. **Templates available**
   - [ ] Templates in ChromaDB `templates` collection
   - [ ] At least 3 templates for testing:
     - [ ] simple_chat
     - [ ] rag_flow
     - [ ] agent_with_tools

3. **MCP Server running**
   - [ ] Tool `build_flow` registered
   - [ ] Flowise client initialized

---

## Test Scenarios

### Scenario 1: Build Simple Chat from Template

**Template**: `simple_chat`

**Steps**:
1. Execute: `build_flow(template_id="simple_chat", name="Test Simple Chat")`
2. Record chatflow_id
3. Verify in Flowise UI or API

**Expected Results**:
- [ ] Returns: `{"status": "success", "chatflow_id": "...", "flow_data": {...}}`
- [ ] chatflow_id is non-empty string
- [ ] flow_data has structure:
  - [ ] `nodes` array (3 nodes expected)
  - [ ] `edges` array
  - [ ] Each node has: `id`, `type`, `data`, `position`
- [ ] Chatflow appears in Flowise: `GET /api/v1/chatflows/{chatflow_id}`
- [ ] Chatflow name = "Test Simple Chat"

**Actual Results**:
- Status: _______________
- chatflow_id: _______________
- Number of nodes: ___
- Nodes positioned: YES / NO
- Chatflow in Flowise: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Tester**: _______________
**Notes**: _______________

**Cleanup**:
- [ ] Delete chatflow: `DELETE /api/v1/chatflows/{chatflow_id}`

---

### Scenario 2: Build RAG Flow from Template

**Template**: `rag_flow`

**Steps**:
1. Execute: `build_flow(template_id="rag_flow", name="Test RAG Flow")`
2. Verify flowData structure

**Expected Results**:
- [ ] Success status
- [ ] flow_data has ≥4 nodes (embeddings, vector store, retriever, chain)
- [ ] Node types include embedding and vector store nodes
- [ ] Nodes positioned left-to-right with ~300px spacing

**Actual Results**:
- Number of nodes: ___
- Node types present: _______________
- Horizontal spacing (avg): ___ px
- Visual layout acceptable: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

**Cleanup**:
- [ ] Delete chatflow

---

### Scenario 3: Build Agent with Tools from Template

**Template**: `agent_with_tools`

**Steps**:
1. Execute: `build_flow(template_id="agent_with_tools", name="Test Agent")`

**Expected Results**:
- [ ] Success status
- [ ] Nodes include agent and tool nodes
- [ ] All nodes have unique IDs

**Actual Results**:
- Status: _______________
- Duplicate IDs found: YES / NO (should be NO)

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

**Cleanup**:
- [ ] Delete chatflow

---

### Scenario 4: Node Positioning Validation

**Template**: `simple_chat`

**Steps**:
1. Build chatflow
2. Examine node positions in flowData

**Expected Results**:
- [ ] Nodes positioned left-to-right
- [ ] Horizontal spacing: 250-350px
- [ ] Vertical spacing: ~200px
- [ ] Starting position: x≈100, y≈100

**Actual Results**:
- Node 1 position: (x=___, y=___)
- Node 2 position: (x=___, y=___)
- Node 3 position: (x=___, y=___)
- Spacing acceptable: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

**Cleanup**:
- [ ] Delete chatflow

---

### Scenario 5: Performance Validation

**Template**: `simple_chat`

**Steps**:
1. Record start time
2. Execute: `build_flow(template_id="simple_chat", name="Perf Test")`
3. Record end time

**Expected Results**:
- [ ] Build completes within 10 seconds (NFR-022)

**Actual Results**:
- Duration: ___ seconds
- Within 10s limit: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

**Cleanup**:
- [ ] Delete chatflow

---

### Scenario 6: Nonexistent Template Error Handling

**Template**: `nonexistent_template`

**Steps**:
1. Execute: `build_flow(template_id="nonexistent_template")`

**Expected Results**:
- [ ] Returns TemplateNotFoundError
- [ ] Error message is clear: "Template 'nonexistent_template' not found"
- [ ] Does not crash
- [ ] No chatflow created in Flowise

**Actual Results**:
- Error type: _______________
- Error message: _______________
- Behavior acceptable: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 7: FlowData Validation

**Template**: `simple_chat`

**Steps**:
1. Build chatflow
2. Validate flowData structure

**Expected Results**:
- [ ] flowData is valid JSON
- [ ] Required keys present: `nodes`, `edges`
- [ ] Each node has required fields:
  - [ ] `id` (unique string)
  - [ ] `type` (node type from Flowise catalog)
  - [ ] `data` (object with node configuration)
  - [ ] `position` (object with `x`, `y` coordinates)

**Actual Results**:
- Valid JSON: YES / NO
- All required fields present: YES / NO
- Flowise accepts flowData: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

**Cleanup**:
- [ ] Delete chatflow

---

## Success Rate Validation (NFR-093: >95%)

Build chatflow from each curated template:

| Template | Build Success | Chatflow Created | Flowise Accessible | Pass |
|----------|---------------|------------------|-------------------|------|
| simple_chat | Y/N | Y/N | Y/N | Y/N |
| rag_flow | Y/N | Y/N | Y/N | Y/N |
| agent_with_tools | Y/N | Y/N | Y/N | Y/N |
| template_4 | Y/N | Y/N | Y/N | Y/N |
| template_5 | Y/N | Y/N | Y/N | Y/N |
| template_6 | Y/N | Y/N | Y/N | Y/N |
| template_7 | Y/N | Y/N | Y/N | Y/N |
| template_8 | Y/N | Y/N | Y/N | Y/N |
| template_9 | Y/N | Y/N | Y/N | Y/N |
| template_10 | Y/N | Y/N | Y/N | Y/N |

**Total Templates**: 10
**Successful Builds**: ___
**Success Rate**: ___% (Must be >95%)

---

## End-to-End Complete Workflow

**Scenario**: Complete Phase 1 workflow

**Steps**:
1. Search nodes: `vector_search_nodes("chatbot with memory", limit=5)`
2. Search templates: `search_templates("simple chatbot", limit=3)`
3. Build chatflow: `build_flow(template_id="simple_chat", name="E2E Test")`
4. Verify in Flowise
5. Clean up

**Expected Results**:
- [ ] All 3 steps succeed
- [ ] Total time <60 seconds
- [ ] Chatflow functional in Flowise

**Actual Results**:
- Node search: SUCCESS / FAIL
- Template search: SUCCESS / FAIL
- Build chatflow: SUCCESS / FAIL
- Total duration: ___ seconds
- Chatflow functional: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Tester**: _______________
**Notes**: _______________

---

## Summary

- **Total Scenarios**: 7 + Success Rate Validation + E2E Workflow
- **Passed**: ___
- **Failed**: ___
- **Pass Rate**: ___%
- **Success Rate**: ___%

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

## Phase 1 Acceptance Decision

**Phase 1 Deliverable**: "Vector search + template-based chatflow creation working end-to-end"

**Criteria**:
- [ ] Vector search accuracy >90%
- [ ] Template build success rate >95%
- [ ] Performance targets met (5s search, 10s build)
- [ ] All critical scenarios pass
- [ ] No P0/P1 defects outstanding

**Decision**: ACCEPT / REJECT Phase 1
**Approver**: _______________
**Date**: _______________

---

**Next Steps**:
- [ ] If ACCEPTED: Proceed to Phase 2 (Connection Inference)
- [ ] If REJECTED: Fix defects and retest
- [ ] Document lessons learned
- [ ] Update templates based on testing feedback
