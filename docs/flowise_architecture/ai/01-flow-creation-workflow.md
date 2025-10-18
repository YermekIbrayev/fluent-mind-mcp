# AI Flow Creation Workflow

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

## High-Level Stages

```
API Request → Parse FlowData → Build Graph → Execute Flow → Return Result
```

## 1. API Entry Point

**Location**: `buildChatflow.ts:executeChatflow()`

```http
POST /api/v1/prediction/:id
{ "question": "User input", "history": [...], "uploads": [...] }
```

**Steps**: Load chatflow → Extract flowData → Parse nodes/edges → Validate type

## 2. Graph Construction

**Location**: `index.ts:constructGraphs():155`

```typescript
const { graph, nodeDependencies } = constructGraphs(nodes, edges)

// Adjacency list + dependency count
graph = { "node_1": ["node_2"], "node_2": [], ... }
nodeDependencies = { "node_1": 0, "node_2": 1, ... }
```

**Types**: Forward (execution), Reversed (dependencies), Non-Directed (connectivity)

## 3. Node Identification

### Ending Nodes (`index.ts:295`)
- No outgoing edges: `graph[nodeId].length === 0`
- Has incoming edges: `nodeDependencies[nodeId] > 0`
- Marked as: `outputs.output === 'EndingNode'`

### Starting Nodes (`index.ts:230`)
- Walk backwards from ending node
- Calculate depth queue
- Starting nodes have `depth === 0`

## 4. Flow Execution (BFS)

**Location**: `index.ts:buildFlow():516`

```typescript
// Initialize queue
for (const nodeId of startingNodeIds) {
  nodeQueue.push({ nodeId, depth: 0 })
}

// Process queue
while (nodeQueue.length) {
  const { nodeId, depth } = nodeQueue.shift()

  // Load & execute node
  const nodeInstance = new nodeModule.nodeClass()
  const nodeData = await resolveVariables(...)
  const result = await nodeInstance.init(nodeData, question)

  // Store & queue neighbors
  flowNodes[index].data.instance = result
  graph[nodeId].forEach(neighborId =>
    nodeQueue.push({ nodeId: neighborId, depth: depth + 1 })
  )
}
```

**Features**: Depth tracking, loop protection (max 3), conditional routing

## 5. Special Nodes

### If/Else Conditional
```typescript
if (nodeType === 'ifElseFunction') {
  const branch = result.type ? 'returnTrue' : 'returnFalse'
  ignoreNodeIds.push(unusedBranch)
}
```

### Set Variable
```typescript
if (nodeType === 'setVariable') {
  dynamicVariables[key] = result.dynamicVariables[key]
}
```

### Vector Upsert
```typescript
if (isUpsert && nodeId === stopNodeId) {
  await nodeInstance.vectorStoreMethods.upsert(nodeData)
  break
}
```

## 6. Variable Resolution

**Location**: `index.ts:resolveVariables():380`

**Priority** (highest first):
1. Variable Overrides (API)
2. Dynamic Variables (runtime)
3. Database Variables (static)
4. System Variables ({{question}}, {{chat_history}})
5. Node References ({{nodeId.data.instance}})

**System Variables**:
- `{{question}}`, `{{chat_history}}`, `{{current_date_time}}`
- `{{file_attachment}}`, `{{runtime_messages_length}}`, `{{loop_count}}`

## 7. Result Collection

```typescript
const endingNode = flowNodes.find(n => n.id === endingNodeId)
const result = endingNode.data.instance

if (isStreaming) {
  for await (chunk of result) sseStreamer.streamToken(chunk)
} else {
  return { text: result }
}
```

## ChatFlow vs AgentFlow

| Type | Execution | Control | Nodes |
|------|-----------|---------|-------|
| ChatFlow | buildFlow() + BFS | Graph-based | Chains, LLMs, Memory |
| AgentFlow | buildAgentGraph() | Agent decisions | Agent nodes + tools |

## Performance

- **Complexity**: O(V + E) for graph build and BFS
- **Loop Protection**: Max 3 iterations per node
- **Parallelization**: Same-depth nodes can run concurrently
- **Optimizations**: Graph caching, component pool, abort controllers

## File References

- `buildChatflow.ts` - Main orchestrator
- `index.ts:155` - constructGraphs()
- `index.ts:230` - getStartingNodes()
- `index.ts:295` - getEndingNodes()
- `index.ts:516` - buildFlow()
- `buildAgentflow.ts` - Agent execution

**All paths**: `packages/server/src/utils/`
