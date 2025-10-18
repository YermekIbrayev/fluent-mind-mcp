# Jina AI Rerank Retriever

**Category**: Retrievers | **Type**: JinaRerankRetriever | **Version**: 1.0

---

## Overview

Jina AI Rerank indexes the documents from most to least semantically relevant to the query.

## Credentials

**Required**: Yes

**Credential Types**:
- jinaAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store Retriever | `VectorStoreRetriever` |  | - |
| Model Name | `options` |  | - |

## Connections

**Accepts Inputs From**:
- Vector Store Retriever (`VectorStoreRetriever`)

**Outputs**: `JinaRerankRetriever`

## Common Use Cases

1. Use Jina AI Rerank Retriever when you need jina ai rerank indexes the documents from most to least semantically relevant to the query.
2. Connect to other nodes that accept `JinaRerankRetriever` input

---

**Source**: `packages/components/nodes/retrievers/JinaRerankRetriever/JinaRerankRetriever.ts`