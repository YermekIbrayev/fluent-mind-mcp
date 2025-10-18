# Chroma

**Category**: Vector Stores | **Type**: Chroma | **Version**: 2.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Chroma, an open-source embedding database

## Credentials

**Required**: Yes

**Credential Types**:
- chromaApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Collection Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| Chroma URL | `string` |  | - |
| Chroma Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Chroma`

## Common Use Cases

1. Use Chroma when you need upsert embedded data and perform similarity search upon query using chroma, an open-source embedding database
2. Connect to other nodes that accept `Chroma` input

---

**Source**: `packages/components/nodes/vectorstores/Chroma/Chroma.ts`