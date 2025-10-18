# LLM Node

**Category**: Sequential Agents | **Type**: LLMNode | **Version**: 4.1

---

## Overview

Run Chat Model and return the output

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Name | `string` |  | - |
| Conversation History | `options` | Use the user question from the historical conversation messages as input. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| System Prompt | `string` |  | - |
| Prepend Messages History | `code` | Prepend a list of messages between System Prompt and Human Prompt. This is useful when you want to p | - |

## Connections

**Accepts Inputs From**:
- Prepend Messages History (`code`)

**Outputs**: `LLMNode`

## Common Use Cases

1. Use LLM Node when you need run chat model and return the output
2. Connect to other nodes that accept `LLMNode` input

---

**Source**: `packages/components/nodes/sequentialagents/LLMNode/LLMNode.ts`