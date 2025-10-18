# ChatOllama

**Category**: Chat Models | **Type**: ChatOllama | **Version**: 5.0

---

## Overview

Chat completion using open-source LLM on Ollama

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Base URL | `string` |  | http://localhost:11434 |
| Model Name | `string` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Cache | `BaseCache` |  | - |
| Temperature | `number` | The temperature of the model. Increasing the temperature will make the model answer more creatively. | - |
| Allow Image Uploads | `boolean` | Allow image input. Refer to the <a href= | - |
| Streaming | `boolean` |  | - |
| JSON Mode | `boolean` | Coerces model outputs to only return JSON. Specify in the system prompt to return JSON. Ex: Format a | - |
| Keep Alive | `string` | How long to keep connection alive. A duration string (such as  | 5m |
| Top P | `number` | Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower | - |
| Top K | `number` | Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse ans | - |
| Mirostat | `number` | Enable Mirostat sampling for controlling perplexity. (default: 0, 0 = disabled, 1 = Mirostat, 2 = Mi | - |
| Mirostat ETA | `number` | Influences how quickly the algorithm responds to feedback from the generated text. A lower learning  | - |
| Mirostat TAU | `number` | Controls the balance between coherence and diversity of the output. A lower value will result in mor | - |
| Context Window Size | `number` | Sets the size of the context window used to generate the next token. (Default: 2048) Refer to <a tar | - |
| Number of GPU | `number` | The number of layers to send to the GPU(s). On macOS it defaults to 1 to enable metal support, 0 to  | - |
| Number of Thread | `number` | Sets the number of threads to use during computation. By default, Ollama will detect this for optima | - |
| Repeat Last N | `number` | Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = | - |
| Repeat Penalty | `number` | Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will penalize repetitions more | - |
| Stop Sequence | `string` | Sets the stop sequences to use. Use comma to seperate different sequences. Refer to <a target= | - |
| Tail Free Sampling | `number` | Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher va | - |

## Connections

**Accepts Inputs From**:
- Cache (`BaseCache`)

**Outputs**: `ChatOllama`

## Common Use Cases

1. Use ChatOllama when you need chat completion using open-source llm on ollama
2. Connect to other nodes that accept `ChatOllama` input

---

**Source**: `packages/components/nodes/chatmodels/ChatOllama/ChatOllama.ts`