# Node Structure and Anatomy

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

## Complete Node Structure

```javascript
{
  // React Flow Properties
  "id": "chatOpenAI_0",              // Unique identifier (REQUIRED)
  "type": "customNode",              // Always "customNode"
  "position": { "x": 100, "y": 200 },
  "width": 300,
  "height": 500,

  // Node Configuration
  "data": {
    "id": "chatOpenAI_0",            // Must match outer id (REQUIRED)
    "name": "chatOpenAI",            // Node type identifier (REQUIRED)
    "label": "ChatOpenAI",           // Display name
    "version": 8.3,
    "type": "ChatOpenAI",            // Primary base class (REQUIRED)
    "category": "Chat Models",
    "baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel"],

    "inputParams": [],               // Parameter definitions
    "inputAnchors": [],              // Connection points (for edges)
    "inputs": {},                    // Actual input values
    "outputAnchors": [],             // Output connection points
    "outputs": {}
  }
}
```

## Critical IDs

### 1. Node ID (REQUIRED)
```javascript
"id": "chatOpenAI_0"  // Format: {nodeName}_{index}
```
- Must be unique across flow
- Must match `data.id`
- Used in edge connections

### 2. Input Parameter IDs
```javascript
"id": "chatOpenAI_0-input-temperature-number"
// Format: {nodeId}-input-{paramName}-{paramType}
```

### 3. Output Anchor IDs
```javascript
"id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel"
// Format: {nodeId}-output-{outputName}-{typeChain}
```

## Input Anchors vs Input Params

### Input Anchors (For Node Connections)
```javascript
"inputAnchors": [{
  "label": "Language Model",
  "name": "model",
  "type": "BaseLanguageModel",  // Type for connection validation
  "id": "llmChain_0-input-model-BaseLanguageModel"
}]
```

### Input Params (For Direct Values)
```javascript
"inputParams": [{
  "label": "Temperature",
  "name": "temperature",
  "type": "number",         // Value type: string, number, boolean, json
  "default": 0.9,
  "optional": true
}]
```

## Inputs Object

### Direct Values
```javascript
"inputs": {
  "temperature": 0.7,
  "modelName": "gpt-4o-mini"
}
```

### Node References
```javascript
"inputs": {
  "model": "{{chatOpenAI_0.data.instance}}"  // Reference another node
}
```

### Array References
```javascript
"inputs": {
  "tools": [
    "{{calculator_0.data.instance}}",
    "{{serpAPI_0.data.instance}}"
  ]
}
```

## Output Anchors

### Single Output
```javascript
"outputAnchors": [{
  "id": "chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel",
  "name": "chatOpenAI",
  "label": "ChatOpenAI",
  "type": "ChatOpenAI | BaseChatModel | BaseLanguageModel"
}]
```

## BaseClasses (REQUIRED)

```javascript
"baseClasses": ["ChatOpenAI", "BaseChatModel", "BaseLanguageModel", "Runnable"]
```
- Defines type hierarchy
- Used for connection validation
- First element usually matches `type` field
- Target can connect if source baseClasses includes target type

## Node Positioning

- Format: `"position": { "x": 100, "y": 200 }`
- Spacing: 300-400px horizontal, 50-100px vertical

## See Also

- [01-creating-flows-api.md](01-creating-flows-api.md) - API endpoints
- [06-nodes-overview.md](06-nodes-overview.md) - Node types
- [07-connecting-nodes.md](07-connecting-nodes.md) - Edges
