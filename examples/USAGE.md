# How to Use the Flowise Chatflow System

**TL;DR**: Just write a simple YAML, run one command, get working chatflow.

---

## The Easiest Way

### 1. Create a YAML file

`my_awesome_bot.yaml`:
```yaml
name: "My Awesome Bot"
deployed: false

spec:
  nodes:
    - template: "chatOpenAI"
      inputs:
        modelName: "gpt-4o-mini"

    - template: "conversationChain"
      inputs: {}

  edges:
    - from: 0
      to: 1
```

### 2. Run ONE command

```bash
python3 push_flow.py --config my_awesome_bot.yaml
```

### 3. Done!

You get:
- ✅ Fully configured chatflow in Flowise
- ✅ All node references fixed automatically
- ✅ Ready to test and deploy
- ✅ Takes ~0.5 seconds

---

## Available Templates

**39 templates** in `node_templates/`:

**LLMs**:
- `chatOpenAI` - OpenAI models (GPT-4, GPT-3.5)
- `chatAnthropic` - Claude models
- `chatLocalAI` - Local LLMs

**Memory**:
- `bufferMemory` - Full conversation history
- `bufferWindowMemory` - Last N messages only

**Chains**:
- `conversationChain` - Basic chat
- `conversationalRetrievalQAChain` - RAG/Q&A

**Tools**:
- `currentDateTime` - Get current time
- `googleCalendarTool` - Calendar access
- `retrieverTool` - Document retrieval

**Storage**:
- `documentStore` - Document management
- `memoryVectorStore` - In-memory vectors
- `faiss` - FAISS vector store

**And 25+ more!**

---

## Common Patterns

### Pattern 1: Simple Chat

```yaml
nodes:
  - template: "chatOpenAI"
  - template: "conversationChain"
edges:
  - {from: 0, to: 1}
```

Result: `ChatOpenAI → ConversationChain`

### Pattern 2: Chat with Memory

```yaml
nodes:
  - template: "chatOpenAI"
  - template: "bufferMemory"
  - template: "conversationChain"
edges:
  - {from: 0, to: 2}  # LLM → Chain
  - {from: 1, to: 2}  # Memory → Chain
```

Result:
```
ChatOpenAI ──┐
             ├──> ConversationChain
BufferMemory ┘
```

### Pattern 3: RAG Q&A

```yaml
nodes:
  - template: "chatOpenAI"
  - template: "documentStore"
  - template: "conversationalRetrievalQAChain"
edges:
  - {from: 0, to: 2}  # LLM → Chain
  - {from: 1, to: 2}  # Docs → Chain
```

Result:
```
ChatOpenAI ────┐
               ├──> RetrievalQAChain
DocumentStore ─┘
```

---

## CLI Mode (No Config File)

Don't want to create a file? Use CLI:

```bash
# Simple 2-node
python3 push_flow.py \
  --name "Quick Bot" \
  --nodes "chatOpenAI,conversationChain" \
  --edges "0-1"

# 3-node with memory
python3 push_flow.py \
  --name "Bot With Memory" \
  --nodes "chatOpenAI,bufferMemory,conversationChain" \
  --edges "0-2,1-2"

# Deploy immediately
python3 push_flow.py \
  --config my_bot.yaml \
  --deploy
```

---

## What Happens Automatically

When you run `push_flow.py`, it automatically:

### 1. Loads Templates (0.1s)
- Reads 39 node templates from `node_templates/`
- Each template has 50+ fields (metadata, anchors, params, etc.)

### 2. Builds Flow (0.1s)
- Creates nodes from templates
- Generates unique IDs (`chatOpenAI_0`, `conversationChain_1`, etc.)
- Creates edges with proper source/target handles
- Validates graph (no cycles)
- Applies hierarchical layout

### 3. Phase 1: Create (0.2s)
- Pushes to Flowise API
- Flowise assigns chatflow ID
- Nodes and edges created

### 4. Phase 2: Fix (0.2s)
- Fetches created chatflow
- Analyzes edge connections
- Updates all `{{nodeId.data.instance}}` references
- Clears optional unused inputs
- Pushes updated flowData

### 5. Done! (0.5s total)
- Returns chatflow ID
- Chatflow ready to use

---

## Example Session

```bash
$ python3 push_flow.py --config flows/simple_chat.yaml

✅ Loaded 39 node templates

🔨 Building flow: Simple Chat
   ✅ Built: 2 nodes, 1 edges

📤 Phase 1: Creating chatflow...
   ✅ Created: 4ffa09ef-491b-4ec6-9fed-66659b6e3610

🔧 Phase 2: Fixing node references...
   ✅ Fixed 1 node references

✅ Success! Chatflow ID: 4ffa09ef-491b-4ec6-9fed-66659b6e3610

🎉 Done! Chatflow ID: 4ffa09ef-491b-4ec6-9fed-66659b6e3610
```

**That's it!** Go to Flowise UI and your chatflow is ready.

---

## Customizing Node Inputs

You can set any node-specific inputs:

```yaml
nodes:
  - template: "chatOpenAI"
    inputs:
      modelName: "gpt-4o-mini"      # Model name
      temperature: 0.7              # Temperature
      maxTokens: 2000               # Max tokens
      streaming: true               # Enable streaming

  - template: "bufferMemory"
    inputs:
      memoryKey: "chat_history"     # Memory key
      sessionId: "user-123"         # Session ID

  - template: "conversationChain"
    inputs:
      systemMessagePrompt: "You are a helpful assistant."
```

**Empty inputs** (`inputs: {}`) use template defaults.

---

## Automatic Type Matching

The script automatically matches output types to compatible input anchors:

```yaml
# Example: ConversationChain has 2 input anchors
#   - anchor 0: model (BaseChatModel)
#   - anchor 1: memory (BaseMemory)

nodes:
  - template: "chatOpenAI"      # Outputs: BaseChatModel
  - template: "bufferMemory"    # Outputs: BaseMemory
  - template: "conversationChain"

edges:
  - from: 0  # chatOpenAI -> conversationChain
    to: 2    # Automatically connects to anchor 0 (model)

  - from: 1  # bufferMemory -> conversationChain
    to: 2    # Automatically connects to anchor 1 (memory)
```

**No need to specify anchor indices** - the script matches types automatically!

## Advanced: Manual Anchor Selection

If needed, you can manually specify anchors:

```yaml
edges:
  - from: 0
    to: 2
    source_anchor: 0  # First output anchor
    target_anchor: 0  # First input anchor

  - from: 1
    to: 2
    source_anchor: 0
    target_anchor: 1  # Second input anchor
```

But most of the time, automatic matching works perfectly.

---

## Troubleshooting

### "Template not found"
- Check template name in `node_templates/`
- Template names are exact (case-sensitive)
- Use `ls node_templates/` to see available templates

### "Flow contains cycles"
- Your edges create a loop
- Check that flow is directed acyclic (DAG)
- Use `from` < `to` for simple flows

### "Connection failed"
- Check `FLOWISE_API_URL` and `FLOWISE_API_KEY` in `.env`
- Verify Flowise instance is running
- Test: `curl $FLOWISE_API_URL/api/v1/chatflows`

---

## Pro Tips

### Tip 1: Start with Examples

```bash
# Try the examples first
python3 push_flow.py --config flows/simple_chat.yaml
python3 push_flow.py --config flows/chat_with_memory.yaml
python3 push_flow.py --config flows/rag_flow.yaml
```

### Tip 2: Use CLI for Quick Tests

```bash
# Test a 2-node flow in one command
python3 push_flow.py --name "Test" --nodes "chatOpenAI,conversationChain" --edges "0-1"
```

### Tip 3: Check Generated Files

```bash
# Generate local files first to inspect
python3 create_example_flows.py

# Then check generated_flows/ to see the structure
```

### Tip 4: Add Your Own Templates

1. Extract node from Flowise UI (export chatflow)
2. Copy node JSON to `node_templates/mynode.json`
3. Use in config: `template: "mynode"`

---

## What Makes This Different

**Before** (manual):
1. Create nodes in UI
2. Connect edges
3. Configure each node
4. Fix variable references manually
5. Test and debug
**Time**: 15+ minutes per flow

**After** (automated):
1. Write 10-line YAML
2. Run one command
**Time**: 0.5 seconds

---

## Summary

**You provide**:
- Chatflow name
- List of templates
- Connections (edges)
- Optional: node inputs

**Script does**:
- Template loading (50+ fields each)
- ID generation
- Edge creation
- Cycle validation
- Layout positioning
- Phase 1 (create)
- Phase 2 (fix references)
- Returns chatflow ID

**Result**: Production-ready chatflow in Flowise!

---

**Questions?** See `flows/README.md` for more examples.
