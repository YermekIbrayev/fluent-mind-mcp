# OpenAI Assistant

**Category**: Agents | **Type**: OpenAIAssistant | **Version**: 4.0

---

## Overview

An agent that uses OpenAI Assistant API to pick the tool and args to call

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Select Assistant | `asyncOptions` |  | - |
| Allowed Tools | `Tool` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Moderation | `Moderation` | Detect text that could generate harmful output and prevent it from being sent to the language model | - |
| Tool Choice | `string` | Controls which (if any) tool is called by the model. Can be  | - |
| Parallel Tool Calls | `boolean` | Whether to enable parallel function calling during tool use. Defaults to true | - |
| Disable File Download | `boolean` | Messages can contain text, images, or files. In some cases, you may want to prevent others from down | - |

## Connections

**Accepts Inputs From**:
- Select Assistant (`asyncOptions`)
- Allowed Tools (`Tool`)
- Input Moderation (`Moderation`)

**Outputs**: `OpenAIAssistant`

## Common Use Cases

1. Use OpenAI Assistant when you need an agent that uses openai assistant api to pick the tool and args to call
2. Connect to other nodes that accept `OpenAIAssistant` input

---

**Source**: `packages/components/nodes/agents/OpenAIAssistant/OpenAIAssistant.ts`