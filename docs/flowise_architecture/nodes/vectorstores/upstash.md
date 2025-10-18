# Upstash Vector

**Category**: Vector Stores | **Type**: Upstash | **Version**: 2.0

---

## Overview

Upsert data as embedding or string and perform similarity search with Upstash, the leading serverless data platform

## Credentials

**Required**: Yes

**Credential Types**:
- upstashVectorApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| File Upload | `boolean` | Allow file upload on the chat | - |
| Upstash Metadata Filter | `string` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Upstash`

## Common Use Cases

1. Use Upstash Vector when you need upsert data as embedding or string and perform similarity search with upstash, the leading serverless data platform
2. Connect to other nodes that accept `Upstash` input

---

**Source**: `packages/components/nodes/vectorstores/Upstash/Upstash.ts`