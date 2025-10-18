# GoogleVertexAI Embeddings

**Category**: Embeddings | **Type**: GoogleVertexAIEmbeddings | **Version**: 2.1

---

## Overview

Google vertexAI API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- googleVertexAuth

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | text-embedding-004 |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Region | `asyncOptions` | Region to use for the model. | - |
| Strip New Lines | `boolean` | Remove new lines from input text before embedding to reduce token count | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)
- Region (`asyncOptions`)

**Outputs**: `GoogleVertexAIEmbeddings`

## Common Use Cases

1. Use GoogleVertexAI Embeddings when you need google vertexai api to generate embeddings for a given text
2. Connect to other nodes that accept `GoogleVertexAIEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/GoogleVertexAIEmbedding/GoogleVertexAIEmbedding.ts`