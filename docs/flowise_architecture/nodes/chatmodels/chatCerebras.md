# ChatCerebras

**Category**: Chat Models | **Type**: ChatCerebras | **Version**: 2.0

---

## Overview

Wrapper around Cerebras Inference API

## Credentials

**Required**: Yes

**Credential Types**:
- cerebrasAIApi

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
| BasePath | `string` |  | https://api.cerebras.ai/v1 |
| BaseOptions | `json` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatCerebras`

## Common Use Cases

1. Use ChatCerebras when you need wrapper around cerebras inference api
2. Connect to other nodes that accept `ChatCerebras` input

---

**Source**: `packages/components/nodes/chatmodels/ChatCerebras/ChatCerebras.ts`