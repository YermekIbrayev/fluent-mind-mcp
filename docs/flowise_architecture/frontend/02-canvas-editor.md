# Canvas Editor

**Component**: `src/views/canvas/`
**Library**: ReactFlow

## Purpose

Visual flow builder for creating AI workflows by dragging and connecting nodes.

## Key Features

- Drag-and-drop nodes from palette
- Connect nodes with edges
- Configure node properties
- Validate connections
- Auto-layout
- Zoom/pan controls
- Minimap
- Undo/redo

## Node Structure

```javascript
{
  id: 'node_abc123',
  type: 'chatOpenAI',
  position: { x: 100, y: 200 },
  data: {
    label: 'ChatOpenAI',
    inputs: {
      modelName: 'gpt-4',
      temperature: 0.9
    },
    outputs: {},
    category: 'Chat Models'
  }
}
```

## Edge Structure

```javascript
{
  id: 'edge_abc123',
  source: 'node_abc123',
  target: 'node_def456',
  sourceHandle: 'output_0',
  targetHandle: 'input_0'
}
```

## Data Flow

1. User drags node from palette
2. Node added to ReactFlow state
3. User connects nodes
4. User configures node properties
5. On save: Flow JSON sent to backend
6. Backend stores in database

## Flow JSON Format

```json
{
  "nodes": [
    {
      "id": "node_1",
      "type": "chatOpenAI",
      "position": { "x": 100, "y": 100 },
      "data": { "inputs": {...} }
    }
  ],
  "edges": [
    {
      "source": "node_1",
      "target": "node_2"
    }
  ]
}
```

## Node Configuration Panel

Auto-generated form based on node metadata:
- String inputs → Text fields
- Number inputs → Number fields
- Boolean inputs → Checkboxes
- Options → Dropdowns
- Credential → Credential selector

## Connection Validation

Rules:
- Output baseClass must match input baseClass
- No circular connections
- Required inputs must be connected

## Canvas Controls

- Pan: Click and drag
- Zoom: Scroll wheel
- Select: Click node
- Multi-select: Ctrl/Cmd + Click
- Delete: Delete key
- Undo: Ctrl/Cmd + Z
- Redo: Ctrl/Cmd + Shift + Z

## Save Flow

```javascript
const handleSave = async () => {
  const flowData = {
    nodes: reactFlowInstance.getNodes(),
    edges: reactFlowInstance.getEdges()
  }

  await api.updateChatflow(id, {
    flowData: JSON.stringify(flowData)
  })
}
```
