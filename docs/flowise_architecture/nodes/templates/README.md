# Node API Request Templates

**Version**: 2.0.0 | **Date**: 2025-10-17 | **Total**: 255 templates

Comprehensive JSON templates for all Flowise nodes, organized by category.

---

## Quick Start

1. Find node in [TEMPLATE_INDEX.md](TEMPLATE_INDEX.md)
2. Copy JSON template
3. Modify `inputs` with values
4. POST to `/api/v1/chatflows/{id}`

---

## Structure

```
templates/
├── TEMPLATE_INDEX.md          # Master index
├── {category}/
│   ├── INDEX.md              # Category index
│   └── {nodeName}.json       # Node template
```

---

## Categories (19)

| Category | Count | Path |
|----------|-------|------|
| Chat Models | 35 | [chatmodels/](chatmodels/) |
| Tools | 41 | [tools/](tools/) |
| Document Loaders | 42 | [documentloaders/](documentloaders/) |
| Vector Stores | 26 | [vectorstores/](vectorstores/) |
| Embeddings | 17 | [embeddings/](embeddings/) |
| Others | 94 | [TEMPLATE_INDEX.md](TEMPLATE_INDEX.md) |

---

## Template Structure

```json
{
  "id": "nodeName_0",
  "type": "customNode",
  "position": {"x": 100, "y": 200},
  "data": {
    "id": "nodeName_0",
    "name": "nodeName",
    "type": "NodeType",
    "credential": "credentialId",
    "inputs": {}
  }
}
```

**Required**: `id`, `data.id`, `data.name`, `data.type`
**Optional**: `data.credential`, `data.inputs`, `position`

---

## Usage Examples

### Chat Model
```json
{
  "id": "chatOpenAI_0",
  "data": {
    "name": "chatOpenAI",
    "credential": "openAIApi_cred",
    "inputs": {"temperature": 0.7, "modelName": "gpt-4o-mini"}
  }
}
```

### Tool
```json
{
  "id": "calculator_0",
  "data": {"name": "calculator", "inputs": {}}
}
```

### Connected Nodes
```json
{
  "id": "agent_0",
  "data": {
    "name": "reactAgentLLM",
    "inputs": {
      "model": "{{chatOpenAI_0.data.instance}}",
      "tools": ["{{calculator_0.data.instance}}"]
    }
  }
}
```

---

## Connection Syntax

**Single**: `"{{nodeId.data.instance}}"`
**Array**: `["{{node1.data.instance}}", "{{node2.data.instance}}"]`

Type must match `baseClasses`.

---

## Field Types

**Values**: `string` | `number` | `boolean` | `options` | `json`
**Connections**: `{{nodeId.data.instance}}`
**Credentials**: Credential ID string

---

## Finding Templates

**By Category**: [TEMPLATE_INDEX.md](TEMPLATE_INDEX.md) → Category → Node
**By Use Case**: Chatbot (chatmodels/ + memory/) | RAG (documentloaders/ + vectorstores/) | Agent (agents/ + tools/)

---

## Validation Rules

1. **ID Unique** - Each `id` unique in flow
2. **ID Match** - Outer `id` = `data.id`
3. **Type Compatible** - Check `baseClasses`
4. **Inputs Complete** - All required inputs set
5. **Credentials Valid** - Referenced creds exist

---

## See Also

- [TEMPLATE_INDEX.md](TEMPLATE_INDEX.md) - All templates
- [Node Docs](../README.md) - Node parameters
- [API Guide](../../api/02-node-structure.md) - API details

---

**Lines**: 144 / 150 max
