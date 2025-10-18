# Condition Agent

**Category**: Sequential Agents | **Type**: ConditionAgent | **Version**: 3.1

---

## Overview

Uses an agent to determine which route to take next

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Name | `string` |  | - |
| Sequential Node | `Start | Agent | LLMNode | ToolNode | CustomFunction | ExecuteFlow` | Can be connected to one of the following nodes: Start, Agent, LLM Node, Tool Node, Custom Function,  | - |
| Conversation History | `options` | Use the user question from the historical conversation messages as input. | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Chat Model | `BaseChatModel` | Overwrite model to be used for this agent | - |
| System Prompt | `string` |  | - |

## Connections

**Accepts Inputs From**:
- Sequential Node (`Start | Agent | LLMNode | ToolNode | CustomFunction | ExecuteFlow`)
- Chat Model (`BaseChatModel`)

**Outputs**: `ConditionAgent`

## Common Use Cases

1. Use Condition Agent when you need uses an agent to determine which route to take next
2. Connect to other nodes that accept `ConditionAgent` input

---

**Source**: `packages/components/nodes/sequentialagents/ConditionAgent/ConditionAgent.ts`