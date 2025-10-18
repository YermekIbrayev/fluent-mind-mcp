# Connecting Nodes - Edge Reference

**Version**: 2.0.0 | **Last Updated**: 2025-10-17

## Edge Anatomy

```javascript
{
  "source": "chatOpenAI_0",
  "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
  "target": "conversationalAgent_0",
  "targetHandle": "conversationalAgent_0-input-model-BaseChatModel",
  "type": "buttonedge",
  "id": "edge-model"
}
```

## Required Fields

1. **source**: Source node ID
2. **sourceHandle**: Output anchor ID from source
3. **target**: Target node ID
4. **targetHandle**: Input anchor ID from target
5. **type**: Always `"buttonedge"`
6. **id**: Unique identifier

## Handle ID Formats

**Source**: `{nodeId}-output-{outputName}-{typeChain}`
Example: `chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel`

**Target**: `{nodeId}-input-{inputName}-{inputType}`
Example: `llmChain_0-input-model-BaseLanguageModel`

## Type Compatibility

Edge connects if source type chain contains target type.

✅ **Compatible**: `ChatOpenAI|BaseChatModel|BaseLanguageModel` → `BaseLanguageModel`
❌ **Incompatible**: `Calculator|Tool` → `BaseChatModel`

## Common Patterns

### Chat Model → Chain
```javascript
{
  "source": "chatOpenAI_0",
  "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
  "target": "llmChain_0",
  "targetHandle": "llmChain_0-input-model-BaseLanguageModel",
  "type": "buttonedge",
  "id": "edge-1"
}
```

### Prompt → Chain
```javascript
{
  "source": "promptTemplate_0",
  "sourceHandle": "promptTemplate_0-output-promptTemplate-PromptTemplate|BasePromptTemplate",
  "target": "llmChain_0",
  "targetHandle": "llmChain_0-input-prompt-BasePromptTemplate",
  "type": "buttonedge",
  "id": "edge-2"
}
```

### Tool → Agent
```javascript
{
  "source": "calculator_0",
  "sourceHandle": "calculator_0-output-calculator-Calculator|Tool",
  "target": "agent_0",
  "targetHandle": "agent_0-input-tools-Tool",
  "type": "buttonedge",
  "id": "edge-3"
}
```

### Memory → Agent
```javascript
{
  "source": "bufferMemory_0",
  "sourceHandle": "bufferMemory_0-output-bufferMemory-BufferMemory|BaseChatMemory",
  "target": "agent_0",
  "targetHandle": "agent_0-input-memory-BaseChatMemory",
  "type": "buttonedge",
  "id": "edge-4"
}
```

## Multiple Connections

**One-to-Many**: Single source → multiple targets
```javascript
[
  { source: "chatOpenAI_0", target: "llmChain_0", ... },
  { source: "chatOpenAI_0", target: "agent_0", ... }
]
```

**Many-to-One**: Multiple sources → single target (requires `"list": true`)
```javascript
[
  { source: "calc_0", target: "agent_0", targetHandle: "agent_0-input-tools-Tool", ... },
  { source: "serp_0", target: "agent_0", targetHandle: "agent_0-input-tools-Tool", ... }
]
```

## Finding Anchor IDs

Check node's `outputAnchors` and `inputAnchors`:

```javascript
// Source node
{ "data": { "outputAnchors": [{ "id": "..." }] } }  // Use as sourceHandle

// Target node
{ "data": { "inputAnchors": [{ "id": "..." }] } }   // Use as targetHandle
```

## Validation Rules

1. Source & target nodes exist
2. Handles match anchor IDs
3. Types compatible
4. No duplicate edges (unless list input)
5. Edge ID unique

## Complete Example

```javascript
{
  "nodes": [
    {
      "id": "chatOpenAI_0",
      "data": {
        "outputAnchors": [{
          "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel"
        }]
      }
    },
    {
      "id": "llmChain_0",
      "data": {
        "inputAnchors": [{
          "id": "llmChain_0-input-model-BaseLanguageModel"
        }]
      }
    }
  ],
  "edges": [{
    "source": "chatOpenAI_0",
    "sourceHandle": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
    "target": "llmChain_0",
    "targetHandle": "llmChain_0-input-model-BaseLanguageModel",
    "type": "buttonedge",
    "id": "edge-model"
  }]
}
```

## Edge ID Patterns

- **Simple**: `"edge-1"`, `"edge-2"`
- **Descriptive**: `"chatOpenAI_0-to-llmChain_0"`
- **Functional**: `"edge-model"`, `"edge-prompt"`

## See Also

- [02-node-structure.md](02-node-structure.md) - Node anchors
- [06-nodes-overview.md](06-nodes-overview.md) - Node types
- [08-flow-examples.md](08-flow-examples.md) - Complete examples
