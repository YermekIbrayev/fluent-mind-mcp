# End

**Category**: Sequential Agents | **Type**: End | **Version**: 2.1

---

## Overview

End conversation

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Sequential Node | `Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow` | Can be connected to one of the following nodes: Agent, Condition, LLM Node, Tool Node, Custom Functi | - |

## Connections

**Accepts Inputs From**:
- Sequential Node (`Agent | Condition | LLMNode | ToolNode | CustomFunction | ExecuteFlow`)

**Outputs**: `End`

## Common Use Cases

1. Use End when you need end conversation
2. Connect to other nodes that accept `End` input

---

**Source**: `packages/components/nodes/sequentialagents/End/End.ts`