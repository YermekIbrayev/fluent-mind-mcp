# ChatOpenAI

**Category**: Chat Models | **Type**: ChatOpenAI | **Version**: 2.0

---

## Overview

Wrapper around OpenAI Chat LLM specific for LlamaIndex

## Credentials

**Required**: Yes

**Credential Types**:
- openAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | gpt-3.5-turbo |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Top Probability | `number` |  | - |
| Timeout | `number` |  | - |
| BasePath | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `ChatOpenAI`

## Common Use Cases

1. Use ChatOpenAI when you need wrapper around openai chat llm specific for llamaindex
2. Connect to other nodes that accept `ChatOpenAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatOpenAI/ChatOpenAI_LlamaIndex.ts`