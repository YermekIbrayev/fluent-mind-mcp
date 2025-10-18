# Testing Strategy: Manual Checklists

[← Back to Plan Index](plan_cc.md)

**Generated**: 2025-10-17
**Content**: Manual test checklist structure and approach

---

## Manual Test Checklists (100% Scenario Coverage per NFR-087)

Each user story has a checklist mapping to acceptance scenarios:

**tests/checklists/user_story_1_checklist.md:**
```markdown
# User Story 1: Vector Search for Node Selection - Test Checklist

## Setup Steps
1. Ensure ChromaDB running with `nodes` collection populated
2. Verify sentence-transformers model loaded
3. Confirm Flowise server accessible

## Test Scenarios

### Scenario 1: Query "chatbot that remembers conversation"
- [ ] Execute: `vector_search_nodes("chatbot that remembers conversation", limit=5)`
- [ ] Expected: ChatOpenAI, BufferMemory, ConversationChain in top 3 results
- [ ] Expected: Response <50 tokens per node
- [ ] Actual Results: _______________
- [ ] Pass/Fail: ___
- [ ] Timestamp: _______________
- [ ] Tester: _______________
- [ ] Notes: _______________

### Scenario 2: Query "search documents using embeddings"
...

## Summary
- Total Scenarios: 4
- Passed: ___
- Failed: ___
- Pass Rate: ___%
```

---

[← Back to Plan Index](plan_cc.md) | [Next: Testing Automated & Utilities →](11-testing-automated-utilities.md)
