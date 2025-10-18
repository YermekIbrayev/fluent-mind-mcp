# Custom Retriever

**Category**: Retrievers | **Type**: CustomRetriever | **Version**: 1.0

---

## Overview

Return results based on predefined format

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store | `VectorStore` |  | - |
| Result Format | `string` | Format to return the results in. Use {{context}} to insert the pageContent of the document and {{met | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |
| Top K | `number` | Number of top results to fetch. Default to vector store topK | - |

## Connections

**Accepts Inputs From**:
- Vector Store (`VectorStore`)

**Outputs**: `CustomRetriever`

## Common Use Cases

1. Use Custom Retriever when you need return results based on predefined format
2. Connect to other nodes that accept `CustomRetriever` input

---

**Source**: `packages/components/nodes/retrievers/CustomRetriever/CustomRetriever.ts`