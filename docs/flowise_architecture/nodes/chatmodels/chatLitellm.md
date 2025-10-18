# ChatLitellm

**Category**: Chat Models | **Type**: ChatLitellm | **Version**: 1.0

---

## Overview

Connect to a Litellm server using OpenAI-compatible API

## Credentials

**Required**: Yes

**Credential Types**:
- litellmApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base URL | `string` |  | - |
| Model Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |
| Max Tokens | `number` |  | - |
| Top P | `number` |  | - |
| Timeout | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatLitellm`

## Common Use Cases

1. Use ChatLitellm when you need connect to a litellm server using openai-compatible api
2. Connect to other nodes that accept `ChatLitellm` input

---

**Source**: `packages/components/nodes/chatmodels/ChatLitellm/ChatLitellm.ts`