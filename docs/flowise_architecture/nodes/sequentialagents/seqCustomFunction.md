# Custom JS Function

**Category**: Sequential Agents | **Type**: CustomFunction | **Version**: 1.0

---

## Overview

Execute custom javascript function

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sequential Node | `Start | Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow` | Can be connected to one of the following nodes: Start, Agent, Condition, LLM Node, Tool Node, Custom | - |
| Function Name | `string` |  | - |
| Javascript Function | `code` |  | - |
| Return Value As | `options` |  | - |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Input Variables | `json` | Input variables can be used in the function with prefix $. For example: $var | - |

## Connections

**Accepts Inputs From**:
- Sequential Node (`Start | Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow`)
- Javascript Function (`code`)

**Outputs**: `CustomFunction`

## Common Use Cases

1. Use Custom JS Function when you need execute custom javascript function
2. Connect to other nodes that accept `CustomFunction` input

---

**Source**: `packages/components/nodes/sequentialagents/CustomFunction/CustomFunction.ts`