# TogetherAIEmbedding

**Category**: Embeddings | **Type**: TogetherAIEmbedding | **Version**: 1.0

---

## Overview

TogetherAI Embedding models to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- togetherAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` | Refer to <a target= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `TogetherAIEmbedding`

## Common Use Cases

1. Use TogetherAIEmbedding when you need togetherai embedding models to generate embeddings for a given text
2. Connect to other nodes that accept `TogetherAIEmbedding` input

---

**Source**: `packages/components/nodes/embeddings/TogetherAIEmbedding/TogetherAIEmbedding.ts`