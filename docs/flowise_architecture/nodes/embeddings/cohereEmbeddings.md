# Cohere Embeddings

**Category**: Embeddings | **Type**: CohereEmbeddings | **Version**: 3.0

---

## Overview

Cohere API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- cohereApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | embed-english-v2.0 |
| Type | `options` | Specifies the type of input passed to the model. Required for embedding models v3 and higher. <a tar | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `CohereEmbeddings`

## Common Use Cases

1. Use Cohere Embeddings when you need cohere api to generate embeddings for a given text
2. Connect to other nodes that accept `CohereEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/CohereEmbedding/CohereEmbedding.ts`