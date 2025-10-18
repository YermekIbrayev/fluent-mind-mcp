# AI Flow Creation Documentation

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

Complete guide to understanding how Flowise AI creates, executes, and manages flows programmatically.

## Overview

Flowise executes AI flows using a **graph-based execution engine**:
- Builds directed acyclic graphs (DAG) from node definitions
- Traverses nodes in topological order using BFS
- Resolves variables and dependencies dynamically
- Handles streaming, memory, and conditional logic
- Supports ChatFlow and AgentFlow types

## Quick Flow Lifecycle

```
API Call → Load Flow → Parse JSON → Build Graph → Execute Nodes → Return Result
```

### 8-Step Execution Process

1. **API Entry**: POST /api/v1/prediction/:id
2. **Load Flow**: Fetch ChatFlow from database
3. **Parse FlowData**: Extract nodes[] + edges[]
4. **Build Graph**: constructGraphs() creates DAG
5. **Identify Nodes**: Find starting and ending nodes
6. **Execute Flow**: BFS traversal with buildFlow()
7. **Collect Result**: Get ending node output
8. **Stream/Return**: Send response to client

## Documentation Files

### [01-flow-creation-workflow.md](01-flow-creation-workflow.md)
**Complete workflow of AI flow execution**

- Graph construction algorithms
- Node identification (starting/ending)
- BFS traversal with depth tracking
- Special nodes (ifElse, setVariable, upsert)
- Variable resolution priority
- ChatFlow vs AgentFlow

**When to read**: Understanding execution lifecycle

### [02-graph-utilities.md](02-graph-utilities.md)
**Graph construction and traversal utilities**

- `constructGraphs()` - Build DAG
- `getStartingNodes()` - Find roots
- `getEndingNodes()` - Find outputs
- Graph types (forward, reversed, non-directed)

**When to read**: Graph algorithm details

### [03-variable-utilities.md](03-variable-utilities.md)
**Variable resolution and configuration**

- `resolveVariables()` - Resolve all variable types
- `replaceInputsWithConfig()` - Apply overrides
- Resolution priority order
- System variables reference

**When to read**: Variable handling logic

### [04-execution-utilities.md](04-execution-utilities.md)
**Flow execution and orchestration**

- `buildFlow()` - Core execution engine
- `executeChatflow()` - Main orchestrator
- Streaming utilities (SSEStreamer)
- Memory and validation utilities

**When to read**: Execution details

### [05-ai-agent-patterns.md](05-ai-agent-patterns.md)
**AI agent flow creation patterns**

- Direct creation (1-touch) - Known node types
- Discovery + creation (2-touch) - Dynamic discovery
- Type-safe node construction
- Pattern selection guide

**When to read**: Building AI agents that create flows

## Core Concepts

### Graph Structure
```typescript
// Flow: LLM → Chain → Output
{
  "llm_0": ["chain_0"],
  "chain_0": ["output_0"],
  "output_0": []
}
```

### Variable Priority (highest to lowest)
1. Variable Overrides (API)
2. Dynamic Variables (runtime)
3. Database Variables (static)
4. System Variables (built-in)
5. Node References (chain)

### Flow Types

**ChatFlow**: Graph-based traversal (buildChatflow)
**AgentFlow**: Agent decision-making (buildAgentGraph)

## Key Files Reference

- `packages/server/src/utils/buildChatflow.ts` - Main orchestrator
- `packages/server/src/utils/index.ts:155` - constructGraphs()
- `packages/server/src/utils/index.ts:230` - getStartingNodes()
- `packages/server/src/utils/index.ts:295` - getEndingNodes()
- `packages/server/src/utils/index.ts:516` - buildFlow()
- `packages/server/src/utils/buildAgentflow.ts` - Agent execution

## Common Patterns

**Simple Chain**: LLM → LLMChain → Output
**Agent**: LLM + Tools → Agent → Output
**Conditional**: Input → ifElse → BranchA/B → Output
**RAG**: VectorStore + LLM → RetrievalChain → Output

## Performance

- **Graph Build**: O(V + E) complexity
- **BFS Traversal**: O(V + E) per execution
- **Loop Protection**: Max 3 iterations per node
- **Parallelization**: Same-depth nodes can run concurrently

## Debugging

1. Enable debug logging: `LOG_LEVEL=debug`
2. Check: `Initializing ${nodeName} (${nodeId})`
3. Verify graph structure and dependencies
4. Trace variable resolution order
5. Monitor depth queue execution

## Related Documentation

- [../api/README.md](../api/README.md) - API endpoints
- [../backend/01-core-app.md](../backend/01-core-app.md) - Server architecture
- [../components/01-node-system.md](../components/01-node-system.md) - Node system

---

**Total Files**: 6 docs (~950 lines total)
- README.md: Overview (155 lines)
- 01-flow-creation-workflow.md: Workflow (154 lines)
- 02-graph-utilities.md: Graph utils (150 lines)
- 03-variable-utilities.md: Variable utils (150 lines)
- 04-execution-utilities.md: Execution utils (150 lines)
- 05-ai-agent-patterns.md: AI patterns (197 lines)
