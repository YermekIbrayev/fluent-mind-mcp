# Meilisearch

**Category**: Vector Stores | **Type**: Meilisearch | **Version**: 1.0

---

## Overview

Upsert embedded data and perform similarity search upon query using Meilisearch hybrid search functionality

## Credentials

**Required**: Yes

**Credential Types**:
- meilisearchApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Embeddings | `Embeddings` |  | - |
| Host | `string` | This is the URL for the desired Meilisearch instance, the URL must not end with a  | - |
| Index Uid | `string` | UID for the index to answer from | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Document | `Document` |  | - |
| Delete Index if exists | `boolean` |  | - |
| Top K | `number` | number of top searches to return as context, default is 4 | - |
| Semantic Ratio | `number` | percentage of sematic reasoning in meilisearch hybrid search, default is 0.75 | - |
| Search Filter | `string` | search filter to apply on searchable attributes | - |

## Connections

**Accepts Inputs From**:
- Document (`Document`)
- Embeddings (`Embeddings`)

**Outputs**: `Meilisearch`

## Common Use Cases

1. Use Meilisearch when you need upsert embedded data and perform similarity search upon query using meilisearch hybrid search functionality
2. Connect to other nodes that accept `Meilisearch` input

---

**Source**: `packages/components/nodes/vectorstores/Meilisearch/Meilisearch.ts`