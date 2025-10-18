# Redis

**Category**: Vector Stores | **Type**: Redis | **Version**: 1.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Redis, an open source, in-memory data structure store

## Credentials

**Required**: Yes

**Credential Types**:
- redisCacheUrlApi
- redisCacheApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Index Name | `string` |  | - |
| Replace Index on Upsert | `boolean` | Selecting this option will delete the existing index and recreate a new one when upserting | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Content Field | `string` | Name of the field (column) that contains the actual content | content |
| Metadata Field | `string` | Name of the field (column) that contains the metadata of the document | metadata |
| Vector Field | `string` | Name of the field (column) that contains the vector | content_vector |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Redis`

## Common Use Cases

1. Use Redis when you need upsert embedded data and perform similarity search upon query using redis, an open source, in-memory data structure store
2. Connect to other nodes that accept `Redis` input

---

**Source**: `packages/components/nodes/vectorstores/Redis/Redis.ts`