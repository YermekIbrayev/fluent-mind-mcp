# Condition

**Category**: Sequential Agents | **Type**: Condition | **Version**: 2.1

---

## Overview

Conditional function to determine which route to take next

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sequential Node | `Start | Agent | LLMNode | ToolNode | CustomFunction | ExecuteFlow` | Can be connected to one of the following nodes: Start, Agent, LLM Node, Tool Node, Custom Function,  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Condition Name | `string` |  | - |
| Condition | `conditionFunction` | If a condition is met, the node connected to the respective output will be executed | - |

## Connections

**Accepts Inputs From**:
- Sequential Node (`Start | Agent | LLMNode | ToolNode | CustomFunction | ExecuteFlow`)
- Condition (`conditionFunction`)

**Outputs**: `Condition`

## Common Use Cases

1. Use Condition when you need conditional function to determine which route to take next
2. Connect to other nodes that accept `Condition` input

---

**Source**: `packages/components/nodes/sequentialagents/Condition/Condition.ts`