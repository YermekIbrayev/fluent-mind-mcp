# ChatFireworks

**Category**: Chat Models | **Type**: ChatFireworks | **Version**: 2.0

---

## Overview

Wrapper around Fireworks Chat Endpoints

## Credentials

**Required**: Yes

**Credential Types**:
- fireworksApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `string` |  | accounts/fireworks/models/llama-v3p1-8b-instruct |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatFireworks`

## Common Use Cases

1. Use ChatFireworks when you need wrapper around fireworks chat endpoints
2. Connect to other nodes that accept `ChatFireworks` input

---

**Source**: `packages/components/nodes/chatmodels/ChatFireworks/ChatFireworks.ts`