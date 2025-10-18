# OpenAI Embedding

**Category**: Embeddings | **Type**: OpenAIEmbedding | **Version**: 2.0

---

## Overview

OpenAI Embedding specific for LlamaIndex

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
| Timeout | `number` |  | - |
| BasePath | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `OpenAIEmbedding`

## Common Use Cases

1. Use OpenAI Embedding when you need openai embedding specific for llamaindex
2. Connect to other nodes that accept `OpenAIEmbedding` input

---

**Source**: `packages/components/nodes/embeddings/OpenAIEmbedding/OpenAIEmbedding_LlamaIndex.ts`