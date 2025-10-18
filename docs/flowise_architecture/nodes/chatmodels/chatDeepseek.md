# ChatDeepseek

**Category**: Chat Models | **Type**: chatDeepseek | **Version**: 1.0

---

## Overview

Wrapper around Deepseek large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- deepseekApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | deepseek-chat |

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
| Stop Sequence | `string` | List of stop words to use when generating. Use comma to separate multiple stop words. | - |
| Base Options | `json` | Additional options to pass to the Deepseek client. This should be a JSON object. | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `chatDeepseek`

## Common Use Cases

1. Use ChatDeepseek when you need wrapper around deepseek large language models that use the chat endpoint
2. Connect to other nodes that accept `chatDeepseek` input

---

**Source**: `packages/components/nodes/chatmodels/Deepseek/Deepseek.ts`