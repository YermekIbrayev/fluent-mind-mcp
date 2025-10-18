# Complete Flow Examples

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

Working examples of creating flows programmatically.

## Example 1: Simple LLM Chain

```javascript
const flowData = {
  nodes: [
    {
      id: "chatOpenAI_0",
      type: "customNode",
      position: { x: 100, y: 100 },
      width: 300,
      height: 500,
      data: {
        id: "chatOpenAI_0",
        name: "chatOpenAI",
        label: "ChatOpenAI",
        version: 8.3,
        type: "ChatOpenAI",
        baseClasses: ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel"],
        inputs: { modelName: "gpt-4o-mini", temperature: 0.7 },
        outputAnchors: [{
          id: "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
          name: "chatOpenAI",
          type: "ChatOpenAI | BaseChatModel | BaseLanguageModel"
        }]
      }
    },
    {
      id: "llmChain_0",
      type: "customNode",
      position: { x: 500, y: 100 },
      width: 300,
      height: 400,
      data: {
        id: "llmChain_0",
        name: "llmChain",
        label: "LLM Chain",
        version: 3,
        type: "LLMChain",
        baseClasses: ["LLMChain", "BaseChain", "Runnable"],
        inputAnchors: [{
          id: "llmChain_0-input-model-BaseLanguageModel",
          name: "model",
          type: "BaseLanguageModel"
        }],
        inputs: { model: "{{chatOpenAI_0.data.instance}}" },
        outputAnchors: [{
          id: "llmChain_0-output-llmChain-LLMChain|BaseChain|Runnable",
          name: "llmChain",
          type: "LLMChain | BaseChain | Runnable"
        }]
      }
    }
  ],
  edges: [{
    source: "chatOpenAI_0",
    sourceHandle: "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
    target: "llmChain_0",
    targetHandle: "llmChain_0-input-model-BaseLanguageModel",
    type: "buttonedge",
    id: "edge-1"
  }],
  viewport: { x: 0, y: 0, zoom: 1 }
};

// Create via API
const response = await fetch('http://localhost:3000/api/v1/chatflows', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    name: "Simple LLM Chain",
    flowData: JSON.stringify(flowData),
    type: "CHATFLOW"
  })
});
```

## Example 2: Helper Functions

```javascript
function createNodeId(nodeName, index = 0) {
  return `${nodeName}_${index}`;
}

function autoPosition(nodeIndex, nodesPerRow = 3) {
  const nodeWidth = 300;
  const spacing = 100;
  const col = nodeIndex % nodesPerRow;
  const row = Math.floor(nodeIndex / nodesPerRow);
  return {
    x: col * (nodeWidth + spacing),
    y: row * 200
  };
}

async function createChatflow(name, flowData, type = 'CHATFLOW') {
  const response = await fetch('http://localhost:3000/api/v1/chatflows', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.FLOWISE_API_KEY}`
    },
    body: JSON.stringify({
      name,
      flowData: JSON.stringify(flowData),
      type,
      deployed: true
    })
  });

  if (!response.ok) throw new Error(`Failed: ${response.statusText}`);
  return await response.json();
}

// Test flow
async function testChatflow(chatflowId, question) {
  const response = await fetch(
    `http://localhost:3000/api/v1/prediction/${chatflowId}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    }
  );
  return await response.json();
}
```

## Example 3: Agent with Tools

```javascript
const agentFlow = {
  nodes: [
    { id: "chatOpenAI_0", /* ... chat model config ... */ },
    { id: "bufferMemory_0", /* ... memory config ... */ },
    { id: "calculator_0", /* ... calculator tool ... */ },
    {
      id: "agent_0",
      data: {
        name: "conversationalAgent",
        inputs: {
          model: "{{chatOpenAI_0.data.instance}}",
          memory: "{{bufferMemory_0.data.instance}}",
          tools: ["{{calculator_0.data.instance}}"]
        }
      }
    }
  ],
  edges: [/* connect all nodes to agent */]
};
```

## Validation Checklist

- [ ] All node IDs are unique
- [ ] Edge source/target nodes exist
- [ ] Handle IDs match anchor IDs
- [ ] Types are compatible
- [ ] flowData is JSON stringified
- [ ] Required inputs have values

## See Also

- [01-creating-flows-api.md](01-creating-flows-api.md)
- [02-node-structure.md](02-node-structure.md)
- [06-nodes-overview.md](06-nodes-overview.md)
- [07-connecting-nodes.md](07-connecting-nodes.md)
