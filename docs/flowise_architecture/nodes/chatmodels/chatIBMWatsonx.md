# ChatIBMWatsonx

**Category**: Chat Models | **Type**: ChatIBMWatsonx | **Version**: 2.0

---

## Overview

Wrapper around IBM watsonx.ai foundation models

## Credentials

**Required**: Yes

**Credential Types**:
- ibmWatsonx

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
| Max Tokens | `number` |  | - |
| Frequency Penalty | `number` | Positive values penalize new tokens based on their existing frequency in the text so far, decreasing | - |
| Log Probs | `boolean` | Whether to return log probabilities of the output tokens or not. If true, returns the log probabilit | - |
| N | `number` | How many chat completion choices to generate for each input message. Note that you will be charged b | - |
| Presence Penalty | `number` | Positive values penalize new tokens based on whether they appear in the text so far, increasing the  | - |
| Top P | `number` | An alternative to sampling with temperature, called nucleus sampling, where the model considers the  | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatIBMWatsonx`

## Common Use Cases

1. Use ChatIBMWatsonx when you need wrapper around ibm watsonx.ai foundation models
2. Connect to other nodes that accept `ChatIBMWatsonx` input

---

**Source**: `packages/components/nodes/chatmodels/ChatIBMWatsonx/ChatIBMWatsonx.ts`