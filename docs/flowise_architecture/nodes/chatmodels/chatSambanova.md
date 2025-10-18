# ChatSambanova

**Category**: Chat Models | **Type**: ChatSambanova | **Version**: 1.0

---

## Overview

Wrapper around Sambanova Chat Endpoints

## Credentials

**Required**: Yes

**Credential Types**:
- sambanovaApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `string` |  | Meta-Llama-3.3-70B-Instruct |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| BasePath | `string` |  | htps://api.sambanova.ai/v1 |
| BaseOptions | `json` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatSambanova`

## Common Use Cases

1. Use ChatSambanova when you need wrapper around sambanova chat endpoints
2. Connect to other nodes that accept `ChatSambanova` input

---

**Source**: `packages/components/nodes/chatmodels/ChatSambanova/ChatSambanova.ts`