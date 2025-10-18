# Jina Embeddings

**Category**: Embeddings | **Type**: JinaEmbeddings | **Version**: 3.0

---

## Overview

JinaAI API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- jinaAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` | Refer to <a href= | jina-embeddings-v3 |
| Dimensions | `number` | Refer to <a href= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Allow Late Chunking | `boolean` | Refer to <a href= | - |

## Connections

**Outputs**: `JinaEmbeddings`

## Common Use Cases

1. Use Jina Embeddings when you need jinaai api to generate embeddings for a given text
2. Connect to other nodes that accept `JinaEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/JinaAIEmbedding/JinaAIEmbedding.ts`