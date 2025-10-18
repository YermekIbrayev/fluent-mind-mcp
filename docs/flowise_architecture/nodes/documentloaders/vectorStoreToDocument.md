# VectorStore To Document

**Category**: Document Loaders | **Type**: Document | **Version**: 2.0

---

## Overview

Search documents with scores from vector store

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store | `VectorStore` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Query | `string` | Query to retrieve documents from vector database. If not specified, user question will be used | - |
| Minimum Score (%) | `number` | Minumum score for embeddings documents to be included | - |

## Connections

**Accepts Inputs From**:
- Vector Store (`VectorStore`)

**Outputs**: `Document`

## Common Use Cases

1. Use VectorStore To Document when you need search documents with scores from vector store
2. Connect to other nodes that accept `Document` input

---

**Source**: `packages/components/nodes/documentloaders/VectorStoreToDocument/VectorStoreToDocument.ts`