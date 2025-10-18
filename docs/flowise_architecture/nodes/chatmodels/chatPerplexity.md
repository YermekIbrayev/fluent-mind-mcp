# ChatPerplexity

**Category**: Chat Models | **Type**: ChatPerplexity | **Version**: 0.1

---

## Overview

Wrapper around Perplexity large language models that use the Chat endpoint

## Credentials

**Required**: Yes

**Credential Types**:
- perplexityApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | sonar |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Top P | `number` |  | - |
| Top K | `number` |  | - |
| Presence Penalty | `number` |  | - |
| Frequency Penalty | `number` |  | - |
| Streaming | `boolean` |  | - |
| Timeout | `number` | Limit citations to URLs from specified domains (e.g., [ | - |
| Proxy Url | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `ChatPerplexity`

## Common Use Cases

1. Use ChatPerplexity when you need wrapper around perplexity large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatPerplexity` input

---

**Source**: `packages/components/nodes/chatmodels/ChatPerplexity/ChatPerplexity.ts`