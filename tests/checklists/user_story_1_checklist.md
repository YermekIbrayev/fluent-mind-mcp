# User Story 1: Vector Search for Node Selection - Test Checklist

**User Story**: As a user, I want to search for Flowise nodes using natural language descriptions to find relevant nodes for my chatflow.

**Acceptance Criteria**:
- AC1: Semantic search returns relevant nodes based on query
- AC2: Results include node metadata (name, description, category)
- AC3: Response tokens ≤50 per node (NFR-026)
- AC4: Search completes within 5 seconds (NFR-020)
- AC5: Search accuracy >90% for known queries (NFR-093)

---

## Setup Steps

Before testing, ensure:

1. **ChromaDB initialized**
   - [ ] ChromaDB running with `nodes` collection
   - [ ] Collection populated with at least 20 node descriptions
   - [ ] Verify: `chromadb_helper.get_collection_count("nodes") >= 20`

2. **Embedding model loaded**
   - [ ] sentence-transformers installed: `pip list | grep sentence-transformers`
   - [ ] all-MiniLM-L6-v2 model accessible
   - [ ] Test: Can generate 384-dim embedding vector

3. **MCP Server running**
   - [ ] Server started: `python -m fluent_mind_mcp.server`
   - [ ] Tool `vector_search_nodes` registered
   - [ ] Health check passes

---

## Test Scenarios

### Scenario 1: Search for Chatbot with Memory Nodes

**Query**: `"chatbot that remembers conversation"`

**Steps**:
1. Execute: `vector_search_nodes("chatbot that remembers conversation", limit=5)`
2. Record results

**Expected Results**:
- [ ] Returns 5 results
- [ ] Top 3 include: `chatOpenAI`, `bufferMemory`, or `conversationChain`
- [ ] Each result has fields: `name`, `label`, `description`, `category`, `relevance_score`
- [ ] Description ≤250 characters (~50 tokens)
- [ ] Relevance scores sorted descending (0.0-1.0)

**Actual Results**:
- Number of results: ___
- Top 3 nodes: _______________, _______________, _______________
- Matched expected nodes: ___ / 3
- Description length (1st result): ___ chars

**Pass/Fail**: ___
**Timestamp**: _______________
**Tester**: _______________
**Notes**: _______________

---

### Scenario 2: Search for Document Retrieval Nodes

**Query**: `"search documents using embeddings"`

**Steps**:
1. Execute: `vector_search_nodes("search documents using embeddings", limit=5)`
2. Record results

**Expected Results**:
- [ ] Returns results related to: embeddings, vector stores, retrievers
- [ ] Expected nodes in top 5: `openAIEmbeddings`, `faiss`, `memoryVectorStore`, or `retrieverTool`
- [ ] Minimum 2/4 expected nodes found

**Actual Results**:
- Top 5 nodes: _______________ (list)
- Matched expected nodes: ___ / 4

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 3: Search for Agent/Tool Nodes

**Query**: `"AI agent with tools"`

**Steps**:
1. Execute: `vector_search_nodes("AI agent with tools", limit=5)`

**Expected Results**:
- [ ] Returns agent-related nodes
- [ ] Expected in top 5: `toolAgent`, `retrieverTool`
- [ ] Category includes "Agents" or "Tools"

**Actual Results**:
- Top 5 nodes: _______________
- Agent/tool nodes found: ___ / 2

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 4: Performance Validation

**Query**: `"test query"`

**Steps**:
1. Record start time
2. Execute: `vector_search_nodes("test query", limit=5)`
3. Record end time

**Expected Results**:
- [ ] Search completes within 5 seconds (NFR-020)
- [ ] Returns valid results

**Actual Results**:
- Duration: ___ seconds
- Within 5s limit: YES / NO

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 5: Empty Query Handling

**Query**: `""` (empty string)

**Steps**:
1. Execute: `vector_search_nodes("", limit=5)`

**Expected Results**:
- [ ] Returns ValidationError or empty results
- [ ] Does not crash or hang
- [ ] Error message is clear

**Actual Results**:
- Behavior: _______________
- Error message (if any): _______________

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

### Scenario 6: Category Filter

**Query**: `"chat model"` with filter `{"category": "Chat Models"}`

**Steps**:
1. Execute: `vector_search_nodes("chat model", limit=5, filter={"category": "Chat Models"})`

**Expected Results**:
- [ ] All results have category = "Chat Models"
- [ ] Expected nodes: `chatOpenAI`, `chatAnthropic`

**Actual Results**:
- All results filtered correctly: YES / NO
- Chat model nodes found: ___

**Pass/Fail**: ___
**Timestamp**: _______________
**Notes**: _______________

---

## Accuracy Validation (NFR-093: >90%)

Using test_data_generator.get_test_queries():

| Query | Expected Nodes (Top 3) | Actual Top 3 | Matches | Pass |
|-------|----------------------|--------------|---------|------|
| "chatbot that remembers conversation" | chatOpenAI, bufferMemory, conversationChain | ___, ___, ___ | ___ / 3 | Y/N |
| "search documents using embeddings" | openAIEmbeddings, faiss, conversationalRetrievalQAChain | ___, ___, ___ | ___ / 3 | Y/N |
| "AI agent with tools" | toolAgent, retrieverTool, chatOpenAI | ___, ___, ___ | ___ / 3 | Y/N |
| "scrape web pages" | cheerioWebScraper, readFile | ___, ___, ___ | ___ / 2 | Y/N |
| "chat model for conversation" | chatOpenAI, chatAnthropic, conversationChain | ___, ___, ___ | ___ / 3 | Y/N |

**Total Expected**: 14
**Total Matched**: ___
**Accuracy**: ___% (Must be >90%)

---

## Summary

- **Total Scenarios**: 6 + Accuracy Validation
- **Passed**: ___
- **Failed**: ___
- **Pass Rate**: ___%
- **Accuracy**: ___%

**Overall Status**: PASS / FAIL
**Sign-off**: _______________
**Date**: _______________

---

## Defects Found

| # | Scenario | Description | Severity | Status |
|---|----------|-------------|----------|--------|
| 1 |          |             |          |        |
| 2 |          |             |          |        |
| 3 |          |             |          |        |

---

**Next Steps**:
- [ ] File defects for failed scenarios
- [ ] Retest after fixes
- [ ] Update test data if needed
- [ ] Document any test data improvements
