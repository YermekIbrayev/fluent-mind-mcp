# ChatCometAPI

**Category**: Chat Models | **Type**: ChatCometAPI | **Version**: 1.0

---

## Overview

Wrapper around CometAPI large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- cometApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` | Enter the model name (e.g., gpt-5-mini, claude-sonnet-4-20250514, gemini-2.0-flash) | gpt-5-mini |

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
| Base Options | `json` | Additional options to pass to the CometAPI client. This should be a JSON object. | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatCometAPI`

## Common Use Cases

1. Use ChatCometAPI when you need wrapper around cometapi large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatCometAPI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatCometAPI/ChatCometAPI.ts`