# ChatTogetherAI

**Category**: Chat Models | **Type**: ChatTogetherAI | **Version**: 2.0

---

## Overview

Wrapper around TogetherAI large language models

## Credentials

**Required**: Yes

**Credential Types**:
- togetherAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` | Refer to <a target= | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatTogetherAI`

## Common Use Cases

1. Use ChatTogetherAI when you need wrapper around togetherai large language models
2. Connect to other nodes that accept `ChatTogetherAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatTogetherAI/ChatTogetherAI.ts`