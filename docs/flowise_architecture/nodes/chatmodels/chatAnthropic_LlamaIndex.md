# ChatAnthropic

**Category**: Chat Models | **Type**: ChatAnthropic | **Version**: 3.0

---

## Overview

Wrapper around ChatAnthropic LLM specific for LlamaIndex

## Credentials

**Required**: Yes

**Credential Types**:
- anthropicApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | claude-3-haiku |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Top P | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `ChatAnthropic`

## Common Use Cases

1. Use ChatAnthropic when you need wrapper around chatanthropic llm specific for llamaindex
2. Connect to other nodes that accept `ChatAnthropic` input

---

**Source**: `packages/components/nodes/chatmodels/ChatAnthropic/ChatAnthropic_LlamaIndex.ts`