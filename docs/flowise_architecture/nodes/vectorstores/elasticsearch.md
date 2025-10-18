# Elasticsearch

**Category**: Vector Stores | **Type**: Elasticsearch | **Version**: 2.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Elasticsearch, a distributed search and analytics engine

## Credentials

**Required**: Yes

**Credential Types**:
- elasticsearchApi
- elasticSearchUserPassword

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Index Name | `string` |  | - |
| Similarity | `options` | Similarity measure used in Elasticsearch. | l2_norm |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Record Manager | `RecordManager` | Keep track of the record to prevent duplication | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)
- Record Manager (`RecordManager`)

**Outputs**: `Elasticsearch`

## Common Use Cases

1. Use Elasticsearch when you need upsert embedded data and perform similarity search upon query using elasticsearch, a distributed search and analytics engine
2. Connect to other nodes that accept `Elasticsearch` input

---

**Source**: `packages/components/nodes/vectorstores/Elasticsearch/Elasticsearch.ts`