# Creating Flows Programmatically via API

**Version**: 1.0.0 | **Last Updated**: 2025-10-17

## API Endpoints

```http
POST   /api/v1/chatflows       # Create
PUT    /api/v1/chatflows/:id   # Update
GET    /api/v1/chatflows/:id   # Get one
GET    /api/v1/chatflows        # List all
DELETE /api/v1/chatflows/:id   # Delete
```

## Request Structure

```json
{
  "name": "My Flow",
  "flowData": "{\"nodes\":[...],\"edges\":[...],\"viewport\":{...}}",
  "type": "CHATFLOW",
  "deployed": true,
  "isPublic": false
}
```

## Required Fields

- **name**: string - Flow display name
- **flowData**: string - JSON stringified flow (nodes, edges, viewport)
- **type**: ChatflowType - CHATFLOW | AGENTFLOW | MULTIAGENT | ASSISTANT

## Optional Fields

- **deployed**: boolean - Active status
- **isPublic**: boolean - Public access
- **chatbotConfig**: string - UI configuration
- **apiConfig**: string - API overrides
- **category**: string - Organization category

## FlowData Structure

```typescript
{
  "nodes": [       // Array of node objects
    {
      "id": "node_0",
      "type": "customNode",
      "position": { "x": 100, "y": 100 },
      "data": { /* node configuration */ }
    }
  ],
  "edges": [       // Array of connections
    {
      "source": "node_0",
      "target": "node_1",
      "sourceHandle": "output_id",
      "targetHandle": "input_id"
    }
  ],
  "viewport": { "x": 0, "y": 0, "zoom": 1 }
}
```

## Flow Types

**CHATFLOW**: Standard conversational flows (chains, LLMs, memory)
**AGENTFLOW**: New sequential agent system
**MULTIAGENT**: Legacy multi-agent (deprecated)
**ASSISTANT**: OpenAI Assistant wrapper

## Example Request

```javascript
const flowData = {
  nodes: [{
    id: "chatOpenAI_0",
    type: "customNode",
    position: { x: 100, y: 100 },
    data: {
      id: "chatOpenAI_0",
      name: "chatOpenAI",
      inputs: { modelName: "gpt-4o-mini", temperature: 0.7 }
    }
  }],
  edges: [],
  viewport: { x: 0, y: 0, zoom: 1 }
};

const response = await fetch('http://localhost:3000/api/v1/chatflows', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    name: "Simple Flow",
    flowData: JSON.stringify(flowData),
    type: "CHATFLOW"
  })
});

const chatflow = await response.json();
```

## Response

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Simple Flow",
  "flowData": "{...}",
  "type": "CHATFLOW",
  "deployed": false,
  "createdDate": "2025-10-17T10:00:00.000Z",
  "updatedDate": "2025-10-17T10:00:00.000Z"
}
```

## Error Responses

```json
{
  "statusCode": 400,
  "message": "Invalid Chatflow Type"
}
```

## Authentication

All endpoints require Bearer token:
```http
Authorization: Bearer YOUR_API_KEY
```

Get API key from Flowise UI: Settings → API Keys

## Next Steps

- [02-node-structure.md](02-node-structure.md) - Node anatomy
- [06-nodes-overview.md](06-nodes-overview.md) - Node types reference
- [07-connecting-nodes.md](07-connecting-nodes.md) - Edge connections
- [08-flow-examples.md](08-flow-examples.md) - Complete examples
