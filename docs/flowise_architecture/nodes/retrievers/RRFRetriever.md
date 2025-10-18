# Reciprocal Rank Fusion Retriever

**Category**: Retrievers | **Type**: RRFRetriever | **Version**: 1.0

---

## Overview

Reciprocal Rank Fusion to re-rank search results by multiple query generation.

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store Retriever | `VectorStoreRetriever` |  | - |
| Language Model | `BaseLanguageModel` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |
| Query Count | `number` | Number of synthetic queries to generate. Default to 4 | - |
| Top K | `number` | Number of top results to fetch. Default to the TopK of the Base Retriever | - |
| Constant | `number` | A constant added to the rank, controlling the balance between the importance of high-ranked items an | - |

## Connections

**Accepts Inputs From**:
- Vector Store Retriever (`VectorStoreRetriever`)
- Language Model (`BaseLanguageModel`)

**Outputs**: `RRFRetriever`

## Common Use Cases

1. Use Reciprocal Rank Fusion Retriever when you need reciprocal rank fusion to re-rank search results by multiple query generation.
2. Connect to other nodes that accept `RRFRetriever` input

---

**Source**: `packages/components/nodes/retrievers/RRFRetriever/RRFRetriever.ts`