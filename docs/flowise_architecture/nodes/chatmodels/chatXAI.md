# ChatXAI

**Category**: Chat Models | **Type**: ChatXAI | **Version**: 2.0

---

## Overview

Wrapper around Grok from XAI

## Credentials

**Required**: Yes

**Credential Types**:
- xaiApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| Max Tokens | `number` |  | - |
| Max Tokens | `number` |  | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatXAI`

## Common Use Cases

1. Use ChatXAI when you need wrapper around grok from xai
2. Connect to other nodes that accept `ChatXAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatXAI/ChatXAI.ts`