# ChatOpenRouter

**Category**: Chat Models | **Type**: ChatOpenRouter | **Version**: 1.0

---

## Overview

Wrapper around Open Router Inference API

## Credentials

**Required**: Yes

**Credential Types**:
- openRouterApi

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
| BasePath | `string` |  | https://openrouter.ai/api/v1 |
| BaseOptions | `json` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatOpenRouter`

## Common Use Cases

1. Use ChatOpenRouter when you need wrapper around open router inference api
2. Connect to other nodes that accept `ChatOpenRouter` input

---

**Source**: `packages/components/nodes/chatmodels/ChatOpenRouter/ChatOpenRouter.ts`