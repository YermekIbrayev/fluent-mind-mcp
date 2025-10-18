# ChatOpenAI Custom

**Category**: Chat Models | **Type**: ChatOpenAI-Custom | **Version**: 4.0

---

## Overview

Custom/FineTuned model using OpenAI Chat compatible API

## Credentials

**Required**: Yes

**Credential Types**:
- openAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` |  | - |

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
| BasePath | `string` |  | - |
| BaseOptions | `json` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatOpenAI-Custom`

## Common Use Cases

1. Use ChatOpenAI Custom when you need custom/finetuned model using openai chat compatible api
2. Connect to other nodes that accept `ChatOpenAI-Custom` input

---

**Source**: `packages/components/nodes/chatmodels/ChatOpenAICustom/ChatOpenAICustom.ts`