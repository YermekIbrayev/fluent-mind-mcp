# ChatBaiduWenxin

**Category**: Chat Models | **Type**: ChatBaiduWenxin | **Version**: 2.0

---

## Overview

Wrapper around BaiduWenxin Chat Endpoints

## Credentials

**Required**: Yes

**Credential Types**:
- baiduQianfanApi

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

**Outputs**: `ChatBaiduWenxin`

## Common Use Cases

1. Use ChatBaiduWenxin when you need wrapper around baiduwenxin chat endpoints
2. Connect to other nodes that accept `ChatBaiduWenxin` input

---

**Source**: `packages/components/nodes/chatmodels/ChatBaiduWenxin/ChatBaiduWenxin.ts`