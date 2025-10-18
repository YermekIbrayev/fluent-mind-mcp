# ChatLocalAI

**Category**: Chat Models | **Type**: ChatLocalAI | **Version**: 3.0

---

## Overview

Use local LLMs like llama.cpp, gpt4all using LocalAI

## Credentials

**Required**: Yes

**Credential Types**:
- localAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base Path | `string` |  | - |
| Model Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| Max Tokens | `number` |  | - |
| Top Probability | `number` |  | - |
| Timeout | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatLocalAI`

## Common Use Cases

1. Use ChatLocalAI when you need use local llms like llama.cpp, gpt4all using localai
2. Connect to other nodes that accept `ChatLocalAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatLocalAI/ChatLocalAI.ts`