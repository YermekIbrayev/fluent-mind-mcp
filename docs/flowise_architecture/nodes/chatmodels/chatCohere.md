# ChatCohere

**Category**: Chat Models | **Type**: ChatCohere | **Version**: 2.0

---

## Overview

Wrapper around Cohere Chat Endpoints

## Credentials

**Required**: Yes

**Credential Types**:
- cohereApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | command-r |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` |  | - |
| Streaming | `boolean` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `ChatCohere`

## Common Use Cases

1. Use ChatCohere when you need wrapper around cohere chat endpoints
2. Connect to other nodes that accept `ChatCohere` input

---

**Source**: `packages/components/nodes/chatmodels/ChatCohere/ChatCohere.ts`