# MongoDB Atlas

**Category**: Vector Stores | **Type**: MongoDB Atlas | **Version**: 1.0

---

## Overview

Upsert embedded data and perform similarity or mmr search upon query using MongoDB Atlas, a managed cloud mongodb database

## Credentials

**Required**: Yes

**Credential Types**:
- mongoDBUrlApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Database | `string` |  | - |
| Collection Name | `string` |  | - |
| Index Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Content Field | `string` | Name of the field (column) that contains the actual content | text |
| Embedded Field | `string` | Name of the field (column) that contains the Embedding | embedding |
| Mongodb Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `MongoDB Atlas`

## Common Use Cases

1. Use MongoDB Atlas when you need upsert embedded data and perform similarity or mmr search upon query using mongodb atlas, a managed cloud mongodb database
2. Connect to other nodes that accept `MongoDB Atlas` input

---

**Source**: `packages/components/nodes/vectorstores/MongoDBAtlas/MongoDBAtlas.ts`