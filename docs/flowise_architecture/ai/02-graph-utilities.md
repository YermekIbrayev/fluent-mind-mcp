# Graph Construction Utilities

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

## constructGraphs()

**Location**: `packages/server/src/utils/index.ts:155`

Builds directed graph from React Flow nodes and edges.

```typescript
function constructGraphs(
  reactFlowNodes: IReactFlowNode[],
  reactFlowEdges: IReactFlowEdge[],
  options?: { isNonDirected?: boolean; isReversed?: boolean }
): { graph: INodeDirectedGraph; nodeDependencies: INodeDependencies }
```

### Algorithm

```typescript
const graph = {}, nodeDependencies = {}

// Initialize
for (const node of nodes) {
  nodeDependencies[node.id] = 0
  graph[node.id] = []
}

// Build edges
if (isReversed) {
  for (const edge of edges) {
    graph[edge.target].push(edge.source)
    nodeDependencies[edge.target]++
  }
} else {
  for (const edge of edges) {
    graph[edge.source].push(edge.target)
    nodeDependencies[edge.target]++
  }
}
```

### Graph Types

- **Forward** (default): Source → Target (execution order)
- **Reversed** (`isReversed: true`): Target → Source (dependencies)
- **Non-Directed** (`isNonDirected: true`): Bidirectional (connectivity)

## getStartingNodes()

**Location**: `packages/server/src/utils/index.ts:230`

Identifies root nodes and calculates depth queue.

```typescript
function getStartingNodes(
  graph: INodeDirectedGraph,
  endNodeId: string
): { startingNodeIds: string[]; depthQueue: IDepthQueue }
```

### Algorithm

```typescript
// 1. Walk backwards from ending node
const depthQueue = { [endNodeId]: 0 }

function walkGraph(nodeId: string) {
  const depth = depthQueue[nodeId]
  graph[nodeId].forEach(parentId => {
    depthQueue[parentId] = Math.max(depthQueue[parentId] ?? 0, depth + 1)
    walkGraph(parentId)
  })
}
walkGraph(endNodeId)

// 2. Reverse depths (starting nodes = depth 0)
const maxDepth = Math.max(...Object.values(depthQueue))
for (const nodeId in depthQueue) {
  depthQueue[nodeId] = Math.abs(depthQueue[nodeId] - maxDepth)
}

// 3. Extract starting nodes
const startingNodeIds = Object.entries(depthQueue)
  .filter(([_, depth]) => depth === 0)
  .map(([id, _]) => id)
```

**Output**: `{ startingNodeIds: ["llm_0"], depthQueue: {"llm_0": 0, "chain_0": 1} }`

## getEndingNodes()

**Location**: `packages/server/src/utils/index.ts:295`

Identifies final output nodes.

```typescript
function getEndingNodes(
  nodeDependencies: INodeDependencies,
  graph: INodeDirectedGraph,
  allNodes: IReactFlowNode[]
): IReactFlowNode[]
```

### Logic

```typescript
// Find candidates
const endingNodeIds = Object.keys(graph).filter(nodeId =>
  graph[nodeId].length === 0 && nodeDependencies[nodeId] > 0
)

// Verify marked as EndingNode
const verified = allNodes.filter(node =>
  endingNodeIds.includes(node.id) &&
  node.data?.outputs?.output === 'EndingNode'
)
```

**Valid Ending Nodes**: LLMChain, ConversationChain, Agents, Custom output nodes

## Usage Pattern

```typescript
// 1. Build graphs
const { graph, nodeDependencies } = constructGraphs(nodes, edges)
const reversedGraph = constructGraphs(nodes, edges, { isReversed: true }).graph

// 2. Find nodes
const endingNodes = getEndingNodes(nodeDependencies, graph, nodes)
const { startingNodeIds, depthQueue } = getStartingNodes(reversedGraph, endingNodes[0].id)

// 3. Execute with buildFlow()
```

## Summary

| Function | Input | Output | Use |
|----------|-------|--------|-----|
| `constructGraphs()` | Nodes, Edges, Options | Graph, Dependencies | Build DAG |
| `getStartingNodes()` | Graph, EndNodeId | Starting IDs, Depths | Find roots |
| `getEndingNodes()` | Graph, Nodes | Ending Nodes | Find outputs |
