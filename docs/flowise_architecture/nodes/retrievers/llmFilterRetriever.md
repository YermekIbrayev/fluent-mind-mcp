# LLM Filter Retriever

**Category**: Retrievers | **Type**: LLMFilterRetriever | **Version**: 1.0

---

## Overview

Iterate over the initially returned documents and extract, from each, only the content that is relevant to the query

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store Retriever | `VectorStoreRetriever` |  | - |
| Language Model | `BaseLanguageModel` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |

## Connections

**Accepts Inputs From**:
- Vector Store Retriever (`VectorStoreRetriever`)
- Language Model (`BaseLanguageModel`)

**Outputs**: `LLMFilterRetriever`

## Common Use Cases

1. Use LLM Filter Retriever when you need iterate over the initially returned documents and extract, from each, only the content that is relevant to the query
2. Connect to other nodes that accept `LLMFilterRetriever` input

---

**Source**: `packages/components/nodes/retrievers/LLMFilterRetriever/LLMFilterCompressionRetriever.ts`