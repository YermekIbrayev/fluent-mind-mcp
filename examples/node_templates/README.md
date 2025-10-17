# Flowise Node Templates

**Extracted**: 2025-10-17
**Source**: Flowise v1.x instance at http://192.168.51.32:3000
**Total Templates**: 39 node types

---

## Purpose

Standalone templates for every Flowise node type, extracted from a working Flowise instance.

**Each template is production-ready** with complete metadata:
- ✅ filePath (component implementation)
- ✅ inputAnchors (connection points)
- ✅ outputAnchors (output connections)
- ✅ inputParams (parameter definitions)
- ✅ All required Flowise internals

---

## Constitution Compliance

**Principle VIII: Token-Efficient Architecture**

**File Organization**: ✅
- Each node type in separate file
- Clear, searchable names
- Single responsibility per template

**File Size**: ⚠️ **Exception Documented**
- Target: 100 lines (ideal)
- Limit: 200 lines (max)
- **Actual**: 61-295 lines

**Rationale for Exception**:
These are **Flowise configuration files** (allowed exception per Constitution).
Node structures are installation-specific and cannot be simplified without breaking functionality.

**Constitution Reference**: [Principle VIII - Exceptions](../../.specify/memory/principles/08-architecture.md#exceptions-allowed)

---

## Quick Start

### 1. Find a Node Template

```bash
# View all available nodes by category
cat INDEX.json

# Or search by name
grep -l "ChatOpenAI" *.json
```

### 2. Load Template

```python
import json

with open('node_templates/chatOpenAI.json', 'r') as f:
    template = json.load(f)

# Get the node structure (deep copy to avoid mutations)
node = json.loads(json.dumps(template['node']))

# ⚠️ CRITICAL: Update node ID and all anchor IDs
update_node_id(node, "my_chat_node")

# Customize inputs
node['data']['inputs']['temperature'] = 0.5
```

**Helper Function** (required when changing IDs):
```python
def update_node_id(node: dict, new_id: str) -> dict:
    """Update node ID and all related anchor IDs."""
    old_id = node['id']
    node['id'] = new_id

    # Update all anchor IDs to match new node ID
    for anchor in node['data'].get('outputAnchors', []):
        if 'id' in anchor:
            anchor['id'] = anchor['id'].replace(old_id, new_id, 1)

    for anchor in node['data'].get('inputAnchors', []):
        if 'id' in anchor:
            anchor['id'] = anchor['id'].replace(old_id, new_id, 1)

    for param in node['data'].get('inputParams', []):
        if 'id' in param:
            param['id'] = param['id'].replace(old_id, new_id, 1)

    return node
```

### 3. Use in Chatflow

```python
import httpx

# Build flowData
flow_data = {
    "nodes": [node],
    "edges": [],
    "viewport": {"x": 0, "y": 0, "zoom": 1}
}

# Create chatflow
response = httpx.post(
    "http://localhost:3000/api/v1/chatflows",
    headers={"Authorization": "Bearer YOUR_KEY"},
    json={
        "name": "My Chatflow",
        "type": "CHATFLOW",
        "deployed": False,
        "flowData": json.dumps(flow_data)
    }
)
```

---

## Template Structure

Each template file contains:

```json
{
  "_metadata": {
    "node_type": "customNode",
    "name": "chatOpenAI",
    "label": "ChatOpenAI",
    "category": "Chat Models",
    "version": 8.3,
    "description": "Wrapper around OpenAI chat models",
    "base_classes": ["ChatOpenAI", "BaseChatModel"],
    "extracted_date": "2025-10-17",
    "source": "Flowise instance",
    "usage_note": "Replace ID and customize inputs before use"
  },
  "node": {
    "id": "chatOpenAI_0",
    "type": "customNode",
    "position": {"x": 100, "y": 200},
    "data": {
      "label": "ChatOpenAI",
      "name": "chatOpenAI",
      "version": 8.3,
      "type": "ChatOpenAI",
      "category": "Chat Models",
      "baseClasses": ["ChatOpenAI", "BaseChatModel"],
      "inputs": { ... },
      "filePath": "/path/to/ChatOpenAI.js",
      "inputAnchors": [ ... ],
      "inputParams": [ ... ],
      "outputAnchors": [ ... ]
    }
  }
}
```

---

## Node Categories

### Chat Models (4 nodes)
- `chatOpenAI.json` - OpenAI chat models (GPT-4, GPT-3.5)
- `chatAnthropic.json` - Anthropic Claude models
- `chatLocalAI.json` - LocalAI chat models
- `ChatCustomLLM_v1.json` - Custom LLM integration

### Memory (2 nodes)
- `bufferMemory.json` - Simple conversation buffer
- `bufferWindowMemory.json` - Sliding window memory (last N messages)

### Chains (2 nodes)
- `conversationChain.json` - Basic conversation chain
- `conversationalRetrievalQAChain.json` - RAG conversation chain

### Vector Stores (3 nodes)
- `faiss.json` - FAISS vector store
- `memoryVectorStore.json` - In-memory vector store
- `documentStoreVS.json` - Document store with vector search

### Tools (6 nodes)
- `currentDateTime.json` - Get current date/time
- `googleCalendarTool.json` - Google Calendar integration
- `readFile.json` - Read files from filesystem
- `writeFile.json` - Write files to filesystem
- `createFolderStructure.json` - Create directory structure
- `retrieverTool.json` - Document retrieval tool

### MCP Tools (2 nodes)
- `customMCP.json` - Custom MCP server integration
- `slackMCP.json` - Slack MCP integration

### Agents (1 node)
- `toolAgent.json` - Function-calling agent

### Multi-Agents (2 nodes)
- `supervisor.json` - Supervisor agent
- `worker.json` - Worker agent

### Agent Flows (9 nodes)
- `startAgentflow.json` - AgentFlow start node
- `llmAgentflow.json` - LLM processing node
- `conditionAgentflow.json` - Conditional branching
- `conditionAgentAgentflow.json` - Multi-condition branching
- `loopAgentflow.json` - Loop control
- `iterationAgentflow.json` - Iteration control
- `directReplyAgentflow.json` - Direct output
- `agentAgentflow.json` - Agent execution
- `stickyNoteAgentflow.json` - Notes/annotations

### Embeddings (1 node)
- `openAIEmbeddings.json` - OpenAI text embeddings

### Document Loaders (2 nodes)
- `cheerioWebScraper.json` - Web scraping loader
- `documentStore.json` - Document storage

### Text Splitters (1 node)
- `htmlToMarkdownTextSplitter.json` - HTML to Markdown splitter

### Retrievers (1 node)
- `customRetriever.json` - Custom retrieval logic

### Prompts (1 node)
- `chatPromptTemplate.json` - Chat prompt template

### Cache (1 node)
- `inMemoryCache.json` - In-memory caching

### Utilities (1 node)
- `stickyNote.json` - Sticky notes for documentation

---

## Common Use Cases

### 1. Create a Simple Chatbot

```python
import json

# Load templates
with open('node_templates/chatOpenAI.json', 'r') as f:
    llm_template = json.load(f)

with open('node_templates/bufferWindowMemory.json', 'r') as f:
    memory_template = json.load(f)

with open('node_templates/conversationChain.json', 'r') as f:
    chain_template = json.load(f)

# Create nodes (deep copy to avoid mutations)
llm = json.loads(json.dumps(llm_template['node']))
update_node_id(llm, "llm_node")
llm['position'] = {'x': 400, 'y': 200}

memory = json.loads(json.dumps(memory_template['node']))
update_node_id(memory, "memory_node")
memory['position'] = {'x': 100, 'y': 200}

chain = json.loads(json.dumps(chain_template['node']))
update_node_id(chain, "chain_node")
chain['position'] = {'x': 700, 'y': 200}

# Connect nodes via input references
chain['data']['inputs']['model'] = "{{llm_node.data.instance}}"
chain['data']['inputs']['memory'] = "{{memory_node.data.instance}}"

# Create edges with proper handles
edges = [
    {
        "id": "edge_llm",
        "source": "llm_node",
        "target": "chain_node",
        "sourceHandle": get_output_handle(llm, "chatOpenAI"),
        "targetHandle": get_input_handle(chain, "model")
    },
    {
        "id": "edge_memory",
        "source": "memory_node",
        "target": "chain_node",
        "sourceHandle": get_output_handle(memory, "bufferWindowMemory"),
        "targetHandle": get_input_handle(chain, "memory")
    }
]

# Create flowData
flow_data = {
    "nodes": [llm, memory, chain],
    "edges": edges,
    "viewport": {"x": 0, "y": 0, "zoom": 1}
}
```

**Helper functions for proper connections**:
```python
def get_output_handle(node: dict, anchor_name: str = None) -> str:
    """Get output anchor ID for creating edges."""
    output_anchors = node['data'].get('outputAnchors', [])
    if anchor_name:
        for anchor in output_anchors:
            if anchor.get('name') == anchor_name:
                return anchor['id']
    return output_anchors[0]['id']  # First output

def get_input_handle(node: dict, anchor_name: str) -> str:
    """Get input anchor ID for creating edges."""
    input_anchors = node['data'].get('inputAnchors', [])
    for anchor in input_anchors:
        if anchor.get('name') == anchor_name:
            return anchor['id']
    raise ValueError(f"No input anchor named '{anchor_name}'")
```

### 2. Create a RAG System

```python
# Load templates
vector_store = load_template('faiss.json')
embeddings = load_template('openAIEmbeddings.json')
retriever = load_template('customRetriever.json')
qa_chain = load_template('conversationalRetrievalQAChain.json')

# Connect and create chatflow
# (similar to above)
```

### 3. Create an Agent

```python
# Load templates
agent = load_template('toolAgent.json')
tool1 = load_template('googleCalendarTool.json')
tool2 = load_template('readFile.json')

# Add tools to agent
agent['data']['inputs']['tools'] = [
    "{{tool1.data.instance}}",
    "{{tool2.data.instance}}"
]
```

---

## Template Modification Guidelines

### ⚠️ CRITICAL: When Changing Node IDs

**You MUST update anchor IDs** when changing a node's ID, otherwise nodes won't connect:

```python
# ❌ WRONG - Anchors still have old IDs
node['id'] = "new_id"  # Connections will break!

# ✅ CORRECT - Update node ID and all anchor IDs
update_node_id(node, "new_id")
```

**Why this matters**:
- Edges connect using anchor IDs like `nodeId-output-type`
- If you change node ID but not anchor IDs, handles won't match
- Result: Nodes appear in UI but aren't actually connected

### Required Changes

1. **Update ID with anchors**: `update_node_id(node, "unique_id")`
2. **Set Position**: `node['position'] = {"x": 100, "y": 200}`
3. **Customize Inputs**: `node['data']['inputs']['param'] = "value"`

### Optional Changes

- Update node label: `node['data']['label'] = "My Custom Node"`
- Adjust UI properties: `node['width'] = 350`
- Modify handles: `node['data']['inputAnchors']` (advanced)

### ⚠️ Do NOT Modify

- `filePath` - Installation-specific, required by Flowise
- `inputAnchors` / `outputAnchors` structure - Required for connections
- `inputParams` / `outputAnchors` structure - Required for UI
- `baseClasses` - Required for type system

---

## Connecting Nodes

Nodes connect via **two mechanisms**:

### 1. Input References (Logical Connection)
```python
# Reference format: {{nodeId.data.instance}}
chain['data']['inputs']['model'] = "{{llm_node.data.instance}}"
```

### 2. Edges (Visual Connection)
```python
{
  "id": "edge_1",
  "source": "source_node_id",
  "target": "target_node_id",
  "sourceHandle": "source_node_id-output-anchorName-Types",
  "targetHandle": "target_node_id-input-anchorName-Type"
}
```

### ⚠️ Critical: Handles Must Match Anchor IDs

The `sourceHandle` and `targetHandle` must **exactly match** the anchor IDs in the nodes:

```python
# Node anchor after update_node_id()
node['data']['outputAnchors'][0]['id']
# → "llm_node-output-chatOpenAI-ChatOpenAI|BaseChatModel"

# Edge must use this exact ID
edge['sourceHandle'] = "llm_node-output-chatOpenAI-ChatOpenAI|BaseChatModel"
```

**Use helper functions** to get correct IDs:
```python
edge = {
    "source": llm['id'],
    "target": chain['id'],
    "sourceHandle": get_output_handle(llm, "chatOpenAI"),  # Gets actual ID
    "targetHandle": get_input_handle(chain, "model")        # Gets actual ID
}
```

---

## Validation

All templates extracted from working Flowise instance and verified to:
- ✅ Contain complete Flowise metadata
- ✅ Include all required fields
- ✅ Work in Flowise UI when used correctly
- ✅ Support proper node connections

---

## Troubleshooting

### Node Doesn't Appear in UI

**Cause**: Missing required fields
**Fix**: Use unmodified template, only change ID and inputs

### Node Appears But Doesn't Work

**Cause**: Incorrect filePath or missing inputAnchors
**Fix**: Use complete template without modifying structure

### Connections Don't Work

**Cause 1**: Anchor IDs not updated when changing node ID
```python
# ❌ This breaks connections
node['id'] = "new_id"  # Anchors still have old ID
```
**Fix**: Use `update_node_id(node, "new_id")`

**Cause 2**: Edge handles don't match anchor IDs
```python
# ❌ Hardcoded handle might not match
edge['sourceHandle'] = "node_1-output-chatOpenAI-..."
```
**Fix**: Use `get_output_handle(node, anchor_name)` to get actual ID

**Cause 3**: Incorrect instance references
```python
# ❌ Wrong reference format
chain['data']['inputs']['model'] = "llm_node"
```
**Fix**: Use `{{nodeId.data.instance}}` format

---

## Programmatic Usage

### Helper Function

```python
def load_node_template(node_type: str, node_id: str, x: int = 100, y: int = 200, **inputs):
    """Load and customize a node template with proper ID updates.

    Args:
        node_type: Template filename without .json
        node_id: Unique ID for this node instance
        x, y: Position coordinates
        **inputs: Input values to customize

    Returns:
        Customized node dict with updated anchor IDs
    """
    import json

    with open(f'node_templates/{node_type}.json', 'r') as f:
        template = json.load(f)

    # Deep copy to avoid mutations
    node = json.loads(json.dumps(template['node']))

    # Update node ID and all anchor IDs
    update_node_id(node, node_id)

    # Set position
    node['position'] = {'x': x, 'y': y}

    # Update inputs
    for key, value in inputs.items():
        node['data']['inputs'][key] = value

    return node
```

### Usage Example

```python
# Create nodes with proper ID updates
llm = load_node_template(
    'chatOpenAI',
    'my_llm',
    x=400, y=200,
    modelName='gpt-4o-mini',
    temperature=0.7
)

memory = load_node_template(
    'bufferWindowMemory',
    'my_memory',
    x=100, y=200,
    k='10'
)

chain = load_node_template(
    'conversationChain',
    'my_chain',
    x=700, y=200,
    model='{{my_llm.data.instance}}',
    memory='{{my_memory.data.instance}}'
)

# Create edges with correct handles
edges = [
    {
        'id': 'edge_llm',
        'source': 'my_llm',
        'target': 'my_chain',
        'sourceHandle': get_output_handle(llm, 'chatOpenAI'),
        'targetHandle': get_input_handle(chain, 'model')
    },
    {
        'id': 'edge_memory',
        'source': 'my_memory',
        'target': 'my_chain',
        'sourceHandle': get_output_handle(memory, 'bufferWindowMemory'),
        'targetHandle': get_input_handle(chain, 'memory')
    }
]
```

---

## Index

See [INDEX.json](INDEX.json) for complete catalog:
- Node type
- Name and label
- Category
- Version
- Description
- Filename
- Number of occurrences in source chatflows

---

## References

- **Extraction Script**: [../extract_node_templates.py](../extract_node_templates.py)
- **Constitution**: [../../.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Working Chatflows Guide**: [../WORKING_CHATFLOWS_GUIDE.md](../WORKING_CHATFLOWS_GUIDE.md)
- **API Field Comparison**: [../../docs/API_FIELD_COMPARISON.md](../../docs/API_FIELD_COMPARISON.md)

---

**Last Updated**: 2025-10-17
**Tested Against**: Flowise v1.x at http://192.168.51.32:3000
