# Connect Nodes Tool

**MCP Tool**: `connect_nodes`

**Purpose**: Programmatically connect two nodes in a Flowise chatflow with automatic beautiful layout.

---

## Overview

The `connect_nodes` tool enables AI assistants to:
1. **Connect nodes** by creating edges between output and input anchors
2. **Auto-layout nodes** using hierarchical algorithm to prevent overlaps
3. **Create professional diagrams** without manual UI positioning

---

## Usage

### Basic Connection

```python
result = await connect_nodes(
    chatflow_id="abc-123-def",
    source_node_id="chatOpenAI_0",
    target_node_id="conversationChain_0",
    auto_layout=True
)
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chatflow_id` | string | ✅ | Unique chatflow identifier |
| `source_node_id` | string | ✅ | ID of node providing output |
| `target_node_id` | string | ✅ | ID of node receiving input |
| `auto_layout` | boolean | ❌ | Apply automatic layout (default: `True`) |

---

## Return Value

```json
{
  "id": "chatflow-123",
  "name": "My Flow",
  "flowData": "{...}",
  "connection": {
    "source": "chatOpenAI_0",
    "target": "conversationChain_0",
    "edge_id": "chatOpenAI_0-output-conversationChain_0-input",
    "auto_layout_applied": true
  }
}
```

---

## Auto-Layout Algorithm

The hierarchical layout algorithm:

1. **Builds graph** from edges (adjacency list)
2. **Computes depth** for each node using BFS from source nodes
3. **Groups nodes** by depth (column)
4. **Positions nodes** with configurable spacing:
   - **Horizontal spacing**: 400px between columns
   - **Vertical spacing**: 250px between nodes
   - **Standard dimensions**: 300×600px per node

### Layout Example

```
Column 0        Column 1        Column 2
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Start   │───→│ LLM     │───→│ Agent   │
└─────────┘    └─────────┘    └─────────┘

               ┌─────────┐    ┌─────────┐
               │ Memory  │───→│ Chain   │
               └─────────┘    └─────────┘
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `NotFoundError` | Chatflow or node doesn't exist | Verify IDs with `list_chatflows` |
| `ValidationError` | No compatible anchors | Check node types are compatible |
| `ValidationError` | Edge already exists | Connection already made |
| `ConnectionError` | Flowise unreachable | Check Flowise is running |

---

## Examples

### Example 1: Build Simple Flow

```python
# Step 1: Create chatflow with 2 disconnected nodes
flow_data = {
    "nodes": [
        {"id": "llm_0", "type": "chatOpenAI", ...},
        {"id": "agent_1", "type": "toolAgent", ...}
    ],
    "edges": []
}

chatflow = await create_chatflow(
    name="Simple Flow",
    flow_data=json.dumps(flow_data)
)

# Step 2: Connect nodes
result = await connect_nodes(
    chatflow_id=chatflow["id"],
    source_node_id="llm_0",
    target_node_id="agent_1",
    auto_layout=True
)

print(f"Connected: {result['connection']['edge_id']}")
```

### Example 2: Build Complex Multi-Node Flow

```python
# Connect multiple nodes in sequence
nodes = [
    ("start_0", "llm_1"),
    ("llm_1", "memory_2"),
    ("memory_2", "agent_3"),
    ("agent_3", "output_4")
]

for source, target in nodes:
    await connect_nodes(
        chatflow_id=chatflow_id,
        source_node_id=source,
        target_node_id=target,
        auto_layout=True  # Applied after each connection
    )
```

### Example 3: Manual Layout (No Auto-Layout)

```python
# Disable auto-layout to preserve manual positioning
result = await connect_nodes(
    chatflow_id=chatflow_id,
    source_node_id="llm_0",
    target_node_id="agent_1",
    auto_layout=False  # Keep existing node positions
)
```

---

## Technical Details

### Anchor Matching

The tool automatically finds compatible anchors:

1. **Extracts output anchors** from source node
2. **Extracts input anchors** from target node
3. **Uses first compatible pair** (can be enhanced to match by type)

### Edge Format

Created edges follow Flowise structure:

```json
{
  "id": "source-sourceHandle-target-targetHandle",
  "source": "chatOpenAI_0",
  "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI",
  "target": "agent_1",
  "targetHandle": "agent_1-input-model-BaseChatModel",
  "type": "buttonedge"
}
```

---

## Integration with Other Tools

### Workflow: Build Complete Flow

```python
# 1. Generate AgentFlow structure
generated = await generate_agentflow_v2(
    description="Research agent with web search"
)

# 2. Create chatflow
chatflow = await create_chatflow(
    name=generated["name"],
    flow_data=generated["flowData"],
    type="AGENTFLOW"
)

# 3. Add custom nodes and connect them
# (nodes created via separate tool)
await connect_nodes(
    chatflow_id=chatflow["id"],
    source_node_id="custom_node_5",
    target_node_id="existing_node_2"
)

# 4. Deploy
await deploy_chatflow(
    chatflow_id=chatflow["id"],
    deployed=True
)
```

---

## Performance

- **Typical execution**: 2-5 seconds
- **Maximum timeout**: 10 seconds
- **Layout computation**: O(N + E) where N=nodes, E=edges
- **API calls**: 2 (get chatflow, update chatflow)

---

## Future Enhancements

Potential improvements:

1. **Smart anchor matching** by type compatibility
2. **Multiple layout algorithms** (force-directed, circular, tree)
3. **Bulk connect** operation (connect multiple pairs at once)
4. **Layout presets** (compact, spacious, presentation)
5. **Edge styling** options (color, line style, labels)

---

## See Also

- [Generate AgentFlow V2](../specs/001-flowise-mcp-server/contracts/generate-agentflow-v2.md)
- [Update Chatflow](../specs/001-flowise-mcp-server/contracts/update-chatflow.md)
- [Layout Utilities](../src/fluent_mind_mcp/utils/layout.py)
