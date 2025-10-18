# ChatOpenAI

**Category**: Chat Models | **Type**: ChatOpenAI | **Version**: 8.3

---

## Overview

Wrapper around OpenAI large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- openAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | gpt-4o-mini |
| Image Resolution | `options` | This parameter controls the resolution in which the model views the image. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| Max Tokens | `number` |  | - |
| Top Probability | `number` |  | - |
| Frequency Penalty | `number` |  | - |
| Presence Penalty | `number` |  | - |
| Timeout | `number` |  | - |
| Strict Tool Calling | `boolean` | Whether the model supports the  | - |
| Stop Sequence | `string` | List of stop words to use when generating. Use comma to separate multiple stop words. | - |
| BasePath | `string` |  | - |
| Proxy Url | `string` |  | - |
| BaseOptions | `json` |  | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `ChatOpenAI`

## Common Use Cases

1. Use ChatOpenAI when you need wrapper around openai large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatOpenAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatOpenAI/ChatOpenAI.ts`