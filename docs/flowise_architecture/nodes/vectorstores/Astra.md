# Astra

**Category**: Vector Stores | **Type**: Astra | **Version**: 2.0

---

## Overview

Upsert embedded data and perform similarity or mmr search upon query using DataStax Astra DB, a serverless vector database that’s perfect for managing mission-critical AI workloads

## Credentials

**Required**: Yes

**Credential Types**:
- AstraDBApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Namespace | `string` |  | - |
| Collection | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Vector Dimension | `number` | Dimension used for storing vector embedding | - |
| Similarity Metric | `string` | cosine | euclidean | dot_product | - |
| Top K | `number` | Number of top results to fetch. Default to 4 | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Astra`

## Common Use Cases

1. Use Astra when you need upsert embedded data and perform similarity or mmr search upon query using datastax astra db, a serverless vector database that’s perfect for managing mission-critical ai workloads
2. Connect to other nodes that accept `Astra` input

---

**Source**: `packages/components/nodes/vectorstores/Astra/Astra.ts`