# Complete Canvas Example

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

Complete working example: LLM Chain with visual layout.

```javascript
const flowData = {
  nodes: [
    {
      id: "chatOpenAI_0",
      type: "customNode",
      width: 300,
      height: 670,
      position: { x: 100, y: 150 },
      positionAbsolute: { x: 100, y: 150 },
      selected: false,
      dragging: false,
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
          label: "ChatOpenAI",
          type: "ChatOpenAI | BaseChatModel | BaseLanguageModel"
        }]
      }
    },
    {
      id: "promptTemplate_0",
      type: "customNode",
      width: 300,
      height: 513,
      position: { x: 450, y: 250 },
      positionAbsolute: { x: 450, y: 250 },
      selected: false,
      dragging: false,
      data: {
        id: "promptTemplate_0",
        name: "promptTemplate",
        label: "Prompt Template",
        version: 4,
        type: "PromptTemplate",
        baseClasses: ["PromptTemplate", "BasePromptTemplate"],
        inputs: { template: "What is {question}?" },
        outputAnchors: [{
          id: "promptTemplate_0-output-promptTemplate-PromptTemplate|BasePromptTemplate",
          name: "promptTemplate",
          label: "PromptTemplate",
          type: "PromptTemplate | BasePromptTemplate"
        }]
      }
    },
    {
      id: "llmChain_0",
      type: "customNode",
      width: 300,
      height: 508,
      position: { x: 800, y: 300 },
      positionAbsolute: { x: 800, y: 300 },
      selected: false,
      dragging: false,
      data: {
        id: "llmChain_0",
        name: "llmChain",
        label: "LLM Chain",
        version: 3,
        type: "LLMChain",
        baseClasses: ["LLMChain", "BaseChain"],
        inputAnchors: [
          {
            id: "llmChain_0-input-model-BaseLanguageModel",
            name: "model",
            label: "Language Model",
            type: "BaseLanguageModel"
          },
          {
            id: "llmChain_0-input-prompt-BasePromptTemplate",
            name: "prompt",
            label: "Prompt",
            type: "BasePromptTemplate"
          }
        ],
        inputs: {
          model: "{{chatOpenAI_0.data.instance}}",
          prompt: "{{promptTemplate_0.data.instance}}"
        },
        outputAnchors: [{
          id: "llmChain_0-output-llmChain-LLMChain|BaseChain",
          name: "llmChain",
          label: "LLMChain",
          type: "LLMChain | BaseChain"
        }]
      }
    },
    {
      id: "stickyNote_0",
      type: "stickyNote",
      width: 300,
      height: 163,
      position: { x: 800, y: 50 },
      positionAbsolute: { x: 800, y: 50 },
      selected: false,
      dragging: false,
      data: {
        id: "stickyNote_0",
        name: "stickyNote",
        inputs: { note: "Simple LLM chain: model + prompt → chain" }
      }
    }
  ],
  edges: [
    {
      source: "chatOpenAI_0",
      sourceHandle: "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
      target: "llmChain_0",
      targetHandle: "llmChain_0-input-model-BaseLanguageModel",
      type: "buttonedge",
      id: "edge-model"
    },
    {
      source: "promptTemplate_0",
      sourceHandle: "promptTemplate_0-output-promptTemplate-PromptTemplate|BasePromptTemplate",
      target: "llmChain_0",
      targetHandle: "llmChain_0-input-prompt-BasePromptTemplate",
      type: "buttonedge",
      id: "edge-prompt"
    }
  ],
  viewport: { x: 0, y: 0, zoom: 1 }
};

// Create via API
await fetch('http://localhost:3000/api/v1/chatflows', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    name: "LLM Chain Example",
    flowData: JSON.stringify(flowData),
    type: "CHATFLOW",
    deployed: true
  })
});
```

## Visual Layout

```
[Sticky Note: x=800, y=50]

[ChatOpenAI]──────→[PromptTemplate]──────→[LLMChain]
x=100, y=150       x=450, y=250           x=800, y=300
```

## Key Points

1. **IDs match**: `id` === `data.id`
2. **Type compatibility**: ChatOpenAI → BaseLanguageModel → LLMChain accepts
3. **Spacing**: 350px horizontal gaps
4. **Handles**: Must match anchor IDs exactly
5. **flowData**: Must be stringified for API

## See Also

- [01-creating-flows-api.md](01-creating-flows-api.md)
- [02-node-structure.md](02-node-structure.md)
- [07-connecting-nodes.md](07-connecting-nodes.md)
- [10-canvas-positioning.md](10-canvas-positioning.md)
- [11-canvas-patterns.md](11-canvas-patterns.md)
