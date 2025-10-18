# Azure ChatOpenAI

**Category**: Chat Models | **Type**: AzureChatOpenAI | **Version**: 7.1

---

## Overview

Wrapper around Azure OpenAI large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- azureOpenAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | - |
| Image Resolution | `options` | This parameter controls the resolution in which the model views the image. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Streaming | `boolean` |  | - |
| Top Probability | `number` |  | - |
| Frequency Penalty | `number` |  | - |
| Presence Penalty | `number` |  | - |
| Timeout | `number` |  | - |
| BasePath | `string` |  | - |
| BaseOptions | `json` |  | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `AzureChatOpenAI`

## Common Use Cases

1. Use Azure ChatOpenAI when you need wrapper around azure openai large language models that use the chat endpoint
2. Connect to other nodes that accept `AzureChatOpenAI` input

---

**Source**: `packages/components/nodes/chatmodels/AzureChatOpenAI/AzureChatOpenAI.ts`