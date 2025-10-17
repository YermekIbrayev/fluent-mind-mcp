# Flowise Node Connection & Flow Logic

**Source**: FlowiseAI/Flowise repository
**Date Extracted**: 2025-10-17

This document captures the core logic for how Flowise handles node connections, flow building, and execution.

---

## 1. Node Creation & Initialization

### 1.1 Unique ID Generation (`genericHelper.js`)

```javascript
export const getUniqueNodeId = (nodeData, nodes) => {
    let suffix = 0
    let baseId = `${nodeData.name}_${suffix}`

    // Increment suffix until a unique ID is found
    while (nodes.some((node) => node.id === baseId)) {
        suffix += 1
        baseId = `${nodeData.name}_${suffix}`
    }

    return baseId
}
```

**Key Points**:
- Node ID format: `{nodeName}_{counter}` (e.g., `llmAgentflow_0`)
- Increments counter until ID is unique
- Checks against all existing nodes

### 1.2 Node Initialization (`initNode`)

```javascript
export const initNode = (nodeData, newNodeId, isAgentflow) => {
    const inputAnchors = []
    const inputParams = []
    const incoming = nodeData.inputs ? nodeData.inputs.length : 0

    // Whitelist of parameter types (not connection anchors)
    const whitelistTypes = [
        'asyncOptions', 'asyncMultiOptions', 'options', 'multiOptions',
        'array', 'datagrid', 'string', 'number', 'boolean', 'password',
        'json', 'code', 'date', 'file', 'folder', 'tabs', 'conditionFunction'
    ]

    // Separate inputs into params vs anchors
    for (let i = 0; i < incoming; i += 1) {
        const newInput = {
            ...nodeData.inputs[i],
            id: `${newNodeId}-input-${nodeData.inputs[i].name}-${nodeData.inputs[i].type}`
        }

        if (whitelistTypes.includes(nodeData.inputs[i].type)) {
            inputParams.push(newInput)  // UI parameters
        } else {
            inputAnchors.push(newInput)  // Connection anchors
        }
    }

    // Initialize outputs
    let outputAnchors = initializeOutputAnchors(nodeData, newNodeId, isAgentflow)

    // Set default values
    nodeData.inputs = initializeDefaultNodeData(nodeData.inputs)
    nodeData.outputs = initializeDefaultNodeData(outputAnchors)
    nodeData.inputAnchors = inputAnchors
    nodeData.inputParams = inputParams
    nodeData.outputAnchors = outputAnchors
    nodeData.id = newNodeId

    return nodeData
}
```

**Key Concepts**:
- **Input Anchors**: Connection points for node-to-node data flow
- **Input Params**: UI parameters (dropdowns, text fields, etc.)
- **Output Anchors**: Output connection points
- ID format: `{nodeId}-{direction}-{name}-{type}`

---

## 2. Node Connections & Edges

### 2.1 Connection Validation (Standard Flows)

```javascript
export const isValidConnection = (connection, reactFlowInstance) => {
    const sourceHandle = connection.sourceHandle
    const targetHandle = connection.targetHandle
    const target = connection.target

    // Extract types from handle IDs
    // Format: "llmChain_0-output-llmChain-BaseChain"
    let sourceTypes = sourceHandle.split('-')[sourceHandle.split('-').length - 1].split('|')
    sourceTypes = sourceTypes.map((s) => s.trim())

    let targetTypes = targetHandle.split('-')[targetHandle.split('-').length - 1].split('|')
    targetTypes = targetTypes.map((t) => t.trim())

    // Check type compatibility
    if (targetTypes.some((t) => sourceTypes.includes(t))) {
        let targetNode = reactFlowInstance.getNode(target)

        if (!targetNode) {
            if (!reactFlowInstance.getEdges().find((e) => e.targetHandle === targetHandle)) {
                return true
            }
        } else {
            const targetNodeInputAnchor =
                targetNode.data.inputAnchors.find((ancr) => ancr.id === targetHandle) ||
                targetNode.data.inputParams.find((ancr) => ancr.id === targetHandle)

            // Allow connection if:
            // 1. Target anchor allows lists, OR
            // 2. No existing connection to this target
            if ((targetNodeInputAnchor &&
                !targetNodeInputAnchor?.list &&
                !reactFlowInstance.getEdges().find((e) => e.targetHandle === targetHandle)) ||
                targetNodeInputAnchor?.list) {
                return true
            }
        }
    }
    return false
}
```

### 2.2 Connection Validation (AgentFlow V2)

```javascript
export const isValidConnectionAgentflowV2 = (connection, reactFlowInstance) => {
    const source = connection.source
    const target = connection.target

    // Prevent self connections
    if (source === target) {
        return false
    }

    // Check if this connection would create a cycle
    if (wouldCreateCycle(source, target, reactFlowInstance)) {
        return false
    }

    return true
}

// Cycle detection using DFS
const wouldCreateCycle = (sourceId, targetId, reactFlowInstance) => {
    if (sourceId === targetId) return true

    // Build directed graph from existing edges
    const graph = {}
    const edges = reactFlowInstance.getEdges()

    edges.forEach((edge) => {
        if (!graph[edge.source]) graph[edge.source] = []
        graph[edge.source].push(edge.target)
    })

    // Check if there's a path from target to source
    const visited = new Set()

    function hasPath(current, destination) {
        if (current === destination) return true
        if (visited.has(current)) return false

        visited.add(current)

        const neighbors = graph[current] || []
        for (const neighbor of neighbors) {
            if (hasPath(neighbor, destination)) {
                return true
            }
        }

        return false
    }

    // If there's a path from target to source,
    // adding source → target will create a cycle
    return hasPath(targetId, sourceId)
}
```

**Key Differences**:
- **Standard Flows**: Type-based validation, checks target handle compatibility
- **AgentFlow V2**: Simpler validation, focuses on cycle prevention
- Both prevent self-connections

### 2.3 Creating Connections (React UI)

```javascript
// From Canvas.jsx
const onConnect = (params) => {
    if (!isValidConnectionAgentflowV2(params, reactFlowInstance)) {
        return
    }

    const nodeName = params.sourceHandle.split('_')[0]
    const targetNodeName = params.targetHandle.split('_')[0]

    // Get node colors for visual styling
    const targetColor = AGENTFLOW_ICONS.find((icon) => icon.name === targetNodeName)?.color
    const sourceColor = AGENTFLOW_ICONS.find((icon) => icon.name === nodeName)?.color

    // Special handling for condition nodes
    let edgeLabel = undefined
    if (nodeName === 'conditionAgentflow' || nodeName === 'conditionAgentAgentflow') {
        const _edgeLabel = params.sourceHandle.split('-').pop()
        edgeLabel = (isNaN(_edgeLabel) ? 0 : _edgeLabel).toString()
    }

    // Special handling for human input nodes
    if (nodeName === 'humanInputAgentflow') {
        edgeLabel = params.sourceHandle.split('-').pop()
        edgeLabel = edgeLabel === '0' ? 'proceed' : 'reject'
    }

    const newEdge = {
        ...params,
        data: {
            ...params.data,
            sourceColor,
            targetColor,
            edgeLabel,
            isHumanInput: nodeName === 'humanInputAgentflow'
        },
        type: 'agentFlow',
        id: `${params.source}-${params.sourceHandle}-${params.target}-${params.targetHandle}`
    }

    setEdges((eds) => addEdge(newEdge, eds))
}
```

---

## 3. Flow Execution Logic

### 3.1 Graph Construction (`buildAgentflow.ts`)

```typescript
// From utils/index.ts (referenced in buildAgentflow.ts)
export const constructGraphs = (nodes, edges, options = {}) => {
    const { isReversed = false } = options

    const graph = {}
    const nodeDependencies = {}

    // Initialize all nodes in graph
    nodes.forEach(node => {
        graph[node.id] = []
        nodeDependencies[node.id] = 0
    })

    // Build adjacency list
    edges.forEach(edge => {
        if (isReversed) {
            // Reversed graph: target -> source
            if (!graph[edge.target]) graph[edge.target] = []
            graph[edge.target].push(edge.source)
        } else {
            // Normal graph: source -> target
            if (!graph[edge.source]) graph[edge.source] = []
            graph[edge.source].push(edge.target)
            nodeDependencies[edge.target]++
        }
    })

    return { graph, nodeDependencies }
}
```

**Result Example**:
```javascript
// graph
{
    'startAgentflow_0': ['conditionAgentflow_0'],
    'conditionAgentflow_0': ['llmAgentflow_0', 'llmAgentflow_1'],
    'llmAgentflow_0': ['llmAgentflow_2'],
    'llmAgentflow_1': ['llmAgentflow_2'],
    'llmAgentflow_2': []
}

// nodeDependencies (number of incoming edges)
{
    'startAgentflow_0': 0,
    'conditionAgentflow_0': 1,
    'llmAgentflow_0': 1,
    'llmAgentflow_1': 1,
    'llmAgentflow_2': 2
}
```

### 3.2 Node Execution Queue

```typescript
interface INodeQueue {
    nodeId: string
    data: any
    inputs: Record<string, any>
}

interface IWaitingNode {
    nodeId: string
    receivedInputs: Map<string, any>
    expectedInputs: Set<string>
    isConditional: boolean
    conditionalGroups: Map<string, string[]>
}

// Main execution loop
const nodeExecutionQueue: INodeQueue[] = []
const waitingNodes: Map<string, IWaitingNode> = new Map()

// Add starting nodes to queue
startingNodeIds.forEach((nodeId) => {
    nodeExecutionQueue.push({
        nodeId,
        data: {},
        inputs: {}
    })
})

// Process queue
while (nodeExecutionQueue.length > 0 && status === 'INPROGRESS') {
    const currentNode = nodeExecutionQueue.shift()

    // Execute node
    const result = await executeNode({...params})

    // Process outputs and add child nodes to queue
    await processNodeOutputs({
        nodeId: currentNode.nodeId,
        result,
        graph,
        nodes,
        edges,
        nodeExecutionQueue,
        waitingNodes
    })
}
```

### 3.3 Dependency Management

```typescript
function setupNodeDependencies(nodeId: string, edges: IReactFlowEdge[], nodes: IReactFlowNode[]): IWaitingNode {
    const inputConnections = getNodeInputConnections(edges, nodeId)

    const waitingNode: IWaitingNode = {
        nodeId,
        receivedInputs: new Map(),
        expectedInputs: new Set(),
        isConditional: false,
        conditionalGroups: new Map()
    }

    // Group inputs by their parent condition nodes
    for (const connection of inputConnections) {
        const conditionParent = findConditionParent(connection.source, edges, nodes)

        if (conditionParent) {
            // This is a conditional input
            waitingNode.isConditional = true
            const group = waitingNode.conditionalGroups.get(conditionParent) || []
            group.push(connection.source)
            waitingNode.conditionalGroups.set(conditionParent, group)
        } else {
            // This is a required input
            waitingNode.expectedInputs.add(connection.source)
        }
    }

    return waitingNode
}

function hasReceivedRequiredInputs(waitingNode: IWaitingNode): boolean {
    // Check non-conditional required inputs
    for (const required of waitingNode.expectedInputs) {
        if (!waitingNode.receivedInputs.has(required)) return false
    }

    // Check conditional groups - need at least one from each group
    for (const [groupId, possibleSources] of waitingNode.conditionalGroups) {
        const hasInputFromGroup = possibleSources.some((source) =>
            waitingNode.receivedInputs.has(source)
        )
        if (!hasInputFromGroup) return false
    }

    return true
}
```

**Key Pattern**:
1. **Regular Dependencies**: Node must wait for ALL expected inputs
2. **Conditional Dependencies**: Node must wait for AT LEAST ONE input from each conditional group
3. **Mixed**: Node can have both regular and conditional dependencies

### 3.4 Processing Node Outputs

```typescript
async function processNodeOutputs({
    nodeId,
    nodeName,
    result,
    graph,
    nodes,
    edges,
    nodeExecutionQueue,
    waitingNodes
}: IProcessNodeOutputsParams) {
    const childNodeIds = graph[nodeId] || []

    // Determine which nodes to ignore based on conditions
    const ignoreNodeIds = await determineNodesToIgnore(currentNode, result, edges, nodeId)

    for (const childId of childNodeIds) {
        if (ignoreNodeIds.includes(childId)) continue

        let waitingNode = waitingNodes.get(childId)

        if (!waitingNode) {
            // First time seeing this node - analyze dependencies
            waitingNode = setupNodeDependencies(childId, edges, nodes)
            waitingNodes.set(childId, waitingNode)
        }

        // Add this node's output to child's received inputs
        waitingNode.receivedInputs.set(nodeId, result)

        // Check if child node is ready to execute
        if (hasReceivedRequiredInputs(waitingNode)) {
            waitingNodes.delete(childId)
            nodeExecutionQueue.push({
                nodeId: childId,
                data: combineNodeInputs(waitingNode.receivedInputs),
                inputs: Object.fromEntries(waitingNode.receivedInputs)
            })
        }
    }
}
```

---

## 4. Variable Resolution

### 4.1 Variable Reference Format

Variables in node inputs can reference:
- `{{$question}}` - User's input question
- `{{$form.fieldName}}` - Form field values
- `{{$vars.variableName}}` - Global variables
- `{{$flow.propertyName}}` - Flow config properties
- `{{nodeId.output.path}}` - Output from previous nodes
- `{{$iteration}}` - Current iteration value
- `{{$chatHistory}}` - Chat history as text
- `{{$loopCount}}` - Current loop iteration count

### 4.2 Resolution Logic

```typescript
const resolveNodeReference = async (value: any): Promise<any> => {
    if (typeof value !== 'string') return value

    const matches = value.match(/{{(.*?)}}/g)
    if (!matches) return value

    let resolvedValue = value
    for (const match of matches) {
        const reference = match.replace(/[{}]/g, '').trim()

        // Question variable
        if (reference === '$question') {
            resolvedValue = resolvedValue.replace(match, question)
        }

        // Form variables
        if (reference.startsWith('$form.')) {
            const variableValue = get(form, reference.replace('$form.', ''))
            resolvedValue = resolvedValue.replace(match, variableValue)
        }

        // Node output variables
        const outputMatch = reference.match(/^(.*?)\.output\.(.+)$/)
        if (outputMatch && agentFlowExecutedData) {
            const [, nodeIdPart, outputPath] = outputMatch
            const cleanNodeId = nodeIdPart.replace('\\', '')

            // Find the last (most recent) matching node
            const nodeData = [...agentFlowExecutedData]
                .reverse()
                .find((d) => d.nodeId === cleanNodeId)

            if (nodeData?.data?.output && outputPath.trim()) {
                const variableValue = get(nodeData.data.output, outputPath)
                resolvedValue = resolvedValue.replace(match, variableValue)
            }
        }
    }

    return resolvedValue
}
```

---

## 5. Key Data Structures

### 5.1 Flow Data Structure

```typescript
interface IReactFlowObject {
    nodes: IReactFlowNode[]
    edges: IReactFlowEdge[]
    viewport: { x: number; y: number; zoom: number }
}

interface IReactFlowNode {
    id: string
    type: 'agentFlow' | 'stickyNote' | 'iteration'
    position: { x: number; y: number }
    data: INodeData
    parentNode?: string  // For nested nodes (e.g., inside iteration)
    extent?: 'parent'    // Keeps node within parent bounds
}

interface IReactFlowEdge {
    id: string
    source: string  // Source node ID
    target: string  // Target node ID
    sourceHandle: string  // Source anchor ID
    targetHandle: string  // Target anchor ID
    type: 'agentFlow'
    data?: {
        sourceColor?: string
        targetColor?: string
        edgeLabel?: string
        isHumanInput?: boolean
    }
}
```

### 5.2 Node Data Structure

```typescript
interface INodeData {
    id: string
    name: string  // Node type name (e.g., 'llmAgentflow')
    label: string  // Display label
    version: number
    type: string
    category: string
    description: string

    inputs: Record<string, any>  // Actual input values
    outputs: Record<string, any>  // Actual output values

    inputParams: INodeParam[]  // UI parameters
    inputAnchors: INodeParam[]  // Input connection points
    outputAnchors: INodeParam[]  // Output connection points

    credential?: string
    selected?: boolean
}
```

---

## 6. Special Node Handling

### 6.1 Condition Nodes

```typescript
// Condition nodes have multiple output branches
async function determineNodesToIgnore(
    currentNode: IReactFlowNode,
    result: any,
    edges: IReactFlowEdge[],
    nodeId: string
): Promise<string[]> {
    const ignoreNodeIds: string[] = []

    if (result.output?.conditions) {
        const outputConditions: ICondition[] = result.output.conditions

        // Find indexes of unfulfilled conditions
        const unfulfilledIndexes = outputConditions
            .map((condition, index) =>
                condition.isFulfilled === false ? index : -1
            )
            .filter((index) => index !== -1)

        // Find nodes connected to unfulfilled condition outputs
        for (const index of unfulfilledIndexes) {
            const ignoreEdge = edges.find((edge) =>
                edge.source === nodeId &&
                edge.sourceHandle === `${nodeId}-output-${index}`
            )

            if (ignoreEdge) {
                ignoreNodeIds.push(ignoreEdge.target)
            }
        }
    }

    return ignoreNodeIds
}
```

### 6.2 Loop Nodes

```typescript
// Loop nodes redirect execution back to earlier nodes
if (nodeName === 'loopAgentflow' && result.output?.nodeID) {
    const loopCount = (loopCounts.get(nodeId) || 0) + 1
    const maxLoop = result.output.maxLoopCount || MAX_LOOP_COUNT

    if (loopCount < maxLoop) {
        loopCounts.set(nodeId, loopCount)

        // Add target node back to execution queue
        nodeExecutionQueue.push({
            nodeId: result.output.nodeID,
            data: result.output,
            inputs: {}
        })
    } else {
        // Max iterations reached, output fallback message
        const fallbackMessage = result.output.fallbackMessage ||
            `Loop completed after reaching maximum iteration count of ${maxLoop}.`
        result.output = { ...result.output, content: fallbackMessage }
    }
}
```

### 6.3 Iteration Nodes (Parent-Child)

```typescript
// Iteration nodes can contain child nodes
const onDrop = useCallback((event) => {
    // ... node creation code ...

    // Check if dropped inside an Iteration node
    const iterationNodes = nodes.filter((node) => node.type === 'iteration')
    let parentNode = null

    for (const iterationNode of iterationNodes) {
        const nodeLeft = iterationNode.position.x
        const nodeRight = nodeLeft + (iterationNode.width || 300)
        const nodeTop = iterationNode.position.y
        const nodeBottom = nodeTop + (iterationNode.height || 250)

        if (position.x >= nodeLeft && position.x <= nodeRight &&
            position.y >= nodeTop && position.y <= nodeBottom) {
            parentNode = iterationNode
            break
        }
    }

    // If dropped inside iteration node, set parent relationship
    if (parentNode) {
        newNode.parentNode = parentNode.id
        newNode.extent = 'parent'
        // Adjust position to be relative to parent
        newNode.position = {
            x: position.x - parentNode.position.x,
            y: position.y - parentNode.position.y
        }
    }
})
```

---

## 7. Summary of Key Patterns

### Architecture
1. **Graph-Based**: Flows are directed acyclic graphs (DAGs) with cycle detection
2. **Queue-Based Execution**: BFS-like traversal with dependency management
3. **Lazy Evaluation**: Nodes execute only when all required inputs are received

### Node Connection Rules
1. **Type Compatibility**: Source output type must match target input type (standard flows)
2. **No Self-Connections**: A node cannot connect to itself
3. **No Cycles**: Connections that create cycles are prevented (AgentFlow V2)
4. **Multiple Inputs**: Some anchors accept multiple connections (list=true)
5. **Single Input**: Most anchors accept only one connection

### Execution Flow
1. Start with nodes that have zero dependencies
2. Execute node → Store result → Mark as complete
3. Notify child nodes → Check if child dependencies satisfied
4. Add ready child nodes to execution queue
5. Continue until queue is empty or error occurs

### Special Cases
- **Conditional Branching**: Only execute fulfilled condition branches
- **Loops**: Re-add target node to queue with iteration count
- **Human-in-Loop**: Pause execution, wait for user input
- **Nested Nodes**: Children execute within parent context (iterations)

---

## 8. Integration Points for MCP Server

To implement similar logic in the MCP server:

1. **Node Schema Definition**: Define input/output schemas for each tool
2. **Graph Validation**: Implement cycle detection and type checking
3. **Variable Resolution**: Parse `{{variable}}` syntax in tool parameters
4. **Execution Engine**: Build queue-based executor with dependency tracking
5. **State Management**: Track execution state, variables, and history
6. **Error Handling**: Graceful failures with execution rollback

This provides a foundation for building visual workflow builders or programmatic flow execution systems.
