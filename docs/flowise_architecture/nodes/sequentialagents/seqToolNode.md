# Tool Node

**Category**: Sequential Agents | **Type**: ToolNode | **Version**: 2.1

---

## Overview

Execute tool and return tool

## Required Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| LLM Node | `LLMNode` |  | - |
| Name | `string` |  | - |
| Update State | `tabs` |  | updateStateMemoryUI |

## Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| Tools | `Tool` |  | - |
| Require Approval | `boolean` | Require approval before executing tools | - |
| Approval Prompt | `string` | Prompt for approval. Only applicable if  | - |
| Approve Button Text | `string` | Text for approve button. Only applicable if  | Yes |
| Reject Button Text | `string` | Text for reject button. Only applicable if  | No |

## Connections

**Accepts Inputs From**:
- Tools (`Tool`)
- LLM Node (`LLMNode`)
- Update State (`tabs`)

**Outputs**: `ToolNode`

## Common Use Cases

1. Use Tool Node when you need execute tool and return tool
2. Connect to other nodes that accept `ToolNode` input

---

**Source**: `packages/components/nodes/sequentialagents/ToolNode/ToolNode.ts`