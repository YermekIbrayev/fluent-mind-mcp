# OpenAI Embeddings

**Category**: Embeddings | **Type**: OpenAIEmbeddings | **Version**: 4.0

---

## Overview

OpenAI API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- openAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | text-embedding-ada-002 |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Strip New Lines | `boolean` |  | - |
| Batch Size | `number` |  | - |
| Timeout | `number` |  | - |
| BasePath | `string` |  | - |
| Dimensions | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `OpenAIEmbeddings`

## Common Use Cases

1. Use OpenAI Embeddings when you need openai api to generate embeddings for a given text
2. Connect to other nodes that accept `OpenAIEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/OpenAIEmbedding/OpenAIEmbedding.ts`