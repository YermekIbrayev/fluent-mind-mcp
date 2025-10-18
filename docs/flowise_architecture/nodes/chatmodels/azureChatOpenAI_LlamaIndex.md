# AzureChatOpenAI

**Category**: Chat Models | **Type**: AzureChatOpenAI | **Version**: 2.0

---

## Overview

Wrapper around Azure OpenAI Chat LLM specific for LlamaIndex

## Credentials

**Required**: Yes

**Credential Types**:
- azureOpenAIApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model Name | `asyncOptions` |  | gpt-3.5-turbo-16k |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Temperature | `number` |  | - |
| Max Tokens | `number` |  | - |
| Top Probability | `number` |  | - |
| Timeout | `number` |  | - |

## Connections

**Accepts Inputs From**:
- Model Name (`asyncOptions`)

**Outputs**: `AzureChatOpenAI`

## Common Use Cases

1. Use AzureChatOpenAI when you need wrapper around azure openai chat llm specific for llamaindex
2. Connect to other nodes that accept `AzureChatOpenAI` input

---

**Source**: `packages/components/nodes/chatmodels/AzureChatOpenAI/AzureChatOpenAI_LlamaIndex.ts`