# Vector Store Retriever

**Category**: Retrievers | **Type**: VectorStoreRetriever | **Version**: 1.0

---

## Overview

Store vector store as retriever to be later queried by MultiRetrievalQAChain

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store | `VectorStore` |  | - |
| Retriever Name | `string` |  | - |
| Retriever Description | `string` | Description of when to use the vector store retriever | - |

## Connections

**Accepts Inputs From**:
- Vector Store (`VectorStore`)

**Outputs**: `VectorStoreRetriever`

## Common Use Cases

1. Use Vector Store Retriever when you need store vector store as retriever to be later queried by multiretrievalqachain
2. Connect to other nodes that accept `VectorStoreRetriever` input

---

**Source**: `packages/components/nodes/retrievers/VectorStoreRetriever/VectorStoreRetriever.ts`