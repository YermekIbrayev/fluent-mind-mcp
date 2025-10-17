# Flowise Chatflow System

Generate and push production-ready chatflows to Flowise automatically.

---

## Quick Start

**Option 1: Push from config** (recommended)
```bash
python3 push_flow.py --config flows/simple_chat.yaml
```

**Option 2: Push from CLI**
```bash
python3 push_flow.py --name "My Chat" --nodes "chatOpenAI,conversationChain" --edges "0-1"
```

**Option 3: Generate local files**
```bash
python3 create_example_flows.py  # Saves to generated_flows/
```

---

## What's Included

### 📦 Node Templates (`node_templates/`)
39 real Flowise node definitions extracted from a working instance:
- ChatOpenAI, Claude, Ollama, etc.
- Memory nodes (Buffer, Window, Redis)
- Chains (Conversation, RetrievalQA, etc.)
- Tools (Calculator, DateTime, Web Browser, etc.)
- Document loaders, Vector stores, Embeddings

### 🚀 Auto-Pusher (`push_flow.py`)
**The main tool** - Automatically pushes chatflows to Flowise:
1. Reads simple YAML config or CLI args
2. Loads node templates
3. Builds flow with proper IDs and edges
4. **Phase 1**: Creates chatflow in Flowise
5. **Phase 2**: Fixes all node references automatically
6. Returns ready-to-use chatflow ID

### 🔨 Generator (`create_example_flows.py`)
Creates local JSON files (for inspection/import):
1. Loads node templates
2. Creates chatflows with proper node IDs
3. Validates graph structure (cycle detection)
4. Applies hierarchical layout
5. Saves complete chatflow JSON files

### ✨ Generated Flows (`generated_flows/`)
4 example chatflows:
- **Simple Chat** - Basic ChatOpenAI → ConversationChain
- **Chat with Memory** - LLM + BufferMemory → Chain
- **RAG Flow** - LLM + DocumentStore → RetrievalQA
- **Agent Flow** - LLM + Tools → Agent

---

## How to Use

### Just Describe What You Want

**Create a YAML file** (`flows/my_flow.yaml`):
```yaml
name: "My Custom Flow"
deployed: false

spec:
  nodes:
    - template: "chatOpenAI"
      inputs:
        modelName: "gpt-4o-mini"

    - template: "bufferMemory"
      inputs: {}

    - template: "conversationChain"
      inputs: {}

  edges:
    - from: 0  # chatOpenAI
      to: 2    # conversationChain

    - from: 1  # bufferMemory
      to: 2    # conversationChain
```

**Push it**:
```bash
python3 push_flow.py --config flows/my_flow.yaml
```

**Done!** The script handles everything:
- ✅ Loads templates
- ✅ Generates unique IDs
- ✅ Creates proper edges
- ✅ Validates no cycles
- ✅ Applies layout
- ✅ Phase 1: Creates in Flowise
- ✅ Phase 2: Fixes all references
- ✅ Returns chatflow ID

---

## How It Works Internally

```python
# 1. Load templates
builder = FlowBuilder(templates_dir)

# 2. Create nodes from templates
llm_node = builder.create_node_from_template(
    "chatOpenAI",
    {"modelName": "gpt-4o-mini", "temperature": 0.7}
)

memory_node = builder.create_node_from_template("bufferMemory")
chain_node = builder.create_node_from_template("conversationChain")

# 3. Connect with edges
edge1 = builder.create_edge(llm_node, chain_node)
edge2 = builder.create_edge(memory_node, chain_node)

# 4. Validate (no cycles)
graph = build_graph_from_flowdata(nodes, edges)
assert not graph.detect_all_cycles()

# 5. Apply layout
nodes = apply_hierarchical_layout(nodes, edges)

# 6. Save
chatflow = {
    "name": "Chat With Memory",
    "flowData": json.dumps({"nodes": nodes, "edges": edges}),
    "type": "CHATFLOW",
    "deployed": False
}
```

---

## Examples

See `flows/` directory for example configs:

**Simple Chat** (`flows/simple_chat.yaml`)
- ChatOpenAI → ConversationChain

**Chat with Memory** (`flows/chat_with_memory.yaml`)
- ChatOpenAI + BufferMemory → ConversationChain

**RAG Q&A** (`flows/rag_flow.yaml`)
- ChatOpenAI + DocumentStore → RetrievalQAChain

Push any example:
```bash
python3 push_flow.py --config flows/simple_chat.yaml
```

---

## Directory Structure

```
examples/
├── push_flow.py                  # 🚀 AUTO-PUSH SCRIPT (main tool)
├── create_example_flows.py       # Generator for local files
├── node_templates/               # 39 real Flowise templates
│   ├── chatOpenAI.json
│   ├── bufferMemory.json
│   ├── conversationChain.json
│   └── ... (36 more)
├── flows/                        # 📝 Simple YAML configs
│   ├── simple_chat.yaml
│   ├── chat_with_memory.yaml
│   ├── rag_flow.yaml
│   └── README.md
└── generated_flows/              # Local JSON files (optional)
    ├── simple_chat.json
    ├── chat_with_memory.json
    └── ...
```

---

## Key Features

✅ **Automatic 2-Phase Push** - Creates and fixes references automatically
✅ **Simple YAML Configs** - Just describe nodes and connections
✅ **Real Templates** - 39 templates from working Flowise instance
✅ **Unique IDs** - Follows Flowise pattern (`name_0`, `name_1`, etc.)
✅ **Cycle Detection** - Validates graph structure
✅ **Hierarchical Layout** - Automatic node positioning
✅ **Type-Safe Connections** - Proper anchor IDs and handles
✅ **CLI Mode** - No config file needed
✅ **Production-Ready** - Fully configured chatflows

## What You Specify vs What Script Does

**You specify** (3 lines of YAML):
```yaml
nodes:
  - template: "chatOpenAI"
  - template: "conversationChain"
edges:
  - from: 0
    to: 1
```

**Script does** (automatically):
- Loads templates with 50+ fields each
- Generates unique node IDs
- Creates proper edge handles
- Validates graph structure
- Applies layout positioning
- Phase 1: Creates in Flowise
- Phase 2: Fixes all `{{nodeId.data.instance}}` references
- Returns ready chatflow ID

**Total time**: ~0.5 seconds

---

## Related Documentation

- **Graph Utilities**: `../src/fluent_mind_mcp/utils/graph.py`
- **Layout Algorithm**: `../src/fluent_mind_mcp/utils/layout.py`
- **Connection Logic**: `../docs/flowise-node-connection-logic.md`

---

**Last Updated**: 2025-10-17
