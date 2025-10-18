# ChatHuggingFace

**Category**: Chat Models | **Type**: ChatHuggingFace | **Version**: 3.0

---

## Overview

Wrapper around HuggingFace large language models

## Credentials

**Required**: Yes

**Credential Types**:
- huggingFaceApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Model | `string` | If using own inference endpoint, leave this blank | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Endpoint | `string` | Using your own inference endpoint | - |
| Temperature | `number` | Temperature parameter may not apply to certain model. Please check available model parameters | - |
| Max Tokens | `number` | Max Tokens parameter may not apply to certain model. Please check available model parameters | - |
| Top Probability | `number` | Top Probability parameter may not apply to certain model. Please check available model parameters | - |
| Top K | `number` | Top K parameter may not apply to certain model. Please check available model parameters | - |
| Frequency Penalty | `number` | Frequency Penalty parameter may not apply to certain model. Please check available model parameters | - |
| Stop Sequence | `string` | Sets the stop sequences to use. Use comma to seperate different sequences. | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatHuggingFace`

## Common Use Cases

1. Use ChatHuggingFace when you need wrapper around huggingface large language models
2. Connect to other nodes that accept `ChatHuggingFace` input

---

**Source**: `packages/components/nodes/chatmodels/ChatHuggingFace/ChatHuggingFace.ts`