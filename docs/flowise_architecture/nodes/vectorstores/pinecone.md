# Pinecone

**Category**: Vector Stores | **Type**: Pinecone | **Version**: 5.0

---

## Overview

Upsert embedded data and perform similarity or mmr search using Pinecone, a leading fully managed hosted vector database

## Credentials

**Required**: Yes

**Credential Types**:
- pineconeApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Pinecone Index | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| Pinecone Namespace | `string` |  | - |
| File Upload | `boolean` | Allow file upload on the chat | - |
| Pinecone Text Key | `string` | The key in the metadata for storing text. Default to  | - |
| Pinecone Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Pinecone`

## Common Use Cases

1. Use Pinecone when you need upsert embedded data and perform similarity or mmr search using pinecone, a leading fully managed hosted vector database
2. Connect to other nodes that accept `Pinecone` input

---

**Source**: `packages/components/nodes/vectorstores/Pinecone/Pinecone.ts`