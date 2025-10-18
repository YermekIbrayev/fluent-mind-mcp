# Chat NVIDIA NIM

**Category**: Chat Models | **Type**: ChatNvidiaNIM | **Version**: 1.1

---

## Overview

Wrapper around NVIDIA NIM Inference API

## Credentials

**Required**: Yes

**Credential Types**:
- nvidiaNIMApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `string` |  | - |
| Base Path | `string` | Specify the URL of the deployed NIM Inference API | - |

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
| Base Options | `json` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatNvidiaNIM`

## Common Use Cases

1. Use Chat NVIDIA NIM when you need wrapper around nvidia nim inference api
2. Connect to other nodes that accept `ChatNvidiaNIM` input

---

**Source**: `packages/components/nodes/chatmodels/ChatNvdiaNIM/ChatNvdiaNIM.ts`