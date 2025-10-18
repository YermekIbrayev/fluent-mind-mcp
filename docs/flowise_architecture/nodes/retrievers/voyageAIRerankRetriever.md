# Voyage AI Rerank Retriever

**Category**: Retrievers | **Type**: VoyageAIRerankRetriever | **Version**: 1.0

---

## Overview

Voyage AI Rerank indexes the documents from most to least semantically relevant to the query.

## Credentials

**Required**: Yes

**Credential Types**:
- voyageAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Vector Store Retriever | `VectorStoreRetriever` |  | - |
| Model Name | `options` |  | - |

## Connections

**Accepts Inputs From**:
- Vector Store Retriever (`VectorStoreRetriever`)

**Outputs**: `VoyageAIRerankRetriever`

## Common Use Cases

1. Use Voyage AI Rerank Retriever when you need voyage ai rerank indexes the documents from most to least semantically relevant to the query.
2. Connect to other nodes that accept `VoyageAIRerankRetriever` input

---

**Source**: `packages/components/nodes/retrievers/VoyageAIRetriever/VoyageAIRerankRetriever.ts`