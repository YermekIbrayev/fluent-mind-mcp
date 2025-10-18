# ChatGoogleGenerativeAI

**Category**: Chat Models | **Type**: ChatGoogleGenerativeAI | **Version**: 3.1

---

## Overview

Wrapper around Google Gemini large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- googleGenerativeAI

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | gemini-1.5-flash-latest |
| Safety Settings | `array` | Safety settings for the model. Refer to the <a href= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Custom Model Name | `string` | Custom model name to use. If provided, it will override the model selected | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| Max Output Tokens | `number` |  | - |
| Top Probability | `number` |  | - |
| Top Next Highest Probability Tokens | `number` | Decode using top-k sampling: consider the set of top_k most probable tokens. Must be positive | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)
- Safety Settings (`array`)

**Outputs**: `ChatGoogleGenerativeAI`

## Common Use Cases

1. Use ChatGoogleGenerativeAI when you need wrapper around google gemini large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatGoogleGenerativeAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatGoogleGenerativeAI/ChatGoogleGenerativeAI.ts`