# ChatMistral

**Category**: Chat Models | **Type**: ChatMistral | **Version**: 1.0

---

## Overview

Wrapper around ChatMistral LLM specific for LlamaIndex

## Credentials

**Required**: Yes

**Credential Types**:
- mistralAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | mistral-tiny |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Top P | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `ChatMistral`

## Common Use Cases

1. Use ChatMistral when you need wrapper around chatmistral llm specific for llamaindex
2. Connect to other nodes that accept `ChatMistral` input

---

**Source**: `packages/components/nodes/chatmodels/ChatMistral/ChatMistral_LlamaIndex.ts`