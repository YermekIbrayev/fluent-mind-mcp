# Couchbase

**Category**: Vector Stores | **Type**: Couchbase | **Version**: 1.0

---

## Overview

Upsert embedded data and load existing index using Couchbase, a award-winning distributed NoSQL database

## Credentials

**Required**: Yes

**Credential Types**:
- couchbaseApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Bucket Name | `string` |  | - |
| Scope Name | `string` |  | - |
| Collection Name | `string` |  | - |
| Index Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Content Field | `string` | Name of the field (column) that contains the actual content | text |
| Embedded Field | `string` | Name of the field (column) that contains the Embedding | embedding |
| Couchbase Metadata Filter | `json` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Couchbase`

## Common Use Cases

1. Use Couchbase when you need upsert embedded data and load existing index using couchbase, a award-winning distributed nosql database
2. Connect to other nodes that accept `Couchbase` input

---

**Source**: `packages/components/nodes/vectorstores/Couchbase/Couchbase.ts`