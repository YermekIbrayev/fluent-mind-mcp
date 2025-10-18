# Pinecone

**Category**: Vector Stores | **Type**: Pinecone | **Version**: 1.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Pinecone, a leading fully managed hosted vector database

## Credentials

**Required**: Yes

**Credential Types**:
- pineconeApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel_LlamaIndex` |  | - |
| Embeddings | `BaseEmbedding_LlamaIndex` |  | - |
| Pinecone Index | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Pinecone Namespace | `string` |  | - |
| Pinecone Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Chat Model (`BaseChatModel_LlamaIndex`)
- Embeddings (`BaseEmbedding_LlamaIndex`)

**Outputs**: `Pinecone`

## Common Use Cases

1. Use Pinecone when you need upsert embedded data and perform similarity search upon query using pinecone, a leading fully managed hosted vector database
2. Connect to other nodes that accept `Pinecone` input

---

**Source**: `packages/components/nodes/vectorstores/Pinecone/Pinecone_LlamaIndex.ts`