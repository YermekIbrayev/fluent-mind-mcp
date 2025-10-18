# Weaviate

**Category**: Vector Stores | **Type**: Weaviate | **Version**: 4.0

---

## Overview

Upsert embedded data and perform similarity or mmr search using Weaviate, a scalable open-source vector database

## Credentials

**Required**: Yes

**Credential Types**:
- weaviateApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Weaviate Scheme | `options` |  | https |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Weaviate`

## Common Use Cases

1. Use Weaviate when you need upsert embedded data and perform similarity or mmr search using weaviate, a scalable open-source vector database
2. Connect to other nodes that accept `Weaviate` input

---

**Source**: `packages/components/nodes/vectorstores/Weaviate/Weaviate.ts`