# GoogleGenerativeAI Embeddings

**Category**: Embeddings | **Type**: GoogleGenerativeAiEmbeddings | **Version**: 2.0

---

## Overview

Google Generative API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- googleGenerativeAI

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | embedding-001 |
| Task Type | `options` | Type of task for which the embedding will be used | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `GoogleGenerativeAiEmbeddings`

## Common Use Cases

1. Use GoogleGenerativeAI Embeddings when you need google generative api to generate embeddings for a given text
2. Connect to other nodes that accept `GoogleGenerativeAiEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/GoogleGenerativeAIEmbedding/GoogleGenerativeAIEmbedding.ts`