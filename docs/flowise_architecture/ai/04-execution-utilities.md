# Flow Execution Utilities

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

## buildFlow()

**Location**: `packages/server/src/utils/index.ts:516`

Core flow execution engine using BFS traversal.

```typescript
async function buildFlow({
  startingNodeIds, reactFlowNodes, reactFlowEdges, graph, depthQueue,
  componentNodes, question, uploadedFilesContent, chatHistory, ...
}: BuildFlowParams)
```

### Execution Loop

```typescript
const nodeQueue = []
const exploredNode = {}
const maxLoop = 3  // Loop protection

// Initialize queue
for (const nodeId of startingNodeIds) {
  nodeQueue.push({ nodeId, depth: 0 })
  exploredNode[nodeId] = { remainingLoop: maxLoop, lastSeenDepth: 0 }
}

// Process queue
while (nodeQueue.length) {
  const { nodeId, depth } = nodeQueue.shift()

  // 1. Load node
  const nodeModule = await import(nodeInstanceFilePath)
  const nodeInstance = new nodeModule.nodeClass()

  // 2. Resolve variables
  const nodeData = await resolveVariables(flowNodeData, ...)

  // 3. Execute
  const result = await nodeInstance.init(nodeData, question, options)

  // 4. Store result
  flowNodes[index].data.instance = result

  // 5. Queue neighbors
  graph[nodeId].forEach(neighborId =>
    nodeQueue.push({ nodeId: neighborId, depth: depth + 1 })
  )
}
```

### Loop Protection

```typescript
if (exploredNode[nodeId]) {
  if (depth > exploredNode[nodeId].lastSeenDepth) {
    exploredNode[nodeId].remainingLoop = maxLoop
    exploredNode[nodeId].lastSeenDepth = depth
  } else if (depth === exploredNode[nodeId].lastSeenDepth) {
    exploredNode[nodeId].remainingLoop--
    if (exploredNode[nodeId].remainingLoop <= 0) continue
  }
}
```

## executeChatflow()

**Location**: `packages/server/src/utils/buildChatflow.ts`

Main orchestrator for chatflow execution.

```typescript
// 1. Load chatflow
const chatflow = await getChatflow(chatflowId)
const flowData = JSON.parse(chatflow.flowData)

// 2. Build graphs
const { graph, nodeDependencies } = constructGraphs(nodes, edges)
const reversedGraph = constructGraphs(nodes, edges, { isReversed: true }).graph

// 3. Find nodes
const endingNodes = getEndingNodes(nodeDependencies, graph, nodes)
const { startingNodeIds, depthQueue } = getStartingNodes(reversedGraph, endingNodes[0].id)

// 4. Execute
await buildFlow({ startingNodeIds, reactFlowNodes: nodes, graph, ... })

// 5. Return result
const result = nodes.find(n => endingNodeIds.includes(n.id)).data.instance
return isStreaming ? streamResult(result) : { text: result }
```

## SSEStreamer

**Location**: `packages/server/src/utils/SSEStreamer.ts`

Server-sent events for real-time streaming.

```typescript
class SSEStreamer {
  streamStartEvent(chatId, chatflowId)
  streamToken(chatId, token)
  streamSourceDocuments(chatId, docs)
  streamArtifacts(chatId, artifacts)
  streamUsedTools(chatId, tools)
  streamAgentReasoning(chatId, reasoning)
  streamEndEvent(chatId, finalAnswer)
  streamTTSStartEvent(chatId, messageId, format)
  streamTTSDataEvent(chatId, messageId, audioBase64)
  streamTTSEndEvent(chatId, messageId)
}
```

**Usage**:
```typescript
sseStreamer.streamStartEvent(chatId, chatflowId)
for await (const chunk of llmStream) {
  sseStreamer.streamToken(chatId, chunk.text)
}
sseStreamer.streamEndEvent(chatId, finalAnswer)
```

## Memory & Validation

### Other Utilities

**getSessionChatHistory** (`index.ts:800`): Retrieves chat history for session
**isFlowValidForStream** (`index.ts:1200`): Validates if flow supports streaming

## Utility Summary

| Utility | Purpose | Key Feature |
|---------|---------|-------------|
| `buildFlow()` | Execute flow | BFS with depth tracking |
| `executeChatflow()` | Orchestrate | End-to-end execution |
| `SSEStreamer` | Stream | Real-time events |
| `getSessionChatHistory()` | Load history | Chat messages |
| `isFlowValidForStream()` | Validate | Streaming support |
