# Execute Flow

**Category**: Sequential Agents | **Type**: ExecuteFlow | **Version**: 1.0

---

## Overview

Execute chatflow/agentflow and return final response

## Credentials

**Required**: Yes

**Credential Types**:
- chatflowApi

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sequential Node | `Start | Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow` | Can be connected to one of the following nodes: Start, Agent, Condition, LLM Node, Tool Node, Custom | - |
| Name | `string` |  | - |
| Select Flow | `asyncOptions` |  | - |
| Input | `options` | Select one of the following or enter custom input | - |

## Connections

**Accepts Inputs From**:
- Sequential Node (`Start | Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow`)
- Select Flow (`asyncOptions`)

**Outputs**: `ExecuteFlow`

## Common Use Cases

1. Use Execute Flow when you need execute chatflow/agentflow and return final response
2. Connect to other nodes that accept `ExecuteFlow` input

---

**Source**: `packages/components/nodes/sequentialagents/ExecuteFlow/ExecuteFlow.ts`