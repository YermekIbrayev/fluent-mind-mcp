# ChatAlibabaTongyi

**Category**: Chat Models | **Type**: ChatAlibabaTongyi | **Version**: 2.0

---

## Overview

Wrapper around Alibaba Tongyi Chat Endpoints

## Credentials

**Required**: Yes

**Credential Types**:
- AlibabaApi

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

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatAlibabaTongyi`

## Common Use Cases

1. Use ChatAlibabaTongyi when you need wrapper around alibaba tongyi chat endpoints
2. Connect to other nodes that accept `ChatAlibabaTongyi` input

---

**Source**: `packages/components/nodes/chatmodels/ChatAlibabaTongyi/ChatAlibabaTongyi.ts`