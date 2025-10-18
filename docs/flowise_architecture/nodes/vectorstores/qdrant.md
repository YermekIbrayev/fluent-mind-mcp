# Qdrant

**Category**: Vector Stores | **Type**: Qdrant | **Version**: 5.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Qdrant, a scalable open source vector database written in Rust

## Credentials

**Required**: Yes

**Credential Types**:
- qdrantApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Qdrant Server URL | `string` |  | - |
| Qdrant Collection Name | `string` |  | - |
| Vector Dimension | `number` |  | - |
| Similarity | `options` | Similarity measure used in Qdrant. | Cosine |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| File Upload | `boolean` | Allow file upload on the chat | - |
| Content Key | `string` | The key for storing text. Default to  | content |
| Metadata Key | `string` | The key for storing metadata. Default to  | metadata |
| Upsert Batch Size | `number` | Upsert in batches of size N | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Qdrant`

## Common Use Cases

1. Use Qdrant when you need upsert embedded data and perform similarity search upon query using qdrant, a scalable open source vector database written in rust
2. Connect to other nodes that accept `Qdrant` input

---

**Source**: `packages/components/nodes/vectorstores/Qdrant/Qdrant.ts`