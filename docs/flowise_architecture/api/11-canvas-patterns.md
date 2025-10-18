# Canvas Layout Patterns

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Pattern 1: Linear Chain (Sequential)

**Use Case**: Data processing pipelines, document indexing

```javascript
const nodes = [
  { id: "loader_0", position: { x: 100, y: 300 } },
  { id: "splitter_0", position: { x: 450, y: 300 } },
  { id: "embeddings_0", position: { x: 800, y: 300 } },
  { id: "vectorstore_0", position: { x: 1150, y: 300 } }
];
```

**Visual**: `[Loader] → [Splitter] → [Embeddings] → [VectorStore]`

## Pattern 2: Fan-In (Multiple → One)

**Use Case**: Chains with multiple inputs, agents with memory and model

```javascript
const nodes = [
  // Sources (left column)
  { id: "llm_0", position: { x: 100, y: 100 } },
  { id: "prompt_0", position: { x: 100, y: 400 } },
  { id: "memory_0", position: { x: 100, y: 700 } },

  // Target (right column, centered)
  { id: "chain_0", position: { x: 500, y: 400 } }
];
```

**Visual**:
```
[LLM]      ↘
[Prompt]   → [Chain]
[Memory]   ↗
```

## Pattern 3: Fan-Out (One → Multiple)

**Use Case**: Shared resources, multiple consumers

```javascript
const nodes = [
  // Source (left)
  { id: "vectorstore_0", position: { x: 100, y: 400 } },

  // Targets (right column)
  { id: "retriever_0", position: { x: 500, y: 100 } },
  { id: "chain_0", position: { x: 500, y: 400 } },
  { id: "agent_0", position: { x: 500, y: 700 } }
];
```

**Visual**:
```
                ↗ [Retriever]
[VectorStore]  → [Chain]
                ↘ [Agent]
```

## Pattern 4: Agent with Tools

**Use Case**: Conversational agents with multiple tools

```javascript
const nodes = [
  // Tools (left)
  { id: "calc_0", position: { x: 100, y: 100 } },
  { id: "search_0", position: { x: 100, y: 400 } },
  { id: "browser_0", position: { x: 100, y: 700 } },

  // Agent components (middle)
  { id: "model_0", position: { x: 500, y: 250 } },
  { id: "memory_0", position: { x: 500, y: 550 } },

  // Agent (right)
  { id: "agent_0", position: { x: 900, y: 400 } }
];
```

## Pattern 5: RAG Pipeline

**Use Case**: Document Q&A, retrieval-augmented generation

```javascript
const nodes = [
  // Indexing (top row)
  { id: "pdf_0", position: { x: 100, y: 100 } },
  { id: "splitter_0", position: { x: 450, y: 100 } },
  { id: "embed_0", position: { x: 800, y: 100 } },
  { id: "pinecone_0", position: { x: 1150, y: 100 } },

  // Query (bottom row)
  { id: "retriever_0", position: { x: 1150, y: 500 } },
  { id: "model_0", position: { x: 800, y: 500 } },
  { id: "chain_0", position: { x: 450, y: 500 } }
];
```

## Best Practices

### 1. Consistent Spacing
```javascript
// ✓ Good
const GAP = 350;
nodes.forEach((n, i) => n.position.x = 100 + (i * GAP));

// ✗ Bad: Random spacing
```

### 2. Logical Flow Direction
```javascript
// ✓ Good: Left-to-right
// [Input] → [Process] → [Output]

// ✓ Good: Top-to-bottom
// [Config] ↓ [Process] ↓ [Output]

// ✗ Bad: Zigzag or backward
```

### 3. Group by Function
```javascript
// ✓ Good
// Data Loading:  x: 100-400
// Processing:    x: 500-800
// Output:        x: 900-1200
```

### 4. Align Nodes
```javascript
// ✓ Horizontal flow: Same Y
nodes.forEach(n => n.position.y = 300);

// ✓ Vertical flow: Same X
nodes.forEach(n => n.position.x = 400);
```

### 5. Visual Hierarchy
```javascript
// Main flow:     y: 400 (center)
// Supporting:    y: 100 (top)
// Annotations:   y: 50  (above)
```

## Common Layouts

### Two-Column (Source → Target)
```javascript
const leftColumn = { x: 100 };
const rightColumn = { x: 500 };
const verticalSpacing = 300;

sources.forEach((n, i) => {
  n.position = { x: leftColumn.x, y: 100 + (i * verticalSpacing) };
});
targets.forEach((n, i) => {
  n.position = { x: rightColumn.x, y: 100 + (i * verticalSpacing) };
});
```

### Three-Stage Pipeline
```javascript
const stages = [100, 500, 900]; // X positions
const centerY = 400;

stages.forEach((x, stageIdx) => {
  stageNodes[stageIdx].position = { x, y: centerY };
});
```

## See Also

- [10-canvas-positioning.md](10-canvas-positioning.md) - Position basics
- [12-canvas-complete-example.md](12-canvas-complete-example.md) - Full example
- [08-flow-examples.md](08-flow-examples.md) - API examples
