# Similarity Score Threshold Retriever

**Category**: Retrievers | **Type**: SimilarityThresholdRetriever | **Version**: 2.0

---

## Overview

Return results based on the minimum similarity percentage

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store | `VectorStore` |  | - |
| Minimum Similarity Score (%) | `number` | Finds results with at least this similarity score | - |
| Max K | `number` | The maximum number of results to fetch | - |
| K Increment | `number` | How much to increase K by each time. It | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |

## Connections

**Accepts Inputs From**:
- Vector Store (`VectorStore`)

**Outputs**: `SimilarityThresholdRetriever`

## Common Use Cases

1. Use Similarity Score Threshold Retriever when you need return results based on the minimum similarity percentage
2. Connect to other nodes that accept `SimilarityThresholdRetriever` input

---

**Source**: `packages/components/nodes/retrievers/SimilarityThresholdRetriever/SimilarityThresholdRetriever.ts`