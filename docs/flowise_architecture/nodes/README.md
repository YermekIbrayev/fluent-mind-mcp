# Flowise Nodes Documentation

**Version**: 2.0.0 | **Date**: 2025-10-17

Complete reference for all Flowise node types, organized by category.

---

## 📚 Node Categories

**AI Models**: [chatmodels/](chatmodels/) | [embeddings/](embeddings/)
**Vector & Retrieval**: [vectorstores/](vectorstores/) | [retrievers/](retrievers/)
**Data Processing**: [documentloaders/](documentloaders/) | [textsplitters/](textsplitters/)
**Agents**: [agents/](agents/) | [sequentialagents/](sequentialagents/) | [multiagents/](multiagents/) | [agentflow/](agentflow/)
**Tools**: [tools/](tools/) (60+ tools)
**Memory & Cache**: [memory/](memory/) | [cache/](cache/) | [recordmanager/](recordmanager/)
**Prompts & Parsing**: [prompts/](prompts/) | [outputparsers/](outputparsers/)
**Specialized**: [responsesynthesizer/](responsesynthesizer/) | [speechtotext/](speechtotext/) | [utilities/](utilities/)

---

## 🔌 API Request Fields

### Required Fields (ALL API requests)
- `id` - Unique node identifier: `{nodeName}_{index}`
- `data.id` - Must match outer `id`
- `data.name` - Node type identifier (e.g., `chatOpenAI`)
- `data.type` - Primary base class (e.g., `ChatOpenAI`)

### Optional Fields (API requests)
- `data.inputs` - Parameter values (see node docs for available params)
- `data.credential` - Credential ID (if authentication required)
- `position` - Node position in canvas: `{x, y}`
- `data.label` - Custom display name

**Templates**: See [templates/](templates/) for JSON examples

---

## 📖 Node Documentation Structure

Each node documentation file includes:

1. **Overview** - What the node does
2. **Credentials** - Required authentication (if any)
3. **Required Parameters** - Must be configured via API `inputs`
4. **Optional Parameters** - Can be configured via API `inputs`
5. **Connections** - Inputs from other nodes (use `{{nodeId.data.instance}}`)
6. **Outputs** - What this node produces
7. **API Example** - JSON template reference

---

## 🎯 Common Usage Patterns

### Simple Chatbot
```
ChatOpenAI → ConversationBufferMemory
```

### RAG System
```
PDF File → TextSplitter → Embeddings → Pinecone → Retriever → ChatOpenAI
```

### Agent with Tools
```
ChatOpenAI → Agent → [Calculator, WebBrowser, CustomTool]
```

---

## 📊 Node Statistics

- **Total Nodes**: 350+
- **Categories**: 15
- **API Templates**: [templates/](templates/)

---

## 🏗️ Node Architecture

### API Request Structure
```json
{
  "id": "nodeName_0",
  "type": "customNode",
  "position": {"x": 100, "y": 200},
  "data": {
    "id": "nodeName_0",
    "name": "nodeName",
    "type": "NodeType",
    "inputs": {
      "param1": "value1"
    }
  }
}
```

### Input Types
- `string` - Text values
- `number` - Numeric values
- `boolean` - true/false
- `options` - Select from list
- `json` - JSON object
- Node references: `"{{nodeId.data.instance}}"`

---

## 📝 File Organization

```
arch/nodes/
├── README.md                    # This file (≤150 lines)
├── templates/                   # JSON API templates
│   ├── README.md
│   ├── node-api-request.json
│   └── {nodeName}.json
├── chatmodels/
│   ├── INDEX.md
│   └── *.md (≤150 lines each)
└── {category}/
    ├── INDEX.md
    └── *.md (≤150 lines each)
```

**Principle**: All files ≤150 lines. Templates in separate JSON files.

---

## 🔗 Related Documentation

- [API - Creating Flows](../api/01-creating-flows-api.md) - API usage
- [API - Node Structure](../api/02-node-structure.md) - Detailed node anatomy
- [Templates](templates/) - JSON request templates

---

**Version**: 2.0.0 | **Maintained by**: Flowise Architecture Team
