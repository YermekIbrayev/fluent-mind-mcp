# In-Memory Vector Store

**Category**: Vector Stores | **Type**: Memory | **Version**: 1.0

---

## Overview

In-memory vectorstore that stores embeddings and does an exact, linear search for the most similar embeddings.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Memory`

## Common Use Cases

1. Use In-Memory Vector Store when you need in-memory vectorstore that stores embeddings and does an exact, linear search for the most similar embeddings.
2. Connect to other nodes that accept `Memory` input

---

**Source**: `packages/components/nodes/vectorstores/InMemory/InMemoryVectorStore.ts`