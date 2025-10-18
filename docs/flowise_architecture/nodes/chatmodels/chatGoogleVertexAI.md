# ChatGoogleVertexAI

**Category**: Chat Models | **Type**: ChatGoogleVertexAI | **Version**: 5.3

---

## Overview

Wrapper around VertexAI large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- googleVertexAuth

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Region | `asyncOptions` | Region to use for the model. | - |
| Custom Model Name | `string` | Custom model name to use. If provided, it will override the model selected | - |
| Temperature | `number` |  | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |
| Streaming | `boolean` |  | - |
| Max Output Tokens | `number` |  | - |
| Top Probability | `number` |  | - |
| Top Next Highest Probability Tokens | `number` | Decode using top-k sampling: consider the set of top_k most probable tokens. Must be positive | - |
| Thinking Budget | `number` | Number of tokens to use for thinking process (0 to disable) | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Region (`asyncOptions`)
- Model Name (`asyncOptions`)

**Outputs**: `ChatGoogleVertexAI`

## Common Use Cases

1. Use ChatGoogleVertexAI when you need wrapper around vertexai large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatGoogleVertexAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatGoogleVertexAI/ChatGoogleVertexAI.ts`