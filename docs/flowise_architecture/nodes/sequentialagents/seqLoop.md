# Loop

**Category**: Sequential Agents | **Type**: Loop | **Version**: 2.1

---

## Overview

Loop back to the specific sequential node

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sequential Node | `Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow` | Can be connected to one of the following nodes: Agent, Condition, LLM Node, Tool Node, Custom Functi | - |
| Loop To | `string` | Name of the agent/llm to loop back to | - |

## Connections

**Accepts Inputs From**:
- Sequential Node (`Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow`)

**Outputs**: `Loop`

## Common Use Cases

1. Use Loop when you need loop back to the specific sequential node
2. Connect to other nodes that accept `Loop` input

---

**Source**: `packages/components/nodes/sequentialagents/Loop/Loop.ts`