# Canvas Positioning Basics

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Critical Concept

**Visual properties control canvas rendering but NOT execution order.**
Execution order is determined by edges (graph topology) via BFS traversal.

## Required Visual Properties

```javascript
{
  "id": "chatOpenAI_0",                    // Must match data.id
  "type": "customNode",                    // "customNode" or "stickyNote"
  "width": 300,                            // Fixed (all nodes)
  "height": 670,                           // Auto-calculated or specified
  "position": { "x": 100, "y": 200 },     // Canvas coordinates
  "positionAbsolute": { "x": 100, "y": 200 }, // Same for flat flows
  "selected": false,                       // UI state
  "dragging": false,                       // UI state
  "data": { /* node config */ }
}
```

## Node Types

| Type | Usage | Typical Height |
|------|-------|----------------|
| `customNode` | Functional nodes | 400-670px |
| `stickyNote` | Annotations | ~163px |

## Dimensions

**Width**: Always 300px (fixed)

**Height** (auto-calculated):
- Chat Models: ~670px
- Prompts: ~513px
- Chains: ~508px
- Tools: ~400-600px
- Sticky Notes: ~163px

## Position Coordinates

```javascript
{
  "position": {
    "x": 175.23,    // Pixels from left edge
    "y": 101.11     // Pixels from top edge
  },
  "positionAbsolute": {
    "x": 175.23,    // Same as position.x (for flat flows)
    "y": 101.11     // Same as position.y
  }
}
```

**Key Points:**
- Origin (0,0) is top-left
- Positive X → right, positive Y → down
- `positionAbsolute` = `position` for standard flows
- Decimals allowed

## State Properties

```javascript
{
  "selected": false,    // Node selected in UI
  "dragging": false     // Node being dragged
}
```

Always `false` when creating programmatically.

## Viewport Settings

```javascript
{
  "viewport": {
    "x": 0,        // Pan offset X
    "y": 0,        // Pan offset Y
    "zoom": 1      // Zoom level (1 = 100%)
  }
}
```

**Common Zoom Levels:**
- `1.0` - Default (100%)
- `0.75` - Zoom out (larger flows)
- `0.5` - Overview
- `1.25` - Zoom in (editing)

## Spacing Recommendations

**Horizontal**: 250-400px between nodes
**Vertical**: 50-150px for stacked nodes

```javascript
// Horizontal layout
[Node 0: x=100] --350px--> [Node 1: x=450] --350px--> [Node 2: x=800]

// Vertical layout
[Node 0: y=100]
      ↓ 150px
[Node 1: y=250]
      ↓ 150px
[Node 2: y=400]
```

## Sticky Notes

```javascript
{
  "id": "stickyNote_0",
  "type": "stickyNote",
  "width": 300,
  "height": 163,
  "position": { "x": 900, "y": 59 },
  "positionAbsolute": { "x": 900, "y": 59 },
  "data": {
    "id": "stickyNote_0",
    "name": "stickyNote",
    "inputs": { "note": "Documentation text" }
  }
}
```

**Placement**: Above nodes (explain section), right side (general notes), or near complex connections.

## Quick Position Helpers

### Horizontal Line
```javascript
nodes.map((n, i) => ({
  ...n,
  position: { x: 100 + (i * 350), y: 200 },
  positionAbsolute: { x: 100 + (i * 350), y: 200 }
}));
```

### Vertical Line
```javascript
nodes.map((n, i) => ({
  ...n,
  position: { x: 400, y: 100 + (i * 150) },
  positionAbsolute: { x: 400, y: 100 + (i * 150) }
}));
```

### Grid
```javascript
nodes.map((n, i) => {
  const col = i % 3;
  const row = Math.floor(i / 3);
  return {
    ...n,
    position: { x: 100 + (col * 350), y: 100 + (row * 150) },
    positionAbsolute: { x: 100 + (col * 350), y: 100 + (row * 150) }
  };
});
```

## See Also

- [11-canvas-patterns.md](11-canvas-patterns.md) - Layout patterns
- [12-canvas-complete-example.md](12-canvas-complete-example.md) - Full example
- [02-node-structure.md](02-node-structure.md) - Node anatomy
