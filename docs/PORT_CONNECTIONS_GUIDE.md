# Flowise Port Connections Guide

**WHY**: Understanding how nodes connect via ports (anchors) is critical for building working chatflows.

## The Problem

When creating chatflows, connectors must attach to **specific ports (anchors)** on nodes, not just to nodes themselves. If edge handles don't match anchor IDs, connections appear but don't work.

## How Port Connections Work

### 1. Every Node Has Anchors (Ports)

Nodes have two types of anchors:
- **Input Anchors**: Ports where data comes IN
- **Output Anchors**: Ports where data goes OUT

### 2. Anchor Structure

Each anchor has:
```json
{
  "id": "nodeId-input|output-anchorName-AllowedTypes",
  "name": "anchorName",
  "label": "Display Label",
  "type": "AllowedType1 | AllowedType2 | ..."
}
```

### 3. Edge Structure

Edges connect anchors using handles:
```json
{
  "id": "edge_1",
  "source": "sourceNodeId",
  "target": "targetNodeId",
  "sourceHandle": "sourceNodeId-output-anchorName-Types",
  "targetHandle": "targetNodeId-input-anchorName-Types"
}
```

## Real Working Example

From ChatGPT Clone flow:

### Node: chatLocalAI_0 (LLM)

**Output Anchor:**
```json
{
  "id": "chatLocalAI_0-output-chatLocalAI-ChatLocalAI|BaseChatModel|BaseChatOpenAI|BaseChatModel|BaseLanguageModel|Runnable",
  "name": "chatLocalAI",
  "type": "ChatLocalAI | BaseChatModel | BaseChatOpenAI | BaseChatModel | BaseLanguageModel | Runnable"
}
```

### Node: conversationChain_0 (Chain)

**Input Anchor:**
```json
{
  "id": "conversationChain_0-input-model-BaseChatModel",
  "name": "model",
  "type": "BaseChatModel"
}
```

### Edge Connecting Them

```json
{
  "source": "chatLocalAI_0",
  "target": "conversationChain_0",
  "sourceHandle": "chatLocalAI_0-output-chatLocalAI-ChatLocalAI|BaseChatModel|BaseChatOpenAI|BaseChatModel|BaseLanguageModel|Runnable",
  "targetHandle": "conversationChain_0-input-model-BaseChatModel"
}
```

**WHY THIS WORKS:**
- `sourceHandle` exactly matches the output anchor ID
- `targetHandle` exactly matches the input anchor ID
- Types are compatible: output includes `BaseChatModel` which input accepts

## Type Compatibility

Output and input types must be compatible:

**Output Types**: `ChatLocalAI | BaseChatModel | BaseChatOpenAI | ...`
**Input Type**: `BaseChatModel`

✓ Compatible because `BaseChatModel` is in the output types.

## Common Mistakes

### ❌ Wrong: Connecting to Node Instead of Port
```json
{
  "source": "llm_node",
  "target": "chain_node"
  // Missing sourceHandle and targetHandle
}
```

### ❌ Wrong: Handle Doesn't Match Anchor ID
```json
{
  "sourceHandle": "llm_node-output-model-BaseChatModel",  // WRONG
  // Actual anchor: "llm_node-output-chatOpenAI-ChatOpenAI|BaseChatModel"
}
```

### ✅ Correct: Exact Match
```json
{
  "source": "llm_node",
  "target": "chain_node",
  "sourceHandle": "llm_node-output-chatOpenAI-ChatOpenAI|BaseChatModel",
  "targetHandle": "chain_node-input-model-BaseChatModel"
}
```

## How to Build Connections Programmatically

### Step 1: Load Node Templates
```python
with open('chatOpenAI.json') as f:
    llm_template = json.load(f)

node = llm_template['node']
```

### Step 2: Update Node ID
```python
from node_builder import update_node_id

update_node_id(node, 'my_llm')
# All anchor IDs automatically updated:
# chatOpenAI_0-output-... → my_llm-output-...
```

### Step 3: Get Anchor IDs
```python
from node_builder import get_output_handle, get_input_handle

# Get output handle
source_handle = get_output_handle(llm_node, 'chatOpenAI')
# Returns: "my_llm-output-chatOpenAI-ChatOpenAI|BaseChatModel|..."

# Get input handle
target_handle = get_input_handle(chain_node, 'model')
# Returns: "chain_node-input-model-BaseChatModel"
```

### Step 4: Create Edge
```python
edge = {
    'id': 'edge_1',
    'source': 'my_llm',
    'target': 'chain_node',
    'sourceHandle': source_handle,
    'targetHandle': target_handle
}
```

## Helper Functions Reference

Located in: `examples/node_templates/node_builder.py`

### update_node_id(node, new_id)
Updates node ID and all anchor IDs automatically.

### get_output_handle(node, anchor_name=None)
Returns output anchor ID for edge `sourceHandle`.

### get_input_handle(node, anchor_name)
Returns input anchor ID for edge `targetHandle`.

### NodeBuilder.connect_via_reference()
High-level method that handles everything automatically.

## Working Examples

All working flows saved in: `examples/working_flows/`

**Simple flows to study:**
- `ChatGPT_Clone_88f4739b.json` (3 edges)
- `Simple_AI_QnA_Bot_(Template_Test_v2_-_Fi_d3077978.json` (2 edges)

**Complex flows:**
- `Python_Script_Creator_1c292e32.json` (10 edges)
- `Google_Calendar_edfd6c70.json` (6 edges)

## Verification Checklist

✓ Each edge has `sourceHandle` and `targetHandle`
✓ `sourceHandle` matches an output anchor ID in source node
✓ `targetHandle` matches an input anchor ID in target node
✓ Output anchor type includes at least one type accepted by input anchor
✓ When changing node IDs, all anchor IDs are also updated

## Summary

**KEY RULE**: Edges connect ANCHORS (ports), not nodes. The `sourceHandle` and `targetHandle` must exactly match the `id` fields in the node's `outputAnchors` and `inputAnchors` arrays.

**ANCHOR ID FORMAT**:
```
{nodeId}-{input|output}-{anchorName}-{Type1|Type2|...}
```

**USE HELPER FUNCTIONS**: Don't build handles manually. Use `get_output_handle()` and `get_input_handle()` from `node_builder.py`.
