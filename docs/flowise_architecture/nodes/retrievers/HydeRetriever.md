# HyDE Retriever

**Category**: Retrievers | **Type**: HydeRetriever | **Version**: 3.0

---

## Overview

Use HyDE retriever to retrieve from a vector store

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Language Model | `BaseLanguageModel` |  | - |
| Vector Store | `VectorStore` |  | - |
| Select Defined Prompt | `options` | Select a pre-defined prompt | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |

## Connections

**Accepts Inputs From**:
- Language Model (`BaseLanguageModel`)
- Vector Store (`VectorStore`)

**Outputs**: `HydeRetriever`

## Common Use Cases

1. Use HyDE Retriever when you need use hyde retriever to retrieve from a vector store
2. Connect to other nodes that accept `HydeRetriever` input

---

**Source**: `packages/components/nodes/retrievers/HydeRetriever/HydeRetriever.ts`