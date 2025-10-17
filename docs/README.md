# Documentation

**Fluent Mind MCP Server** - Complete documentation for Flowise chatflow management.

---

## 🎯 Quick Navigation

**What are you trying to do?**

| I want to... | Go to |
|--------------|-------|
| **Create a working chatflow** | [Node Templates](../examples/node_templates/) |
| **Understand API field names** | [API Field Comparison](API_FIELD_COMPARISON.md) |
| **Learn chatflow creation** | [Working Chatflows Guide](../examples/WORKING_CHATFLOWS_GUIDE.md) |
| **Use MCP tools** | [MCP Server Documentation](../README.md) |
| **Understand the data model** | [Data Model](../specs/001-flowise-mcp-server/data-model.md) |
| **Understand node connections** | [Flowise Connection Logic](flowise-node-connection-logic.md) |
| **Work with flow graphs** | [Graph Utilities](../src/fluent_mind_mcp/utils/graph.py) |

---

## 📚 Documentation Structure

### /docs (This Directory)

**[API_FIELD_COMPARISON.md](API_FIELD_COMPARISON.md)** - Critical Reference
- Documented vs actual Flowise API fields
- Field naming (camelCase vs snake_case)
- Missing fields discovered
- Real API responses
- **Use this when**: Debugging API issues or updating models

**[flowise-node-connection-logic.md](flowise-node-connection-logic.md)** - Node Connection Patterns ✨ NEW
- Node creation and initialization patterns
- Connection validation algorithms (cycle detection)
- Flow execution logic (queue-based processing)
- Variable resolution system
- Dependency management patterns
- **Use this when**: Building flow execution engines or understanding Flowise internals

**[../examples/flowise-flow-examples.json](../examples/flowise-flow-examples.json)** - Flow Pattern Examples ✨ NEW
- Linear, conditional, loop, iteration flows
- Variable resolution examples
- Human-in-the-loop patterns
- Complete JSON structures
- **Use this when**: Testing flows or learning flow patterns

### /examples

**[node_templates/](../examples/node_templates/)** - Production-Ready Templates ✅
- 39 standalone node templates
- Extracted from working Flowise instance
- Complete with all required metadata
- **Use this when**: Building chatflows programmatically

**[WORKING_CHATFLOWS_GUIDE.md](../examples/WORKING_CHATFLOWS_GUIDE.md)** - How-To Guide
- Why simple nodes don't work
- How to use node templates
- Real working examples
- **Use this when**: Learning to create functional chatflows

**[README.md](../examples/README.md)** - API Structure Reference
- Field naming conventions
- JSON structure examples
- Common mistakes
- **Use this when**: Understanding API structure

### /specs

**[data-model.md](../specs/001-flowise-mcp-server/data-model.md)** - Data Model Specification
- Complete Chatflow entity definition
- Field validation rules
- Pydantic model reference
- **Use this when**: Implementing models or validation

**[spec.md](../specs/001-flowise-mcp-server/spec.md)** - Feature Specification
- 5 user stories
- Requirements and acceptance criteria
- **Use this when**: Understanding project scope

**[plan.md](../specs/001-flowise-mcp-server/plan.md)** - Implementation Plan
- Architecture decisions
- Task breakdown (122 tasks)
- **Use this when**: Understanding implementation

---

## 🔑 Key Concepts

### 1. Field Naming: camelCase Not snake_case

**Critical**: Flowise API uses camelCase, not snake_case

```python
# ✅ CORRECT
{
    "flowData": "...",
    "isPublic": false,
    "workspaceId": "uuid",
    "createdDate": "2025-10-17T00:00:00Z"
}

# ❌ WRONG
{
    "flow_data": "...",
    "is_public": false,
    "workspace_id": "uuid",
    "created_date": "2025-10-17T00:00:00Z"
}
```

**See**: [API_FIELD_COMPARISON.md](API_FIELD_COMPARISON.md)

### 2. Simplified Nodes Don't Work

Creating nodes with minimal structure **doesn't work** in Flowise UI:

```json
{
  "id": "node_1",
  "type": "chatOpenAI",
  "data": {
    "inputs": {"modelName": "gpt-4o-mini"}
  }
}
```

**Why**: Missing required Flowise metadata (filePath, inputAnchors, outputAnchors, etc.)

**Solution**: Use [node templates](../examples/node_templates/)

**See**: [WORKING_CHATFLOWS_GUIDE.md](../examples/WORKING_CHATFLOWS_GUIDE.md)

### 3. flowData Must Be JSON String

```python
# ✅ CORRECT
{
    "name": "My Chatflow",
    "flowData": json.dumps({"nodes": [...], "edges": [...]})
}

# ❌ WRONG
{
    "name": "My Chatflow",
    "flowData": {"nodes": [...], "edges": [...]}
}
```

---

## 🛠️ Implementation Reference

### MCP Server

**Source Code**: `src/fluent_mind_mcp/`

```
src/fluent_mind_mcp/
├── models/
│   ├── chatflow.py         # Chatflow, FlowData, Node, Edge models
│   ├── config.py           # FlowiseConfig
│   └── responses.py        # PredictionResponse, Error models
├── client/
│   └── flowise_client.py   # HTTP client
├── services/
│   └── chatflow_service.py # Business logic
├── utils/                   # ✨ NEW
│   ├── graph.py            # Graph operations (cycle detection, topological sort)
│   ├── layout.py           # Node positioning algorithms
│   └── validators.py       # Input validation
└── server.py               # MCP server implementation
```

### 8 MCP Tools

1. **list_chatflows** - Query all chatflows
2. **get_chatflow** - Get chatflow details
3. **run_prediction** - Execute chatflow
4. **create_chatflow** - Create new chatflow
5. **update_chatflow** - Modify chatflow
6. **deploy_chatflow** - Toggle deployment
7. **delete_chatflow** - Remove chatflow
8. **generate_agentflow_v2** - Generate AgentFlow V2

---

## 📖 Documentation History

### Timeline

1. **Initial Documentation** - Generic reference from GitHub
2. **API Verification** - Tested against live Flowise instance
3. **Field Discovery** - Found camelCase vs snake_case issue ✅
4. **Field Correction** - Updated all documentation
5. **Node Template Extraction** - Created 39 standalone templates ✅
6. **Consolidation** - Removed redundant docs (this update)

### What Was Removed

- ❌ `flowise-api-verification.md` - Outdated (had wrong field names)
- ❌ `flowise-nodes-reference.md` - Redundant (replaced by node templates)

### What Remains

- ✅ `API_FIELD_COMPARISON.md` - Accurate field reference
- ✅ `examples/node_templates/` - 39 working templates
- ✅ `examples/WORKING_CHATFLOWS_GUIDE.md` - Usage guide

---

## 🧪 Testing

### Test Coverage

- **Unit Tests**: 183 passing ✅
- **Integration Tests**: 75/91 passing (82%)
- **Acceptance Tests**: 68/68 passing (100%) ✅

### Running Tests

```bash
# All tests
pytest tests/

# Unit only
pytest tests/unit/

# Acceptance only
pytest tests/acceptance/
```

---

## 🔗 External References

- **Flowise Documentation**: https://docs.flowiseai.com/
- **Flowise GitHub**: https://github.com/FlowiseAI/Flowise
- **MCP Protocol**: https://modelcontextprotocol.io/

---

## 📝 Contributing

When updating documentation:

1. ✅ Keep field names in camelCase (match API)
2. ✅ Test against live Flowise instance
3. ✅ Update both docs and examples
4. ✅ Verify all tests pass
5. ✅ Follow constitution file size limits (≤200 lines)

---

## 🎓 Learning Path

**Beginner**: Start here
1. [README.md](../README.md) - Project overview
2. [examples/node_templates/QUICK_REFERENCE.md](../examples/node_templates/QUICK_REFERENCE.md) - Quick start
3. [examples/WORKING_CHATFLOWS_GUIDE.md](../examples/WORKING_CHATFLOWS_GUIDE.md) - Learn the patterns

**Intermediate**: Building chatflows
1. [examples/node_templates/](../examples/node_templates/) - Browse templates
2. [examples/node_templates/node_builder.py](../examples/node_templates/node_builder.py) - Use helper utilities
3. [API_FIELD_COMPARISON.md](API_FIELD_COMPARISON.md) - Understand API structure

**Advanced**: Contributing & Internals
1. [specs/001-flowise-mcp-server/spec.md](../specs/001-flowise-mcp-server/spec.md) - Full specification
2. [specs/001-flowise-mcp-server/data-model.md](../specs/001-flowise-mcp-server/data-model.md) - Data model
3. [flowise-node-connection-logic.md](flowise-node-connection-logic.md) - ✨ Flow execution patterns
4. [utils/graph.py](../src/fluent_mind_mcp/utils/graph.py) - ✨ Graph algorithms
5. [.specify/memory/constitution.md](../.specify/memory/constitution.md) - Development principles

---

**Last Updated**: 2025-10-17
**Documentation Version**: 2.0.0 (Consolidated)
