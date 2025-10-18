# Cohere Rerank Retriever

**Category**: Retrievers | **Type**: Cohere Rerank Retriever | **Version**: 1.0

---

## Overview

Cohere Rerank indexes the documents from most to least semantically relevant to the query.

---

## Credentials

**Required**: Yes

**API Field**: `data.credential`

**Credential Types**:
- `cohereApi` - Cohere API key

---

## API Required Fields

| Field | API Path | Type | Description | Default |
|-------|----------|------|-------------|---------|
| Node ID | `id` | string | Unique identifier: `cohereRerankRetriever_{index}` | - |
| Data ID | `data.id` | string | Must match outer `id` | - |
| Node Name | `data.name` | string | Must be: `cohereRerankRetriever` | - |
| Node Type | `data.type` | string | Must be: `Cohere Rerank Retriever` | - |
| Base Retriever | `data.inputs.baseRetriever` | reference | Connection to VectorStoreRetriever | - |

---

## API Optional Fields

| Field | API Path | Type | Description | Default |
|-------|----------|------|-------------|---------|
| Model Name | `data.inputs.model` | string | Rerank model to use | `rerank-v3.5` |
| Query | `data.inputs.query` | string | Custom query (if not user question) | - |
| Top K | `data.inputs.topK` | number | Number of results to return | 4 |

**Model Options**: `rerank-v3.5`, `rerank-english-v3.0`, `rerank-multilingual-v3.0`

---

## Connections

**Accepts Inputs From**:
- Vector Store Retriever (`VectorStoreRetriever`)
  - API: `"baseRetriever": "{{vectorStoreRetriever_0.data.instance}}"`

**Outputs**: `Cohere Rerank Retriever`, `BaseRetriever`

---

## API Template

See: [templates/cohere-rerank-retriever.json](../templates/cohere-rerank-retriever.json)

```json
{
  "id": "cohereRerankRetriever_0",
  "data": {
    "name": "cohereRerankRetriever",
    "credential": "cohereApi_cred_id",
    "inputs": {
      "baseRetriever": "{{vectorStoreRetriever_0.data.instance}}",
      "model": "rerank-v3.5",
      "topK": 4
    }
  }
}
```

---

## Common Use Cases

1. **Improve retrieval quality**: Rerank documents from vector search for better relevance
2. **Multi-lingual search**: Use `rerank-multilingual-v3.0` for non-English content
3. **RAG optimization**: Insert between retriever and LLM for higher quality context

---

**Source**: `packages/components/nodes/retrievers/CohereRerankRetriever/CohereRerankRetriever.ts:37-80`