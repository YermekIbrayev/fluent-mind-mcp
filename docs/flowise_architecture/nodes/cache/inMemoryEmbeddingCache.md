# InMemory Embedding Cache

**Category**: Cache | **Type**: InMemoryEmbeddingCache | **Version**: 1.0

---

## Overview

Cache generated Embeddings in memory to avoid needing to recompute them.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Namespace | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Embeddings (`Embeddings`)

**Outputs**: `InMemoryEmbeddingCache`

## Common Use Cases

1. Use InMemory Embedding Cache when you need cache generated embeddings in memory to avoid needing to recompute them.
2. Connect to other nodes that accept `InMemoryEmbeddingCache` input

---

**Source**: `packages/components/nodes/cache/InMemoryCache/InMemoryEmbeddingCache.ts`