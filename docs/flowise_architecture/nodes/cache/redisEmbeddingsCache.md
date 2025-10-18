# Redis Embeddings Cache

**Category**: Cache | **Type**: RedisEmbeddingsCache | **Version**: 1.0

---

## Overview

Cache generated Embeddings in Redis to avoid needing to recompute them.

## Credentials

**Required**: Yes

**Credential Types**:
- redisCacheApi
- redisCacheUrlApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Time to Live (ms) | `number` |  | - |
| Namespace | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Embeddings (`Embeddings`)

**Outputs**: `RedisEmbeddingsCache`

## Common Use Cases

1. Use Redis Embeddings Cache when you need cache generated embeddings in redis to avoid needing to recompute them.
2. Connect to other nodes that accept `RedisEmbeddingsCache` input

---

**Source**: `packages/components/nodes/cache/RedisCache/RedisEmbeddingsCache.ts`