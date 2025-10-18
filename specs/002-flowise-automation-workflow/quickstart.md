# Quickstart: Chatflow Automation

**Time**: 5 minutes | **Audience**: Developers | **Prerequisites**: Flowise MCP Server (Feature 001), Python 3.12+

---

## 1. Install Dependencies (30s)

```bash
pip install chromadb sentence-transformers
python -c "import chromadb; import sentence_transformers; print('OK')"
```

---

## 2. Initialize Vector Database (2m)

```bash
python -m fluent_mind_mcp.chatflow_automation.vector_db.setup

# This will:
# - Create chroma_db/ directory
# - Download all-MiniLM-L6-v2 model (~80MB)
# - Create 5 collections (nodes, templates, sdd_artifacts, failed_artifacts, sessions)
# - Populate node descriptions (87 nodes) and flow templates (10 templates)
```

**Expected**: `Initialization complete! [87 nodes, 10 templates added]`

---

## 3. Test Vector Search (1m)

```bash
python -c "
from fluent_mind_mcp.chatflow_automation.vector_search.service import VectorSearchService
service = VectorSearchService()
results = service.search_nodes('chat with memory', max_results=3)
print(f'Found {len(results)} nodes with scores >0.7')
"
```

**Expected**: 3 relevant nodes (ChatOpenAI, BufferMemory, ConversationChain)

---

## 4. Test Template Search (1m)

```bash
python -c "
from fluent_mind_mcp.chatflow_automation.flow_templates.service import TemplateService
service = TemplateService()
results = service.search_templates('customer support chatbot')
print(f'Found {len(results)} templates')
"
```

**Expected**: 1-3 relevant templates

---

## 5. Test build_flow (30s)

Requires Flowise connection.

```bash
python -c "
from fluent_mind_mcp.chatflow_automation.flow_builder.service import FlowBuilderService
service = FlowBuilderService()
result = service.build_flow(template_id='tmpl_simple_chat')
print(f'Created: {result.chatflow_id} - {result.name}')
"
```

**Expected**: Chatflow created successfully

---

## 6. Verify System Health (15s)

```bash
python -m fluent_mind_mcp.chatflow_automation.vector_db.client health_check
```

**Expected**:
```
System Health: HEALTHY
- Vector DB: OK (5 collections, 97 entries)
- Embedding Model: OK (all-MiniLM-L6-v2)
- Flowise API: OK (circuit: CLOSED)
- Node Catalog: FRESH (last refresh: 2h ago)
```

---

## Next Steps

**For Implementation**: Run `/speckit.tasks` to generate task breakdown, follow TDD cycle

**For Testing**: Use manual checklists in `checklists/` + run `pytest tests/critical_path/`

**For Usage**: Use MCP tools (search_nodes, search_templates, build_flow, refresh_node_catalog, get_system_health)

---

## Troubleshooting

**ChromaDB init fails**: Check disk space (~500MB), verify write permissions
**Embedding download slow**: Check internet, downloads from Hugging Face (~80MB), caches in `~/.cache/huggingface/`
**No search results**: Check DB initialized (`ls chroma_db/`), run health check, lower similarity threshold (0.5)
**Flowise connection fails**: Verify Flowise running, check `FLOWISE_API_URL`, circuit breaker may be open (check health)

---

**File Size**: 93 lines | **Status**: ✅ GREEN ZONE
