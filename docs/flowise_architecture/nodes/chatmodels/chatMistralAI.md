# ChatMistralAI

**Category**: Chat Models | **Type**: ChatMistralAI | **Version**: 4.0

---

## Overview

Wrapper around Mistral large language models that use the Chat endpoint

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
| Cache | `BaseCache` |  | - |
| Temperature | `number` | What sampling temperature to use, between 0.0 and 1.0. Higher values like 0.8 will make the output m | - |
| Streaming | `boolean` |  | - |
| Max Output Tokens | `number` | The maximum number of tokens to generate in the completion. | - |
| Top Probability | `number` | Nucleus sampling, where the model considers the results of the tokens with top_p probability mass. S | - |
| Random Seed | `number` | The seed to use for random sampling. If set, different calls will generate deterministic results. | - |
| Safe Mode | `boolean` | Whether to inject a safety prompt before all conversations. | - |
| Override Endpoint | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)
- Model Name (`asyncOptions`)

**Outputs**: `ChatMistralAI`

## Common Use Cases

1. Use ChatMistralAI when you need wrapper around mistral large language models that use the chat endpoint
2. Connect to other nodes that accept `ChatMistralAI` input

---

**Source**: `packages/components/nodes/chatmodels/ChatMistral/ChatMistral.ts`