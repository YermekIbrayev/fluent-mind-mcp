# Node Templates - Quick Reference

**Quick examples** for the most common nodes.

⚠️ **IMPORTANT**: Always use `update_node_id()` when changing node IDs! See [Helper Functions](#helper-functions) section.

---

## Most Used Nodes

### ChatOpenAI

```python
import json

with open('node_templates/chatOpenAI.json', 'r') as f:
    template = json.load(f)

# Deep copy to avoid mutations
node = json.loads(json.dumps(template['node']))

# ⚠️ CRITICAL: Update node ID and all anchor IDs
update_node_id(node, "my_llm")

# Set position
node['position'] = {"x": 100, "y": 200}

# Customize inputs
node['data']['inputs']['modelName'] = "gpt-4o-mini"
node['data']['inputs']['temperature'] = 0.7
node['data']['inputs']['maxTokens'] = 1000
```

**Common Parameters**:
- `modelName`: "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"
- `temperature`: 0.0-2.0 (default: 0.9)
- `maxTokens`: Max response tokens
- `streaming`: true/false

---

### Buffer Window Memory

```python
with open('node_templates/bufferWindowMemory.json', 'r') as f:
    template = json.load(f)

node = template['node']
node['id'] = "my_memory"
node['position'] = {"x": 100, "y": 300}

# Customize
node['data']['inputs']['k'] = "10"  # Keep last 10 messages
node['data']['inputs']['memoryKey'] = "chat_history"
```

**Common Parameters**:
- `k`: Number of messages to keep (default: "4")
- `memoryKey`: Key for memory storage (default: "chat_history")

---

### Conversation Chain

```python
with open('node_templates/conversationChain.json', 'r') as f:
    template = json.load(f)

node = template['node']
node['id'] = "my_chain"
node['position'] = {"x": 400, "y": 200}

# Connect to other nodes
node['data']['inputs']['model'] = "{{my_llm.data.instance}}"
node['data']['inputs']['memory'] = "{{my_memory.data.instance}}"

# Customize
node['data']['inputs']['systemMessagePrompt'] = "You are a helpful assistant."
```

**Common Parameters**:
- `model`: Reference to LLM node
- `memory`: Reference to memory node
- `systemMessagePrompt`: System message
- `chatPromptTemplate`: Optional custom prompt

---

### FAISS Vector Store

```python
with open('node_templates/faiss.json', 'r') as f:
    template = json.load(f)

node = template['node']
node['id'] = "my_vectorstore"
node['position'] = {"x": 100, "y": 400}

# Connect embeddings
node['data']['inputs']['embeddings'] = "{{my_embeddings.data.instance}}"

# Customize
node['data']['inputs']['topK'] = "5"
```

**Common Parameters**:
- `embeddings`: Reference to embeddings node
- `topK`: Number of results to return (default: "4")

---

### OpenAI Embeddings

```python
with open('node_templates/openAIEmbeddings.json', 'r') as f:
    template = json.load(f)

node = template['node']
node['id'] = "my_embeddings"
node['position'] = {"x": 100, "y": 500}

# Customize
node['data']['inputs']['modelName'] = "text-embedding-3-small"
```

**Common Parameters**:
- `modelName`: "text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"

---

### Tool Agent

```python
with open('node_templates/toolAgent.json', 'r') as f:
    template = json.load(f)

node = template['node']
node['id'] = "my_agent"
node['position'] = {"x": 700, "y": 200}

# Connect model, memory, and tools
node['data']['inputs']['model'] = "{{my_llm.data.instance}}"
node['data']['inputs']['memory'] = "{{my_memory.data.instance}}"
node['data']['inputs']['tools'] = [
    "{{tool1.data.instance}}",
    "{{tool2.data.instance}}"
]

# Customize
node['data']['inputs']['systemMessage'] = "You are a helpful agent."
node['data']['inputs']['maxIterations'] = "5"
```

**Common Parameters**:
- `model`: Reference to LLM node
- `memory`: Reference to memory node
- `tools`: Array of tool references
- `systemMessage`: System prompt
- `maxIterations`: Max agent iterations

---

## Helper Functions

### Required Helpers (Copy these to your code)

```python
def update_node_id(node: dict, new_id: str) -> dict:
    """Update node ID and all related anchor IDs."""
    old_id = node['id']
    node['id'] = new_id

    # Update all anchor IDs
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


def create_node(template_name: str, node_id: str, x: int = 100, y: int = 100, **inputs):
    """Quick node creation from template with proper ID updates.

    Args:
        template_name: Template filename without .json
        node_id: Unique ID for node
        x, y: Position coordinates
        **inputs: Input values to set

    Returns:
        Customized node dict with updated anchor IDs
    """
    import json
    from pathlib import Path

    template_path = Path('node_templates') / f'{template_name}.json'
    with open(template_path, 'r') as f:
        template = json.load(f)

    # Deep copy to avoid mutations
    node = json.loads(json.dumps(template['node']))

    # Update node ID and all anchor IDs
    update_node_id(node, node_id)

    # Set position
    node['position'] = {"x": x, "y": y}

    # Set inputs
    for key, value in inputs.items():
        node['data']['inputs'][key] = value

    return node
```

**Usage**:

```python
# Create nodes with proper ID updates
llm = create_node('chatOpenAI', 'llm1', 100, 100,
                  modelName='gpt-4o-mini',
                  temperature=0.7)

memory = create_node('bufferWindowMemory', 'mem1', 100, 300,
                     k='10')

chain = create_node('conversationChain', 'chain1', 400, 200,
                    model='{{llm1.data.instance}}',
                    memory='{{mem1.data.instance}}',
                    systemMessagePrompt='You are helpful.')

# Create edges with proper handles (IMPORTANT!)
edges = [
    {
        "id": "e1",
        "source": "llm1",
        "target": "chain1",
        "sourceHandle": get_output_handle(llm, "chatOpenAI"),
        "targetHandle": get_input_handle(chain, "model")
    },
    {
        "id": "e2",
        "source": "mem1",
        "target": "chain1",
        "sourceHandle": get_output_handle(memory, "bufferWindowMemory"),
        "targetHandle": get_input_handle(chain, "memory")
    }
]

# Build flowData
flow_data = {
    "nodes": [llm, memory, chain],
    "edges": edges,
    "viewport": {"x": 0, "y": 0, "zoom": 1}
}

# Create chatflow
import httpx

response = httpx.post(
    'http://localhost:3000/api/v1/chatflows',
    headers={'Authorization': 'Bearer YOUR_KEY'},
    json={
        'name': 'My Chatflow',
        'type': 'CHATFLOW',
        'deployed': False,
        'flowData': json.dumps(flow_data)
    }
)

print(f"Created: {response.json()['id']}")
```

---

## Common Patterns

### Basic Chatbot

```python
llm = create_node('chatOpenAI', 'llm', 100, 200)
memory = create_node('bufferWindowMemory', 'mem', 100, 400)
chain = create_node('conversationChain', 'chain', 400, 300,
                    model='{{llm.data.instance}}',
                    memory='{{mem.data.instance}}')
```

### RAG System

```python
embeddings = create_node('openAIEmbeddings', 'emb', 100, 100)
vectorstore = create_node('faiss', 'vs', 100, 300,
                          embeddings='{{emb.data.instance}}')
llm = create_node('chatOpenAI', 'llm', 400, 100)
qa_chain = create_node('conversationalRetrievalQAChain', 'qa', 700, 200,
                       model='{{llm.data.instance}}',
                       vectorStore='{{vs.data.instance}}')
```

### Agent with Tools

```python
llm = create_node('chatOpenAI', 'llm', 100, 100)
memory = create_node('bufferMemory', 'mem', 100, 300)
tool1 = create_node('currentDateTime', 't1', 400, 100)
tool2 = create_node('readFile', 't2', 400, 300)
agent = create_node('toolAgent', 'agent', 700, 200,
                    model='{{llm.data.instance}}',
                    memory='{{mem.data.instance}}',
                    tools=['{{t1.data.instance}}', '{{t2.data.instance}}'])
```

---

## Node Reference

| Template | Category | Description |
|----------|----------|-------------|
| `chatOpenAI.json` | Chat Models | OpenAI GPT models |
| `chatAnthropic.json` | Chat Models | Anthropic Claude |
| `bufferMemory.json` | Memory | Simple buffer |
| `bufferWindowMemory.json` | Memory | Sliding window |
| `conversationChain.json` | Chains | Basic conversation |
| `conversationalRetrievalQAChain.json` | Chains | RAG conversation |
| `faiss.json` | Vector Stores | FAISS vector DB |
| `openAIEmbeddings.json` | Embeddings | OpenAI embeddings |
| `toolAgent.json` | Agents | Function-calling agent |
| `currentDateTime.json` | Tools | Date/time tool |
| `readFile.json` | Tools | File reading |
| `writeFile.json` | Tools | File writing |
| `googleCalendarTool.json` | Tools | Calendar integration |
| `customMCP.json` | MCP Tools | Custom MCP server |
| `supervisor.json` | Multi-Agents | Supervisor agent |
| `worker.json` | Multi-Agents | Worker agent |

See [INDEX.json](INDEX.json) for complete list of 39 templates.

---

**Full Documentation**: [README.md](README.md)
