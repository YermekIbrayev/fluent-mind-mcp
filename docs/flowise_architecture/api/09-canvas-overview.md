# Canvas Visualization - Overview

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Important: Documentation Split

The canvas visualization documentation has been split into focused files (each ≤150 lines):

1. **[10-canvas-positioning.md](10-canvas-positioning.md)** - Position, dimensions, viewport
2. **[11-canvas-patterns.md](11-canvas-patterns.md)** - Common layout patterns
3. **[12-canvas-complete-example.md](12-canvas-complete-example.md)** - Full working example

## Quick Reference

### Visual vs Execution

**KEY CONCEPT**: Visual properties (position, width, height) control canvas rendering but DO NOT affect execution order.

Execution order is determined by edges (graph topology) using BFS traversal from starting nodes.

### Required Visual Properties

Every node needs:
- `id`: Unique identifier (must match data.id)
- `type`: "customNode" or "stickyNote"
- `width`: 300 (fixed for all nodes)
- `height`: Auto-calculated (400-670px typically)
- `position`: `{ x, y }` canvas coordinates
- `positionAbsolute`: Same as position for flat flows
- `selected`: false (UI state)
- `dragging`: false (UI state)
- `data`: Node configuration

### Spacing Guidelines

- **Horizontal**: 250-400px between nodes
- **Vertical**: 50-150px for stacked nodes

### Common Patterns

1. **Linear Chain**: `A → B → C → D` (sequential processing)
2. **Fan-In**: `A ↘ B → D` (multiple sources → one target)
           `C ↗`
3. **Fan-Out**: `A → B` (one source → multiple targets)
            `  → C`
4. **Agent**: Tools + Model + Memory → Agent
5. **RAG**: Documents → Processing → VectorStore → Retrieval → Generation

## Viewport

```javascript
{
  "viewport": {
    "x": 0,     // Pan offset
    "y": 0,     // Pan offset
    "zoom": 1   // 1 = 100%
  }
}
```

## Position Helpers

### Horizontal Layout
```javascript
nodes.map((n, i) => ({ ...n, position: { x: 100 + (i * 350), y: 200 }}));
```

### Vertical Layout
```javascript
nodes.map((n, i) => ({ ...n, position: { x: 400, y: 100 + (i * 150) }}));
```

### Grid Layout
```javascript
nodes.map((n, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  return { ...n, position: { x: 100 + (col * 350), y: 100 + (row * 150) }};
});
```

## Best Practices

1. **Consistent Spacing**: Use constants for gaps
2. **Logical Flow**: Left-to-right or top-to-bottom
3. **Group by Function**: Related nodes close together
4. **Align Nodes**: Same Y for horizontal, same X for vertical
5. **Visual Hierarchy**: Main flow center, supporting nodes around it

## Quick Start

```javascript
const flowData = {
  nodes: [
    {
      id: "node_0",
      type: "customNode",
      width: 300,
      position: { x: 100, y: 200 },
      positionAbsolute: { x: 100, y: 200 },
      data: { id: "node_0", name: "chatOpenAI", inputs: {...} }
    }
  ],
  edges: [],
  viewport: { x: 0, y: 0, zoom: 1 }
};
```

## Documentation Map

- **Basics**: [10-canvas-positioning.md](10-canvas-positioning.md)
- **Patterns**: [11-canvas-patterns.md](11-canvas-patterns.md)
- **Complete Example**: [12-canvas-complete-example.md](12-canvas-complete-example.md)
- **Node Structure**: [02-node-structure.md](02-node-structure.md)
- **Edges**: [07-connecting-nodes.md](07-connecting-nodes.md)
- **API**: [01-creating-flows-api.md](01-creating-flows-api.md)

## See Also

All three detailed canvas files for comprehensive guidance on positioning, layout patterns, and complete examples.
