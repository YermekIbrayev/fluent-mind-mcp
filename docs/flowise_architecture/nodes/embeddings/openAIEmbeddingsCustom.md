# OpenAI Embeddings Custom

**Category**: Embeddings | **Type**: OpenAIEmbeddingsCustom | **Version**: 3.0

---

## Overview

OpenAI API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- openAIApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Strip New Lines | `boolean` |  | - |
| Batch Size | `number` |  | - |
| Timeout | `number` |  | - |
| BasePath | `string` |  | - |
| BaseOptions | `json` |  | - |
| Model Name | `string` |  | - |
| Dimensions | `number` |  | - |

## Connections

**Outputs**: `OpenAIEmbeddingsCustom`

## Common Use Cases

1. Use OpenAI Embeddings Custom when you need openai api to generate embeddings for a given text
2. Connect to other nodes that accept `OpenAIEmbeddingsCustom` input

---

**Source**: `packages/components/nodes/embeddings/OpenAIEmbeddingCustom/OpenAIEmbeddingCustom.ts`