# IBM Watsonx Embeddings

**Category**: Embeddings | **Type**: WatsonxEmbeddings | **Version**: 1.0

---

## Overview

Generate embeddings for a given text using open source model on IBM Watsonx

## Credentials

**Required**: Yes

**Credential Types**:
- ibmWatsonx

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` |  | ibm/slate-30m-english-rtrvr |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Truncate Input Tokens | `number` | Truncate the input tokens. | - |
| Max Retries | `number` | The maximum number of retries. | - |
| Max Concurrency | `number` | The maximum number of concurrencies. | - |

## Connections

**Outputs**: `WatsonxEmbeddings`

## Common Use Cases

1. Use IBM Watsonx Embeddings when you need generate embeddings for a given text using open source model on ibm watsonx
2. Connect to other nodes that accept `WatsonxEmbeddings` input

---

**Source**: `packages/components/nodes/embeddings/IBMWatsonxEmbedding/IBMWatsonxEmbedding.ts`