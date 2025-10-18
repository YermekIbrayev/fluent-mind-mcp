# SimpleStore

**Category**: Vector Stores | **Type**: SimpleVectorStore | **Version**: 1.0

---

## Overview

Upsert embedded data to local path and perform similarity search

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel_LlamaIndex` |  | - |
| Embeddings | `BaseEmbedding_LlamaIndex` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Base Path to store | `string` | Path to store persist embeddings indexes with persistence. If not specified, default to same path wh | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Chat Model (`BaseChatModel_LlamaIndex`)
- Embeddings (`BaseEmbedding_LlamaIndex`)

**Outputs**: `SimpleVectorStore`

## Common Use Cases

1. Use SimpleStore when you need upsert embedded data to local path and perform similarity search
2. Connect to other nodes that accept `SimpleVectorStore` input

---

**Source**: `packages/components/nodes/vectorstores/SimpleStore/SimpleStore.ts`