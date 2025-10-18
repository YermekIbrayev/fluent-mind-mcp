# Agent

**Category**: Sequential Agents | **Type**: Agent | **Version**: 4.1

---

## Overview

Agent that can execute tools

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Agent Name | `string` |  | - |
| Conversation History | `options` | Use the user question from the historical conversation messages as input. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| System Prompt | `string` |  | - |
| Prepend Messages History | `code` | Prepend a list of messages between System Prompt and Human Prompt. This is useful when you want to p | - |

## Connections

**Accepts Inputs From**:
- Prepend Messages History (`code`)

**Outputs**: `Agent`

## Common Use Cases

1. Use Agent when you need agent that can execute tools
2. Connect to other nodes that accept `Agent` input

---

**Source**: `packages/components/nodes/sequentialagents/Agent/Agent.ts`