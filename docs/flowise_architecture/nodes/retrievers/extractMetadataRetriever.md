# Extract Metadata Retriever

**Category**: Retrievers | **Type**: ExtractMetadataRetriever | **Version**: 1.0

---

## Overview

Extract keywords/metadata from the query and use it to filter documents

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store | `VectorStore` |  | - |
| Chat Model | `BaseChatModel` |  | - |
| Prompt | `string` | Prompt to extract metadata from query | - |
| JSON Structured Output | `datagrid` | Instruct the model to give output in a JSON structured schema. This output will be used as the metad | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from retriever. If not specified, user question will be used | - |

## Connections

**Accepts Inputs From**:
- Vector Store (`VectorStore`)
- Chat Model (`BaseChatModel`)
- JSON Structured Output (`datagrid`)

**Outputs**: `ExtractMetadataRetriever`

## Common Use Cases

1. Use Extract Metadata Retriever when you need extract keywords/metadata from the query and use it to filter documents
2. Connect to other nodes that accept `ExtractMetadataRetriever` input

---

**Source**: `packages/components/nodes/retrievers/ExtractMetadataRetriever/ExtractMetadataRetriever.ts`