# HuggingFace Inference Embeddings

**Category**: Embeddings | **Type**: HuggingFaceInferenceEmbeddings | **Version**: 1.0

---

## Overview

HuggingFace Inference API to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- huggingFaceApi

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `string` | If using own inference endpoint, leave this blank | - |
| Endpoint | `string` | Using your own inference endpoint | - |

## Connections

**Outputs**: `HuggingFaceInferenceEmbeddings`

## Common Use Cases

1. Use HuggingFace Inference Embeddings when you need huggingface inference api to generate embeddings for a given text
2. Connect to other nodes that accept `HuggingFaceInferenceEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/HuggingFaceInferenceEmbedding/HuggingFaceInferenceEmbedding.ts`