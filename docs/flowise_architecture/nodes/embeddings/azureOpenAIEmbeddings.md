# Azure OpenAI Embeddings

**Category**: Embeddings | **Type**: AzureOpenAIEmbeddings | **Version**: 2.0

---

## Overview

Azure OpenAI API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- azureOpenAIApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Batch Size | `number` |  | 100 |
| Timeout | `number` |  | - |
| BasePath | `string` |  | - |
| BaseOptions | `json` |  | - |

## Connections

**Outputs**: `AzureOpenAIEmbeddings`

## Common Use Cases

1. Use Azure OpenAI Embeddings when you need azure openai api to generate embeddings for a given text
2. Connect to other nodes that accept `AzureOpenAIEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/AzureOpenAIEmbedding/AzureOpenAIEmbedding.ts`