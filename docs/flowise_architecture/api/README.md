# Programmatic Flow Creation Guide

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

Complete documentation for creating and managing Flowise chatflows via API.

## Quick Start

```javascript
// 1. Create flow structure
const flowData = {
  nodes: [{
    id: "chatOpenAI_0",
    type: "customNode",
    position: { x: 100, y: 100 },
    data: {
      id: "chatOpenAI_0",
      name: "chatOpenAI",
      inputs: { modelName: "gpt-4o-mini" }
    }
  }],
  edges: [],
  viewport: { x: 0, y: 0, zoom: 1 }
};

// 2. Create via API
const response = await fetch('http://localhost:3000/api/v1/chatflows', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    name: "My Flow",
    flowData: JSON.stringify(flowData),
    type: "CHATFLOW"
  })
});
```

## Documentation Files

### Core API & Structure
- **[01-creating-flows-api.md](01-creating-flows-api.md)** - REST endpoints, request/response, authentication, flow types
- **[02-node-structure.md](02-node-structure.md)** - Node anatomy, IDs, anchors, baseClasses
- **[07-connecting-nodes.md](07-connecting-nodes.md)** - Edge structure, handles, type compatibility

### Node References
- **[03-nodes-llm.md](03-nodes-llm.md)** - Chat models (OpenAI, Anthropic, Ollama), prompts
- **[04-nodes-agents.md](04-nodes-agents.md)** - Memory, chains, agents, tools
- **[05-nodes-rag.md](05-nodes-rag.md)** - Document loaders, splitters, embeddings, vector stores
- **[06-nodes-overview.md](06-nodes-overview.md)** - Quick reference for all node types

### Examples & Patterns
- **[08-flow-examples.md](08-flow-examples.md)** - Complete working examples, helper functions, validation
- **[12-canvas-complete-example.md](12-canvas-complete-example.md)** - Full LLM chain with visual layout

### Canvas & Visual Layout
- **[09-canvas-overview.md](09-canvas-overview.md)** - Visual properties, positioning basics
- **[10-canvas-positioning.md](10-canvas-positioning.md)** - Layout algorithms, auto-positioning
- **[11-canvas-patterns.md](11-canvas-patterns.md)** - Common visual patterns, best practices

## Learning Paths

**Quick Start** (15 min): `01 → 08`
**Complete** (60 min): `01 → 02 → 03/04/05 → 07 → 08`
**Visual Focus** (30 min): `02 → 09 → 10 → 12`

## Key Concepts

**Flow**: `{ nodes: [], edges: [], viewport: {...} }` - Complete chatflow structure
**Node**: Building block with `id`, `data.name`, `inputs`, `baseClasses`, `anchors`
**Edge**: Connection with `source`, `target`, `sourceHandle`, `targetHandle`
**Type Compatibility**: Source baseClasses must include target input type

## CRUD Operations

```javascript
// CREATE
POST /api/v1/chatflows { name, flowData, type }

// READ
GET /api/v1/chatflows/:id
GET /api/v1/chatflows (list all)

// UPDATE
PUT /api/v1/chatflows/:id { name, flowData, deployed }

// DELETE
DELETE /api/v1/chatflows/:id
```

## Additional Resources

**Architecture**: [../01-overview.md](../01-overview.md), [../02-monorepo-structure.md](../02-monorepo-structure.md)
**Node Specs**: [../nodes/README.md](../nodes/README.md) - Detailed specs for 303+ nodes
**Source Code**: `/packages/components/nodes/` - Node implementations
**Examples**: `/packages/server/marketplaces/chatflows/` - Official flow examples

## License

Apache 2.0 - Part of the Flowise project
