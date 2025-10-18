# Embeddings Filter Retriever

**Category**: Retrievers | **Type**: EmbeddingsFilterRetriever | **Version**: 1.0

---

## Overview

A document compressor that uses embeddings to drop documents unrelated to the query

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store Retriever | `VectorStoreRetriever` |  | - |
| Embeddings | `Embeddings` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |
| Similarity Threshold | `number` | Threshold for determining when two documents are similar enough to be considered redundant. Must be  | - |
| K | `number` | The number of relevant documents to return. Can be explicitly set to undefined, in which case simila | - |

## Connections

**Accepts Inputs From**:
- Vector Store Retriever (`VectorStoreRetriever`)
- Embeddings (`Embeddings`)

**Outputs**: `EmbeddingsFilterRetriever`

## Common Use Cases

1. Use Embeddings Filter Retriever when you need a document compressor that uses embeddings to drop documents unrelated to the query
2. Connect to other nodes that accept `EmbeddingsFilterRetriever` input

---

**Source**: `packages/components/nodes/retrievers/EmbeddingsFilterRetriever/EmbeddingsFilterRetriever.ts`