# Flowise REST API Reference

Documentation of Flowise API endpoints needed for Fluent Mind MCP implementation.

## Base Configuration

```
Base URL: http://localhost:3000 (or configured FLOWISE_API_URL)
Authentication: Optional API key via header or query parameter
Content-Type: application/json
```

## Authentication

If Flowise instance is secured:
```
Header: Authorization: Bearer YOUR_API_KEY
OR
Query param: ?apiKey=YOUR_API_KEY
```

## Endpoints

### 1. List Chatflows

**Endpoint:** `GET /api/v1/chatflows`

**Description:** Retrieve all chatflows

**Request:**
```
GET /api/v1/chatflows
```

**Response:**
```json
[
  {
    "id": "abc-123-def",
    "name": "My Chatflow",
    "type": "CHATFLOW",
    "deployed": true,
    "isPublic": false,
    "createdDate": "2025-10-16T12:00:00.000Z",
    "updatedDate": "2025-10-16T12:00:00.000Z"
  }
]
```

**Fields:**
- `id` (string): UUID of chatflow
- `name` (string): Display name
- `type` (string): CHATFLOW | AGENTFLOW | MULTIAGENT | ASSISTANT
- `deployed` (boolean): Deployment status
- `isPublic` (boolean): Public access flag
- `createdDate` (string): ISO 8601 timestamp
- `updatedDate` (string): ISO 8601 timestamp

---

### 2. Get Chatflow

**Endpoint:** `GET /api/v1/chatflows/{id}`

**Description:** Get detailed chatflow including flowData

**Request:**
```
GET /api/v1/chatflows/abc-123-def
```

**Response:**
```json
{
  "id": "abc-123-def",
  "name": "My Chatflow",
  "flowData": "{\"nodes\":[...],\"edges\":[...]}",
  "type": "CHATFLOW",
  "deployed": true,
  "isPublic": false,
  "chatbotConfig": "{}",
  "apiConfig": "{}",
  "createdDate": "2025-10-16T12:00:00.000Z",
  "updatedDate": "2025-10-16T12:00:00.000Z"
}
```

**Additional Fields:**
- `flowData` (string): JSON string containing nodes and edges
- `chatbotConfig` (string): JSON string with chatbot configuration
- `apiConfig` (string): JSON string with API configuration

---

### 3. Create Chatflow

**Endpoint:** `POST /api/v1/chatflows`

**Description:** Create new chatflow

**Request:**
```json
POST /api/v1/chatflows
Content-Type: application/json

{
  "name": "My New Chatflow",
  "type": "CHATFLOW",
  "flowData": "{\"nodes\":[],\"edges\":[]}",
  "deployed": false,
  "isPublic": false
}
```

**Required Fields:**
- `name` (string): Chatflow name
- `flowData` (string): JSON string with flow structure

**Optional Fields:**
- `type` (string): Default "CHATFLOW"
- `deployed` (boolean): Default false
- `isPublic` (boolean): Default false
- `chatbotConfig` (string): Chatbot settings
- `apiConfig` (string): API settings

**Response:**
```json
{
  "id": "new-abc-123",
  "name": "My New Chatflow",
  "flowData": "{\"nodes\":[],\"edges\":[]}",
  "type": "CHATFLOW",
  "deployed": false
}
```

---

### 4. Update Chatflow

**Endpoint:** `PUT /api/v1/chatflows/{id}`

**Description:** Update existing chatflow (supports partial updates)

**Request:**
```json
PUT /api/v1/chatflows/abc-123-def
Content-Type: application/json

{
  "name": "Updated Name",
  "deployed": true
}
```

**Updatable Fields:**
- `name` (string): New name
- `flowData` (string): New flow structure
- `type` (string): New type
- `deployed` (boolean): Deployment status
- `isPublic` (boolean): Public access
- `chatbotConfig` (string): Chatbot config
- `apiConfig` (string): API config

**Response:**
```json
{
  "id": "abc-123-def",
  "name": "Updated Name",
  "deployed": true,
  "updatedDate": "2025-10-16T13:00:00.000Z"
}
```

---

### 5. Delete Chatflow

**Endpoint:** `DELETE /api/v1/chatflows/{id}`

**Description:** Delete chatflow permanently

**Request:**
```
DELETE /api/v1/chatflows/abc-123-def
```

**Response:**
```json
{
  "message": "Chatflow deleted successfully"
}
```

---

### 6. Run Prediction

**Endpoint:** `POST /api/v1/prediction/{chatflowId}`

**Description:** Execute chatflow with input

**Request:**
```json
POST /api/v1/prediction/abc-123-def
Content-Type: application/json

{
  "question": "What is the capital of France?"
}
```

**Optional Fields:**
- `overrideConfig` (object): Override chatflow config
- `history` (array): Conversation history
- `sessionId` (string): Session identifier

**Response:**
```json
{
  "text": "The capital of France is Paris.",
  "questionMessageId": "msg-123",
  "chatMessageId": "msg-456",
  "sessionId": "session-789"
}
```

---

### 7. Generate AgentFlow V2

**Endpoint:** `POST /api/v1/agentflowv2-generator/generate`

**Description:** Generate AgentFlow V2 from natural language description

**Request:**
```json
POST /api/v1/agentflowv2-generator/generate
Content-Type: application/json

{
  "description": "Create a research agent that searches the web and summarizes findings"
}
```

**Response:**
```json
{
  "flowData": "{\"nodes\":[...],\"edges\":[...]}",
  "name": "Research Agent",
  "description": "Agent that searches web and summarizes"
}
```

---

## Data Models

### ChatflowType Enum
```
"CHATFLOW" | "AGENTFLOW" | "MULTIAGENT" | "ASSISTANT"
```

### FlowData Structure
```json
{
  "nodes": [
    {
      "id": "node-1",
      "type": "customNode",
      "data": {
        "label": "Start"
      },
      "position": {"x": 100, "y": 100}
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "source": "node-1",
      "target": "node-2"
    }
  ]
}
```

## Error Responses

**Format:**
```json
{
  "error": "Error message",
  "statusCode": 400
}
```

**Common Status Codes:**
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (invalid API key)
- `404` - Not Found (chatflow doesn't exist)
- `500` - Internal Server Error

## Source References

Based on Flowise source code:
- `packages/server/src/routes/chatflows/index.ts`
- `packages/server/src/controllers/chatflows/index.ts`
- `packages/server/src/database/entities/ChatFlow.ts`
- `packages/server/src/Interface.ts`

Repository: https://github.com/FlowiseAI/Flowise
