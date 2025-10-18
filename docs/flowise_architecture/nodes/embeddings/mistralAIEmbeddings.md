# MistralAI Embeddings

**Category**: Embeddings | **Type**: MistralAIEmbeddings | **Version**: 2.0

---

## Overview

MistralAI API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- mistralAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | mistral-embed |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Batch Size | `number` |  | - |
| Strip New Lines | `boolean` |  | - |
| Override Endpoint | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `MistralAIEmbeddings`

## Common Use Cases

1. Use MistralAI Embeddings when you need mistralai api to generate embeddings for a given text
2. Connect to other nodes that accept `MistralAIEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/MistralEmbedding/MistralEmbedding.ts`