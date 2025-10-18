# AWS Bedrock Embeddings

**Category**: Embeddings | **Type**: AWSBedrockEmbeddings | **Version**: 5.0

---

## Overview

AWSBedrock embedding models to generate embeddings for a given text

## Credentials

**Required**: Yes

**Credential Types**:
- awsApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Region | `asyncOptions` |  | us-east-1 |
| Model Name | `asyncOptions` |  | amazon.titan-embed-text-v1 |
| Cohere Input Type | `options` | Specifies the type of input passed to the model. Required for cohere embedding models v3 and higher. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Custom Model Name | `string` | If provided, will override model selected from Model Name option | - |

## Connections

**Accepts Inputs From**:
- Region (`asyncOptions`)
- Model Name (`asyncOptions`)

**Outputs**: `AWSBedrockEmbeddings`

## Common Use Cases

1. Use AWS Bedrock Embeddings when you need awsbedrock embedding models to generate embeddings for a given text
2. Connect to other nodes that accept `AWSBedrockEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/AWSBedrockEmbedding/AWSBedrockEmbedding.ts`