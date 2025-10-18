# OpenSearch

**Category**: Vector Stores | **Type**: OpenSearch | **Version**: 3.0

---

## Overview

Upsert embedded data and perform similarity search upon query using OpenSearch, an open-source, all-in-one vector database

## Credentials

**Required**: Yes

**Credential Types**:
- openSearchUrl

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Index Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `OpenSearch`

## Common Use Cases

1. Use OpenSearch when you need upsert embedded data and perform similarity search upon query using opensearch, an open-source, all-in-one vector database
2. Connect to other nodes that accept `OpenSearch` input

---

**Source**: `packages/components/nodes/vectorstores/OpenSearch/OpenSearch.ts`