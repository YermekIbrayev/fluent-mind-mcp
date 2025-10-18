# SingleStore

**Category**: Vector Stores | **Type**: SingleStore | **Version**: 1.0

---

## Overview

Upsert embedded data and perform similarity search upon query using SingleStore, a fast and distributed cloud relational database

## Credentials

**Required**: Yes

**Credential Types**:
- singleStoreApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Host | `string` |  | - |
| Database | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Table Name | `string` |  | - |
| Content Column Name | `string` |  | - |
| Vector Column Name | `string` |  | - |
| Metadata Column Name | `string` |  | - |
| Top K | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `SingleStore`

## Common Use Cases

1. Use SingleStore when you need upsert embedded data and perform similarity search upon query using singlestore, a fast and distributed cloud relational database
2. Connect to other nodes that accept `SingleStore` input

---

**Source**: `packages/components/nodes/vectorstores/Singlestore/Singlestore.ts`