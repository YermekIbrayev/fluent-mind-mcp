# ChatAnthropic

**Category**: Chat Models | **Type**: ChatAnthropic | **Version**: 8.0

---

## Overview

Wrapper around ChatAnthropic large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- anthropicApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | claude-3-haiku |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| Max Tokens | `number` |  | - |
| Top P | `number` |  | - |
| Top K | `number` |  | - |
| Extended Thinking | `boolean` | Enable extended thinking for reasoning model such as Claude Sonnet 3.7 | - |
| Budget Tokens | `number` | Maximum number of tokens Claude is allowed use for its internal reasoning process | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `ChatAnthropic`

## Common Use Cases

1. Use ChatAnthropic when you need wrapper around chatanthropic large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatAnthropic` input

---

**Source**: `packages/components/nodes/chatmodels/ChatAnthropic/ChatAnthropic.ts`