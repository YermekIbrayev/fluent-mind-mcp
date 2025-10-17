# Flow Configurations

Simple YAML configs to push chatflows to Flowise.

---

## Quick Start

```bash
# Push a flow from config
python3 ../push_flow.py --config simple_chat.yaml

# Push with CLI
python3 ../push_flow.py --name "My Chat" --nodes "chatOpenAI,conversationChain" --edges "0-1"
```

---

## Config Format

```yaml
name: "Flow Name"
deployed: false  # true to deploy immediately

spec:
  nodes:
    - template: "chatOpenAI"       # Template name from node_templates/
      inputs:
        modelName: "gpt-4o-mini"   # Node-specific inputs
        temperature: 0.7

    - template: "conversationChain"
      inputs: {}

  edges:
    - from: 0  # Source node index
      to: 1    # Target node index
      # Automatic type matching - no need to specify anchors!
      # source_anchor: 0  # Optional: manual override
      # target_anchor: 0  # Optional: manual override
```

---

## Automatic Type Matching

**No need to worry about anchor indices!** The script automatically matches:

- **ChatOpenAI** (BaseChatModel) → **ConversationChain** anchor 0 (model)
- **BufferMemory** (BaseMemory) → **ConversationChain** anchor 1 (memory)

Example:
```yaml
nodes:
  - template: "chatOpenAI"
  - template: "bufferMemory"
  - template: "conversationChain"

edges:
  - from: 0  # Auto-connects to model anchor
    to: 2
  - from: 1  # Auto-connects to memory anchor
    to: 2
```

The script compares output types with input anchor types and finds the best match automatically.

---

## Available Templates

See `../node_templates/` for 39 available templates:

**LLMs**: chatOpenAI, chatAnthropic, chatLocalAI
**Memory**: bufferMemory, bufferWindowMemory
**Chains**: conversationChain, conversationalRetrievalQAChain
**Tools**: currentDateTime, googleCalendarTool, retrieverTool
**Storage**: documentStore, memoryVectorStore, faiss
**And more**: 30+ other templates

---

## Examples

### Simple Chat
```bash
python3 ../push_flow.py --config simple_chat.yaml
```

**What it creates**:
- ChatOpenAI (gpt-4o-mini) → ConversationChain

### Chat with Memory
```bash
python3 ../push_flow.py --config chat_with_memory.yaml
```

**What it creates**:
```
ChatOpenAI ──┐
             ├──> ConversationChain
BufferMemory ┘
```

### RAG Q&A
```bash
python3 ../push_flow.py --config rag_flow.yaml
```

**What it creates**:
```
ChatOpenAI ────┐
               ├──> RetrievalQAChain
DocumentStore ─┘
```

---

## CLI Mode

Don't need a config file? Use CLI:

```bash
# Simple 2-node flow
python3 ../push_flow.py \
  --name "Quick Chat" \
  --nodes "chatOpenAI,conversationChain" \
  --edges "0-1"

# 3-node flow with multiple inputs
python3 ../push_flow.py \
  --name "Chat With Memory" \
  --nodes "chatOpenAI,bufferMemory,conversationChain" \
  --edges "0-2,1-2"

# Deploy immediately
python3 ../push_flow.py \
  --config my_flow.yaml \
  --deploy
```

---

## How It Works

The script automatically handles the 2-phase push:

**Phase 1: Create**
- Loads node templates
- Generates unique node IDs
- Creates edges with proper handles
- Validates no cycles
- Applies hierarchical layout
- Pushes to Flowise

**Phase 2: Fix**
- Fetches created chatflow
- Analyzes edge connections
- Updates all `{{nodeId.data.instance}}` references
- Clears optional inputs with no edges
- Pushes updated flowData

**Result**: Fully configured chatflow ready to use!

---

## What You Specify

**You provide** (simple):
- Chatflow name
- List of node templates
- Connections between nodes
- Node input values

**Script handles** (complex):
- Loading templates
- Generating unique IDs
- Creating proper edge handles
- Cycle detection
- Layout positioning
- 2-phase push
- Reference fixing

---

## Custom Templates

Want to add your own template?

1. Extract node from Flowise UI
2. Save as `node_templates/mytemplate.json`
3. Use in config: `template: "mytemplate"`

---

**Last Updated**: 2025-10-17
